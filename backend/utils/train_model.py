import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

from utils.preprocessing import load_data, split_features_labels, create_pipeline
import os

# ensure output folder exists
os.makedirs("models", exist_ok=True)
 
def train_and_save_model(csv_path: str):
    # 1. Load and split
    df = load_data(csv_path)
    X_raw, y = split_features_labels(df)

    # 2. Preprocessing pipeline
    pipeline, cat_cols, num_cols = create_pipeline(X_raw)
    X_processed = pipeline.fit_transform(X_raw)

    # 3. Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y, test_size=0.2, random_state=42, stratify=y
    )

    # 4. Train model
    model = RandomForestClassifier(
        n_estimators=100, max_depth=10, random_state=42, class_weight='balanced'
    )
    model.fit(X_train, y_train)

    # 5. Evaluate
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    # 6. Save model & pipeline
    joblib.dump(model, "models/model.pkl")
    joblib.dump(pipeline, "models/pipeline.pkl")

    print("✅ Model and pipeline saved.")


if __name__ == "__main__":
    train_and_save_model("employee.csv")
