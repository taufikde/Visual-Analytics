from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import joblib
import shap
import os
import pandas as pd
import numpy as np

# Import preprocessing helpers
try:
    from utils.preprocessing import load_data, split_features_labels
except ImportError:
    from preprocessing import load_data, split_features_labels

# Ensure model artifacts exist
MODEL_PATH = "models/model.pkl"
PIPELINE_PATH = "models/pipeline.pkl"
if not os.path.exists(MODEL_PATH) or not os.path.exists(PIPELINE_PATH):
    raise FileNotFoundError("Model or pipeline not found. Please run training first.")

# Load model and pipeline
dmodel = joblib.load(MODEL_PATH)
pipeline = joblib.load(PIPELINE_PATH)
# Initialize SHAP explainer
tree_explainer = shap.TreeExplainer(dmodel)

# Load static data and compute predictions at startup
CSV_PATH = "employee.csv"
df_full = load_data(CSV_PATH)
X_raw_all, _ = split_features_labels(df_full)
X_proc_all = pipeline.transform(X_raw_all)
probs_all = dmodel.predict_proba(X_proc_all)[:, 1]
# Get SHAP values and select class-1 explanations
shap_vals = tree_explainer.shap_values(X_proc_all)
# Handle both binary and multi-class cases
if isinstance(shap_vals, list):
    shap_array_all = shap_vals[1]  # For binary classification, take positive class
else:
    shap_array_all = shap_vals

# Prepare top 5 at-risk employees
top_results = []
feature_names = pipeline.named_steps['preprocessor'].get_feature_names_out()
for idx, prob in enumerate(probs_all):
    # get raw numpy vectors
    raw_contribs = shap_array_all[idx]
    raw_vals     = X_proc_all[idx]

    # convert to plain Python lists
    contrib_list = raw_contribs.flatten().tolist()
    val_list     = raw_vals.flatten().tolist()      # or .toarray().flatten().tolist() if sparse

    # now zip and filter
    feats = [
        (f, imp) 
        for f, imp, val in zip(feature_names, contrib_list, val_list)
        if val != 0
    ]

    top_feats = sorted(feats, key=lambda x: abs(x[1]), reverse=True)[:5]
    top_results.append({
        "employee_index": idx,
        "probability": float(prob),
        "top_features": [
            {"feature": f, "impact": float(imp)} for f, imp in top_feats
        ]
    })

# sort globally by probability and keep top 5
TOP_EMPLOYEES = sorted(top_results, key=lambda x: x['probability'], reverse=True)[:5]

# FastAPI setup
app = FastAPI(title="Attrition Prediction API")

domains = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=domains,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schemas
class Employee(BaseModel):
    Age: int
    BusinessTravel: str
    DailyRate: int
    Department: str
    DistanceFromHome: int
    Education: int
    EducationField: str
    EnvironmentSatisfaction: int
    Gender: str
    HourlyRate: int
    JobInvolvement: int
    JobLevel: int
    JobRole: str
    JobSatisfaction: int
    MaritalStatus: str
    MonthlyIncome: int
    MonthlyRate: int
    NumCompaniesWorked: int
    OverTime: str
    PercentSalaryHike: int
    PerformanceRating: int
    RelationshipSatisfaction: int
    StockOptionLevel: int
    TotalWorkingYears: int
    TrainingTimesLastYear: int
    WorkLifeBalance: int
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsSinceLastPromotion: int
    YearsWithCurrManager: int

class PredictionResult(BaseModel):
    employee_index: int
    probability: float = Field(..., description="Probability of attrition (0-1)")
    top_features: List[dict] = Field(..., description="Top feature impacts for this prediction")

@app.get("/top_employees", response_model=List[PredictionResult])
def get_top_employees():
    """
    Return the precomputed top 5 at-risk employees from static dataset.
    """
    return TOP_EMPLOYEES

@app.post("/predict", response_model=List[PredictionResult])
def predict(employees: List[Employee], top_n: Optional[int] = 5):
    """
    Predict attrition probabilities for a list of employees,
    returning top_n at-risk employees sorted by probability.
    """
    df = pd.DataFrame([emp.model_dump() for emp in employees])
    X_proc = pipeline.transform(df)
    probs = dmodel.predict_proba(X_proc)[:, 1]
    shap_vals = tree_explainer.shap_values(X_proc)
    
    # Handle both binary and multi-class cases
    if isinstance(shap_vals, list):
        shap_array = shap_vals[1]  # For binary classification, take positive class
    else:
        shap_array = shap_vals

    results = []
    feature_names_local = pipeline.named_steps['preprocessor'].get_feature_names_out()
    for idx, prob in enumerate(probs):
        contributions = shap_array[idx]
        # Ensure contributions is a 1D array and convert to list
        if isinstance(contributions, np.ndarray):
            contrib_list = contributions.flatten().tolist()
        else:
            contrib_list = contributions if isinstance(contributions, list) else [contributions]
        
        feat_imp = list(zip(feature_names_local, contrib_list))
        top_feats = sorted(feat_imp, key=lambda x: abs(x[1]), reverse=True)[:top_n]
        top_features = [{"feature": f, "impact": float(imp)} for f, imp in top_feats]
        results.append({"employee_index": idx, "probability": float(prob), "top_features": top_features})

    return sorted(results, key=lambda x: x['probability'], reverse=True)[:top_n]

@app.get("/health")
def health_check():
    return {"status": "ok"}