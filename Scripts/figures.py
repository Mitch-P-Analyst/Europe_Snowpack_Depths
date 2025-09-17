# Custom visualisation figures


# 03_Visualisations



# Country_Trends_Figure

def country_trends_fig(per_station,avg_country, show: bool = False):
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots   
    import numpy as np
    
    countries = sorted(per_station['country'].unique())
    palette   = px.colors.qualitative.Set1  # pick any qualitative palette you like
    color_map = {c: palette[i % len(palette)] for i, c in enumerate(countries)}

    fig = make_subplots(
        rows=1, cols=2, column_widths=[0.65, 0.35], shared_yaxes=True,
        subplot_titles=("Stations (Theil–Sen slope per decade)", "Country")
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

                # put station-specific fields here
                customdata=np.c_[psc['station_id'].to_numpy(),
                             psc.get('name', psc['station_id']).to_numpy()],  # optional name



                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "<b>Station ID</b> %{customdata[0]}<br>"
                    "<b>Slope:</b> %{x:.2f} cm/decade<br>"
                    "<b>p:</b> %{y:.3f}" 
                    "<extra></extra>"
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
                    "Slope: %{x:.2f} cm/decade<br>"
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
        title="Hamed–Rao–adjusted MK; Theil–Sen slopes of snowpack depths",
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
    import numpy as np

    # Months Orders
    order = ['Nov','Dec','Jan','Feb','Mar','Apr','May'] # Seasonal

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
        subplot_titles=("Stations (Theil–Sen slope per decade)", "Month")
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


                # put station-specific fields here
                customdata=np.c_[tsm['station_id'].to_numpy(),
                             tsm.get('name', tsm['station_id']).to_numpy()],  # optional name


                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "<b>Station ID:</b> %{customdata[0]}<br>"
                    "<br>Slope:<br> %{x:.2f} cm/decade<br>"
                    "<br>p:<br> %{y:.3f}" 
                    "<extra></extra>"
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
                    "Slope: %{x:.2f} cm/decade<br>"
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
        title="Hamed–Rao–adjusted MK; Sen slope of snowpack depth per station / per month ",
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
    import plotly.express as px 
    import math
    import pandas as pd
   
    # Month order
    order = ['Nov','Dec','Jan','Feb','Mar','Apr','May'] # Seasonal
    

       # --- consistent Set1 colors per country ---
    countries = sorted(avg_country_month['country'].unique())
    palette   = px.colors.qualitative.Set1                  # the Set1 scheme (9 colors)
    # repeat palette if you have >9 countries
    colors = (palette * math.ceil(len(countries)/len(palette)))[:len(countries)]
    color_map = {c: col for c, col in zip(countries, colors)}

    # 3) enforce order on the data and sort rows accordingly
    cov = avg_country_month.copy()
    cov['month_name'] = pd.Categorical(cov['month_name'],
                                       categories=order, ordered=True)
    cov = cov.sort_values(['country', 'month_name'])


    fig = px.line(cov, x='month_name', y='median_stations_per_year', color='country', color_discrete_map=color_map,
                markers=True, title='Coverage: Median Number of Stations Per Year (by month)',
                labels={
                    'country':'Country'
                })
    fig.update_xaxes(categoryorder='array', categoryarray=order, title='Month')
    fig.update_yaxes(title='Stations / Year')
    
    if show:   
        fig.show()

    return fig



def country_station_slope_distrib(typical_station_month,avg_country_month, show: bool = False):
    import plotly.express as px
    import math
    import plotly.graph_objects as go

       # --- consistent Set1 colors per country ---
    countries = sorted(avg_country_month['country'].unique())
    palette   = px.colors.qualitative.Set1                  # the Set1 scheme (9 colors)
    # repeat palette if you have >9 countries
    colors = (palette * math.ceil(len(countries)/len(palette)))[:len(countries)]
    color_map = {c: col for c, col in zip(countries, colors)}

    # One row per station-month with columns: country, slope_sen_per_decade, p
    station = typical_station_month  # if present

    # Round values for chart
    station_rounded = station.round(4)

    fig = px.violin(station_rounded, x='country', y='slope_sen_per_decade', color='country',color_discrete_map=color_map,
                    box=True, points='all', hover_data=['p','station_id','month_name'], height=500,
                    labels={
                        'month_name':'Month',
                        'p':'p-value',
                        'station_id':'Station ID',
                        'country':'Country',
                        'slope_sen_per_decade':'Slope / Decade'
                    })
    fig.add_hline(y=0, line_dash='dash', line_color='blue')

    # Overlay macro country slopes as diamonds
    over = avg_country_month.groupby('country', as_index=False).agg(
        macro_slope=('slope_per_decade','median')  # or mean; up to you
    )
    fig.add_trace(go.Scatter(
        x=over['country'], y=over['macro_slope'], mode='markers',
        marker=dict(symbol='diamond', size=12, color='black'),
        name='Aggregated Country Series - Median (♦)'
    ))

    fig.update_layout(title='Distribution of station slopes by country',
                    yaxis_title='Slope (cm/decade)', xaxis_title='')
    if show:   
        fig.show()

    return fig





# Distribution of station slopes by month
def month_station_slope_distrib(typical_station_month,avg_month, show: bool = False):
    import plotly.express as px
    import math
    import plotly.graph_objects as go
    import pandas as pd

    # Months Orders
    order = ['Nov','Dec','Jan','Feb','Mar','Apr','May'] # Seasonal

    # Order Station Months
    typical_station_month['month_name'] = pd.Categorical(
        typical_station_month['month_name'], categories=order, ordered=True)
    avg_month['month_name'] = pd.Categorical(avg_month['month_name'], categories=order, ordered=True)
    months = list(order)

    # Consistent coloring
    palette   = px.colors.qualitative.Set2  # pick any qualitative palette you like
    color_map = {m: palette[i % len(palette)] for i, m in enumerate(months)}


    # One row per station-month with columns: country, slope_sen_per_decade, p
    station = typical_station_month  # if present

    # Round values for chart
    station_rounded = station.round(4)

    fig = px.violin(station_rounded, x='month_name', y='slope_theil_per_decade', color='month_name',color_discrete_map=color_map,
                    box=True, points='all', hover_data=['p','station_id','country'], height=500,
                    labels={
                        'month_name':'Month',
                        'p':'p-value',
                        'station_id':'Station ID',
                        'country':'Country',
                        'slope_theil_per_decade':'Slope / Decade'
                    })
    fig.add_hline(y=0, line_dash='dash', line_color='blue')

    # Overlay macro country slopes as diamonds
    over = avg_month.groupby('month_name', as_index=False).agg(
        macro_slope=('slope_per_decade','median')  # or mean; up to you
    )
    fig.add_trace(go.Scatter(
        x=over['month_name'], y=over['macro_slope'], mode='markers',
        marker=dict(symbol='diamond', size=12, color='black'),
        name='Aggregated Month Series — Median (♦)'
    ))

    fig.update_layout(title='Distribution of station slopes by month',
                    yaxis_title='Slope (cm/decade)', xaxis_title='')
    if show:   
        fig.show()

    return fig


def country_month_heat(avg_country_month, typical_country_month, show: bool = False,
                       annotate_percent: bool = True):
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go

    # Month order (seasonal)
    order = ['Nov','Dec','Jan','Feb','Mar','Apr','May']

    # Merge macro p and make a flag for the black dot
    sig = avg_country_month.loc[:, ['country','month_name','p']].copy()
    sig['sig'] = sig['p'] <= 0.05

    H = typical_country_month.merge(sig, on=['country','month_name'], how='left')

    # Pivot what we need
    Z = (H.pivot_table(index='country', columns='month_name',
                       values='median_slope_theil_per_decade')
           .reindex(columns=order))
    PCT = (H.pivot_table(index='country', columns='month_name',
                         values='percent_sig')
             .reindex(columns=order))
    
    N = (H.pivot_table(index='country', columns='month_name',
                       values='num_stations'))

    # -- Heatmap with custom hover that includes percent_sig
    fig = go.Figure(go.Heatmap(
        z=Z.values,
        x=Z.columns, y=Z.index,
        colorscale='RdBu_r', zmid=0,
        colorbar=dict(title='cm/decade'),
        # pass percent_sig as customdata so we can format in hover
        customdata=PCT.values,
        hovertemplate=(
            "Month: %{x}<br>"
            "Country: %{y}<br>"
            "Median station slope: %{z:.2f} cm/decade<br>"
            "<extra></extra>"
        )
    ))

    # after you build Z (slopes) and PCT (percent_sig), also build N (counts)
    CD = np.dstack([PCT.values, N.values])   # customdata: [percent, n]
    fig.data[0].update(
    customdata=CD,
    hovertemplate=(
        "Month: %{x}<br>"
        "Country: %{y}<br>"
        "Median station slope: %{z:.2f} cm/decade<br>"
        "Significant share: %{customdata[0]:.0f}% (n_stations=%{customdata[1]:,})"
        "<extra></extra>"
    )
)


    # OPTIONAL: print the percent in each cell (e.g., "42%")
    if annotate_percent:
        for cy in Z.index:
            for mx in Z.columns:
                pct = PCT.loc[cy, mx]
                if pd.notna(pct):
                    # choose text color against the background: light cells => black, dark => white
                    zval = Z.loc[cy, mx]
                    font_color = 'white' if abs(zval) >= 1.5 else 'black'
                    fig.add_trace(go.Scatter(
                        x=[mx], y=[cy], mode='text',
                        text=[f"{pct:.0f}%"],
                        textfont=dict(color=font_color, size=12),
                        showlegend=False, hoverinfo='skip'
                    ))

    fig.update_layout(
        title=dict(
        text=(
            "Median station Theil–Sen slope by country × month"
            "<br><sup>Labels show % of station–month series with MK p ≤ 0.05; "
            "</sup>"
        ),
        x=0.5, xanchor='center'
    ),
        xaxis_title='', yaxis_title=''
    )

    if show:
        fig.show()

    return fig





# Elevation Band Heatmap
def elevation_band_heat(avg_elevation_month, show: bool = False):
    import numpy as np
    import plotly.express as px
    import plotly.graph_objects as go

    month_order = ['Nov','Dec','Jan','Feb','Mar','Apr','May']
    y_order = ['Low Elevation','Mid Elevation','High Elevation']  # adjust if you prefer a different order

    pivot = (avg_elevation_month
            .pivot_table(index='elevation_band', columns='month_name', values='slope_per_decade')
            .reindex(index=y_order, columns=month_order))
    import numpy as np
    import plotly.express as px
    import plotly.graph_objects as go

    # Pivot for z (slopes) and for custom p-values, same index/column order
    Z = (avg_elevation_month.pivot_table(index='elevation_band',
                                        columns='month_name',
                                        values='slope_per_decade')
        .reindex(index=y_order, columns=month_order))

    P = (avg_elevation_month.pivot_table(index='elevation_band',
                                        columns='month_name',
                                        values='p')             # p-values of months
        .reindex(index=y_order, columns=month_order)).astype(float)
    
    N = (avg_elevation_month.pivot_table(index='elevation_band', columns='month_name',
                                         values='n_years')
         .reindex(index=y_order, columns=month_order))          # years of data

    M = (avg_elevation_month.pivot_table(index='elevation_band', columns='month_name',
                                         values='median_stations_per_year')
         .reindex(index=y_order, columns=month_order))          # median # stations




    fig = px.imshow(
        Z,
        color_continuous_scale='RdBu_r',
        origin='lower',
        # keep the scale centered at 0 (optional but nice)
        zmin=-np.nanmax(np.abs(Z.values)),
        zmax= np.nanmax(np.abs(Z.values)),
        labels=dict(color='Slope (cm/decade)'),
        title='Macro Theil–Sen slope by elevation band × month (● = macro p ≤ 0.05)'
    )

    # ---- attach custom p-values to the HEATMAP and format its hover ----
    # ---- attach customdata: [p, n_years, median_stations_per_year] ----
    # (shape must be (rows, cols, k))
    custom = np.dstack([P.to_numpy(), N.to_numpy(), M.to_numpy()])
    fig.data[0].customdata = custom

    fig.data[0].hovertemplate = (
        "Month: %{x}<br>"
        "Elevation band: %{y}<br>"
        "Slope: %{z:.2f} cm/decade<br>"
        "p-value: %{customdata[0]:.4f}<br>"
        "Years of data: %{customdata[1]:.0f}<br>"
        "Median # stations: %{customdata[2]:.0f}"
        "<extra></extra>"
    )

    # ---- optional: overlay significance dots (and show p to 4 dp) ----
    sig = avg_elevation_month.query('p <= 0.05')
    fig.add_trace(go.Scatter(
        x=sig['month_name'],
        y=sig['elevation_band'],
        mode='markers',
        marker=dict(color='black', size=8),
        showlegend=False,
        customdata=sig['p'].to_numpy(),
        hovertemplate='Month: %{x}<br>Elevation band: %{y}<br>p-value: %{customdata:.4f}<extra></extra>'
    ))

    label_map = {
    'Low Elevation':  'Low Elevation (≤1,000 m)',
    'Mid Elevation':  'Mid Elevation (1,001–2,000 m)',
    'High Elevation': 'High Elevation (>2,000 m)',
}

    fig.update_xaxes(title_text='Month', categoryorder='array', categoryarray=month_order)
    fig.update_yaxes(title_text='Elevation Band',
        categoryorder='array',
        categoryarray=y_order,                      # keep data categories
        tickmode='array',
        tickvals=y_order,                           # same categories as in data
        ticktext=[label_map[v] for v in y_order])   # what the viewer sees)
    fig.update_coloraxes(colorbar_title='cm/decade')

    if show:   
        fig.show()

    return fig


#------------