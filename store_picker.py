#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stratified sampler for stores (or any units).

- Allocates sample quotas across strata based on their sizes
- Draws a stratified random sample
- Simple CLI: CSV in → CSV out
"""

import math
from typing import Dict, Hashable, Iterable, Mapping, Optional

import numpy as np
import pandas as pd


# =========================
# Core allocation + sampling
# =========================

def alloc_proportional_with_min(
    total: int,
    capacities: Mapping[Hashable, int],
    min_per_stratum: int = 1,
) -> Dict[Hashable, int]:
    """
    Allocate sample sizes across strata.

    Rules:
    - No stratum > its capacity
    - Total allocated <= total
    - Aim for at least `min_per_stratum` per non-empty stratum
    """
    keys = list(capacities.keys())
    if not keys or total <= 0:
        return {k: 0 for k in keys}

    # Drop zero-capacity strata
    capacities = {k: v for k, v in capacities.items() if v > 0}
    keys = list(capacities.keys())
    if not keys:
        return {}

    total_pop = sum(capacities.values())
    if total_pop == 0:
        return {k: 0 for k in keys}

    # If total is too small to hit min_per_stratum everywhere, fall back to size-based allocation
    min_total = len(keys) * min_per_stratum
    if total < min_total:
        base = total // len(keys)

        alloc = {k: min(base, capacities[k]) for k in keys}
        sorted_keys = sorted(keys, key=lambda k: capacities[k], reverse=True)

        i = 0
        # Safety guard in case many strata hit capacity
        while sum(alloc.values()) < total and i < len(sorted_keys) * 2:
            k = sorted_keys[i % len(sorted_keys)]
            if alloc[k] < capacities[k]:
                alloc[k] += 1
            i += 1
        return alloc

    # Start by giving the minimum to each stratum
    alloc = {k: min(min_per_stratum, capacities[k]) for k in keys}
    remaining = total - sum(alloc.values())
    if remaining <= 0:
        return alloc

    # Allocate remaining proportionally to remaining capacity
    remaining_capacity = {k: capacities[k] - alloc[k] for k in keys}
    remaining_total = sum(v for v in remaining_capacity.values() if v > 0)
    if remaining_total <= 0:
        return alloc

    extra_alloc: Dict[Hashable, int] = {}
    running_total = 0
    for k in keys:
        cap_rem = remaining_capacity[k]
        if cap_rem <= 0:
            extra_alloc[k] = 0
            continue
        prop = cap_rem / remaining_total
        add = min(int(math.floor(remaining * prop)), cap_rem)
        extra_alloc[k] = add
        running_total += add

    # Distribute any leftover to strata with the most remaining capacity
    leftover = remaining - running_total
    if leftover > 0:
        sorted_keys = sorted(
            keys,
            key=lambda k: remaining_capacity[k] - extra_alloc[k],
            reverse=True,
        )
        i = 0
        while leftover > 0 and i < len(sorted_keys) * 2:
            k = sorted_keys[i % len(sorted_keys)]
            if extra_alloc[k] < remaining_capacity[k]:
                extra_alloc[k] += 1
                leftover -= 1
            i += 1

    for k in keys:
        alloc[k] += extra_alloc[k]

    return alloc


def pick_stores(
    df: pd.DataFrame,
    *,
    id_col: str,
    strat_cols: Iterable[str],
    target_n: int,
    random_state: Optional[int] = None,
    min_per_stratum: int = 1,
) -> pd.DataFrame:
    """
    Stratified random sample from a dataframe.

    Parameters
    ----------
    df : input dataframe, one row per unit
    id_col : unique identifier column
    strat_cols : columns to define strata
    target_n : desired total sample size
    random_state : seed for reproducibility
    min_per_stratum : minimum units to try to take from each stratum
    """
    if id_col not in df.columns:
        raise KeyError(f"Missing required ID column: {id_col}")

    strat_cols = list(strat_cols)
    missing = [c for c in strat_cols if c not in df.columns]
    if missing:
        raise KeyError(f"Missing stratification columns: {missing}")

    # Drop rows without an ID
    df = df.dropna(subset=[id_col]).copy()

    # Standardise stratification columns
    for col in strat_cols:
        df[col] = (
            df[col]
            .fillna("UNKNOWN")
            .astype(str)
            .str.strip()
            .str.upper()
        )

    # Tuple key for each stratum
    df["_stratum_key"] = df[strat_cols].apply(
        lambda r: tuple(r.values.tolist()),
        axis=1,
    )

    # Stratum capacities and quotas
    stratum_counts = df["_stratum_key"].value_counts()
    capacities = stratum_counts.to_dict()
    total_target = min(target_n, len(df))

    quotas = alloc_proportional_with_min(
        total=total_target,
        capacities=capacities,
        min_per_stratum=min_per_stratum,
    )

    rng = np.random.default_rng(random_state)
    selected_parts = []

    for key, quota in quotas.items():
        if quota <= 0:
            continue
        stratum_data = df[df["_stratum_key"] == key]
        if stratum_data.empty:
            continue

        n_sample = min(quota, len(stratum_data))
        sampled = stratum_data.sample(
            n=n_sample,
            random_state=rng.integers(0, 1_000_000),
        )
        selected_parts.append(sampled)

    if selected_parts:
        selected = pd.concat(selected_parts, ignore_index=True)
    else:
        selected = df.head(0)

    # Top-up globally if some strata were too small
    if len(selected) < total_target:
        need = total_target - len(selected)
        remaining = df[
            ~df[id_col].astype(str).isin(selected[id_col].astype(str))
        ]
        if not remaining.empty:
            additional = remaining.sample(
                n=min(need, len(remaining)),
                random_state=rng.integers(0, 1_000_000),
            )
            selected = pd.concat([selected, additional], ignore_index=True)

    # Drop helper column
    if "_stratum_key" in selected.columns:
        selected = selected.drop(columns=["_stratum_key"])

    return selected


def summarise_sample(
    selected: pd.DataFrame,
    strat_cols: Iterable[str],
) -> None:
    """Print a simple distribution summary of the sample."""
    if selected.empty:
        print("\nNo rows selected; nothing to summarise.")
        return

    for col in strat_cols:
        if col in selected.columns:
            print(f"\nBy {col}:")
            counts = selected[col].value_counts().sort_index()
            total = len(selected)
            for value, count in counts.items():
                pct = (count / total) * 100 if total > 0 else 0.0
                print(f"  {value}: {count} ({pct:.1f}%)")


# =========================
# CLI wrapper
# =========================

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Stratified sampler: CSV in → stratified CSV sample out.",
    )
    parser.add_argument("input_csv", help="Input CSV file path")
    parser.add_argument("output_csv", help="Output CSV file path")
    parser.add_argument(
        "--target-n",
        type=int,
        required=True,
        help="Total sample size you want (e.g. 160).",
    )
    parser.add_argument(
        "--id-col",
        default="Store_ID",
        help='Unique ID column name (default: "Store_ID").',
    )
    parser.add_argument(
        "--strat-cols",
        nargs="+",
        default=["Country", "Region", "Store_Format", "Store_Type", "Category"],
        help="Stratification columns (space-separated).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed (default: 42).",
    )
    parser.add_argument(
        "--min-per-stratum",
        type=int,
        default=1,
        help="Minimum units per stratum (default: 1).",
    )

    args = parser.parse_args()

    df = pd.read_excel(args.input_csv)
    print(f"Loaded {len(df)} rows from {args.input_csv}")

    selected = pick_stores(
        df,
        id_col=args.id_col,
        strat_cols=args.strat_cols,
        target_n=args.target_n,
        random_state=args.seed,
        min_per_stratum=args.min_per_stratum,
    )

    selected.to_csv(args.output_csv, index=False)
    print(f"\nSaved {len(selected)} rows to {args.output_csv}")

    summarise_sample(selected, args.strat_cols)


if __name__ == "__main__":
    main()
