SELECT 
	provider AS "Country",
	name AS "Weather Station",
	longitude,
	latitude,
	elevation,
	hn_year_start,
	hn_year_end,
	hs_year_start,
	hs_year_end
from meta
WHERE provider = 'FR_METEOFRANCE'
ORDER BY name

