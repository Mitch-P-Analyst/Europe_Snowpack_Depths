-- Create a new database for the snowpack data
CREATE DATABASE alps_snowpack;

-- Create a table for weather stations metadata
CREATE TABLE weather_stations (
	station_id SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	latitude NUMERIC(9,6),
	longitude NUMERIC(9,6),
	elevation NUMERIC(6,2),
	country TEXT
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
	SELECT 
		name, 
		latitude, 
		longitude, 
		elevation, 
		country, 
		provider
	FROM 
		csv_read('/Users/mitchellpalmer/Projects/France_Snowpack_Depths/meta_all.csv')

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
CREATE TABLE fr_meteofrance (
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
		SELECT
			name, 
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
			SCD100_gapfill
		FROM 
			csv_read('/Users/mitchellpalmer/Projects/France_Snowpack_Depths/fr_meteofrance.csv');

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
	ON weather_stations.name = fr_meteofrance.name



SELECT *
FROM monthly_snowpack
ORDER BY station_id DESC

SELECT *
FROM fr_meteofrance
WHERE name = 'Cap_ferrat'

SELECT *
FROM monthly_snowpack
WHERE station_id = 13

SELECT * 
FROM weather_stations
WHERE provider = 'AT_HZB'


INSERT INTO monthly_snowpack 
	( 
	station_id,
	year,
	month,
	hnsum
		)
SELECT
	weather_stations.station_id,
	at_hzb.year,
	at_hzb.month,
	at_hzb.hnsum
FROM at_hzb
JOIN weather_stations 
	ON weather_stations.name = at_hzb.name


SELECT * 
FROM at_hzb


CREATE  TABLE CH_METEOSWISS
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
	
INSERT INTO monthly_snowpack 
	( 
	station_id,
	year,
	month,
	hnsum
		)
SELECT
	weather_stations.station_id,
	ch_meteoswiss.year,
	ch_meteoswiss.month,
	ch_meteoswiss.hnsum
FROM ch_meteoswiss
JOIN weather_stations 
	ON weather_stations.name = ch_meteoswiss.name

	
CREATE  TABLE CH_SLF
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

INSERT INTO monthly_snowpack 
	( 
	station_id,
	year,
	month,
	hnsum
		)
SELECT
	weather_stations.station_id,
	ch_slf.year,
	ch_slf.month,
	ch_slf.hnsum
FROM ch_slf
JOIN weather_stations 
	ON weather_stations.name = ch_slf.name


CREATE  TABLE DE_DWD
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

INSERT INTO monthly_snowpack 
	( 
	station_id,
	year,
	month,
	hnsum
		)
SELECT
	weather_stations.station_id,
	de_dwd.year,
	de_dwd.month,
	de_dwd.hnsum
FROM de_dwd
JOIN weather_stations 
	ON weather_stations.name = de_dwd.name

CREATE  TABLE IT_BZ
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

INSERT INTO monthly_snowpack 
	( 
	station_id,
	year,
	month,
	hnsum
		)
SELECT
	weather_stations.station_id,
	it_bz.year,
	it_bz.month,
	it_bz.hnsum
FROM it_bz
JOIN weather_stations 
	ON weather_stations.name = it_bz.name

CREATE  TABLE IT_FVG
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

INSERT INTO monthly_snowpack 
	( 
	station_id,
	year,
	month,
	hnsum
		)
SELECT
	weather_stations.station_id,
	it_fvg.year,
	it_fvg.month,
	it_fvg.hnsum
FROM it_fvg
JOIN weather_stations 
	ON weather_stations.name = it_fvg.name

SELECT * 
FROM de_dwd

SELECT *
FROM weather_stations
WHERE name = 'Aach'

SELECT *
FROM monthly_snowpack
WHERE station_id = 2274

CREATE  TABLE IT_LOMBARDIA
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

INSERT INTO monthly_snowpack 
	( 
	station_id,
	year,
	month,
	hnsum
		)
SELECT
	weather_stations.station_id,
	IT_LOMBARDIA.year,
	IT_LOMBARDIA.month,
	IT_LOMBARDIA.hnsum
FROM IT_LOMBARDIA
JOIN weather_stations 
	ON weather_stations.name = IT_LOMBARDIA.name

CREATE  TABLE IT_TN
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

INSERT INTO monthly_snowpack 
	( 
	station_id,
	year,
	month,
	hnsum
		)
SELECT
	weather_stations.station_id,
	IT_TN.year,
	IT_TN.month,
	IT_TN.hnsum
FROM IT_TN
JOIN weather_stations 
	ON weather_stations.name = IT_TN.name

CREATE  TABLE IT_VDA_CF
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

INSERT INTO monthly_snowpack 
	( 
	station_id,
	year,
	month,
	hnsum
		)
SELECT
	weather_stations.station_id,
	IT_VDA_CF.year,
	IT_VDA_CF.month,
	IT_VDA_CF.hnsum
FROM IT_VDA_CF
JOIN weather_stations 
	ON weather_stations.name = IT_VDA_CF.name

CREATE  TABLE IT_VENETO
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

INSERT INTO monthly_snowpack 
	( 
	station_id,
	year,
	month,
	hnsum
		)
SELECT
	weather_stations.station_id,
	IT_VENETO.year,
	IT_VENETO.month,
	IT_VENETO.hnsum
FROM IT_VENETO
JOIN weather_stations 
	ON weather_stations.name = IT_VENETO.name

CREATE  TABLE SI_ARSO
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

INSERT INTO monthly_snowpack 
	( 
	station_id,
	year,
	month,
	hnsum
		)
SELECT
	weather_stations.station_id,
	SI_ARSO.year,
	SI_ARSO.month,
	SI_ARSO.hnsum
FROM SI_ARSO
JOIN weather_stations 
	ON weather_stations.name = SI_ARSO.name

SELECT 
	COUNT(DISTINCT(weather_stations.station_id)) AS Num_stations_meta,
	COUNT(DISTINCT(monthly_snowpack.station_id)) AS Num_stations_inserted
FROM weather_stations
FULL OUTER JOIN monthly_snowpack
	ON weather_stations.station_id = monthly_snowpack.station_id

-- Assessing INSERT Queries from provider tables into monthly_snowpack
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
-- Filter for monthly_snowpack > year 2000

SELECT *
FROM weather_stations

SELECT *
FROM monthly_snowpack
WHERE year >= 2000
