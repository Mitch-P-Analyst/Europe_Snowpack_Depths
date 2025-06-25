CREATE TABLE avg_monthly_snowpack AS
SELECT
  name AS weather_station,
  month,
  ROUND(AVG(hnsum), 2) AS avg_hnsum
FROM
  data_monthly_fr_meteofrance
WHERE
  year >= 2000
  AND hnsum IS NOT NULL
GROUP BY
  name, month
ORDER BY
  name, month;
