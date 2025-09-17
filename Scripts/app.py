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
from Scripts.figures import country_trends_fig, month_trends_fig, country_coverage, country_month_heat, elevation_band_heat, month_station_slope_distrib, country_station_slope_distrib

coverage_fig = country_coverage(avg_country_month)

country_station_disb = country_station_slope_distrib(typical_station_month, avg_country_month)
country_fig = country_trends_fig(per_station,avg_country)

month_station_disb = month_station_slope_distrib(typical_station_month, avg_month)
month_fig = month_trends_fig(typical_station_month,avg_month)

country_month_heatmap = country_month_heat(avg_country_month, typical_country_month)
elevation_fig = elevation_band_heat(avg_elevation_month)

# Create app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],  # optional
    assets_folder=str(ASSETS_DIR),)





app.layout = dbc.Container([
    html.Div(className='app-header', 
             children=[
             html.H1("European Snowpack Depth Trends",className='display-1')
            ]),

    dbc.Row([
        dbc.Col(html.Div(className='introduction',children=[
            html.H3("A statistical analysis of average snowpack depth across weather stations in the European Alps"),
            html.P("Data was sourced from the Zenodo repository and included monthly measurements from 2794 weather stations across 12 providers in countries of the European Alps between 1865 - 2019. Through exploratory data analysis requiring a minimum of 30 years of month-level data across winter months, and restricting to weather stations inside the Alpine Convention 2025 geographical permitoer of the Euroepean Alpes, the analytic sample is composed of 795 stations. " \
            "These stations produced 5,309 station-month time series between the years of 1936-2019."),
            html.P("Trends were evaluated with the Mann–Kendall test (with Hamed–Rao autocorrelation adjustment) and Theil–Sen slope estimates, comparing patterns across months, countries, and elevation bands."),
            html.Hr()
            ]))
            ]),

    dbc.Row([
        dbc.Col(html.Div(className='chart-header',
                         children=[
                             html.H2("Station Coverage for each Country",className='display-2'),
                             html.P("This chart shows, by country and winter month, the median number of stations per year that pass the analysis filters of ≥ 30 years of data and ≥ 10 stations/year. It communicates quality check on data coverage for the country and month-level trend plots that follow.")
                             ])),
        dbc.Col(dcc.Graph(id='country-coverage',figure=coverage_fig),width=12),
        dbc.Col(html.Div(className='chart-interpretation',
                         children=[
                             html.Ul([
                                 html.Li("Italy compises the month with the lowest median quantity of weather stations subject to statsitical anlaysis at 42 in May and November."),
                                 html.Li("Germany, Switerzland, France, Slovenia range bewteen 48 - 151 across all winter months."),
                                 html.Li("Austria provides a consistently high quantity of weather stations meeting threshold requirements at a minimum of 358 stations.")]),
                             html.Hr()
            ]))
        ]),

    dbc.Row([
        dbc.Col(html.Div(className='section-header',children=[
            html.H2("Country Trends",className='display-2')
            ]))
        ]),

    dbc.Row([
        dbc.Col(html.Div(className='chart-header',children=[
            html.H3("Distribution Of Station Slopes Per Country Month",className='display-3'),
            html.P("This chart shows the distribution of station–month time-series slopes (Theil–Sen, cm/decade) by country. Each dot is one station-month series summarized in the violin spread. \
                   The black ♦ marks a macro signal, the median of the country-month slopes across the winter season (Nov–May), which captures each country’s central seasonal trend while remaining robust to outliers and month-to-month imbalance. \
                   The horizontal dashed blue line is zero-slope change; values below it indicate long-term declines.")
        ])),
        dbc.Col(dcc.Graph(id='country_distrib',figure=country_station_disb),width=12),
        dbc.Col(html.Div(className='chart-interpretation',children=[
             html.P("Extreme values are visibly present in both postive and negative directions for countries France, Germany, Italy and Switzerland. While all 5,309 station-month time series present in this chart have undergone cleaning meeting thresholds of >= 30 years of data and Mann–Kendall statistica testing with Hamed–Rao autocorrelation adjustments, further analysis may be viable to review extreme values"),
             html.P("All countries, except Italy, present a negative median Theil-Sen slope value per decade for the typical regional weather station. Comparatively, all countries present a negative mean/average Theil-Sen slope value per decade across their country, within the Interquartile Range of the typical-station distribution.")
                    ])),
        dbc.Col(html.Div(className='chart-header',children=[
            html.H3("Country-Year Mean Snowpack Series",className='display-3'),
            html.P("This figure compares station-level and country-level trend results using the Mann–Kendall (MK) test with the Hamed–Rao autocorrelation adjustment and Theil–Sen slope estimates (cm/decade)."),
            html.Ul([
                html.Li([
                    html.Strong('Left Chart: '),'Each point is a station’s Theil–Sen slope plotted against its two-sided MK p-value.'
                ]),
                html.Li([
                    html.Strong('Right Chart: '),'One point per country from MK applied to the country–year mean snowpack time series.'
                ]),
                html.Li([
                    html.Strong('Guide Lines: '),
                    html.Ul([
                        html.Li("The horizontal dashed red line marks the significance threshold (α = 0.05); points below it are statistically significant. "),
                        html.Li("The vertical dashed blue line marks zero slope (left = declines; right = increases).")
                    ])
                ]),
            ])
        ]),
        width=12),

        dbc.Col(dcc.Graph(id='country-trends',figure=country_fig),width=12),
        dbc.Col(html.Div(className='chart-interpretation',children=[
            html.P("Countries Italy, Slovenia, and Austria exhibit statistically significant decreases in country-level mean snowpack depth, with Sen slopes of roughly −2 to −4 cm per decade. Germany and Switzerland show negative but non-significant trends (about −1 cm/decade), meaning the decreases are not distinguishable from zero at 𝛼 = 0.05. France shows a non-significant slight increase. Results are from Mann–Kendall (Hamed–Rao) tests applied to country-year average snowpack series; slopes are reported in cm per decade."),
        html.Hr()]))
        ]),
        
    dbc.Row([
        dbc.Col(html.Div(className='section-header',children=[
            html.H2("Monthly Trends",className='display-2')
            ]))
        ]),

    dbc.Row([
        dbc.Col(html.Div(className='chart-header',children=[
            html.H3("Distribution Of Station Slopes Per Month",className='display-3'),
            html.P("This chart shows the distribution of Theil–Sen slopes (cm/decade) for all station–month time series. Each dot is one station-month series for the violin summarizes its spread including summary statistics. "),
            html.P('The black ♦ is the month’s median across stations from a a macro-aggreated summary for that month. Diamonds below 0 indicate that the median station-month series from aggreated tests show declines that month; the more negative, the steeper the decline.'),
            html.P('The horizontal dashed blue line is zero-slope change; values below it indicate long-term declines.')
        ])),
        dbc.Col(dcc.Graph(id='month_distrib',figure=month_station_disb),width=12),
        dbc.Col(html.Div(className='chart-interpretation',children=[
            html.P('Each violin shows the distribution of station-month Theil–Sen slopes for a given month (cm/decade). The dashed blue line marks zero slope. The black ♦ is the month-aggregate median—the median slope from the aggregated month series (i.e., one series per month created by aggregating stations and then estimating its trend.'),
            html.P(["A difference is present between the ",
                    html.Strong("Macro (aggregated) median (per month) ♦"),
                    " and the ",
                    html.Strong("Station-level median (per month)"),
                    " box (the IQR, from Q1 to Q3) for each month. ",
                    "This difference in median in the macro-aggregation tends to yield differents slopes than the typical station and therefore producing an aggregation bias. How much the month-aggregate median differs from the typical station's median is mentioned below."]),
            html.Ul([
                html.Li("February shows the largest aggregation bias (−2.1 cm/decade): the month-aggregate median is much more negative than the typical station’s median."),
                html.Li("May and December also skew more negative (−1.09 and −0.83 cm/decade)."),
                html.Li("November and March are slightly positive (+0.36 and +0.34 cm/decade), meaning the aggregate month series is a bit less negative than the typical station’s behaviour in those months.")
                ]),
            html.P("Across months, distributions remain predominantly on the negative side of zero, consistent with overall declines in snowpack, but the magnitude of that decline depends on how you aggregate."),
            html.P([html.Strong("Area Of Concern")]),
            html.P("Aggregating first (then estimating a single trend) does not always equal the median of station-level trends. Seasonal changes in coverage, station heterogeneity, and nonlinearity can make the aggregate month series exaggerate winter-core declines (Feb) relative to the typical station, and occasionally mute them (Nov/Mar)."),
            html.P("Further analysis of this aggregation bias should be applicable to continuing this project.")
        ]))
    ]),

    dbc.Row([
        dbc.Col(html.Div(className='chart-header',children=[
            html.H3("Month Mean Snowpack Series",className='display-3'),
            html.P("This figure uses the same dataframes of station-month-level and month-level trend results. Each point is the Theil–Sen slope (cm/decade) and p-value computed on the month-average time snowpack series of Nov -> May, produced from the Hamed–Rao autocorrelation adjustment variant of the Mann-Kendall test."),
            html.Ul([
                html.Li([html.Strong("Left Chart: "), "Station-Months: each point is a station-month time series Theil–Sen slope plotted against its two-sided MK p-value."]),
                html.Li([html.Strong("Right Chart: "),"Month: one point per Month from MK applied to the Month mean snowpack time series."]),
                html.Li([html.Strong("Guide Lines: "),
                         html.Ul([
                             html.Li("The horizontal dashed red line marks the significance threshold (α = 0.05); points below it are statistically significant. "),
                             html.Li("The vertical dashed blue line marks zero slope (left = declines; right = increases).")
                         ])
                        ])
                    ])
        ])),
        dbc.Col(dcc.Graph(id='month-trends',figure=month_fig),width=12),
        dbc.Col(html.Div(className='chart-interpretation',children=[
            html.P("Months April and May exhibit statistically significant decreases in European-Alps mean snowpack depth, with Sen slopes of roughly  -1.60 and -1.10 cm per decade respectively. All other winter months, February, December, January, November and March show negative but non-significant trends, with Sen Slopes of roughly -0.55 to -1.90 cm per decade. \n "
            "These decreases ccannot be distinguished from zero trend due to insufficient evidence (α=0.05). "),
            html.P("Further analysis can investiage changes in weather patterns of Springs months (April, May) to link correlation of decreasing Sen slopes of mean snowpack depths. ")
        ]))
    ]),

    dbc.Row([
        dbc.Col(html.Div(className='chart-header',children=[
            html.H3("Country Month Heatmap",className='display-3'),
            html.P("The following figure shows the median Theil-Sen slope per decade for the typical station of each country-month."),
            html.P("The value ontop of heat squares is the share of the station-month series that are statistically significant by the Hamed–Rao–adjusted Mann–Kendall test (two-sided, α = 0.05)."),
            html.Ul([
                html.Li([
                    html.Strong("Guide Lines: "),
                    html.Ul([
                        html.Li("Use color to compare the magnitude and direction of the typical (median) station trend for each country-month."),
                        html.Li("Use the percent lbel to gauge how widespread that statistically significant trend is across stations for that country-month."),
                        html.Li("The denominator for each tile is the number of stations available after quantility control in that country-month (Hover statistic:  'n_stations').")
                    ])
                ])
            ])
        ])),
        dbc.Col(dcc.Graph(id='cm-heatmap',figure=country_month_heatmap),width=12),
        dbc.Col(html.Div(className='chart-interpretation',children=[
            html.P(["Each tile shows the ",
                    html.Strong("median station-level"),
                    " Theil–Sen slope (cm/decade) for a given country-month. Color encodes the slope (blue = decline, red = increase; centered at 0), and the label is the share of station-month series that are statistically significant by the Hamed–Rao–adjusted Mann–Kendall test (two-sided, α = 0.05). Hover text includes the exact slope and the number of stations contributing to that cell."]),
            html.P([html.Strong("Declines dominate. "),"Most tiles are blue, indicating negative trends in mean snowpack depth."]),
            html.Ul([
                html.Li("Slovenia (Nov–Dec): Declines of 2.5 - 3.48 cm/decade with 43–64% of station series significant."),
                html.Li("Italy (Apr): Declines at 2.55 cm/decade with 50% significance."),
                html.Li("France (Mar): Declines at 4.09 cm/decade with 26% significant."),
                html.Li("Austria (Nov) and Switzerland (Apr) show significant shares on fringe months of 3.33 - 2.64 cm/decade at 41% and 31% significance respestively.")
            ]),
            html.P("Many cells have low station-level significance. In those months/countries, the median slope should be viewed as descriptive signal rather than broad, station-level consensus."),
            html.P("Seasonality & geography matter. The trends seem to be more negative during the fringe months of early winter and early spring for several countries. Mowever, the month of May lacks strong signifinace and any station-level trends due to overwhelming median levels at 0.00 cm/decade. This finding is conflictive with Macro Aggregation trends of previous charts and is an objective for further analysis")
        ])),
        html.Hr()
    ]),

    dbc.Row([
        dbc.Col(html.Div(className='section-header',children=[
            html.H2("Elevation Band Trends",className='display-2')
            ]))
    ]),
    dbc.Row([
        dbc.Col(html.Div(className="chart-header",children=[
            html.H3("Elevation Band Heatmap",className="display-3"),
            html.P(["The following figure shows the Theil-Sen slope per decade for the for ",html.Strong("month-level mean snowpack depth for each Elevation Band")," across the European Alps."]),
            html.P("The calculated slope is the Theil–Sen estimate computed on the yearly mean snowpack series for each elevation band and month (i.e., slope of the band-level mean across years)"),
            html.Ul([
                html.Li("Guide Lines: "),
                html.Ul([
                    html.Li("Use color to compare the magnitude and direction of the typical (median) station trend for each elevation bands."),
                    html.Li(["The ",html.Strong("●")," black dot ontop of heat squares marks marks cells where the Hamed–Rao–adjusted Mann–Kendall test indicates the trend is statistically significant (p ≤ 0.05)."]),
                    html.Li("Hover Tile Details:"),
                    html.Ul([
                        html.Li("Slope: Theil-San Monotonic trend in cm/decade."),
                        html.Li("p-value: Mann-Kendall (Hamed-Rao varient) two-side p-value."),
                        html.Li("Years Of Data: The count of years contributing to that elevation band-month estimate."),
                        html.Li("Median # Stations: The median number of stations per year within that elevation band-month tile")
                        ])
                    ])
                ]),
            html.P(["Treat cells with ",html.Strong("few years or few stations")," with extra casution due to small sample sizes."]),  
            ])),
        dbc.Col(dcc.Graph(id='elev-heat',figure=elevation_fig),width=12),
        dbc.Col(html.Div(className='chart-interpretation',children=[
            html.P("All elevation bands see a general decline in average snowpack depth per month. Strongest declines at High Elevation (>2,000 m). All tiles predominantly blue, with April showing the largest decrease, but at an extreme level even with ● p ≤ 0.05."),
            html.P(["High Elevation has fewer contributing stations (hover shows median stations/year ≈ 13–19 and years of data). "
            "Data cleaning requirements during MK testing (≥ 30 station-years per time-month series) reduced station availability, especially at High Elevation (a reduction of 60 to ~16). The median stations/year in the hovers reflect this post-cleaning support. ",html.Strong("Treat those cells as higher-variance")," as small samples can yield unstable estimates."]),
            html.P("Late-season signals at lower bands: In May, both Mid (1,000–2,000 m) and Low (≤1,000 m) show small but significant declines (●), while earlier months at these bands are weak or non-significant."),
            html.P("P-values are unadjusted across 21 cells; small significant signals (especially in May at lower bands) should be interpreted with that context.")
        ])),
        html.Hr()
    ]),
    dbc.Row([
        dbc.Col(html.Div(className="conclusion",children=[
            html.H2("Conclusion",className='display-2'),
            html.P("Alpine winter snowpack is declining, with statistically significant, strongest losses at high elevations in late winter/early spring, led by Italy, Slovenia, and Austria. While aggregated summaries often look more negative than station-level medians."),
            html.P([html.Strong("Station-level Trends "),"are present across most countries and months. A majority of station–month series show negative Theil–Sen slopes; These distribution centers sit below zero. Recurrent patterns of stronger declines in early spring (especially at high elevations) are evident. Further outlier cleaning may refine a small share of extreme points but does not change the overall picture."]),
            html.P([html.Strong("Geographical Context "),"Italy, Slovenia, and Austria display statistically significant decreases across several months. France, Switzerland, and Germany generally show smaller or non-significant declines. These east/south vs. west/north differences provide potential further analysis on regional storm tracking and snowfall changes."]),
            html.P([html.Strong("Aggregation Bias "),"observed when comparing the median of station distributions with the macro (country/month) median. This consistent gap shows macro aggregation often yields more negative slopes. For interpretation and reporting, detailing which summary is reference recommendation is to use both medians."]),
            html.P([html.Strong("Date coverage "), "and strict quality control cleaning (≥ 30 years per station, Hamed–Rao MK adjustment) reduced the dataset from 2,794 stations to 795. This improved statistical reliability but left fewer high-elevation series, which should be read with appropriate caution. Limited station counts also explain isolated non-significant tiles in the country-month and elevation-band heatmaps. Expanding to additional sources on Zenodo could strengthen coverage."]),
            html.H3("References",className='display-3'),
            html.Ul([
                html.Li(html.A("Zenodo.org Records #5109574",href="https://zenodo.org/records/5109574",target="_blank", rel="noopener noreferrer")),
                html.Li(html.A("Alpine Convention Organsiation",href="https://www.atlas.alpconv.org/layers/geonode_data:geonode:Alpine_Convention_Perimeter_2025",target="_blank", rel="noopener noreferrer"))
            ])
        ]))
    ]),
    dbc.Row([
        dbc.Col(html.Div(className="conclusion")),
        html.Hr()
    ])
])


# Launch app
if __name__ == "__main__":
    app.run(debug=True)