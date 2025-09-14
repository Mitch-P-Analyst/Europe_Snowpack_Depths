# Custom visualisation figures


# 03_Visualisations



# Country_Trends_Figure

def country_trends_fig(per_station,avg_country, show: bool = False):
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots   
    
    countries = sorted(per_station['country'].unique())
    palette   = px.colors.qualitative.Set1  # pick any qualitative palette you like
    color_map = {c: palette[i % len(palette)] for i, c in enumerate(countries)}

    fig = make_subplots(
        rows=1, cols=2, column_widths=[0.65, 0.35], shared_yaxes=True,
        subplot_titles=("Stations (Theil–Sen slope per decade)", "Country averages")
    )

    # One legend item per country; traces that share legendgroup toggle together
    for c in countries:
        psc = per_station[per_station['country'] == c]
        avg = avg_country[avg_country['country'] == c]
        col = color_map[c]

        # Left panel: station points
        fig.add_trace(
            go.Scatter(
                x=psc['median_slope_theil_per_decade'],
                y=psc['p_combined'],
                mode="markers",
                name=c,
                legendgroup=c,
                marker=dict(color=col,size=6, opacity=0.55),
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Slope: %{x:.2f} cm/decade<br>"
                    "p: %{y:.3f}<extra></extra>"
                ),
                text=psc['country'],
                showlegend=True,     # legend item shown here
            ),
            row=1, col=1
        )

        # Right panel: country average point (bigger marker + label)
        fig.add_trace(
            go.Scatter(
                x=avg['slope_per_decade'],
                y=avg['p'],
                mode="markers+text",
                text=avg['country_abr'],
                textposition="top center",
                marker=dict(color=col,size=12, line=dict(width=1.5, color="black")),
                name=c,
                legendgroup=c,
                showlegend=False,    # use the same legend item as the left trace
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Avg slope: %{x:.2f} cm/decade<br>"
                    "p: %{y:.3f}<extra></extra>"
                ),
            ),
            row=1, col=2
        )

    # Guides: p=0.05 and zero slope on both subplots
    for col in (1, 2):
        fig.add_hline(y=0.05, line_dash="dash", line_color="red", row=1, col=col)
        fig.add_vline(x=0.0, line_dash="dash", line_color="blue", row=1, col=col)

    # Nice defaults
    fig.update_layout(
        title="Hamed–Rao–adjusted MK; Theil–Sen slopes of mean snowpack depths",
        legend_title="Toggle countries",
        legend=dict(groupclick="togglegroup"),   # one click toggles both traces for a country
        margin=dict(l=60, r=20, t=60, b=60),
    )

    fig.update_xaxes(title_text="Slope (cm/decade)", row=1, col=1)
    fig.update_xaxes(title_text="Slope (cm/decade)", row=1, col=2)
    fig.update_yaxes(title_text="p-value (two-sided)")
    
    if show:   # optional convenience
        fig.show()

    return fig



# Month_Trends_Figure

def month_trends_fig(typical_station_month,avg_month, show: bool = False):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import pandas as pd
    import plotly.express as px

    # Months Orders
    order = ['Jan','Feb','Mar','Apr','May','Nov','Dec']  # include only months you plot

    # Order Station Months
    typical_station_month['month_name'] = pd.Categorical(
        typical_station_month['month_name'], categories=order, ordered=True)
    avg_month['month_name'] = pd.Categorical(avg_month['month_name'], categories=order, ordered=True)
    months = list(order)

    # Consistent coloring
    palette   = px.colors.qualitative.Set2  # pick any qualitative palette you like
    color_map = {m: palette[i % len(palette)] for i, m in enumerate(months)}

    fig = make_subplots(
        rows=1, cols=2, column_widths=[0.65, 0.35], shared_yaxes=True,
        subplot_titles=("Stations (Theil–Sen slope per decade)", "Month averages")
    )

    # One legend item per country; traces that share legendgroup toggle together
    for m in months:
        tsm = typical_station_month[typical_station_month['month_name'] == m]
        avg = avg_month[avg_month['month_name'] == m]
        col = color_map[m]

        # Left panel: station points
        fig.add_trace(
            go.Scatter(
                x=tsm['slope_sen_per_decade'],
                y=tsm['p'],
                mode="markers",
                name=m,
                legendgroup=m,
                marker=dict(color=col,size=6, opacity=0.55),
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Slope: %{x:.2f} cm/decade<br>"
                    "p: %{y:.3f}<extra></extra>"
                ),
                text=tsm['month_name'],
                showlegend=True,     # legend item shown here
            ),
            row=1, col=1
        )

        # Right panel: month average point (bigger marker + label)
        fig.add_trace(
            go.Scatter(
                x=avg['slope_per_decade'],
                y=avg['p'],
                mode="markers+text",
                text=avg['month_name'],
                textposition="top center",
                marker=dict(color=col,size=12, line=dict(width=1.5, color="black")),
                name=m,
                legendgroup=m,
                showlegend=False,    # use the same legend item as the left trace
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Avg slope: %{x:.2f} cm/decade<br>"
                    "p: %{y:.3f}<extra></extra>"
                ),
            ),
            row=1, col=2
        )

    # Guides: p=0.05 and zero slope on both subplots
    for col in (1, 2):
        fig.add_hline(y=0.05, line_dash="dash", line_color="red", row=1, col=col)
        fig.add_vline(x=0.0, line_dash="dash", line_color="blue", row=1, col=col)




    # Nice defaults
    fig.update_layout(
        title="Hamed–Rao–adjusted MK; Sen slope of mean snowpack depth per station / per month-average",
        legend_title="Toggle months",
        legend=dict(groupclick="togglegroup"),   # one click toggles both traces for a country
        margin=dict(l=60, r=20, t=60, b=60),
    )

    fig.update_xaxes(title_text="Slope (cm/decade)", row=1, col=1)
    fig.update_xaxes(title_text="Slope (cm/decade)", row=1, col=2)
    fig.update_yaxes(title_text="p-value (two-sided)")

    if show:   # optional convenience
        fig.show()

    return fig


# Country Coverage Number Of Stations
def country_coverage(avg_country_month, show: bool = False):
    # Month order
    order = ['Jan','Feb','Mar','Apr','May','Nov','Dec']
    import plotly.express as px
    cov = avg_country_month.copy()
    cov['month_name'] = cov['month_name'].astype('category')
    fig = px.line(cov, x='month_name', y='median_stations_per_year', color='country',
                markers=True, title='Coverage: Median Number of Stations Per Year (by month)',
                labels={
                    'country':'Country'
                })
    fig.update_xaxes(categoryorder='array', categoryarray=order, title='Month')
    fig.update_yaxes(title='Stations / Year')
    
    if show:   
        fig.show()

    return fig
#------------