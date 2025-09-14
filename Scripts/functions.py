# 02_EDA

# Get Month Name

import calendar

def get_month_name(month_number) -> str | None:
    """
    Convert month number (1..12) to abbreviated name like 'Jan'.
    Returns None for invalid inputs.
    """
    try:
        m = int(month_number)
        if 1 <= m <= 12:
            return calendar.month_abbr[m]   # 'Jan', 'Feb', ...
    except (TypeError, ValueError):
        pass
    return None
    

# Get Country Abreviation

COUNTRY_ABR = {
    'Austria': 'AT',
    'France': 'FR',
    'Germany': 'DE',
    'Italy': 'IT',
    'Slovenia': 'SI',
    'Switzerland': 'CH',
}

def get_country_abr(country_name: str) -> str:
    """
    Map full country name to ISO-like abbreviation; 
    fall back to original name if not found.
    """
    return COUNTRY_ABR.get(country_name, country_name)
    


# 03_Visualisations



# Country_Trends_Figure

def country_trends_fig(per_station,avg_country):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots   
    
    countries = sorted(per_station['country'].unique())

    fig = make_subplots(
        rows=1, cols=2, column_widths=[0.65, 0.35], shared_yaxes=True,
        subplot_titles=("Stations (Theil–Sen slope per decade)", "Country averages")
    )

    # One legend item per country; traces that share legendgroup toggle together
    for c in countries:
        psc = per_station[per_station['country'] == c]
        avg = avg_country[avg_country['country'] == c]

        # Left panel: station points
        fig.add_trace(
            go.Scatter(
                x=psc['median_slope_theil_per_decade'],
                y=psc['p_combined'],
                mode="markers",
                name=c,
                legendgroup=c,
                marker=dict(size=6, opacity=0.55),
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
                marker=dict(size=12, line=dict(width=1.5, color="black")),
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

    fig.show()



# Month_Trends_Figure

def month_trends_fig(typical_station_month,avg_month):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    order = ['Jan','Feb','Mar','Apr','May','Nov','Dec']  # include only months you plot
    typical_station_month['month_name'] = pd.Categorical(
        typical_station_month['month_name'], categories=order, ordered=True)
    avg_month['month_name'] = pd.Categorical(avg_month['month_name'], categories=order, ordered=True)
    months = list(order)

    fig = make_subplots(
        rows=1, cols=2, column_widths=[0.65, 0.35], shared_yaxes=True,
        subplot_titles=("Stations (Theil–Sen slope per decade)", "Month averages")
    )

    # One legend item per country; traces that share legendgroup toggle together
    for m in months:
        tsm = typical_station_month[typical_station_month['month_name'] == m]
        avg = avg_month[avg_month['month_name'] == m]

        # Left panel: station points
        fig.add_trace(
            go.Scatter(
                x=tsm['slope_sen_per_decade'],
                y=tsm['p'],
                mode="markers",
                name=m,
                legendgroup=m,
                marker=dict(size=6, opacity=0.55),
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
                marker=dict(size=12, line=dict(width=1.5, color="black")),
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

    fig.show()
#------------