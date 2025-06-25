# France_Snowpack_Depths
A PostgreSQL project exploring trends of average monthly snowdepths at French weather stations from Météo-France.

This project focused on isolating average snowpack depth across France's national weather stations for future analysis of snow depth trends.

## Data Source
- Kaggle Dataset 'European Alps Snow Depth Observations'
  - Referencing Zendo.org Records 5109574#
    - meta_all.csv
    - data_monthly_FR_METEOFRANCE.csv
   
### Data Manipulation
- Monthly snow depth (`hnsum`) per station
- Time range: 1992–2024 (filtered to 2000+)

## Database Schema

- `fr_weather_stations`: Weather station metadata (latitude, longitude, elevation (metres))
- `avg_monthly_snowpack`: Avgerage monthly snowpack per weather station (Filtered from year 2000 onwards)

## Data Objectives
- Clean and normailize entities for weather data anlysis
- Calcualte average winter seasonal snowpack depth for each weather station

## 📂 Key SQL Files
- `france_weather_stations.sql`: Base filtering
- `Avg_French_Snowpack_Depths.sql`: Aggregated table creation

  
