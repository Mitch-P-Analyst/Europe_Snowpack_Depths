# Packages
import dash
import pandas as pd
from dash import html, dcc
from dash.dependencies import Output, Input
import plotly as pt
import dash_bootstrap_components as dbc 
from pathlib import Path
import sys 
import os

# Directories
REPO_ROOT = Path(__file__).resolve().parent.parent      # Main Repo Directory
sys.path.insert(0, str(REPO_ROOT))                      # Assign REPO ROOT as Directory 0 for Import searches
ASSETS_DIR = REPO_ROOT / "app/assets"


# Git LFS support
LFS_POINTER_SIGNATURE = "version https://git-lfs.github.com/spec/v1"

# AI Recommended procedure to ensure CSVs successful
def ensure_lfs_data_downloaded(file_path: Path) -> None:
    """Raise a helpful error if the target file is still an unfetched Git LFS pointer."""

    if not file_path.exists():
        return

    try:
        with file_path.open("r", encoding="utf-8", errors="ignore") as file_obj:
            first_line = file_obj.readline()
    except OSError:
        return

    if LFS_POINTER_SIGNATURE in first_line:
        raise RuntimeError(
            f"{file_path} appears to be a Git LFS pointer file. Please run `git lfs install && git lfs pull` to download "
            "the required datasets before launching the Dash app."
        )

# AI Recommended procedure to ensure CSVs successful
def read_dataset(relative_path: str, **kwargs):
    file_path = REPO_ROOT / relative_path
    ensure_lfs_data_downloaded(file_path)
    kwargs.setdefault("index_col", False)
    return pd.read_csv(file_path, **kwargs)

# Load Files

# Macro-perspective Trends
avg_country = read_dataset('Data/Cleaned/Tests/med_country_trends.csv')                  # Average Snowpack Depth Trend Per Country
avg_country_month = read_dataset('Data/Cleaned/Tests/med_country_month_trends.csv')      # Average Snowpack Depth Trend Per Country Month
avg_month = read_dataset('Data/Cleaned/Tests/med_month_trends.csv')                      # Average Snowpack Depth Trend per Month
avg_elevation_month = read_dataset('Data/Cleaned/Tests/med_elevation_month_trends.csv')  # Average Snowpack Depth Trend Per Elevation Bad Mong
# Micro-persective Trends
typical_country = read_dataset('Data/Cleaned/Tests/station-month-time-series-by-country.csv')                # Typical Snowpack Depth Trend of Weather Station Per Country 
typical_country_month = read_dataset('Data/Cleaned/Tests/station-month-time-series-by-country-month.csv')    # Typical Snowpack Depth Trend of Weather Station Per Country Month
typical_station_month = read_dataset('Data/Cleaned/Tests/station-month-time-series.csv')                     # Typical Snowpack Depth Trend of Weather Station Per Month
per_station = read_dataset('Data/Cleaned/Tests/per_station_series.csv')                                      # Annual Snowpack Depth Trend per Weather Station

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
            html.H3("A Statistical Analysis of Average Snowpack Depth Across Weather Stations in the European Alps"),
            html.P("Sourced from the Zenodo repository, project data included monthly measurements from 2794 weather stations across 12 providers in countries of the European Alps between 1865 - 2019. Through exploratory data analysis, requiring a minimum of 30 years of month-level data across winter months, and restricting to weather stations inside Alpine Convention's 2025 geographical perimeter of the European Alps, the analytic sample is composed of 795 stations. " \
            "These stations produced 5,309 station-month time series between the years of 1936-2019."),
            html.P("Trends were evaluated with the Mann–Kendall test (with Hamed–Rao autocorrelation adjustment) and Theil–Sen slope estimates, comparing patterns across months, countries, and elevation bands."),
            html.P("Data is assessed to two approaches;"),
            html.Ul([
                html.Li([html.Strong("Station-level (Micro) View — 'What is a typical station doing?'"), " For each station (and month), a time series of average snow depth is built, then an estimated Theil–Sen slope and MK p-value computed, followed by summary the distribution across stations by month/country/elevation. The median of station slopes represents the “typical station” and is robust to outliers."]),
                html.Li([html.Strong("Aggregated-series (Macro) View — 'What is the area-wide series doing?'"), " For each grouping (e.g., month across all stations, a country, or an elevation band), stations are aggregated per year (using the median to reduce outlier influence) to form a single time series, then the estimated Theil–Sen slope and MK p-value on that series is computed. This gives an area-wide/seasonal trend."])
                ]),
            html.P("Aggregation Effect : The macro slope (trend of an aggregated series) differs from the micro median of station slopes throughout this project. This is mentioned during analysis and therefore showed and compared both throughout."),
            html.Hr()
            ]))
            ]),

    dbc.Row([
        dbc.Col(html.Div(className='chart-header',
                         children=[
                             html.H2("Station Coverage for each Country",className='display-2'),
                             html.P("This chart shows, by country and winter month, the median number of stations per year that pass the analysis filters of ≥ 30 years of data and ≥ 10 stations/year. It communicates quality check on data coverage for the country and month level trend plots that follow.")
                             ])),
        dbc.Col(dcc.Graph(id='country-coverage',figure=coverage_fig),width=12),
        dbc.Col(html.Div(className='chart-interpretation',
                         children=[
                             html.Ul([
                                 html.Li("Italy has the lowest median quantity of weather stations subject to statsitical anlaysis at 42 in months May and November."),
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
            html.P("This chart shows the distribution of station–month time series slopes (Theil–Sen, cm/decade) by country. Each dot in the violin spread is an individual station-month series. \
                   The black diamond ♦ marks a macro signal, showing the Theil–Sen slope (cm/decade) from the Hamed–Rao MK adjustment of the median of the country-level seasonal aggregated series. This captures each country’s central seasonal trend while remaining robust to outliers and month-to-month imbalance. \
                   The horizontal dashed blue line is zero-slope change; values below it indicate long-term declines.")
        ])),
        dbc.Col(dcc.Graph(id='country_distrib',figure=country_station_disb),width=12),
        dbc.Col(html.Div(className='chart-interpretation',children=[
             html.P("Extreme values are present in both postive and negative directions for countries France, Germany, Italy and Switzerland. While all 5,309 station-month time series presented in this chart have undergone cleaning, meeting thresholds of >= 30 years of data during Mann–Kendall testing, further analysis may be viable to review extreme values."),
             html.P("All countries, except Italy, present a negative median Theil-Sen slope value per decade for the typical regional weather station. Comparatively, all countries except Switerzland present a negative Theil-Sen slope across the aggreated country-level. " \
             "This variation between country-level aggregation and the median station-level value raises awareness about aggregation effect causing potential bias.")
                    ])),
        dbc.Col(html.Div(className='chart-header',children=[
            html.H3("Country-Year Mean Snowpack Series",className='display-3'),
            html.P("This figure compares station-level and country-level trend results using the Mann–Kendall (MK) test with the Hamed–Rao autocorrelation adjustment and Theil–Sen slope estimates (cm/decade)."),
            html.Ul([
                html.Li([
                    html.Strong('Left Chart: '),'Each point is a station’s Theil–Sen slope plotted against its two-sided MK p-value.'
                ]),
                html.Li([
                    html.Strong('Right Chart: '),'One point per country from MK applied to the country–year aggregated snowpack series.'
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
            html.P("Countries Italy, Slovenia, Austria and Germany exhibit statistically significant decreases in country-level snowpack depth, with Theil-Sen slopes of  −1.51 to −2.84 cm per decade. Switzerland shows a negative, but non-significant trend of -0.65 cm/decade. Therefore this decrease is not distinguishable from zero at 𝛼 = 0.05. France shows a non-significant and 0.00 cm slope."),
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
            html.P("This chart shows the distribution of Theil–Sen slopes (cm/decade) for all station–month time series. Each dot in the violin spread is an individual station-month series."),
            html.P('The black diamond ♦ is the Theil-Sen Slope of the median value in aggregated month-series for that respective month. Diamonds below a value of 0 indicate that the month-series Theil-Sen slope declines that month; the more negative, the steeper the decline.'),
            html.P('The horizontal dashed blue line is zero-slope change; values below it indicate long-term declines.')
        ])),
        dbc.Col(dcc.Graph(id='month_distrib',figure=month_station_disb),width=12),
        dbc.Col(html.Div(className='chart-interpretation',children=[
            html.P('Each violin is the distribution of station–month Theil–Sen slopes (cm/decade) for that month. The dashed blue line marks zero slope.'),
            html.P(['The black diamond ♦ is the Theil–Sen slope of the Marco monthly-series for each month (Nov–May). The Marco monthly series the aggregation of stations by month to form one time series, then a single Theil–Sen slope is computed on the ',html.Strong('median value'),' of that series.']),
            html.P(["A difference is present between the ",
                    html.Strong("Macro month-series ♦"),
                    " and the ",
                    html.Strong("Station-level median IQR box "),
                    "for each month. This difference in slope between the aggregated month-series and station-level median yields stronger negative results for core winter months (Dec, Jan, Feb) and postive results for fringe winter months (Nov, Mar, Apr) as a result of aggregation. Observing this difference in trends as an aggregation effect should be noted for potential biases, along with further consideration for aggreation affect on core verus fringe winter months. How much the month-aggregate median differs from the typical station's median is mentioned below."]),
            html.P('Aggregation effect (macro vs. typical station)'),
            html.Ul([
                html.Li("Core winter months December, January and February show large negative aggregation effects of -1.11 , -0.21 and -1.72 cm/decade respectively. Therefore the macro series is more negative than the typical station (stronger declines)."),
                html.Li("Fringe winter months November, March and April show positive aggregation effects of +0.54 , +0.83 and +0.60 cm/decade respectively. Skewing the opposite direction to the other months mentioned above. Therefore the macro series is more positive than the typical station"),
                html.Li("May exhibits no change in Theil-Sen slope between station-level and aggreated month-series.")
                ]),
            html.P("Across months, distributions remain predominantly on the negative side of zero, consistent with overall declines in snowpack, but the the magnitude depends on whether you summarize first (macro ♦) or summarize last (median of station slopes)."),
            html.P([html.Strong("Area Of Concern")]),
            html.P("The diamond ♦ macro-perspectives, of aggregating first (then estimating a single trend), varies from the median of station-level trends by a range of +0.83 to -1.72 cm/decade. Seasonal changes appears to exaggerate fringe winter months, relative to the typical station, and mute core winter months in comparison."),
            html.P("Further analysis of this aggregation effect should be applicable to continuing this project.")
        ]))
    ]),

    dbc.Row([
        dbc.Col(html.Div(className='chart-header',children=[
            html.H3("Month Snowpack Series",className='display-3'),
            html.P("This figure uses the same dataframes of station-month-level and month-level trend results. Each point is the Theil–Sen slope (cm/decade) and p-value computed on the month-average time snowpack series of Nov to May."),
            html.Ul([
                html.Li([html.Strong("Left Chart: "), "Each point is a station-month time series Theil–Sen slope plotted against its two-sided MK p-value."]),
                html.Li([html.Strong("Right Chart: "),"One point per Month from MK applied to the Month-level snowpack time series."]),
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
            html.P("December exhibits a statistically significant decrease in snowpack depth, with Theil-Sen slopes of -2.22 cm/decade. May is also statistically significant, but exhibits a Theil-Sen slope of 0.00."),
            html.P("All other winter months show non-significant trends, with Theil-Sen slopes between 0.00 to -1.57 cm/decade." \
            "These other months cannot be distinguished from zero trend due to insufficient evidence (α=0.05). "),
            html.P("Further analysis should investigate changes in weather patterns and temperature changes of fringe months to link correlation of decreasing Theil-Sen slopes of snowpack depths.")
        ]))
    ]),

    dbc.Row([
        dbc.Col(html.Div(className='chart-header',children=[
            html.H3("Country Month Heatmap",className='display-3'),
            html.P("The following figure shows the median Theil-Sen slope per decade for the typical station of each country-month."),
            html.P("The value presented on each heat square is the share of the station-month series that is statistically significant by the Hamed–Rao–adjusted Mann–Kendall test (two-sided, α = 0.05)."),
            html.Ul([
                html.Li([
                    html.Strong("Guide Lines: "),
                    html.Ul([
                        html.Li("Use color to compare the magnitude and direction of the typical (median) station trend for each country-month."),
                        html.Li("Use the percent label to gauge how widespread that statistically significant trend is across stations for that country-month."),
                        html.Li("The denominator for each tile is the number of stations available after quantility control in that country-month (Hover statistic: 'n_stations').")
                    ])
                ])
            ])
        ])),
        dbc.Col(dcc.Graph(id='cm-heatmap',figure=country_month_heatmap),width=12),
        dbc.Col(html.Div(className='chart-interpretation',children=[
            html.P(["Each tile shows the ",
                    html.Strong("median station-level"),
                    " Theil–Sen slope (cm/decade) for a given country-month."]),
            html.P([html.Strong("Declines dominate. "),"Most tiles are blue, indicating negative trends in mean snowpack depth."]),
            html.Ul([
                html.Li("Slovenia (Nov–Dec): Declines of 1.11 - 3.48 cm/decade with 43 – 64% of station series significant."),
                html.Li("Italy (Apr): Declines at 2.55 cm/decade with 50% significance."),
                html.Li("France (Mar): Declines at 4.09 cm/decade with 26% significant."),
                html.Li("Austria (Nov) and Switzerland (Apr) show significant shares on fringe months of 3.33 - 2.64 cm/decade at 41% and 31% significance respestively."),
                html.Li("April as month is strongly declining across all countries with reasonably high shares of statistical signifiance across each tile.")
            ]),
            html.P("Many cells have low station-level significance. In those months/countries, the median slope should be viewed as descriptive signal rather than broad, station-level consensus."),
            html.P("Seasonality & geography matter. The trends seem to be more negative during the fringe months of early winter and early spring for several countries. However, the month of May lacks strong signifinace and any station-level trends due to overwhelming median levels at 0.00 cm/decade.")
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
            html.P(["The following figure shows the Theil-Sen slope per decade for the ",html.Strong("month-level snowpack depth for each Elevation Band")," (i.e., slope of the elevation band-level median across years)"]),
            html.Ul([
                html.Li("Guide Lines: "),
                html.Ul([
                    html.Li("Use color to compare the magnitude and direction of the aggregated station-month median value trend for each elevation bands."),
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
            html.P("All elevation bands see a general decline in snowpack depth per month. Strongest declines at High Elevation (>2,000 m). All tiles predominantly blue, with April showing the largest decrease, but at an extreme level even with ● p ≤ 0.05."),
            html.P(["High Elevation has fewer contributing stations (hover shows median stations/year ≈ 13–19 and years of data). "
            "Data cleaning requirements during MK testing (≥ 30 station-years per time-month series) reduced station availability, especially at High Elevation (a reduction of 60 to ~16). The median stations/year in the hovers reflect this post-cleaning support. ",html.Strong("Treat those cells as higher-variance")," as small samples can yield unstable estimates."]),
            html.P("Late-season signals at lower bands: In May, the Mid Elevation(1,000–2,000 m) shows a small but significant declines (●), while earlier months at these bands are weak or non-significant."),
            html.P("P-values are unadjusted across 21 cells; small significant signals (especially in May at lower bands) should be interpreted with that context.")
        ])),
        html.Hr()
    ]),
    dbc.Row([
        dbc.Col(html.Div(className="conclusion",children=[
            html.H2("Conclusion",className='display-2'),
            html.P("Alpine winter snowpack is declining, with statistically significant, strongest losses at high elevations in early winter/early spring, led by Italy, Slovenia, Austria and Germany. While aggregated summaries are exaggerated in core months and muted in fringe months compared to station-level medians."),
            html.P([html.Strong("Station-level Trends "),"are present across most countries and months. A majority of station–month series show negative Theil–Sen slopes with distribution centers below zero. Recurring patterns of stronger declines in early winter and early spring (especially at high elevations) are evident. Further outlier cleaning may address a small share of extreme points, but does not change the overall picture."]),
            html.P([html.Strong("Geographical Context "),"Italy, Slovenia and Austria display strong statistically significant decreases across several months. France, Switzerland, and Germany generally show smaller or non-significant declines. These south/east vs. north/west differences provide potential further analysis on regional storm tracking and snowfall changes."]),
            html.P([html.Strong("Aggregation Effect "),"is observed when we compare the Theil–Sen slope of the country-level and month-level aggregated winter series (stations aggregated first, then trend estimated) with the median of station-level trends (or month-level medians). We see a consistent gap between the aggregated series and the station-level / month-level medians, usually yielding a more negative slope for core months and more positive slope for fringe months from aggregations. This project does not dive into proving a directional distortion from aggregation, therefore for interpretation, report both summaries and state explicitly which one you reference."]),
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

def main():
    port = int(os.getenv("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=True)

