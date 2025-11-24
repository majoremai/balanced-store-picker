## Grocery Example with The Store Picker™

This example uses the provided demo file: **[`demo_universe_grocery.csv`](examples/demo_universe_grocery.csv)**.
It shows how _**The Store Picker™**_ behaves on a realistic grocery estate.

## 1. The universe

The demo file contains **300 synthetic grocery stores** with:

- `Store_ID`
- `Region` <sub> (North, South, East, West) </sub>
- `Format` <sub> (Convenience, Superstore, Metro, Extra) </sub>
- `Staffing_Model` <sub> (Internal, Agency) </sub>
- `Local_Demographics` <sub> (Urban, Suburban, Rural) </sub>
- `Weekly_Sales`
- `Competitor_Density`

It’s not a real retailer, but the mix is intentionally realistic: 
more Convenience and Superstore, more Urban/Suburban, a spread of performance and competition.

A small sample looks like this: 
<small>
| Store_ID | Region | Format      | Staffing_Model | Local_Demographics | Weekly_Sales | Competitor_Density |
|----------|--------|-------------|----------------|--------------------|--------------|--------------------|
| S0001    | North  | Convenience | Internal       | Urban              | 132,000      | 3                  |
| S0002    | South  | Superstore  | Agency         | Suburban           | 118,500      | 5                  |
| S0003    | East   | Metro       | Internal       | Urban              | 141,200      | 4                  |
</small>

## 2. The brief
> [!NOTE]
> “We need a balanced callfile of **150 stores** for a measurement cycle. 
> We care about coverage by Region and Format. 
> The callfile needs to be fair, explainable and easy to regenerate.”

So we decide to stratify by:

- `Region`
- `Format`

This means we’re explicitly asking _*The Store Picker™*_ to balance across those two dimensions.


## 3. Running _The Store Picker™_

### Command line

From the repo root:

```bash
python store_picker.py \
    examples/demo_universe_grocery.csv \
    examples/demo_callfile_grocery.csv \
    --target-n 150 \
    --id-col Store_ID \
    --strat-cols Region Format
````

### Or inside Python

```python
import pandas as pd
from store_picker import pick_stores, summarise_sample

df = pd.read_excel("examples/demo_universe_grocery.csv")

selected = pick_stores(
    df,
    id_col="Store_ID",
    strat_cols=["Region", "Format"],
    target_n=150,
    random_state=42,
)

summarise_sample(selected, ["Region", "Format"])
selected.to_csv("examples/demo_callfile_grocery.csv", index=False)
```

## 4. What _The Store Picker™_ actually does

Behind the scenes, _*The Store Picker™*_ is doing **five** simple things:

1. **Clean the data**
   It standardises `Region` and `Format` values so “north”, “North ” and “NORTH” are treated the same.

2. **Group the stores**
   It builds segments such as:

   * North × Convenience
   * South × Superstore
   * East × Metro
   * West × Extra

3. **Allocate fairly**
   For each Region × Format segment, it calculates how many stores should be taken based on:

   * how many stores sit in that segment
   * the overall target of 150
   * a minimum “at least 1 where possible” rule

4. **Pick stores consistently**
   Within each segment it selects stores using a reproducible random process.
   Same universe + same settings = same callfile.

5. **Check the distribution**
   It prints out how many stores were selected in each Region and Format so you can quickly see whether the callfile looks reasonable.


## 5. Example outcome _(illustrative)_

After running the tool, you might see a distribution like:

                 REGION
        ┌────────┬────────┬────────┬────────┐
        │ North  │ South  │ East   │ West   │
        └────────┴────────┴────────┴────────┘
            ↓         ↓        ↓        ↓
        ┌────────┬────────┬────────┬────────┐
        │ Conven.│ Superst│ Metro  │ Extra  │
        │ Conven.│ Superst│ Metro  │ Extra  │   ← Format split within each region
        │ Conven.│ Superst│ Metro  │ Extra  │
        │ Conven.│ Superst│ Metro  │ Extra  │
        └────────┴────────┴────────┴────────┘

**By Region _(example):**

* North: 37
* South: 39
* East: 36
* West: 38

**By Format (example):**

* Convenience: 55
* Superstore: 48
* Metro: 27
* Extra: 20

>[!NOTE]
>The exact numbers will depend on the underlying universe, but the principle holds:
>**"larger segments contribute more, smaller ones still get a voice."**

What matters is that the callfile:

* Reflects how the estate is actually built
* Is not skewed towards “favourite” regions or formats
* Can be explained in a single slide to a commercial director


## 6. Why this example works for you

This demo universe and example are designed to:

* Feel close to real grocery reality
* Show how simple the interaction can be (one command, clear output)
* Demonstrate _*The Store Picker™*_ as a **practical planning tool**, not an abstract algorithm

You can now:
* 🔁 Swap in your own universe
* 🎯 Change target size (e.g., 80, 200, 500 stores)
* 🧩 Stratify by different attributes (e.g., `Region`, `Format`, `Local_Demographics`)


> [!TIP]
> Use the same narrative with stakeholders:
> “We didn’t just pick stores. We **structured** the universe, **allocated** fairly, and **built** a callfile we can justify.”
