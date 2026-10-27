# 🌙 Midnight Cart: The 2 AM Problem — Quick-Commerce Optimization & ML Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://midnight-cart.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4%2B-F7931E.svg)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg)](https://pandas.pydata.org/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 🚀 **Live Interactive Demo:** **[https://midnight-cart.streamlit.app/](https://midnight-cart.streamlit.app/)**  
> **An end-to-end data engineering, predictive machine learning, and unit economics optimization platform for a 15-minute campus micro-fulfillment center.**  
> Diagnoses root causes of surging late-night order cancellations, models checkout risk without data leakage, and delivers actionable operational and pricing interventions yielding **+₹11,674 (+14.9%) net profit expansion**.

---

## 📖 The Problem Statement: The "2 AM" Quick-Commerce Paradox

### 1. Business Context & The Story
**Midnight Cart** is a quick-commerce **dark store** serving university campus hostels and student housing. The store promises delivery in **~15 minutes**, serving college students who order late-night study fuel—Maggi noodles, energy drinks, snacks, and phone chargers—especially during high-stress exam periods at 1 AM.

> 💡 **What is a "Dark Store"?**  
> A dark store (similar to **Blinkit**, **Zepto**, or **Swiggy Instamart**) is a hyper-local micro-fulfillment center that is **closed to the walk-in public**. Instead of ordinary retail shopping aisles, it operates like a high-speed mini-warehouse where staff ("pickers") pack online orders in under 90 seconds, and delivery riders rush them to hostel gates within 10–15 minutes.

### 2. The Core Paradox
Over the past 90 days, the business experienced a baffling operational divergence:
* 📈 **Order volume surged by +33%** due to strong campus word-of-mouth.
* 📉 **Realised profit remained completely flat** (~₹78,000 across the entire 90-day cycle).
* 🚨 **Late-night customer cancellations and complaints surged dramatically after 23:00 (11:00 PM)**.

### 3. The Executive Dilemma
City Operations Head **Rohan Mehta** can make **one major strategic intervention** next month:
* **Option A:** Hire additional late-night delivery riders?
* **Option B:** Overhaul the marketing coupon and discount policy?
* **Option C:** Re-layout the dark store and change late-night SKU picking priority?

To make the right call, Rohan commissioned an in-depth data audit to answer four fundamental business questions:
1. **Who cancels?** What operational, behavioral, or geographical signals separate cancelled orders from fulfilled orders?
2. **Where does the money bleed?** Exactly which operational hours, delivery zones, product categories, and promotional coupons are destroying margins?
3. **Can cancellations be predicted early?** Can a machine learning model reliably flag cancellation risk *at checkout time* ($T=0$) before a rider is dispatched, without relying on post-outcome data leakage?
4. **What concrete decisions should Rohan make?** Provide **3 evidence-backed decisions** with exact, mathematically audited Rupee (₹) calculations.

---

## ⚡ Executive Summary: The 90-Day Reality

Midnight Cart operates a campus quick-commerce dark store promising ~15-minute delivery. Over a 90-day period, order volume grew by **+33%**, yet realised profit remained flat and customer complaints surged after 23:00 (11:00 PM).

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               THE 90-DAY STORE BASELINE                                │
├──────────────────────────┬──────────────────────────┬──────────────────────────────────┤
│ Baseline Realised Profit │ The Cancellation Ceiling │ Total Projected Profit Expansion │
│         ₹78,183          │         ₹10,255          │      +₹11,674 (+14.9% Net Lift)  │
└──────────────────────────┴──────────────────────────┴──────────────────────────────────┘
```

### The Core Diagnosis:
1. **The 23:00 Capacity Cliff:** Active riders drop by **50% (from 8.0 to 3.9)** at 22:59 right when student demand surges, causing quoted ETA to explode from 13.7m to 20.1m and cancellations to surge from 8% to **40% (71.2% during Exam Weeks)**.
2. **The Electronics Profit Bleed:** Electronics represents only **8.6% of orders**, yet generates **43% of total store profit** and accounts for **60% of all cancellation profit loss** (₹6,150 out of ₹10,255).
3. **Negative Coupon Unit Economics:** `FIRST50` (flat ₹50 off with no Minimum Order Value) burns **-₹18.50 per order** (88% loss rate) and cancels at **51.0% when combined with Cash on Delivery (COD)**.

### The Unified Solution (+₹11,674 / 90 Days):
* **Decision 1 (Pricing/Marketing):** Restructure `FIRST50` into a ₹199+ MOV prepaid discount $\rightarrow$ **+₹6,974 net profit swing**.
* **Decision 2 (Fleet Re-Timing):** Reallocate 4 idle afternoon riders to the 10:30 PM–02:00 AM window ($0 hiring cost) $\rightarrow$ **+₹3,700 margin recovered**.
* **Decision 3 (Warehouse Logistics):** Pre-bin top 10 electronics SKUs at packing counter (SLA < 90s) $\rightarrow$ **+₹1,000 tech profit protected**.

---

## 📁 Repository Structure

```
Midnight_Cart/
├── .gitignore                         # Comprehensive Python, environment & cache ignore rules
├── LICENSE                            # MIT Open-Source License
├── README.md                          # Master project documentation
├── requirements.txt                   # Production Python package dependencies
│
├── plan/
│   └── IMPLEMENTATION_PLAN.md         # Complete strategic blueprint & financial working
│
├── src/                               # Modular execution engine
│   ├── data_pipeline.py               # Data sanitation, deduplication & sensor imputation
│   ├── clean_orders.csv               # Sanitized dataset (2,685 clean records)
│   ├── coupon_policy.py               # Unit economics simulation & coupon restructuring
│   ├── train_model.py                 # Leakage-free Logistic Regression training & eval
│   ├── run_all.py                     # Master runner (executes complete pipeline in 4s)
│   └── app.py                         # Streamlit Executive Ops Simulator (Interactive Cockpit)
│
└── data/                              # Raw transactional order data
    └── midnight_cart_orders.csv       # Raw transactional order log (2,784 records)
```

---

## 🛠️ Data Pipeline & Engineering Hygiene

Before performing analytics or modeling, the raw dataset (`midnight_cart_orders.csv`, 2,784 rows) underwent rigorous data cleaning in `src/data_pipeline.py`:

| Problem Identified | Engineering Treatment | Operational Justification |
|---|---|---|
| **84 Exact Duplicate Rows** | Purged via `df.drop_duplicates()` | Prevents double-counting transaction volumes and train/test leakage. |
| **Dual Datetime Formats** | Parsed mixed `YYYY-MM-DD` and `DD/MM/YYYY` strings | Unlocks accurate hourly analysis and temporal feature engineering. |
| **Operating Day Boundary** | Mapped store operating cycle (10:00 AM – 02:00 AM) | Orders from 00:00 to 01:59 belong to the previous operational business date. |
| **15 Zero-Basket Rows** | Filtered (`basket_value_inr > 0`) | Removes internal test pings and corrupted zero-margin entries. |
| **25 Zone Misspellings** | Consolidated into 6 standardized clusters | Resolves fragmented geography (`Kaveri`, `Ganga`, `Yamuna`, `Narmada`, `Market Road PGs`, `Faculty Colony`). |
| **16 Zero-Rider Telemetry Drops** | Imputed with hourly median (8 riders) | Sensor failure on Sept 9; delivered orders cannot have 0 riders on duty. |
| **Target Leakage Columns** | Strictly excluded `rating` and `refund_inr` | These columns only exist post-cancellation; including them produces artificial 97% AUC leakage. |

**Exported Dataset:** **2,685 verified, leak-free orders** saved to `src/clean_orders.csv`.

### Raw Dataset Schema & Data Dictionary (18 Attributes)

The raw transactional dataset (`data/midnight_cart_orders.csv`) contains 2,784 records logged across 90 days:

| Attribute | Type | Operational Meaning |
|---|---|---|
| `order_id` | String | Unique transactional order identifier (e.g., `MC-00001`). |
| `order_datetime` | String | Timestamp when customer placed the order (mixed datetime strings). |
| `hostel_zone` | String | Campus delivery destination (25 raw misspelled variants $\rightarrow$ 6 clean clusters). |
| `items_count` | Integer | Total count of items in the cart basket. |
| `basket_value_inr`| Numeric | Gross cart value in Indian Rupees (₹) before coupon discount. |
| `discount_inr` | Numeric | Discount amount deducted from basket (₹). |
| `top_category` | String | Primary category: `Snacks`, `Drinks`, `Instant food`, `Electronics`, `Stationery`, `Health`. |
| `margin_pct` | Float | Product category gross margin percentage (e.g., 0.35 for Electronics). |
| `payment_mode` | String | Payment settlement method: `UPI`, `Card`, or `Cash on delivery` (COD). |
| `coupon_code` | String | Promo code applied: `NONE`, `FIRST50` (₹50 off), or `EXAM20` (20% off). |
| `is_first_order` | String | Customer acquisition flag (`Y` = first order, `N` = repeat user). |
| `exam_week` | String | Academic cycle flag (`Y` = mid/final exam weeks, `N` = regular weeks). |
| `rain_mm` | Numeric | Rainfall telemetry in millimeters at the order hour. |
| `riders_on_duty` | Integer | Active delivery fleet personnel working during that hour. |
| `eta_shown_min` | Numeric | Estimated delivery time quoted to student at app checkout. |
| `cancelled` | Integer | **Target Variable:** `1 = Cancelled`, `0 = Delivered successfully`. |
| `rating` | Float | Post-delivery student rating (1–5; strictly blank on cancellations). |
| `refund_inr` | Numeric | Refund amount issued (₹; post-cancellation variable). |

---

## 🔍 Key Analytical Discoveries

All findings were extracted through hypothesis testing ($t$-tests, $\chi^2$ tests) and multivariate modeling:

### 1. The 23:00 Capacity Cliff
* At 22:00 (10 PM), the store operates with **8.0 active riders**, maintaining an average ETA of **13.7 minutes** and an **8.1% cancellation rate**.
* At 23:00 (11 PM), active riders drop by **50% to 3.9 riders**, while quoted ETA explodes to **20.1 minutes**.
* Cancellations spike to **40% overall**, and during **Exam Week at 23:00, cancellations hit an astronomical 71.2% (52 of 73 orders abandoned)**.

### 2. The Non-Linear 18-Minute ETA Threshold
Student patience is non-linear—delivery delays behave as a cliff rather than a gentle slope:
* **$\le 14$ minutes:** **10.5% cancellation rate** (Normal campus tolerance).
* **15–18 minutes:** **19.8% cancellation rate** (Acceptable study-break buffer).
* **19–24 minutes:** **53.2% cancellation rate** (The psychological tipping point).
* **$\ge 25$ minutes:** **71.4% cancellation rate** (Complete order abandonment).
* **Workload Queuing Ratio:** When order load exceeds **1.0 order per rider-hour**, cancellations double ($13\% \rightarrow 28\%$). Above **1.5 orders per rider-hour**, cancellations surge to **60.3%**.

### 3. The Electronics Paradox
* `Electronics` accounts for only **8.6% of order volume (232 orders)**, yet its **34.9% gross margin** generates **43% of total store profit**.
* Electronics accounts for **60% of all lost cancellation margin (₹6,150 out of ₹10,255)**.
* At 23:00, electronics cancellations surge to **39%**, and **74% of all gross profit lost after 11 PM** is in cancelled chargers, adapters, and cables.

### 4. The `FIRST50` Subsidy Drain
* `FIRST50` gave flat ₹50 off with no Minimum Order Value. Students ordered ₹40–₹60 baskets, paying ₹0 to ₹10 out-of-pocket.
* **88% of all `FIRST50` orders made a net loss (312 of 354 orders)**, burning an average of **-₹18.50 per order** (total 90-day loss: -₹4,587).
* When combined with Cash on Delivery (COD), `FIRST50` cancellation rate reached **51.0%** due to zero customer commitment.

---

## 🤖 Predictive Machine Learning Model

A leakage-free **Logistic Regression** model was trained using only features available at checkout time ($T=0$):

* **Features Used:** `items_count`, `basket_value_inr`, `discount_inr`, `rain_mm`, `riders_on_duty`, `eta_shown_min`, `payment_mode`, `coupon_code`, `is_first_order`, `exam_week`, `zone`, `top_category`, `is_late_night`.
* **Validation Strategy:** 75/25 Stratified Train/Test Split (trained on 2,013 orders; evaluated on **672 unseen orders**).
* **Class Weighting:** `class_weight='balanced'` to account for the 14.7% cancellation base rate.

```
==================================================
MODEL EVALUATION ON UNSEEN TEST DATA (672 Orders)
==================================================
Recall (Class 1)   : 63.64% (Catches ~2 of 3 true cancellations)
Precision (Class 1): 30.58% (2.1x lift over baseline 14.7% cancel rate)
ROC-AUC Score      : 0.775  (Strong discriminative separation)
Accuracy           : 72.8%  (Deliberately deprioritized due to class imbalance)
```

### Top Cancellation Drivers (Odds Ratios)
* **`Market Road PGs` (3.35×):** Off-campus gate delays multiply cancellation odds by 3.35× vs. Faculty Colony.
* **`Narmada Hostel` (2.47×):** Perimeter walking delay multiplier.
* **`Coupon: FIRST50` (2.35×):** Zero-commitment micro-orders multiply cancellation odds by 2.35×.
* **`Quoted ETA (+3.6m)` (1.52×):** Every +3.6 min increase multiplies cancellation odds by 1.52×.
* **`Payment: Card` (0.27×) & `UPI` (0.41×):** **Protective!** Digital prepayment reduces cancellation odds by 59% to 73% compared to Cash on Delivery.

### Precision vs. Recall Operational Design:
* **Why 64% Recall Matters:** In quick commerce, a missed cancellation wastes a 25-minute midnight rider trip (-₹150 loss). High recall catches cancellations before dispatch.
* **Why 31% Precision is Handled Operationally:** A false alarm costs ₹0 because we **never** block or cancel customer orders. The system triggers positive nudges (e.g., *"Pay via UPI to unlock Priority 12-min Dispatch"*), improving cash collection with zero negative customer friction.

---

## 💼 Strategic Action Plan & Financial Working

```
┌────────────────────────────────────────────────────────────────────────┐
│                   ROHAN'S 3 ACTIONS (₹11,674 / 90 DAYS)                │
├──────────────────────────┬──────────────────────────┬──────────────────┤
│ 1. Restructure FIRST50   │ 2. Dynamic Fleet Shift   │ 3. Electronics   │
│    (Threshold + Combos)  │    (Re-time, Don't Hire) │    Fast-Lane     │
│    +₹6,974 / 90 days     │    +₹3,700 / 90 days     │    +₹1,000 / 90d │
└──────────────────────────┴──────────────────────────┴──────────────────┘
```

### Decision 1: Restructure `FIRST50` (The "One Big Change")
* **Action:** Replace flat ₹50 discount with **"₹40 OFF on ₹199+ (Prepaid only)"** and in-cart combo boosters (*"Add Maggi for ₹1 at ₹149"*). Completely disable Cash on Delivery on discounted first orders.
* **Financial Working:** Current loss is -₹4,587 across 354 orders. Under the new policy, qualifying orders yield +₹2,387 net profit.
  $$\text{Net Profit Swing} = +₹2,387 - (-₹4,587) = \mathbf{+₹6,974 \text{ (+₹2,325 / month)}}$$

### Decision 2: Re-Time Existing Fleet (Do NOT Hire New Riders)
* **Action:** Reallocate 4 idle afternoon riders (12:00 PM–4:00 PM, load: 0.36 orders/hr) to 10:30 PM–02:00 AM. Maintain 8 riders until 01:00 AM during the 14 exam days.
* **Financial Working:** Recovers ~70 cancelled orders across the 11 PM–2 AM window $\rightarrow$ **+₹3,700 net margin (+₹1,233 / month)**.
* **The Economic Proof Against Hiring:** Recovering ₹3,700 across 188 night hours yields **~₹20 per rider-hour**. Market delivery wages in Roorkee are ₹60–₹80/hour. Hiring new riders would result in an immediate net loss of over ₹9,000. Re-timing idle daytime hours costs **₹0**.

### Decision 3: "Electronics-First" Counter Fast-Lane
* **Action:** Pre-bin top 10 chargers, cables, and power banks directly at the dispatch packing counter with **Gold Priority Tags**. Slashes warehouse pick SLA from 6.5m to under 90 seconds.
* **Financial Working:** Late-night lost margin in electronics is ₹4,713. Priority counter picking saves half of the residual loss $\rightarrow$ **+₹1,000 protected margin (+₹333 / month)**.

**TOTAL 90-DAY NET PROFIT LIFT:** **+₹11,674 (+14.9% expansion on ₹78,183 baseline)**.  
*(Note: Total cancellation loss across the store was ₹10,255. Projections claiming ₹80,000+ are mathematically impossible.)*

---

## 🖥️ Interactive Operations Simulator (Streamlit App)

> 🌐 **Experience the Live Web App:** **[https://midnight-cart.streamlit.app/](https://midnight-cart.streamlit.app/)**  
> Access the executive simulator directly in your browser without any local setup.

Or run locally via terminal:

```powershell
streamlit run src/app.py
```

### Simulator Modules:
1. **11 PM Fleet & Cancellation Simulator:** Interactively adjust active riders on duty (3 to 9 riders) to observe real-time non-linear changes in quoted ETA, cancellation rate, and recovered margin.
2. **Coupon Economics Simulator:** Adjust Minimum Order Value (MOV) sliders and discount rates to view the exact margin swing and distribution of profitable vs. loss-making orders.
3. **Real-Time Checkout Risk Predictor:** Live inference module calculating cancellation probability based on cart basket value, payment mode, delivery zone, and active fleet size.
4. **Historical Order Explorer:** Interactive Plotly filtering across all 2,685 clean records with revenue and margin waterfalls.

---

## 🚀 Quick Start: Running the Project Locally

### 1. Clone & Set Up Environment
```powershell
git clone https://github.com/Pradeepthi-P01/Midnight_Cart.git
cd Midnight_Cart
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Execute Master Data & Modeling Pipeline
Run the full data sanitation, coupon analysis, and model training in **4 seconds**:
```powershell
python src/run_all.py
```

### 3. Launch Interactive Command Cockpit
```powershell
streamlit run src/app.py
```

---

## 📊 Summary of Key Metrics

| Metric | Baseline | Optimized / Target | Impact |
| :--- | :---: | :---: | :--- |
| **90-Day Net Profit** | ₹78,183 | **₹89,857** | **+₹11,674 (+14.9%)** |
| **23:00 Active Riders** | 3.9 riders | **8.0 riders** | 50% fleet collapse eliminated |
| **23:00 Quoted ETA** | 20.1 mins | **< 14.0 mins** | Restores 15-min brand promise |
| **Exam Week 23:00 Cancellations** | 71.2% | **< 18.0%** | Recovers 70+ orders |
| **FIRST50 Loss-Making Orders** | 88.0% | **0.0%** | MOV ₹199 stops micro-order bleed |
| **COD FIRST50 Cancel Rate** | 51.0% | **0.0%** | Disabled on discount baskets |
| **ML Model Recall / ROC-AUC** | N/A | **63.6% / 0.775** | Intercepts 6 of 10 cancellations |

---

*Repository maintained by Pradeepthi P · Built with Python, Pandas, Scikit-Learn & Streamlit.*
