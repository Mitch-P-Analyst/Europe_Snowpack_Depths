# European Alps Average Monthly Snowpack Depths
A PostgreSQL & Tableuau Visualisation project exploring trends of average monthly snowdepths from 2794 weather stations across Germany, Italy, France, Austria, Switerland.

This project focused on isolating average snowpack depth across weather stations in the European Alps for future inferenital analysis of snow depth trends.

## Data Source
- Kaggle Dataset 'European Alps Snow Depth Observations'
  - Referencing Zendo.org Records 5109574#
    
   
### Data Manipulation
- Metadata of 2979 Available weather stations condensed to 2794 in relavence to avaiable Monthly Snowpack Depths from 12 providers. 
- Monthly snow depth (`hnsum`) per station
  - Null Values removed
- Time range: 1864–2024 (filtered to 2000+)

## Database Schema

- `weather_stations_list`: European Alps Weather station metadata
    ([SerialPK] Station_id ,
    name, 
    latitude, 
    longitude, 
    elevation (metres), 
    country, 
    provider )
- `european_alps_monthly_snowpack_y2000+`: Average monthly snowpack per weather station (Filtered from year 2000 onwards)
    ([PK] id,
    [FK] Station_id,
    year,
    month,
    hnsum
    )


## Data Objectives
- Clean and normailize entities for weather data analysis
- Calcualte average winter seasonal snowpack depth for each weather station
- Consolidate monthly snowpack data from 12 providers into one entity

## 📂 Key SQL Files
- `france_weather_stations.sql`: Base filtering
- `Avg_French_Snowpack_Depths.sql`: Aggregated table creation

  
