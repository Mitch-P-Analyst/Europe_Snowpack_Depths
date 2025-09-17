# European Alps Average Monthly Snowpack Depths

## Project Overiew
A PostgreSQL & Python Visualisation project exploring trends of monthly snowdepths from 2794 weather stations across Germany, Italy, France, Austria, Slovenia & Switerland.

This project focused on isolating average snowpack depth across weather stations in the European Alps for future inferenital analysis of snow depth trends.

## Dash Application
Run the DASH Application to review the project summary

### Tools
- Pandas
- Plotly
- pymannkendall
- Stats
- Shapely
- GeoJson

### Run Installation & Dash App
``` bash
git clone https://github.com/Mitch-P-Analyst/Europe_Snowpack_Depths.git
cd Europe_Snowpack_Depths
git lfs install
git lfs pull
pip install -r requirements.txt
python -m app
```

## Repository Structure
```
├── app/                                                  
│   │ ├── app.py                                          # DASH application
│   │ ├── assests/                                        # DASH application styling
│   │ │ ├── style.css               
│   │ │ ├── style.css.map           
│   │ │ └── style.scss                                    # Master scss styling
├── Data/ 
│   ├── Artifacts/
│   │ └── alps_mask.gpkg                                  # European Alps Boundary Masks   
│   ├── Cleaned/       
│   │ ├── Tests/                                          # Statistical Analysis Data Sheets  
│   │ │ └── /
│   │ └── /                                               # Cleaned SQL Data outputs from 01_Data_Cleaning.sql
│   └── Raw/     
│     ├── Alpine_Convention_Perimeter_2025/               # Alpine Convention Perimeter data
│     └── European Alps Snow Depth Observations Data/     # Zenodo European Alps Snow Depth Observations
├── Notebooks/                                            # Notebooks/
│   ├── 02_EDA.ipynb
│   ├── 03_Statistical_Testing.ipynb
│   └── 04_Visualisations.ipynb
├── Outputs/  
│   ├── Data_ERD.png                                      # SQL ERD Output
│   ├── weather_stations_in_alps.png                      # Visualisation of Alpine Convention Perimeter filtering
│   └── yearly_snowpack_reliability.png                   # Visualisation of time frame filtering
├── Scripts/  
│   ├── app.sql
│   ├── 01_Data_Cleaning.sql
│   ├── figures.py                                        # 04_Visualisation & DASH App figure functions
│   └── functions.py                                      # Statistical Testing custom functions
├── .gitattributes
├── gitignore
├── requirements.txt
└── README.md/   

```

## Data 

### Content
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

### Data Source
- Kaggle Dataset 'European Alps Snow Depth Observations'
  - Referencing [Zenodo.org Records #5109574](https://zenodo.org/records/5109574)
- Geographical Perimeter GDF European Alps Mask 
  - Sourced from Alpine Convention region. Updated in 2025.
    - [Alpine Convention Organsiation](https://www.atlas.alpconv.org/layers/geonode_data:geonode:Alpine_Convention_Perimeter_2025)
   
#### Data Manipulation

- Metadata of 2979 Available weather stations condensed to 2794 in relavence to avaiable Monthly Snowpack Depths from 12 providers. 
- Monthly snow depth (`hnsum`) per station
  - Null Values removed
- Time range: 1864–2024

### Database Schema

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


#### Data Objectives
- Clean and normailize entities for weather data analysis
- Calcualte average winter seasonal snowpack depth for each weather station
- Consolidate monthly snowpack data from 12 providers into one entity
- Analyze statistically significant trends across numerous groupings
- Visualise Theil-Sen slopes for monotonic trends across categories countries, months and elevation bands
- Conclude inference from statistical models for winter snowpack trend.


## Procedure 

### 01 Data Cleaning

- SQL File
  - `01_Data_Cleaning.sql`
    - Base filtering
    - Aggregated table creation

- Data Import Instructions (PostgreSQL)
To load the raw metadata and snowpack data from CSVs into PostgreSQL, use the following command:

```sql
COPY weather_stations
FROM './Data/Raw/European Alps Snow Depth Observations Data/meta_all.csv'
DELIMITER ',' CSV HEADER;
```

### 02 Exploratory Data Analysis (EDA)

- [View & Learn Data](##view--learn-data)

- [Clean & Organise Data](##clean--organise-data)
    - [Segregate by 'Winter' months](#segregate-by-winter-months)
    - [Identify Stations in European Alps](#identify-stations-in-european-alps)
    - [Data Filtering](#data-filtering)
        - [Assess Data Validity](#assess-data-validity)
        - [Focus Range](#focus-range)
        - [Filter by Country](#filter-by-country)
        - [Filter by Elevation Band](#filter-by-elevation

### 03 Statistical Testing

  [Mann-Kendall Test](#mann_kendal-testing)
    - [Function & Application](#Function--Application)

- [Station-Centric (micro perspective)](#Station-Centric-(micro-perspective))
    - [Station-Month time series](#station-month-time-series)
    - [Station-Month time series by Country / Month](#station-month-time-series-by-country--month)
    - [Station-Month time series by Country](#station-month-time-series-by-country)

- [Region-Centric (macro perspective)](#region-centric-marco-perspective)
    - [Slope Per Country & Month](#slope-per-country-month) 
    - [Slope Per Month](#slope-per-month)
    - [Slope Per Elevation Band & Month](#slope-per-elevation-band--month)

### 04 Visualisations
  - [Station Coverage](#station-coverage-for-each-country) 
  - [Country Trends](#country-trends)
      - [Distribution Of Station Slopes Per Country Month](#distribution-of-station-slopes-per-country-month)
      - [Country-Year Mean Snowpack Series](#country-year-mean-snowpack-series)
  - [Month Trends](#month-trends)
      - [Distribution Of Station Slopes Per Month](#distribution-of-station-slopes-per-month)
      - [Month Mean Snowpack Series](#month-mean-snowpack-series)
      - [Country Month Heatmap](#country-month-heatmap)
  - [Elevation Band](#elevation-band-heatmap)
      - [Elevation Band Heatmap](#elevation-band-heatmap)


  
