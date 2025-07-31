import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Step 1: Load Data
def load_data(csv_path: str) -> pd.DataFrame:
    """Load the employee CSV data into a DataFrame."""
    df = pd.read_csv(csv_path)
    return df

# Step 2: Split Features and Labels
def split_features_labels(df: pd.DataFrame):
    """
    Split the DataFrame into features (X) and target (y), dropping
    non-informative columns.
    """
    df_copy = df.copy()
    y = df_copy["Attrition"].map({"Yes": 1, "No": 0})
    X = df_copy.drop(columns=[
        "Attrition", "EmployeeNumber", "EmployeeCount",
        "Over18", "StandardHours"
    ])
    return X, y

# Step 3: Create Preprocessing Pipeline
def create_pipeline(X: pd.DataFrame):
    """
    Create a preprocessing pipeline for numerical and categorical features.
    Returns the pipeline along with lists of categorical and numerical columns.
    """
    # Explicitly define categorical features
    categorical_cols = [
        "BusinessTravel", "Department", "EducationField",
        "Gender", "JobRole", "MaritalStatus", "OverTime"
    ]

    # Explicitly define numerical features
    numerical_cols = [
        "Age", "DailyRate", "DistanceFromHome", "Education",
        "EnvironmentSatisfaction", "HourlyRate", "JobInvolvement",
        "JobLevel", "JobSatisfaction", "MonthlyIncome", "MonthlyRate",
        "NumCompaniesWorked", "PercentSalaryHike", "PerformanceRating",
        "RelationshipSatisfaction", "StockOptionLevel", "TotalWorkingYears",
        "TrainingTimesLastYear", "WorkLifeBalance", "YearsAtCompany",
        "YearsInCurrentRole", "YearsSinceLastPromotion", "YearsWithCurrManager"
    ]

    # Define transformers
    cat_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    num_transformer = StandardScaler()

    # Combine transformers into a column transformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, numerical_cols),
            ('cat', cat_transformer, categorical_cols)
        ]
    )

    # Build full preprocessing pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor)
    ])

    return pipeline, categorical_cols, numerical_cols
