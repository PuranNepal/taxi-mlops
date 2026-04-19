CREATE
OR REPLACE TABLE taxi_mlops.feature_table AS
WITH
    base AS (
        SELECT
            pickup_hour,
            PULocationID,
            pickup_count,
            EXTRACT(
                HOUR
                FROM
                    pickup_hour
            ) AS hour,
            EXTRACT(
                DAYOFWEEK
                FROM
                    pickup_hour
            ) AS day_of_week,
            EXTRACT(
                MONTH
                FROM
                    pickup_hour
            ) AS month
        FROM
            taxi_mlops.demand_hourly
    ),
    features AS (
        SELECT
            pickup_hour,
            PULocationID,
            pickup_count,
            hour,
            day_of_week,
            month,
            CASE
                WHEN day_of_week IN (1, 7) THEN 1
                ELSE 0
            END AS is_weekend,
            LAG (pickup_count, 1) OVER (
                PARTITION BY
                    PULocationID
                ORDER BY
                    pickup_hour
            ) AS lag_1,
            LAG (pickup_count, 24) OVER (
                PARTITION BY
                    PULocationID
                ORDER BY
                    pickup_hour
            ) AS lag_24,
            AVG(pickup_count) OVER (
                PARTITION BY
                    PULocationID
                ORDER BY
                    pickup_hour ROWS BETWEEN 24 PRECEDING
                    AND 1 PRECEDING
            ) AS rolling_24
        FROM
            base
    )
SELECT
    *
FROM
    features
WHERE
    lag_1 IS NOT NULL
    AND lag_24 IS NOT NULL
    AND rolling_24 IS NOT NULL;