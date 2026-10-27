"""
Midnight Cart: Leakage-Free Logistic Regression Model
Run: python src/train_model.py
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, recall_score, precision_score

def train_and_evaluate(data_path="src/clean_orders.csv"):
    print(f"Loading clean data from: {data_path}")
    df = pd.read_csv(data_path)
    
    # Strictly define features available AT CHECKOUT TIME (T=0)
    # FORBIDDEN (Leakage): rating, refund_inr
    num_features = ['items_count', 'basket_value_inr', 'discount_inr', 'rain_mm', 'riders_on_duty', 'eta_shown_min']
    cat_features = ['payment_mode', 'coupon_code', 'is_first_order', 'exam_week', 'zone', 'top_category', 'is_late_night']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_features),
            ('cat', OneHotEncoder(drop='first', sparse_output=False), cat_features)
        ]
    )
    
    clf = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42))
    ])
    
    X = df[num_features + cat_features]
    y = df['cancelled'].astype(int)
    
    # 75/25 Stratified Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    print(f"Training on {len(X_train)} orders; Testing on {len(X_test)} UNSEEN orders.")
    clf.fit(X_train, y_train)
    
    # Predictions on unseen test set
    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]
    
    rec = recall_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    
    print("\n" + "="*50)
    print("PHASE 2: MODEL EVALUATION ON UNSEEN ORDERS")
    print("="*50)
    print(f"Recall (Class 1)   : {rec:.2%} (Share of true cancellations caught)")
    print(f"Precision (Class 1): {prec:.2%} (Share of flagged orders really cancelled)")
    print(f"ROC-AUC Score      : {auc:.3f}")
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, digits=2))
    
    # Feature Importance (Odds Ratios)
    cat_encoder = clf.named_steps['preprocessor'].named_transformers_['cat']
    cat_feature_names = cat_encoder.get_feature_names_out(cat_features).tolist()
    all_feature_names = num_features + cat_feature_names
    coefficients = clf.named_steps['classifier'].coef_[0]
    
    coef_df = pd.DataFrame({
        'Feature': all_feature_names,
        'Coefficient': coefficients,
        'Odds_Ratio': np.exp(coefficients)
    }).sort_values('Odds_Ratio', ascending=False)
    
    print("\n" + "="*50)
    print("TOP CANCEL DRIVERS (ODDS RATIOS)")
    print("="*50)
    print(coef_df.head(10).to_string(index=False))
    print("\nTOP PROTECTIVE DRIVERS:")
    print(coef_df.tail(5).to_string(index=False))
    
    return clf

if __name__ == "__main__":
    train_and_evaluate()
