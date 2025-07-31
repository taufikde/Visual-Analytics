"""
Generate static API endpoints from FastAPI backend for GitHub Pages deployment
This script replicates the logic from your main.py FastAPI server
"""

import json
import sys
from pathlib import Path
import joblib
import shap
import numpy as np

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Import preprocessing helpers
try:
    from utils.preprocessing import load_data, split_features_labels
except ImportError:
    try:
        from preprocessing import load_data, split_features_labels
    except ImportError:
        print("⚠ Could not import preprocessing functions. Please ensure they exist.")
        load_data = None
        split_features_labels = None

def create_static_api():
    """Generate static JSON files that mimic API endpoints"""
    
    # Create output directory
    static_api_dir = backend_dir / "static_api"
    static_api_dir.mkdir(exist_ok=True)
    
    try:
        # Load your models
        model_path = backend_dir / "models" / "model.pkl"
        pipeline_path = backend_dir / "models" / "pipeline.pkl"
        csv_path = backend_dir / "employee.csv"
        
        if not model_path.exists():
            print(f"❌ Model file not found at {model_path}")
            return
        if not pipeline_path.exists():
            print(f"❌ Pipeline file not found at {pipeline_path}")
            return
        if not csv_path.exists():
            print(f"❌ CSV file not found at {csv_path}")
            return
            
        # Load model and pipeline
        dmodel = joblib.load(model_path)
        pipeline = joblib.load(pipeline_path)
        print(f"✓ Loaded model and pipeline")
        
        # Initialize SHAP explainer
        tree_explainer = shap.TreeExplainer(dmodel)
        print(f"✓ Initialized SHAP explainer")
        
        # Load and process data (replicating your main.py logic)
        if load_data and split_features_labels:
            df_full = load_data(str(csv_path))
            X_raw_all, _ = split_features_labels(df_full)
            X_proc_all = pipeline.transform(X_raw_all)
            probs_all = dmodel.predict_proba(X_proc_all)[:, 1]
            
            # Get SHAP values
            shap_vals = tree_explainer.shap_values(X_proc_all)
            if isinstance(shap_vals, list):
                shap_array_all = shap_vals[1]  # For binary classification, take positive class
            else:
                shap_array_all = shap_vals
            
            # Prepare top 5 at-risk employees (replicating your exact logic)
            top_results = []
            feature_names = pipeline.named_steps['preprocessor'].get_feature_names_out()
            
            for idx, prob in enumerate(probs_all):
                contributions = shap_array_all[idx]
                # Ensure contributions is a 1D array and convert to list
                if isinstance(contributions, np.ndarray):
                    contrib_list = contributions.flatten().tolist()
                else:
                    contrib_list = contributions if isinstance(contributions, list) else [contributions]
                
                feat_imp = list(zip(feature_names, contrib_list))
                # sort by absolute impact and take top 5
                top_feats = sorted(feat_imp, key=lambda x: abs(x[1]), reverse=True)[:5]
                top_features = [{"feature": f, "impact": float(imp)} for f, imp in top_feats]
                top_results.append({
                    "employee_index": idx, 
                    "probability": float(prob), 
                    "top_features": top_features
                })
            
            # Sort globally by probability and keep top 5
            top_employees = sorted(top_results, key=lambda x: x['probability'], reverse=True)[:5]
            
            # Save top employees data (this matches your /top_employees endpoint)
            with open(static_api_dir / "top_employees.json", "w") as f:
                json.dump(top_employees, f, indent=2)
            print("✓ Generated top_employees.json")
            
        else:
            print("⚠ Could not process data due to missing preprocessing functions")
            # Create empty top employees file
            with open(static_api_dir / "top_employees.json", "w") as f:
                json.dump([], f)
            print("✓ Generated empty top_employees.json")

        # Generate model info endpoint
        model_info = {
            "status": "success",
            "model_loaded": True,
            "pipeline_loaded": True,
            "model_type": str(type(dmodel).__name__),
            "features": getattr(dmodel, 'feature_names_in_', []).tolist() if hasattr(dmodel, 'feature_names_in_') else [],
            "n_features": getattr(dmodel, 'n_features_in_', 0) if hasattr(dmodel, 'n_features_in_') else 0
        }
        
        with open(static_api_dir / "model-info.json", "w") as f:
            json.dump(model_info, f, indent=2)
        print("✓ Generated model-info.json")

        # Generate a health check endpoint
        health_data = {
            "status": "healthy",
            "service": "Attrition Prediction API",
            "version": "1.0.0",
            "timestamp": "static-build"
        }
        
        with open(static_api_dir / "health.json", "w") as f:
            json.dump(health_data, f, indent=2)
        print("✓ Generated health.json")

        # Create an index of available endpoints
        endpoints = {
            "available_endpoints": [
                "/api/health.json",
                "/api/model-info.json", 
                "/api/top_employees.json"
            ],
            "note": "These are static JSON files generated from the FastAPI backend"
        }
        
        with open(static_api_dir / "index.json", "w") as f:
            json.dump(endpoints, f, indent=2)
        print("✓ Generated index.json")

        print(f"\n✅ Static API files generated successfully in {static_api_dir}")
        print("Files created:")
        for file in static_api_dir.glob("*.json"):
            print(f"  - {file.name}")
            
    except Exception as e:
        print(f"❌ Error generating static API: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    create_static_api()