"""
Midnight Cart: Phase 1 Commercial Coupon Policy Engine
Run: python src/coupon_policy.py
"""

import sys
import os
import pandas as pd
import numpy as np

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def audit_coupon_policy(data_path="src/clean_orders.csv"):
    df = pd.read_csv(data_path)
    
    print("=" * 65)
    print("PHASE 1: COMMERCIAL COUPON AUDIT & RESTRUCTURING")
    print("=" * 65)
    
    # Baseline coupon performance on clean dataset
    print("\n1. HISTORICAL COUPON PERFORMANCE (DELIVERED ORDERS):")
    delivered = df[df['cancelled'] == 0]
    
    summary = []
    for code, group in delivered.groupby('coupon_code'):
        cnt = len(group)
        gmv = group['basket_value_inr'].sum()
        avg_b = group['basket_value_inr'].mean()
        gm = group['gross_margin_inr'].sum()
        disc = group['discount_inr'].sum()
        net = gm - disc
        net_per_order = net / cnt
        summary.append({
            'Coupon': code,
            'Delivered Orders': cnt,
            'Total GMV (Rs)': round(gmv),
            'Avg Basket (Rs)': round(avg_b, 1),
            'Gross Margin (Rs)': round(gm, 1),
            'Discount Paid (Rs)': round(disc, 1),
            'Net Profit (Rs)': round(net, 1),
            'Net / Order (Rs)': round(net_per_order, 2)
        })
        
    summary_df = pd.DataFrame(summary)
    print(summary_df.to_string(index=False))
    
    # Audit FIRST50 Bleed
    f50_all = df[df['coupon_code'] == 'FIRST50']
    f50_deliv = delivered[delivered['coupon_code'] == 'FIRST50']
    loss_making = (f50_deliv['net_margin_inr'] < 0).sum()
    
    print("\n2. THE FIRST50 UNIT ECONOMICS DISASTER:")
    print(f"   * Total FIRST50 orders placed : {len(f50_all)}")
    print(f"   * FIRST50 cancellation rate   : {f50_all['cancelled'].mean():.1%}")
    print(f"   * FIRST50 delivered orders    : {len(f50_deliv)}")
    print(f"   * Loss-making orders          : {loss_making} out of {len(f50_deliv)} ({loss_making/len(f50_deliv):.1%})")
    print(f"   * Total Realised Net Loss     : -Rs. {abs(f50_deliv['net_margin_inr'].sum()):,.2f}")
    print(f"   * Average Net Profit / Order  : -Rs. {abs(f50_deliv['net_margin_inr'].mean()):.2f}")
    
    # Phase 1 Restructured Policy: MOV Rs 199 + Prepaid Only
    print("\n3. PHASE 1 RESTRUCTURED POLICY SIMULATION:")
    print("   Rule A: Enforce Minimum Order Value (MOV) of Rs 199")
    print("   Rule B: Rs 40 Flat Discount (Capped CAC)")
    print("   Rule C: Prepaid Only (Disable COD on First Discounted Orders)")
    
    qualifying = f50_all[(f50_all['basket_value_inr'] >= 199) & (f50_all['payment_mode'] != 'COD')].copy()
    
    # Financial projection on qualifying orders
    qualifying['new_discount'] = 40.0
    qualifying['new_net_margin'] = qualifying['gross_margin_inr'] - qualifying['new_discount']
    
    realised_loss = f50_deliv['net_margin_inr'].sum()
    new_profit = qualifying['new_net_margin'].sum()
    swing = new_profit - realised_loss
    
    print(f"\n   * Qualifying orders under new policy : {len(qualifying)}")
    print(f"   * Average basket on qualifying orders: Rs. {qualifying['basket_value_inr'].mean():.1f}")
    print(f"   * Average gross margin per order     : Rs. {qualifying['gross_margin_inr'].mean():.2f}")
    print(f"   * New discount per order             : Rs. 40.00")
    print(f"   * New net profit per order           : +Rs. {qualifying['new_net_margin'].mean():.2f}")
    print(f"   * Total 90-Day New Profit            : +Rs. {new_profit:,.2f}")
    print(f"   -------------------------------------------------------------")
    print(f"   WINNER: NET BOTTOM-LINE SWING FOR ROHAN: +Rs. {swing:,.2f} (+Rs. {swing/3:,.0f}/month)")
    print("=" * 65)
    
    return swing

if __name__ == "__main__":
    audit_coupon_policy()
