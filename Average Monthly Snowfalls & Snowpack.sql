SELECT 
    month,
	AVG(hnsum) AS "Average Snow Fall",
	AVG(hsmean) AS "Average Snow Depth)",
	AVG(hsmax) AS "Average Maximum Snow Depth"
FROM fr_meteofrance
GROUP BY month
ORDER BY month


