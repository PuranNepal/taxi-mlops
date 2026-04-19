CREATE OR REPLACE TABLE taxi_mlops.demand_hourly AS
SELECT
  TIMESTAMP_TRUNC(tpep_pickup_datetime, HOUR) AS pickup_hour,
  PULocationID,
  COUNT(*) AS pickup_count
FROM taxi_mlops.raw_trips
GROUP BY 1, 2
ORDER BY PULocationID, pickup_hour;