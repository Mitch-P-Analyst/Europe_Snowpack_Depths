# European Alps Average Monthly Snowpack Depths
A PostgreSQL & Python Visualisation project exploring trends of average monthly snowdepths from 2794 weather stations across Germany, Italy, France, Austria, Slovenia & Switerland.

This project focused on isolating average snowpack depth across weather stations in the European Alps for future inferenital analysis of snow depth trends.

# Data 

## Content
- 2794 stations from Germany, Italy, France, Austria, Slovenia & Switerland
- Daily stations snow depth and depth of snowfall, as .zips, grouped by data provider. 
- Monthly stations data as .zips, grouped by data provider. 
  - mean snow depth (hnsum)
  - sum of depth of snowfall
  - maximum snow depth
  - days with snow cover (1-100cm thresholds)
- Station Meta data
  - name
  - latitude
  - longitude
  - elevation

## Data Source
- Kaggle Dataset 'European Alps Snow Depth Observations'
  - Referencing [Zenodo.org Records #5109574](https://zenodo.org/records/5109574)
- Geographical Perimeter GDF European Alps Mask 
  - Sourced from Alpine Convention region. Updated in 2025.
    - [Alpine Convention Organsiation](https://www.atlas.alpconv.org/layers/geonode_data:geonode:Alpine_Convention_Perimeter_2025)
   
## Data Manipulation

- Metadata of 2979 Available weather stations condensed to 2794 in relavence to avaiable Monthly Snowpack Depths from 12 providers. 
- Monthly snow depth (`hnsum`) per station
  - Null Values removed
- Time range: 1864–2024

## Database Schema

- `weather_stations`: European Alps Weather station metadata
    ([SerialPK] Station_id ,
    name, 
    latitude, 
    longitude, 
    elevation (metres), 
    country, 
    provider )
- `monthy_snowpack`: Average monthly snowpack per weather station
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
- Analyze statistically significant trends across numerous groupiings


# Part 1 Data Cleaning

## SQL File
- `01_Data_Cleaning.sql`
  - Base filtering
  - Aggregated table creation
- ### Data Import Instructions (PostgreSQL)

To load the raw metadata and snowpack data from CSVs into PostgreSQL, use the following command:

```sql
COPY weather_stations
FROM './Data/Raw/European Alps Snow Depth Observations Data/meta_all.csv'
DELIMITER ',' CSV HEADER;
```

# Part 2 EDA

## Notebook
- `02_EDA.ipynb`
  - [View & Learn Data](##view--learn-data)

  - [Clean & Organise Data](##clean--organise-data)
      - Segregate by 'Winter' months
      - Identify Stations in European Alps
      - Data Filtering
      - Assess Data Validity
          - Focus Range
          - Filter by Country
          - Filter by Elevation Band

# Part 3 Statistical Testing

  - [Statistical Testing](##statistical-testing)
      - Mann-Kendall Tests
          - Month
          - Elevation & Month
          - Country

  - [Visualisations](##visualisations)
      - Man-Kendall Test Results
          - Month & Elevation
          - Country



  
