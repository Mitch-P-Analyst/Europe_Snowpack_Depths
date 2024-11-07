SELECT 
	name AS "Weather Station",
    month,
	ROUND(AVG(hnsum),2) AS "Average Snow Fall",
	ROUND(AVG(hsmean),2) AS "Average Snow Depth",
	ROUND(AVG(hsmax),2) AS "Average Maximum Snow Depth"
FROM fr_meteofrance
GROUP BY name, month
ORDER BY name, month


