-- Create a new database for the snowpack data
CREATE DATABASE alps_snowpack;

-- Create a table for weather stations metadata
CREATE TABLE weather_stations (
	station_id SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	latitude NUMERIC(9,6),
	longitude NUMERIC(9,6),
	elevation NUMERIC(6,2),
	country TEXT,
	provider TEXT NOT NULL, 
);

-- Insert metadata for weather stations
INSERT INTO weather_stations 
	(name, 
	latitude, 
	longitude, 
	elevation, 
	country, 
	provider)
	
	COPY weather_stations
	FROM './Raw Data CSVs/European Alps Snow Depth Observations Data/meta_all.csv'
	DELIMITER ',' CSV HEADER;

-- Create a table for monthly snowpack data
CREATE TABLE monthly_snowpack (
	id INTEGER PRIMARY KEY
	station_id INTEGER REFERENCES weather_stations(station_id),
	year INTEGER NOT NULL,
	month INTEGER NOT NULL,
	hnsum NUMERIC(5,2),
)

-- Create a table for each provider's snowpack data from 'Raw Data CSVs' folder
-- For example, for MeteoFrance
CREATE TABLE fr_meteofrance 
	( 
	name text,
	year INTEGER,
	month INTEGER,
	hnsum NUMERIC(5,2),
	hsmean NUMERIC(5,2),
	hsmax NUMERIC(5,2),
	SCD1 NUMERIC(5,2),
	SCD1gt NUMERIC(5,2),
	SCD10 NUMERIC(5,2),
	SCD20 NUMERIC(5,2),
	SCD30 NUMERIC(5,2),
	SCD50 NUMERIC(5,2),
	SCD100 NUMERIC(5,2),
	HSmean_gapfill NUMERIC(5,2),
	frac_gapfilled NUMERIC(5,2),
	HSmax_gapfill NUMERIC(5,2),
	SCD1_gapfill NUMERIC(5,2),
	SCD1gt_gapfill NUMERIC(5,2),
	SCD10_gapfill NUMERIC(5,2),
	SCD20_gapfill NUMERIC(5,2),
	SCD30_gapfill	NUMERIC(5,2),
	SCD50_gapfill NUMERIC(5,2),
	SCD100_gapfill NUMERIC(5,2)
	);

-- Insert data from MeteoFrance CSV into the table
INSERT INTO fr_meteofrance 
	(name, 
	year, 
	month, 
	hnsum, 
	hsmean, 
	hsmax, 
	SCD1, 
	SCD1gt, 
	SCD10, 
	SCD20, 
	SCD30, 
	SCD50, 
	SCD100, 
	HSmean_gapfill, 
	frac_gapfilled, 
	HSmax_gapfill, 
	SCD1_gapfill, 
	SCD1gt_gapfill, 
	SCD10_gapfill, 
	SCD20_gapfill, 
	SCD30_gapfill, 
	SCD50_gapfill, 
	SCD100_gapfill)
		
		COPY weather_stations
		FROM './Raw Data CSVs/European Alps Snow Depth Observations Data/date_monthly_FR_METEROFRANCE.csv'
		DELIMITER ',' CSV HEADER;
-- Repeat the above steps for other providers, e.g., AT_HZB, CH_METEOSWISS, etc.

-- Insert data from MeteoFrance into monthly_snowpack table
-- This assumes that the weather_stations table has been populated with the corresponding station names
INSERT INTO monthly_snowpack 
	( 
	station_id,
	year,
	month,
	hnsum
		)
SELECT
	weather_stations.station_id,
	fr_meteofrance.year,
	fr_meteofrance.month,
	fr_meteofrance.hnsum
FROM fr_meteofrance
JOIN weather_stations 
	ON LOWER(TRIM(weather_stations.name)) = LOWER(TRIM(fr_meteofrance.name))
-- This join ensures that the station names match, accounting for case and whitespace differences

-- Repeat the above insert for other providers, e.g. AT_HZB, CH_meteoswiss, etc.

### Data Validation 
-- Assess the completeness of the data and the success of the INSERT queries

-- Confirm the number of unique station_ids in weather_stations and monthly_snowpack
-- This will help identify if any station_ids are missing from the monthly_snowpack table

SELECT 
	COUNT(DISTINCT(weather_stations.station_id)) AS Num_stations_meta,
	COUNT(DISTINCT(monthly_snowpack.station_id)) AS Num_stations_inserted
FROM weather_stations
FULL OUTER JOIN monthly_snowpack
	ON weather_stations.station_id = monthly_snowpack.station_id

-- Identify any weather stations that do not have corresponding monthly_snowpack records
-- Process providing extended details about the missing records
-- This will help identify if any station_ids are missing from the monthly_snowpack table

SELECT 
	ws.station_id AS station_id_meta,
	ws.name,
	ws.provider,
	ms.station_id AS station_id_inserted
FROM weather_stations as ws
FULL OUTER JOIN monthly_snowpack as ms
	ON ws.station_id = ms.station_id
WHERE ms.station_id IS NULL
ORDER BY ws.provider

SELECT 
	DISTINCT ws.provider
FROM weather_stations as ws
FULL OUTER JOIN monthly_snowpack as ms
	ON ws.station_id = ms.station_id
WHERE ms.station_id IS NULL 


-- Addressing missing station_ids from provider tables
-- If weather stations are missing from above queries
-- Perform summary view below for which providers have missing station_ids in monthly_snowpack 


INSERT INTO monthly_snowpack 
	( 
	station_id,
	year,
	month,
	hnsum
		)
SELECT
	weather_stations.station_id,
	CH_meteoswiss.year,
	CH_meteoswiss.month,
	CH_meteoswiss.hnsum
FROM CH_meteoswiss
JOIN weather_stations 
	ON weather_stations.name = CH_meteoswiss.name

INSERT INTO monthly_snowpack 
	( 
	station_id,
	year,
	month,
	hnsum
		)
SELECT
	weather_stations.station_id,
	fr_meteofrance.year,
	fr_meteofrance.month,
	fr_meteofrance.hnsum
FROM fr_meteofrance
JOIN weather_stations 
	ON weather_stations.name = fr_meteofrance.name

-- Delete weather_stations records where no monthly_snowpack data is present in provider tables

SELECT 
	ws.station_id AS station_id_meta,
	ws.name,
	ws.provider,
	ms.station_id AS station_id_inserted
FROM weather_stations as ws
FULL OUTER JOIN monthly_snowpack as ms
	ON ws.station_id = ms.station_id
WHERE ms.station_id IS NULL
ORDER BY ws.provider

DELETE FROM weather_stations ws
WHERE NOT EXISTS (
    SELECT 1
    FROM monthly_snowpack ms
    WHERE ms.station_id = ws.station_id
);

-- Confirm weather_stations with no monthly_snowpack records are deleted.
SELECT 
	COUNT(DISTINCT(weather_stations.station_id)) AS Num_stations_meta,
	COUNT(DISTINCT(monthly_snowpack.station_id)) AS Num_stations_inserted
FROM weather_stations
FULL OUTER JOIN monthly_snowpack
	ON weather_stations.station_id = monthly_snowpack.station_id

-- Download your two successfully cleaned tables for analysis.

SELECT *
FROM weather_stations

SELECT *
FROM monthly_snowpack

