SELECT name AS Weather_Station,
		longitude,
		latitude,
		elevation
FROM meta
WHERE provider = 'FR_METEOFRANCE'
