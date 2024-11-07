-- This SQL Query summarizes and groups the data for further analysis. The starting point for data exploration.


select 
	name AS "weather station",
	year,
	month,
	AVG(hnmean) AS "total snow depth",
	AVG(hsmean) AS "average snow depth",
	AVG(hsmax) AS "max snow depth"
FROM fr_meteofrance
GROUP BY name, year, month
ORDER BY name, year, month