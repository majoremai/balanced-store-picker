# Majórem Store Picker™ 
### Build balanced callfiles with confidence and clarity.

## Why this exists
> [!NOTE]
> Callfiles shape how teams show up in the market. Yet most callfiles are built from habit: recycled lists, legacy priorities, or whatever feels familiar. The result is uneven coverage, skewed insights and missed opportunities.

The **Majórem Store Picker™** changes that. 
It offers a simple, structured way to create a callfile that genuinely reflects your universe — not guesswork, not convenience, not a spreadsheet stitched together at speed.

It’s built for teams who want their field decisions to be fairer, smarter and anchored in reality.
##


## What it does (in plain English)

The Store Picker™ takes your full store universe and:

1. **Cleans and standardises it** 
2. **Groups stores into meaningful segments** (e.g., Region × Format) 
3. **Works out how many stores each segment should contribute** 
4. **Selects those stores in a fair, consistent way** 
5. **Produces a balanced callfile you can stand behind**

No complexity for the sake of it. 
No technical friction. 
Just a clear, defensible selection — every time.

---

## Who it’s for

- Field teams who want a callfile they can trust 
- Strategy and insights teams running measurement cycles or pilots 
- Commercial leads who want to remove bias from planning 
- Anyone tired of “the same old stores” making the list 

If you’ve ever questioned whether a callfile is truly representative, this is designed for you.

---

## The idea in one picture

```

┌────────────────────┐
│   Store Universe   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│   Make it clean    │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│   Group by what    │
│      matters       │
│ (Region, Format…)  │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Allocate fairly    │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Pick consistently │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│    Diagnostics     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Balanced Callfile
  (you can explain 
   in one slide)
└────────────────────┘

````
---

## How to use it

### Command line

```bash
python store_picker.py \
    Input_Stores.xlsx \
    Output_Callfile.csv \
    --target-n 150 \
    --id-col Store_ID \
    --strat-cols Country Region Store_Format Store_Type Category
````

### Or inside Python

```python
from store_picker import pick_stores

selected = pick_stores(
    df,
    id_col="Store_ID",
    strat_cols=["Country", "Region", "Store_Format", "Store_Type", "Category"],
    target_n=150,
)
```
That’s all you need.

---

## What makes it “Majórem”

Majórem builds tools that make field strategy feel modern, not mechanical.

We believe great tools should:

* **Be simple enough to trust**
* **Be transparent enough to explain**
* **Be flexible enough to reuse and scale**
* **Support real commercial routines**, not idealised ones

The Store Picker™ reflects that philosophy: practical, structured and designed for the way teams actually work.

##

## A real example (anonymised)

A national supplier needed 120 stores for a measurement cycle.

The old approach was manual — “grab a few from each region.”
It felt easy, but it consistently oversampled big, familiar stores and ignored newer formats.

With the Store Picker™:

* Every region contributed proportionally
* Smaller formats weren’t lost in the mix
* The team could justify their selection in one slide
* Re-running the callfile for future cycles took seconds

Focused conversations replaced debates about “why that store?”.
The field team gained clarity.
Leadership gained confidence.

## 

## What’s included

* The Store Picker™ engine
* A simple command-line interface
* A worked example using synthetic data
* A sample project brief that mirrors real use cases
* A roadmap for future enhancements

Everything is written to be clear, practical and easy to adapt.

---

## Where this is heading

The Store Picker™ is the first step in Majórem’s broader **Field Intelligence Suite** — a set of tools designed to modernise how organisations plan, measure and deploy field activity.

Next on the path:

* Opportunity-weighted selection
* Diagnostic packs with automated reporting
* YAML workflows for non-technical teams
* Integration with route planning and ROI models

Majórem’s aim is simple:
Make field strategy cleaner, smarter and more confident.

---

## Licence

MIT Licence. Use it, build on it, or adapt it to your own workflow.

````
