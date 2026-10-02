# 7Learnings Data Scientist Case Study: Retail Demand Forecasting

Welcome to the **7Learnings Data Scientist Case Study**!

At **7Learnings**, we build state-of-the-art predictive machine learning platforms that optimize pricing and demand forecasting for leading enterprise e-commerce and retail brands. Our algorithms process hundreds of millions of transactions, customer signals, and pricing elasticities to automate daily business decisions.

This challenge represents a realistic sample of the analytical and engineering challenges faced by our Data Science team.

---

## 1. Problem Statement

Your objective is to build a machine learning model that predicts **daily product-level unit sales** (`sales_before_returns` aggregated at the `(product_id, date)` grain) for a **14-day forecast horizon**:

$$\mathbf{Forecast\ Horizon:\ 2026\text{-}09\text{-}07\ through\ 2026\text{-}09\text{-}20\ (inclusive)}$$

For every active product, your model must output the predicted sales for each day in this 14-day window.

---

## 2. Historical Cutoff & Temporal Leakage Warning

> ⚠️ **CRITICAL TEMPORAL LEAKAGE WARNING**:
> - **Training Cutoff Date:** `2026-09-06 23:59:59`
> - While the provided database contains raw transaction logs extending into September 2026, you **must strictly train and build features using ONLY data recorded on or before the cutoff date** (`<= 2026-09-06`).
> - In enterprise forecasting systems, future ground truth is strictly unavailable at execution time. Any feature engineered with lookahead leakage (e.g., rolling features or traffic metrics computed over the test horizon) will lead to disqualification.
> - Transactions after `2026-09-06` serve solely as the ground-truth benchmark during internal evaluation.

---

## 3. Dataset Description (`7ldata.duckdb`)

The dataset is provided as a local [DuckDB](https://duckdb.org/) database in `7ldata.duckdb` (or compressed as `7ldata.duckdb.zst`). It contains 5 core retail tables:

| Table | Description | Key Columns |
| :--- | :--- | :--- |
| `transactions` | Granular basket-level transaction records | `market, channel, product_id, time, sales_before_returns, order_id, returns, basket_position, revenue, profit, tax_rate` |
| `product_attributes` | Product catalog metadata & hierarchy | `product_id, product_group_id, brand, product_category_1/2/3, season, color, cur_gross_red_price, gross_recom_price, is_own_brand, item_role` |
| `promotions` | Promotion campaigns and discounts | `market, channel, product_id, active_since, active_till, promotion_name, voucher_rate` |
| `stock` | Daily inventory snapshots per product | `market, channel, product_id, active_since, end_liquidation_value, stock_start_of_day` |
| `traffic` | Daily online traffic, impressions, and marketing cost | `market, channel, product_id, active_since, active_till, total_clicks, paid_clicks, marketing_cost` |

> 🔍 **Data Quality Notice**:
> The `transactions` table has arrived directly from raw upstream retail pipelines and contains data quality anomalies that you must audit, document, and clean before modeling.

---

## 4. Structure of the Challenge

The challenge is divided into four key stages:

### Part 1: Data Quality Audit & Cleaning
- Perform a thorough data quality and hygiene audit on the raw `transactions` table.
- Identify any anomalies, corrupted records, or inconsistencies, document your findings, and apply appropriate cleaning steps before downstream aggregation and modeling.

### Part 2: Feature Engineering & Aggregation
- Aggregate transactions to daily product-level sales (`(product_id, date)`).
- You are free to engineer any features you see fit for your model using the provided tables (`product_attributes`, `promotions`, `stock`, `traffic`, and cleaned transactions).
- Ensure all feature engineering strictly respects the training cutoff (`<= 2026-09-06`) to prevent lookahead leakage.
- *Tip: DuckDB SQL allows fast in-database aggregation and joins with minimal memory overhead.*

### Part 3: Predictive Modeling
- Build a predictive model to forecast daily product-level unit sales for the 14-day horizon.
- You can use any model architecture or auditable library of your choice, provided you provide reproducible code and any extra dependencies needed to run it. XGBoost is pre-installed in the environment as a recommended starting point.
- Formulate a clear multi-day forecasting strategy and establish a sound time-based validation split to evaluate your model locally.

### Part 4: Model Evaluation & Business Insights
- Evaluate predictions on standard retail forecasting metrics:
  - **WAPE** (Weighted Absolute Percentage Error): $\frac{\sum |y - \hat{y}|}{\sum y}$
  - **MAE** (Mean Absolute Error)
  - **RMSE** (Root Mean Squared Error)
  - **Forecast Bias**: $\frac{\sum \hat{y} - \sum y}{\sum y}$
- **Retail Tradeoffs:** Discuss the business implications of asymmetric loss. In retail replenishment, what is the operational cost of under-forecasting (stockouts, lost revenue, customer churn) versus over-forecasting (excess holding costs, markdowns, inventory spoilage)?
- Inspect feature importances or model drivers and interpret what drives your predictions.

---

## 5. Deliverables & Submission Format

You may submit your solution as:
1. The completed **`Coding Challenge.ipynb`** Jupyter Notebook, **OR**
2. A clean, modular Python repository/scripts.

### Output File: `predictions.csv`
Your code must generate a `predictions.csv` file saved in the root of the project directory.

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

## 6. AI Usage & Transparency Policy

At 7Learnings, we recognize modern generative AI assistants (ChatGPT, Claude, GitHub Copilot, Cursor, etc.) as powerful everyday productivity enhancers. **You are fully permitted to use AI tools during this case study.**

However, we uphold strict standards of transparency and technical mastery:
1. **Disclosure:** You must explicitly document which AI tools were used and the capacity in which they assisted you (e.g., generating boilerplate SQL, debugging errors, suggesting feature transformations). A dedicated markdown declaration cell is provided in `Coding Challenge.ipynb`.
2. **Personal Mastery:** You are expected to deeply understand and defend every architectural decision, equation, and line of code submitted. During the technical interview, our engineers will discuss your code in detail, ask you to justify choices, explain tradeoffs, and reason about alternative designs.

---

## 7. Environment Setup & Data Preparation

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
   The repository includes the compressed database `7ldata.duckdb.zst`. If you are setting up on a remote instance or fresh environment without the local file, fetch the archive from the candidate release bucket:
   ```bash
   # Optional: Download archive from GCS if not present locally
   # gcloud storage cp gs://7learnings-candidate-datasets/intermediate/7ldata.duckdb.zst .

   # Decompress the zstd archive to generate 7ldata.duckdb (241 MB):
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

## 8. Evaluation Criteria

We review submissions across four dimensions:
1. **Data Intuition & Hygiene:** Did you catch the data quality pitfalls? Are your cleaning heuristics sound and robust?
2. **Methodological Rigor:** Did you strictly prevent temporal data leakage? Is your validation strategy realistic?
3. **Forecasting Performance & Code Quality:** How accurate are your predictions on WAPE/MAE? Is your code clean, reproducible, and well-structured?
4. **Business Acumen:** Can you translate model outputs into commercial retail context and explain tradeoff decisions?

Good luck, and we look forward to reviewing your solution!
