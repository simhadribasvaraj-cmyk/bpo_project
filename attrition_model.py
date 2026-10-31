"""
================================================================================
VOICESERVE BPO - PREDICTIVE ATTRITION RISK MODELING (BONUS DELIVERABLE)
DA-06: Employee Performance, Compensation and Attrition Trend Analysis
Team: DataVerse Squad, Codegnan
================================================================================
Builds an interpretable Machine Learning Model (Random Forest & Logistic Regression),
evaluates feature importances, and scores all current active employees to generate
a targeted, ranked intervention watchlist.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_employee_data.csv")
DATA_DIR = os.path.join(BASE_DIR, "data")
PBI_DIR = os.path.join(BASE_DIR, "powerbi")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")

df = pd.read_csv(DATA_PATH)

print("--- TRAINING ATTRITION RISK PREDICTION MODEL ---")

# Feature selection
numeric_features = [
    "monthly_salary", "incentive_amount", "total_pay", "last_hike_percent",
    "survey_score", "training_hours", "avg_calls_handled", "avg_quality_score",
    "avg_customer_rating", "avg_attendance_percent", "tenure_months"
]

categorical_features = ["centre", "process", "role", "shift", "age_group"]

X = df[numeric_features + categorical_features].copy()
y = df["attrition_flag"].copy()

# Preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric_features),
        ("cat", OneHotEncoder(drop="first", sparse_output=False), categorical_features)
    ]
)

X_trans = preprocessor.fit_transform(X)
cat_encoder = preprocessor.named_transformers_["cat"]
encoded_cat_names = cat_encoder.get_feature_names_out(categorical_features).tolist()
all_feature_names = numeric_features + encoded_cat_names

# Train / Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_trans, y, test_size=0.25, random_state=42, stratify=y
)

# Train Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=150, max_depth=6, random_state=42, class_weight="balanced")
rf_model.fit(X_train, y_train)

# Evaluate on test set
y_pred = rf_model.predict(X_test)
y_prob = rf_model.predict_proba(X_test)[:, 1]
roc_auc = roc_auc_score(y_test, y_prob)

print(f"Model Performance:")
print(f" - ROC-AUC Score: {roc_auc:.3f}")
print("\nClassification Report (Test Set):")
print(classification_report(y_test, y_pred, digits=3))

# Feature Importance
importances = rf_model.feature_importances_
df_importance = pd.DataFrame({
    "Feature": all_feature_names,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

print("\nTop 10 Most Predictive Features of Attrition:")
print(df_importance.head(10).to_string(index=False))

# Plot Feature Importance
plt.figure(figsize=(10, 6))
top_features = df_importance.head(12)
sns.barplot(data=top_features, x="Importance", y="Feature", hue="Feature", palette="Blues_r", legend=False)
plt.title("VoiceServe Attrition Prediction Model: Key Predictive Drivers", fontsize=14, fontweight="bold", pad=12)
plt.xlabel("Random Forest Feature Importance (MDI)", fontsize=12)
plt.ylabel("Workforce Metric / Attribute", fontsize=12)
plt.tight_layout()
chart_path = os.path.join(CHARTS_DIR, "attrition_model_feature_importance.png")
plt.savefig(chart_path, dpi=300)
plt.close()
print(f"Saved feature importance chart to: {chart_path}")

# -------------------------------------------------------------
# SCORE CURRENT ACTIVE EMPLOYEES
# -------------------------------------------------------------
active_mask = (df["attrition_flag"] == 0)
df_active = df[active_mask].copy()

X_active_trans = preprocessor.transform(df_active[numeric_features + categorical_features])
active_probs = rf_model.predict_proba(X_active_trans)[:, 1]

df_active["attrition_risk_score"] = np.round(active_probs * 100, 1)

def assign_risk_tier(prob):
    if prob >= 70.0:
        return "Critical Risk"
    elif prob >= 50.0:
        return "High Risk"
    elif prob >= 30.0:
        return "Medium Risk"
    else:
        return "Low Risk"

df_active["risk_tier"] = df_active["attrition_risk_score"].apply(assign_risk_tier)
df_active = df_active.sort_values(by="attrition_risk_score", ascending=False)

risk_summary = df_active["risk_tier"].value_counts()
print("\nCurrent Active Workforce Risk Distribution:")
for tier, count in risk_summary.items():
    print(f" - {tier}: {count} employees ({(count/len(df_active))*100:.1f}%)")

# Export Active Scored Employees for HR & Power BI
scored_export_cols = [
    "employee_id", "centre", "process", "role", "shift", "tenure_months",
    "monthly_salary", "incentive_amount", "last_hike_percent",
    "avg_attendance_percent", "avg_quality_score", "avg_customer_rating",
    "survey_score", "attrition_risk_score", "risk_tier"
]
active_scored_path = os.path.join(DATA_DIR, "attrition_risk_scored.csv")
df_active[scored_export_cols].to_csv(active_scored_path, index=False)
df_active[scored_export_cols].to_csv(os.path.join(PBI_DIR, "Fact_Active_Risk_Watchlist.csv"), index=False)

print(f"\nSUCCESS: Exported {len(df_active)} scored active employees to:")
print(f" - {active_scored_path}")
print(f" - {os.path.join(PBI_DIR, 'Fact_Active_Risk_Watchlist.csv')}")
