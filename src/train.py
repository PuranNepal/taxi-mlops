from google.cloud import bigquery
import joblib
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


PROJECT_ID = "taxi-mlops"
DATASET = "taxi_mlops"
TABLE = "feature_table"


def load_data():
    """
    Read feature table from BigQuery.
    """
    client = bigquery.Client(project=PROJECT_ID)

    query = f"""
    SELECT
        pickup_hour,
        PULocationID,
        pickup_count,
        hour,
        day_of_week,
        month,
        is_weekend,
        lag_1,
        lag_24,
        rolling_24
    FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
    ORDER BY pickup_hour
    """

    df = client.query(query).to_dataframe()
    return df


def train_model(demand):
    """
    input: demand df
    selects features, 80% time-based train test split, trains random forest
    output: trained model dump
    """
    features = [
        "hour",
        "day_of_week",
        "month",
        "is_weekend",
        "lag_1",
        "lag_24",
        "rolling_24",
    ]

    target = "pickup_count"

    split_date = demand["pickup_hour"].quantile(0.8)

    train = demand[demand["pickup_hour"] <= split_date]
    test = demand[demand["pickup_hour"] > split_date]

    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(train[features], train[target])

    preds = model.predict(test[features])
    rmse = np.sqrt(mean_squared_error(test[target], preds))

    print("RMSE:", rmse)

    joblib.dump(model, "models/model.joblib")


if __name__ == "__main__":
    df = load_data()
    train_model(df)