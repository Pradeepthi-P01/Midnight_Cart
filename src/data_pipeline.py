"""
Midnight Cart: Data Cleaning & Feature Pipeline
Run: python src/data_pipeline.py
"""

import os
import pandas as pd
import numpy as np

def run_pipeline(input_path="data/midnight_cart_orders.csv", output_path="src/clean_orders.csv"):
    print(f"Loading raw data from: {input_path}")
    df = pd.read_csv(input_path)
    initial_shape = df.shape
    print(f"Initial raw shape: {initial_shape}")
    
    # 1. Deduplication (Purge 84 duplicate rows)
    df = df.drop_duplicates()
    print(f"Shape after deduplication: {df.shape} (Removed {initial_shape[0] - df.shape[0]} duplicates)")
    
    # 2. Datetime Parsing (Reconcile dual datetime formats)
    d1 = pd.to_datetime(df["order_datetime"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
    d2 = pd.to_datetime(df["order_datetime"], format="%d/%m/%Y %H:%M", errors="coerce")
    df["order_dt"] = d1.fillna(d2)
    df["order_hour"] = df["order_dt"].dt.hour
    
    # 3. Store Day Mapping (10 AM to 2 AM: orders from 00:00 to 01:59 belong to prev day)
    df["store_date"] = df["order_dt"].apply(
        lambda dt: dt.date() - pd.Timedelta(days=1) if dt.hour < 10 else dt.date()
    )
    
    # 4. Filter Zero-Basket Ghost Orders (15 rows)
    ghost_mask = df["basket_value_inr"] == 0
    ghost_count = ghost_mask.sum()
    df = df[~ghost_mask].copy()
    print(f"Dropped {ghost_count} zero-basket ghost orders. Current shape: {df.shape}")
    
    # 5. Zone Name Standardization (25 spellings into 6 clean clusters)
    def clean_zone(z):
        z = str(z).strip().lower()
        if "market" in z: return "Market Road PGs"
        elif "kaveri" in z: return "Kaveri Hostel"
        elif "ganga" in z: return "Ganga Hostel"
        elif "yamuna" in z: return "Yamuna Hostel"
        elif "narmada" in z: return "Narmada Hostel"
        elif "faculty" in z: return "Faculty Colony"
        return "Other"
    df["zone"] = df["hostel_zone"].apply(clean_zone)
    
    # 6. Sensor Imputation (16 rows on Sept 9 with riders_on_duty == 0)
    zero_riders_mask = df["riders_on_duty"] == 0
    zero_riders_count = zero_riders_mask.sum()
    median_by_hour = df[df["riders_on_duty"] > 0].groupby("order_hour")["riders_on_duty"].median()
    df.loc[zero_riders_mask, "riders_on_duty"] = df.loc[zero_riders_mask, "order_hour"].map(median_by_hour)
    print(f"Imputed {zero_riders_count} sensor dropout rows where riders_on_duty == 0.")
    
    # 7. Payment Mode Standardization
    df["payment_mode"] = df["payment_mode"].replace({"Cash on delivery": "COD"})
    
    # 8. Operational Feature Engineering
    df["is_late_night"] = df["order_hour"].apply(lambda h: 1 if h in [23, 0, 1] else 0)
    df["gross_margin_inr"] = df["basket_value_inr"] * (df["margin_pct"] / 100.0)
    df["discount_inr"] = df["discount_inr"].fillna(0)
    df["net_margin_inr"] = df["gross_margin_inr"] - df["discount_inr"]
    
    # Save clean dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"SUCCESS: Exported {len(df)} clean orders to {output_path}")
    return df

if __name__ == "__main__":
    run_pipeline()
