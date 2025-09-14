# Packages
import dash
import pandas as pd
from dash import html, dcc
from dash.dependencies import Output, Input
import plotly as pt
import dash_bootstrap_components as dbc 
from pathlib import Path
import sys 

# Directories
REPO_ROOT = Path(__file__).resolve().parent.parent      # Main Repo Directory
sys.path.insert(0, str(REPO_ROOT))                      # Assign REPO ROOT as Directory 0 for Import searches
ASSETS_DIR = REPO_ROOT / "assets"




# Load Files

# Macro-perspective Trends
avg_country = pd.read_csv(REPO_ROOT / 'Data/Cleaned/Tests/avg_country_trends.csv',index_col=False)                  # Average Snowpack Depth Trend Per Country
avg_country_month = pd.read_csv(REPO_ROOT / 'Data/Cleaned/Tests/avg_country_month_trends.csv',index_col=False)      # Average Snowpack Depth Trend Per Country Month
avg_month = pd.read_csv(REPO_ROOT / 'Data/Cleaned/Tests/avg_month_trends.csv',index_col=False)                      # Average Snowpack Depth Trend per Month
avg_elevation_month = pd.read_csv(REPO_ROOT / 'Data/Cleaned/Tests/avg_elevation_month_trends.csv',index_col=False)  # Average Snowpack Depth Trend Per Elevation Bad Mong

# Micro-persective Trends
typical_country = pd.read_csv(REPO_ROOT / 'Data/Cleaned/Tests/station-month-time-series-by-country.csv',index_col=False)                # Typical Snowpack Depth Trend of Weather Station Per Country 
typical_country_month = pd.read_csv(REPO_ROOT / 'Data/Cleaned/Tests/station-month-time-series-by-country-month.csv',index_col=False )    # Typical Snowpack Depth Trend of Weather Station Per Country Month
typical_station_month = pd.read_csv(REPO_ROOT / 'Data/Cleaned/Tests/station-month-time-series.csv',index_col=False)                     # Typical Snowpack Depth Trend of Weather Station Per Month
per_station = pd.read_csv(REPO_ROOT / 'Data/Cleaned/Tests/per_station_series.csv',index_col=False)                                      # Annual Snowpack Depth Trend per Weather Station


# Custom Figures
from Scripts.figures import country_trends_fig
from Scripts.figures import month_trends_fig
from Scripts.figures import country_coverage


coverage_fig = country_coverage(avg_country_month)
country_fig = country_trends_fig(per_station,avg_country)
month_fig = month_trends_fig(typical_station_month,avg_month)


# Create app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],  # optional
    assets_folder=str(ASSETS_DIR),)





app.layout = dbc.Container([
    html.Div(className='app-header', 
             children=[
             html.H1("European Snowpack Depth Trends",className='display-3')
            ]),
    dbc.Row([
        dbc.Col(html.Div(className='introduction',children=[
            html.H3("A statistical analysis of average snowpack depth across weather stations in the European Alps"),
            html.P("Data was sourced from the Zenodo repository and included monthly measurements from 2794 weather stations across 12 providers in countries of the European Alps between 1865 - 2019. Through exploratory data analsysis requiring a minimum of 30 years of month-level data across winter months, and restricting to weather stations inside the Alpine Convention 2025 geographical permitoer of the Euroepean Alpes, the analytic sample is composed of 795 stations. These stations produced 5,309 station-month time series between the years of 1936-2019."),
            html.P("Trends were evaluated with the Mann–Kendall test (with Hamed–Rao autocorrelation adjustment) and Theil–Sen slope estimates, comparing patterns across months, countries, and elevation bands."),
            html.Hr()
            ]))
            ]),

    dbc.Row([
        dbc.Col(html.Div(className='chart-header',
                         children=[
                             html.H2("Number Of Weather Stations Per Year",className='display-4'),
                             html.P("Median number of weather stations for each country reaching minimum of 30 years of month-level data")
                             ])),
        dbc.Col(dcc.Graph(id='country-coverage',figure=coverage_fig),width=12),
        dbc.Col(html.Div(className='chart-interpreation',
                         children=[
                             html.P("Italy compises the month with the lowest median quantity of weather stations subject to statsitical anlaysis at 42 in May and November." \
                                    "Germany, Switerzland, France, Slovenia range bewteen 48 - 151 across all winter months. Austria provides a consistentl high quantity of weather stations meeting threshold requirements at a minimum of 358 stations."),
                             html.Hr()
            ]))
        ]),

    dbc.Row([
        dbc.Col(html.Div(className='chart-header',children=[
            html.H2("Average Country Snowpack Trends",className='display-4'),
            html.P("Utilsing Hamed-Rao Variants of Mann Kendall Statistical Testing, the average of each Country's Weather Station located in the European Alps, averaged ")
        ])),
        dbc.Col(dcc.Graph(id='country-trends',figure=country_fig),width=12),
        dbc.Col(html.Div(className='chart-interpreation',children=[
            html.P("Countries Italy, Slovenia, and Austria exhibit statistically significant decreases in country-level mean snowpack depth, with Sen slopes of roughly −2 to −4 cm per decade. Germany and Switzerland show negative but non-significant trends (about −1 cm/decade), meaning the decreases are not distinguishable from zero at 𝛼 = 0.05. France shows a non-significant slight increase. Results are from Mann–Kendall (Hamed–Rao) tests applied to country-year average snowpack series; slopes are reported in cm per decade."),
        html.Hr()]))
        ]),

    dbc.Row([
        dbc.Col([
            html.Div(id="data-insights", className="data-insights"),
            html.Div(id="sig-country-trends",className="sig-country-trends")
        ], width=8),
        dbc.Col([
            html.Div(id="country-details",className="country-details")
        ],width=4)
        ]),

    dbc.Row([
        dbc.Col(html.Div(className='chart-header',children=[
            html.H2("Average Month Snowpack Trends",className='display-4'),
            html.P("Utilsing Hamed-Rao Variants of Mann Kendall Statistical Testing, the average of each Month's Weather Station located in the European Alps.")
        ])),
        dbc.Col(dcc.Graph(id='month-trends',figure=month_fig),width=12),
        dbc.Col(html.Div(className='chart-interpreation',children=[
            html.P("Months April and May exhibit statistically significant decreases in European-Alps mean snowpack depth, with Sen slopes of roughly  -1.60 and -1.10 cm per decade respectively. All other winter months, February, December, January, November and March show negative but non-significant trends, with Sen Slopes of roughly -0.55 to -1.90 cm per decade. \n "
            "These decreases ccannot be distinguished from zero trend due to insufficient evidence (α=0.05). "),
            html.P("Further analysis can investiage changes in weather patterns of Springs months (April, May) to link correlation of decreasing Sen slopes of mean snowpack depths. ")


        ]))
    ]),
])


# Launch app
if __name__ == "__main__":
    app.run(debug=True)