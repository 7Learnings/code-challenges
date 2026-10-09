# 7Learnings Data Scientist Case Study: Retail Demand Forecasting

Welcome to the **7Learnings Data Scientist Case Study**!

At **7Learnings**, we build state-of-the-art predictive machine learning platforms that optimize pricing and demand forecasting for leading enterprise e-commerce and retail brands. Our algorithms process hundreds of millions of transactions, customer signals, and pricing elasticities to automate daily business decisions.

This challenge represents a realistic sample of the analytical and engineering challenges faced by our Data Science team.

---
## 1. Problem Statement

Your objective is to build a machine learning model that predicts **daily product-level unit sales** (`sales_before_returns` aggregated at the `(product_id, date)` grain) for a **14-day forecast horizon**:

$$\mathbf{Forecast\ Horizon:\ 2026\text{-}09\text{-}07\ through\ 2026\text{-}09\text{-}20\ (inclusive)}$$

Use the exact `(product_id, date)` pairs in `sample_prediction.csv` as the target population. Forecast observed unit sales before returns for market `DE`, channel `myshop.de`, summed at product-day level. Explain any assumptions about future operating conditions that affect your forecast.

---
## 2. Historical Cutoff

- **Training Cutoff Date:** `2026-09-06 23:59:59`
- Use only transactions, inventory observations, and realized traffic available on or before the cutoff. Any later observations in the database are reserved for evaluation.
- **Promotion calendar:** For this exercise, treat the supplied `promotions` table as the plan known on September 6, including campaigns scheduled during the forecast horizon. State any assumptions needed to interpret that plan.
- For historical validation, recreate the information available at that earlier forecast origin. The supplied promotion plan is not evidence that future campaigns were already known at earlier origins; use only campaigns already underway then unless earlier availability can be established. Document uncertainty about the timing of other features, including catalog-derived metrics.

---
## 3. Deliverables & Submission Format

You may submit your solution as:
1. The completed **`Coding Challenge.ipynb`** Jupyter Notebook, **OR**
2. A clean, modular Python repository/scripts.

Include the baseline comparison, investigation SQL and its displayed or saved outputs, the supporting table or chart, and the client memo. These may all live in the notebook; scripts should include brief run instructions and saved results. Keep the three-hour limit and note any unfinished work.

### Output File: `predictions.csv`
Your code must generate a `predictions.csv` file saved in the root of the project directory. A `sample_prediction.csv` file is provided in this repository to illustrate the expected structure and target `(product_id, date)` pairs.

The CSV must match the following format:
```csv
product_id,date,predicted_sales
667836,2026-09-07,1.45
667836,2026-09-08,1.20
...
```
- **Columns:** `product_id` (string), `date` (YYYY-MM-DD), `predicted_sales` (numeric float/int).
- **Prediction Period:** `2026-09-07` through `2026-09-20` (14 days) for all active catalog products.

---
## 4. Environment Setup & Data Preparation

### Prerequisites
- Python 3.10+ (tested on Python 3.10, 3.11, 3.12, 3.14)
- Virtual environment tool (`venv` or `uv`)
- `zstd` (Zstandard compression CLI)

### Installation & Data Decompression

1. **Clone / Enter directory:**
   ```bash
   cd /path/to/intermediate
   ```

2. **Acquire & Decompress Database Archive:**
   Download the compressed database archive (`7ldata.duckdb.zst`, ~123 MiB):
   ```bash
   # Download archive:
   curl -O https://storage.googleapis.com/candidate-01-7l-datascience/7ldata.duckdb.zst
   # Alternatively with gcloud:
   # gcloud storage cp gs://candidate-01-7l-datascience/7ldata.duckdb.zst .

   # Decompress the zstd archive to generate 7ldata.duckdb (~241 MiB):
   zstd -d 7ldata.duckdb.zst -o 7ldata.duckdb
   ```
   *Note: If `7ldata.duckdb` already exists in your workspace, decompression is not needed.*

3. **Create & activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   *Alternative with `uv`:*
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

4. **Launch JupyterLab:**
   ```bash
   jupyter lab "Coding Challenge.ipynb"
   ```

---
## 5. AI Usage & Transparency Policy

At 7Learnings, we recognize modern generative AI assistants (ChatGPT, Claude, GitHub Copilot, Cursor, etc.) as powerful everyday productivity enhancers. **You are fully permitted to use AI tools for this case study.**

However, we uphold strict standards of transparency and technical mastery:
1. **Disclosure:** You must explicitly document which AI tools were used and the capacity in which they assisted you (e.g., generating boilerplate SQL, debugging errors, suggesting feature transformations). A dedicated markdown declaration cell is provided in `Coding Challenge.ipynb`.
2. **Analytical Ownership:** You should be able to trace your conclusions to the underlying records, explain your data preparation, joins, validation, and assumptions, and discuss how new information could change your recommendation. AI assistance and model complexity are not measures of analytical ownership.

---
## 6. Time Allotment

We respect your time and don't expect you to spend more than 3 hours on this. Try to get as far as you can, your solutions will then be discussed in the next interview, feel free to also add comments and explain what you intended to do.

We do not expect hyperparameter grid searches across dozens of algorithms; we prioritize clear data intuition, validation design, and clean reasoning.

Suggested time allocation: 40 minutes for data analysis, 70 minutes for features and forecasting, 50 minutes for the investigation and memo, and 20 minutes for the final export and reproducibility check. A simple, justified model is sufficient; prioritize a complete analytical argument over model complexity.

---
## 7. Dataset Description (`7ldata.duckdb`)

The dataset is provided as a local [DuckDB](https://duckdb.org/) database in `7ldata.duckdb` (or compressed as `7ldata.duckdb.zst`). It contains 5 core retail tables:

| Table | Description | Key Columns |
| :--- | :--- | :--- |
| `transactions` | Granular basket-level transaction records | `market, channel, product_id, time, sales_before_returns, order_id, returns, basket_position, revenue, profit, tax_rate` |
| `product_attributes` | Product catalog metadata & hierarchy | `product_id, product_group_id, brand, product_category_1/2/3, season, color, cur_gross_red_price, gross_recom_price, is_own_brand, item_role` |
| `promotions` | Promotion campaigns and discounts | `market, channel, product_id, active_since, active_till, promotion_name, voucher_rate` |
| `stock` | Dated inventory snapshots per product | `market, channel, product_id, active_since, end_liquidation_value, stock_start_of_day` |
| `traffic` | Daily online traffic, impressions, and marketing cost | `market, channel, product_id, active_since, active_till, total_clicks, paid_clicks, marketing_cost` |

---
## 8. Structure of the Challenge

The challenge is divided into four key stages:

### Part 1: Data Analysis

- Analyze the provided data and summarize your findings about its structure, coverage, and relationships relevant to the forecasting task.
- Decide whether any data preparation, transformations, or enrichment are needed. Document what you chose to do and why.

### Part 2: Feature Engineering

- You are free to engineer any features you see fit for your model using the provided tables (`product_attributes`, `promotions`, `stock`, `traffic`, and `transactions`).
- *Tip: DuckDB SQL allows fast in-database aggregation and joins with minimal memory overhead.*

### Part 3: Predictive Modeling
- Build a predictive model to forecast daily product-level unit sales for the 14-day horizon.
- You can use any model architecture or auditable library of your choice, provided you provide reproducible code and any extra dependencies needed to run it. XGBoost is pre-installed in the environment as a recommended starting point.
- Include a simple baseline and compare it with one proposed approach. You may retain the baseline as your final model if the comparison supports that decision.
- Evaluate a full 14-day historical forecast window ending on or before September 6. Explain how you generate all 14 days without using observations from inside that window as features.

### Part 4: Forecast Evaluation & Merchandise Planner Investigation

#### 1. Quantitative Evaluation

Compare the baseline and your proposed approach on the same historical 14-day window using:

- **WAPE:** $\frac{\sum |y - \hat{y}|}{\sum y}$
- **MAE** and **RMSE**
- **Forecast Bias:** $\frac{\sum \hat{y} - \sum y}{\sum y}$

Report results overall and for the investigation cohort below. State how you handle a zero denominator. Report WAPE and bias consistently as fractions or percentages.

#### 2. Merchandise Planner Investigation

The merchandise planner is reviewing products with `item_role = 'Focus article'` and `product_category_2 = 'Tops'` in `product_attributes`. They ask:

> "Sales for this group appear lower in August 24–September 6 than in August 10–23. Should we reduce our sales forecast for September 7–20? Investigate the evidence and recommend what we should do."

Use information available at the September 6 cutoff:

1. Verify the planner's observation using your cleaned data. Show the cohort size, sales totals for both periods, and the change. Explain any material sensitivity to your cleaning or coverage assumptions.
2. Investigate at least two plausible explanations using transactions and relevant supporting tables. Submit executable DuckDB SQL and its output, plus one compact table or chart. Explain which evidence supports each explanation and which evidence is missing or contradicts it. Account for table coverage and join grain.
3. Explain the implication for your sales forecast. Test one consequential modeling assumption with a small historical comparison or sensitivity check. You may reuse your baseline comparison; a result that does not improve performance is acceptable if explained. Distinguish sensitivity to an assumption from evidence that a change improves accuracy.

There is no requirement to identify a single cause or recommend a forecast reduction. A supported conclusion that the available data cannot resolve an explanation is valid. Feature importance plots are optional.

#### 3. Client Memo

Write a memo of **at most 300 words**, in **3–5 bullets**, for the merchandise planner. Include:

- Your recommended action and two quantified findings, traceable to your submitted outputs.
- The strongest alternative explanation or uncertainty, and the additional information that would most affect your decision.
- The commercial consequence if your recommendation is wrong, and one condition that would change it. State any cost assumptions you use.

Distinguish observed facts, interpretations, and assumptions. We will discuss your evidence and ask how your recommendation changes under a revised business assumption during the interview.

---
## 9. Evaluation Criteria

We assess submissions across four dimensions:

1. **Data Reasoning (30%):** Are cleaning decisions supported, joins sound, findings reproducible, and competing explanations assessed against the records?
2. **Forecasting & Validation (25%):** Is the comparison with the baseline fair, free of temporal leakage, and informative about the full 14-day forecast and the investigation cohort?
3. **Business Judgment (25%):** Does the memo turn quantified evidence into an actionable recommendation with explicit uncertainty and commercial tradeoffs?
4. **Communication (20%):** Are your findings, assumptions, uncertainties, and recommendations clearly explained and supported by evidence?

Runnable code and the required prediction file are basic deliverables. Model complexity, extensive tuning, and elaborate software architecture do not earn additional credit by themselves.

Good luck, and we look forward to reviewing your solution!
