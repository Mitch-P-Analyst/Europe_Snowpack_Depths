SELECT 
    name AS "Weather Station",
    MIN(year) AS "Earliest Record",
    MAX(year) AS "Latest Record",
    ROUND(AVG(CASE WHEN month = '11' THEN hnsum END),2) AS "Avg. Nov. Snow Fall",
    ROUND(AVG(CASE WHEN month = '11' THEN hsmean END),2) AS "Avg. Nov. Average Snow Depth",
    ROUND(AVG(CASE WHEN month = '11' THEN hsmax END),2) AS "Avg. Nov. Max Snow Depth",
	ROUND(AVG(CASE WHEN month = '12' THEN hnsum END),2) AS "Avg. Dec. Snow Fall",
    ROUND(AVG(CASE WHEN month = '12' THEN hsmean END),2) AS "Avg. Dec. Average Snow Depth",
    ROUND(AVG(CASE WHEN month = '12' THEN hsmax END),2) AS "Avg. Dec. Max Snow Depth",
	ROUND(AVG(CASE WHEN month = '1' THEN hnsum END),2) AS "Avg. Jan. Snow Fall",
    ROUND(AVG(CASE WHEN month = '1' THEN hsmean END),2) AS "Avg. Jan. Average Snow Depth",
    ROUND(AVG(CASE WHEN month = '1' THEN hsmax END),2) AS "Avg. Jan. Max Snow Depth",
    ROUND(AVG(CASE WHEN month = '2' THEN hnsum END),2) AS "Avg. Feb. Snow Fall",
    ROUND(AVG(CASE WHEN month = '2' THEN hsmean END),2) AS "Avg. Feb. Average Snow Depth",
    ROUND(AVG(CASE WHEN month = '2' THEN hsmax END),2) AS "Avg. Feb. Max Snow Depth",
	ROUND(AVG(CASE WHEN month = '3' THEN hnsum END),2) AS "Avg. Mar. Snow Fall",
    ROUND(AVG(CASE WHEN month = '3' THEN hsmean END),2) AS "Avg. Mar. Average Snow Depth",
    ROUND(AVG(CASE WHEN month = '3' THEN hsmax END),2) AS "Avg. Mar. Max Snow Depth",
	ROUND(AVG(CASE WHEN month = '4' THEN hnsum END),2) AS "Avg. Apr. Snow Fall",
    ROUND(AVG(CASE WHEN month = '4' THEN hsmean END),2) AS "Avg. Apr.Average Snow Depth",
    ROUND(AVG(CASE WHEN month = '4' THEN hsmax END),2) AS "Avg. Apr. Max Snow Depth"
FROM fr_meteofrance
WHERE month IN ('11','12','1','2','3','4')
GROUP BY name
ORDER BY name;

