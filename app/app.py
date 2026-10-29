from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import style as s

# ---------- Page setup ----------
st.set_page_config(page_title="Exoplanet Explorer", page_icon=":material/public:", layout="wide", initial_sidebar_state="collapsed")
s.apply_style()
s.force_english_direction()
s.space_background()


# ---------- Load data ----------
@st.cache_data
def load_data():
    path = Path(__file__).parent / "clean_data.csv"
    return pd.read_csv(path)


df = load_data()

# ---------- Hero ----------
nearest = df[df["earth_like"] & df["radius_measured"]].nsmallest(1, "distance_ly").iloc[0]
s.hero(len(df), nearest["planet_name"], nearest["distance_ly"])

# -----------------------------
# ---------- Sidebar ----------
TYPE_ORDER = ["Earth-sized", "Super-Earth", "Neptune-like", "Jupiter-like", "Larger than Jupiter"]
method_options = ["All methods"] + df["discovery_method"].value_counts().index.tolist()
year_min, year_max = int(df["discovery_year"].min()), int(df["discovery_year"].max())

with st.sidebar:
    s.html('<div style="font-family:\'Space Grotesk\',sans-serif; font-size:15px; letter-spacing:0.32em; margin-bottom:18px;">EXOPLANET EXPLORER</div>')
    s.html('<div class="label">About the data</div>')
    st.write(
        f"All {len(df):,} confirmed exoplanets from NASA's Exoplanet Archive "
        f"(Planetary Systems Composite Parameters), discovered {year_min}–{year_max}. "
        "One row per planet: how it was found, its size, orbit, temperature and host star."
    )
    st.markdown("[exoplanetarchive.ipac.caltech.edu](https://exoplanetarchive.ipac.caltech.edu)")

    st.divider()
    s.html('<div class="label" style="margin-bottom:8px;">Filters</div>')

    method = st.selectbox("Discovery method", method_options)
    years = st.slider("Discovery year", year_min, year_max, (year_min, year_max))
    types = st.multiselect("Planet type", TYPE_ORDER, default=TYPE_ORDER)
    measured_only = st.checkbox(
        "Measured values only",
        help="Hide planets whose radius was calculated from their mass instead of being measured.",
    )

# ---------- Apply the filters ----------
filtered = df[df["discovery_year"].between(years[0], years[1])]

if method != "All methods":
    filtered = filtered[filtered["discovery_method"] == method]

all_types_selected = len(types) == len(TYPE_ORDER)
filtered = filtered[filtered["planet_type"].isin(types) | (all_types_selected & filtered["planet_type"].isna())]

if measured_only:
    filtered = filtered[filtered["radius_measured"]]

with st.sidebar:
    s.html(f"""
    <div class="stat" style="margin-top:12px;">
      <div class="card-head"><span class="label">Data source</span><span class="pill pill-good">CLEANED</span></div>
      <span style="font-size:13px; color:#C3CED8;">NASA Exoplanet Archive · 25 Oct 2026</span>
      <span class="stat-sub">Showing {len(filtered):,} of {len(df):,} planets</span>
    </div>
    """)

if filtered.empty:
    st.warning("No planets match these filters. Try widening the year range or selecting more planet types.")
    st.stop()

active = [method, f"{years[0]}–{years[1]}",
          "all planet types" if all_types_selected else f"{len(types)} planet types"]
if measured_only:
    active.append("measured values only")
s.html(f"""
<div style="display:flex; flex-wrap:wrap; align-items:center; gap:8px; margin:0 0 16px 0;">
  <span class="label">Active filters</span>
  {''.join(f'<span class="pill pill-good">{a}</span>' for a in active)}
  <span class="stat-sub">· open the sidebar (» top left) to change them</span>
</div>
""")

# ---------- Key numbers (react to the filters) ----------
measured = filtered[filtered["radius_measured"]]
candidates = measured[measured["earth_like"]].sort_values("distance_ly")
transit_share = (filtered["discovery_method"] == "Transit").mean() * 100

if len(candidates) > 0:
    nearest_value = f"{candidates['distance_ly'].iloc[0]:.1f} ly"
    nearest_sub = candidates["planet_name"].iloc[0]
else:
    nearest_value, nearest_sub = "None", "no match with these filters"

s.stat_cards([
    {"label": "Planets", "value": f"{len(filtered):,}", "sub": f"discovered {years[0]}–{years[1]}", "pill": "CLEANED", "kind": "good"},
    {"label": "Methods", "value": filtered["discovery_method"].nunique(), "sub": f"Transit found {transit_share:.0f}%", "pill": "BIAS", "kind": "warn"},
    {"label": "Earth-like", "value": len(candidates), "sub": "with a measured size", "pill": "RARE", "kind": "info"},
    {"label": "Nearest", "value": nearest_value, "sub": nearest_sub, "pill": "TARGET", "kind": "good"},
])

# ---------- Tabs ----------
tab_overview, tab_discoveries, tab_earth, tab_data = st.tabs(
    ["Overview", "Discoveries", "Earth 2.0 Finder", "Data"]
)

# ---------- Tab 1: Overview ----------
with tab_overview:

    # Chart 1: radius valley histogram
    with st.container(border=True, key="card_radius"):
        s.card_header("Planet sizes", "The radius valley", f"MEASURED RADII · {len(measured):,}")

        if measured.empty:
            st.info("No planets with a measured radius match these filters.")
        else:
            edges = np.logspace(np.log10(0.5), np.log10(20), 41)
            counts, _ = np.histogram(measured["radius_earth"], bins=edges)
            centers = np.sqrt(edges[:-1] * edges[1:])
            colors = [s.AMBER if 1.6 <= c < 2.0 else s.MINT for c in centers]

            fig = go.Figure(go.Bar(
                x=centers, y=counts, width=edges[1:] - edges[:-1],
                marker_color=colors, marker_line_width=0,
                customdata=np.stack([edges[:-1], edges[1:]], axis=1),
                hovertemplate="%{customdata[0]:.2f}–%{customdata[1]:.2f} Earth radii<br>%{y} planets<extra></extra>",
            ))
            in_valley = (centers >= 1.6) & (centers < 2.0)
            valley_top = counts[in_valley].max()
            fig.add_annotation(x=np.log10(1.79), y=valley_top, text="RADIUS VALLEY",
                               showarrow=True, arrowhead=0, arrowwidth=1, arrowcolor=s.AMBER,
                               ax=0, ay=-45, yanchor="bottom",
                               font=dict(color=s.AMBER, size=11))
            s.style_chart(fig, height=340)
            fig.update_xaxes(type="log", tickvals=[0.5, 1, 1.5, 2, 3, 5, 10, 20],
                             ticktext=["0.5", "1", "1.5", "2", "3", "5", "10", "20"],
                             title="Planet radius (Earth = 1, log scale)")
            fig.update_yaxes(title="Number of planets")
            st.plotly_chart(fig, theme=None, config={"displayModeBar": False})

        s.insight("Small planets cluster at about 1.3 and 2.5 Earth radii, with a gap at 1.6–2.0 "
                  "(Fulton et al., 2017). Planets rarely end up this size, likely because many lose "
                  "their atmospheres to radiation from their star.")

    # Charts 2 and 3 side by side
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True, key="card_methods"):
            s.card_header("Discovery methods", "How were they found?", "LOG SCALE", "info")
            method_counts = filtered["discovery_method"].value_counts().sort_values()
            fig = px.bar(x=method_counts.values, y=method_counts.index, orientation="h",
                         log_x=True, text=method_counts.values)
            fig.update_traces(marker_color=s.MINT, textposition="outside", cliponaxis=False,
                              hovertemplate="%{y}: %{x:,} planets<extra></extra>")
            s.style_chart(fig, height=380, left=190)
            fig.update_xaxes(title="Number of planets (log scale)")
            fig.update_yaxes(title=None)
            st.plotly_chart(fig, theme=None, config={"displayModeBar": False})

    with col2:
        with st.container(border=True, key="card_types"):
            s.card_header("Planet types", "Which types are most common?")
            type_counts = filtered["planet_type"].value_counts().reindex(TYPE_ORDER).dropna()
            fig = px.bar(x=type_counts.index, y=type_counts.values, text=type_counts.values,
                         color=type_counts.index,
                         color_discrete_sequence=[s.MINT, s.CYAN, s.LILAC, s.AMBER, s.CORAL])
            fig.update_traces(textposition="outside", cliponaxis=False,
                              hovertemplate="%{x}: %{y:,} planets<extra></extra>")
            s.style_chart(fig, height=380)
            fig.update_layout(showlegend=False)
            fig.update_xaxes(title=None)
            fig.update_yaxes(title="Number of planets")
            st.plotly_chart(fig, theme=None, config={"displayModeBar": False})

    s.insight("Transit found about 74% of all planets. Neptune-like planets are the most common type, "
              "while Earth-sized planets are only about 9%, partly because small planets are harder to detect.")

    # Data quality gauges
    s.html('<div style="height: 28px;"></div>')
    s.card_header("Data quality", "How much of the data was really measured?")
    n = len(filtered)
    mass_measured = (filtered["mass_quality"] == "Measured").sum()
    radius_measured = filtered["radius_measured"].sum()
    both_reliable = ((filtered["mass_quality"] == "Measured") & filtered["radius_measured"]
                     & ~filtered["suspicious_density"]).sum()
    nearby = (filtered["distance_ly"] < 100).sum()

    s.gauge_cards([
        {"label": "Masses measured", "pct": round(mass_measured / n * 100), "value": f"{mass_measured:,}",
         "sub": f"of {n:,} planets", "color": s.AMBER, "pill": "LOW", "kind": "warn"},
        {"label": "Radii measured", "pct": round(radius_measured / n * 100), "value": f"{radius_measured:,}",
         "sub": f"of {n:,} planets", "color": s.MINT, "pill": "GOOD", "kind": "good"},
        {"label": "Mass + radius", "pct": round(both_reliable / n * 100), "value": f"{both_reliable:,}",
         "sub": "both measured", "color": s.CYAN, "pill": "RELIABLE", "kind": "info"},
        {"label": "Within 100 ly", "pct": round(nearby / n * 100), "value": f"{nearby:,}",
         "sub": "planets close to us", "color": s.LILAC, "pill": "NEARBY", "kind": "info"},
    ])

# ---------- Tab 2: Discoveries ----------
TOP_METHODS = ["Transit", "Radial Velocity", "Microlensing", "Imaging"]
METHOD_COLORS = {"Transit": s.MINT, "Radial Velocity": s.CYAN, "Microlensing": s.AMBER,
                 "Imaging": s.LILAC, "Other": s.SLATE}

with tab_discoveries:

    # Chart 4: discoveries per year, stacked by method
    with st.container(border=True, key="card_years"):
        s.card_header("Timeline", "Discoveries per year", f"{years[0]}–{years[1]}", "info")

        grouped = filtered.assign(
            method_group=filtered["discovery_method"].where(filtered["discovery_method"].isin(TOP_METHODS), "Other")
        )
        per_year = grouped.groupby(["discovery_year", "method_group"]).size().reset_index(name="planets")

        fig = px.bar(per_year, x="discovery_year", y="planets", color="method_group",
                     category_orders={"method_group": TOP_METHODS + ["Other"]},
                     color_discrete_map=METHOD_COLORS)
        fig.update_traces(marker_line_width=0, hovertemplate="%{y:,} planets")
        s.style_chart(fig, height=400)
        fig.update_layout(bargap=0.15, margin_t=60, hovermode="x unified")
        fig.update_xaxes(title="Discovery year", dtick=4)
        fig.update_yaxes(title="Number of planets")
        st.plotly_chart(fig, theme=None, config={"displayModeBar": False})

        s.insight("The 2014 and 2016 spikes are NASA's Kepler telescope confirming hundreds of planets at once "
                  "(1,502 in 2016 alone). Before 2010, Radial Velocity found most planets; since 2018, "
                  "the TESS telescope has kept a steady pace.")

    # Chart 5: orbital period by method (detection bias)
    with st.container(border=True, key="card_periods"):
        s.card_header("Detection bias", "Each method finds a different kind of planet", "ORBITAL PERIOD · DAYS", "warn")

        box_data = filtered[filtered["discovery_method"].isin(TOP_METHODS)].dropna(subset=["orbital_period_days"])

        if box_data.empty:
            st.info("None of the four main methods match these filters.")
        else:
            fig = px.box(box_data, x="orbital_period_days", y="discovery_method", color="discovery_method",
                         log_x=True, points=False,
                         category_orders={"discovery_method": TOP_METHODS},
                         color_discrete_map=METHOD_COLORS)
            fig.update_traces(hovertemplate=None, hoverinfo="skip", selector=dict(type="box"))

            stats = box_data.groupby("discovery_method")["orbital_period_days"].describe()
            stats = stats.reindex([m for m in TOP_METHODS if m in stats.index])
            fig.add_trace(go.Scatter(
                x=stats["50%"], y=stats.index, mode="markers",
                marker=dict(size=18, color="rgba(0,0,0,0)"),
                customdata=np.stack([stats["25%"], stats["75%"], stats["count"]], axis=1),
                hovertemplate="<b>%{y}</b><br>Median: %{x:,.0f} days<br>"
                              "Middle 50%: %{customdata[0]:,.0f}–%{customdata[1]:,.0f} days<br>"
                              "Planets: %{customdata[2]:,.0f}<extra></extra>",
                showlegend=False,
            ))

            fig.add_vline(x=365, line_dash="dash", line_color=s.CORAL, line_width=1)
            fig.add_annotation(x=np.log10(365), y=1, yref="paper", text="EARTH'S YEAR", showarrow=False,
                               xanchor="left", yanchor="bottom", xshift=4, font=dict(color=s.CORAL, size=11))
            s.style_chart(fig, height=360, left=130)
            fig.update_layout(showlegend=False, boxmode="overlay")
            fig.update_xaxes(title="Orbital period (days, log scale)")
            fig.update_yaxes(title=None)
            st.plotly_chart(fig, theme=None, config={"displayModeBar": False})

            medians = box_data.groupby("discovery_method")["orbital_period_days"].median()
            parts = [f"{m}: {medians[m]:,.0f} days" for m in TOP_METHODS if m in medians]
            s.insight("Median orbital period · " + " · ".join(parts) + ". Transit mostly finds planets very close "
                      "to their stars, because they pass in front of them often. Since Transit found most planets, "
                      "the dataset favors these close-in worlds. This is detection bias.")

# ---------------------------------------------
# ---------- Tab 3: Earth 2.0 Finder ----------
with tab_earth:
    s.card_header("Earth 2.0 Finder", "Define \"Earth-like\" and see what matches")
    st.caption("Only planets with a measured radius are included. Sidebar filters also apply.")

    c1, c2, c3 = st.columns(3)
    with c1:
        r_range = st.slider("Planet radius (Earth = 1)", 0.3, 4.0, (0.5, 1.6), step=0.05)
    with c2:
        e_range = st.slider("Energy received (Earth = 1)", 0.1, 5.0, (0.35, 1.75), step=0.05)
    with c3:
        max_dist = st.slider("Max distance (light-years)", 10, 3000, 1200, step=10)

    pool = filtered[filtered["radius_measured"] & (filtered["insolation_earth"] > 0) & filtered["distance_ly"].notna()]
    matches = pool[
        pool["radius_earth"].between(r_range[0], r_range[1])
        & pool["insolation_earth"].between(e_range[0], e_range[1])
        & (pool["distance_ly"] <= max_dist)
    ].sort_values("distance_ly")

    if len(matches) > 0:
        top_system = matches["star_name"].value_counts()
        s.stat_cards([
            {"label": "Matching planets", "value": len(matches), "sub": f"out of {len(pool):,} with a measured size", "pill": "MATCH", "kind": "good"},
            {"label": "Nearest match", "value": f"{matches['distance_ly'].iloc[0]:.1f} ly", "sub": matches["planet_name"].iloc[0], "pill": "TARGET", "kind": "good"},
            {"label": "Busiest system", "value": top_system.index[0], "sub": f"{top_system.iloc[0]} matching planets", "pill": "SYSTEM", "kind": "info"},
        ])
    else:
        st.info("No planets match these settings. Try widening the radius or energy range.")

    col_chart, col_table = st.columns([3, 2])

    with col_chart:
        with st.container(border=True, key="card_finder_chart"):
            s.card_header("Size vs. energy", "Where are the matches?", f"{len(matches)} MATCHES")

            others = pool.drop(matches.index)
            fig = go.Figure()
            fig.add_vrect(x0=e_range[0], x1=e_range[1], fillcolor=s.MINT, opacity=0.08, line_width=0, layer="below")
            fig.add_hrect(y0=r_range[0], y1=r_range[1], fillcolor=s.CYAN, opacity=0.06, line_width=0, layer="below")
            fig.add_trace(go.Scatter(
                x=others["insolation_earth"], y=others["radius_earth"], mode="markers", name="Other planets",
                marker=dict(size=4, color="#4E6173"), text=others["planet_name"],
                hovertemplate="%{text}<br>Energy: %{x:.2f} · Radius: %{y:.2f}<extra></extra>",
            ))
            fig.add_trace(go.Scatter(
                x=matches["insolation_earth"], y=matches["radius_earth"], mode="markers", name="Matches",
                marker=dict(size=10, color=s.MINT, line=dict(width=1, color=s.CARD)),
                text=matches["planet_name"], customdata=matches["distance_ly"],
                hovertemplate="<b>%{text}</b><br>Energy: %{x:.2f} · Radius: %{y:.2f}<br>%{customdata:.1f} light-years away<extra></extra>",
            ))
            fig.add_trace(go.Scatter(
                x=[1], y=[1], mode="markers", name="Earth",
                marker=dict(size=16, symbol="star", color=s.CORAL),
                hovertemplate="Earth<extra></extra>",
            ))
            s.style_chart(fig, height=420)
            fig.update_layout(margin_t=60)
            fig.update_xaxes(type="log", autorange="reversed",
                             tickvals=[10000, 100, 1, 0.01], ticktext=["10,000×", "100×", "1×", "0.01×"],
                             title="Energy received from star (Earth = 1, log scale) → colder")
            fig.update_yaxes(type="log", tickvals=[0.5, 1, 2, 5, 10, 20, 50],
                             ticktext=["0.5", "1", "2", "5", "10", "20", "50"],
                             title="Radius (Earth = 1, log scale)")
            st.plotly_chart(fig, theme=None, config={"displayModeBar": False})

    with col_table:
        with st.container(border=True, key="card_finder_table"):
            s.card_header("Nearest matches", "Matching planets", "LIGHT-YEARS", "info")
            table = matches[["planet_name", "radius_earth", "insolation_earth", "planet_temp_k", "distance_ly", "discovery_year"]]
            st.dataframe(
                table, hide_index=True, height=420,
                column_config={
                    "planet_name": st.column_config.TextColumn("Planet"),
                    "radius_earth": st.column_config.NumberColumn("Radius", format="%.2f"),
                    "insolation_earth": st.column_config.NumberColumn("Energy", format="%.2f"),
                    "planet_temp_k": st.column_config.NumberColumn("Temp (K)", format="%.0f"),
                    "distance_ly": st.column_config.NumberColumn("Distance (ly)", format="%.1f"),
                    "discovery_year": st.column_config.NumberColumn("Found", format="%d"),
                },
            )

    s.insight("Proxima Centauri b (4.2 light-years) is closer than any match, but its size has never been "
              "measured, so it is not included. \"Earth-like\" here is a simple screen based on size and energy, "
              "not a confirmation that a planet could support life.", title="NOTE", note=True)

# ---------------------------------
# ---------- Tab 4: Data ----------
PREVIEW_COLS = ["planet_name", "star_name", "discovery_method", "discovery_year", "planet_type",
                "radius_earth", "mass_earth", "mass_quality", "orbital_period_days",
                "planet_temp_k", "insolation_earth", "star_class", "distance_ly"]
STATS_COLS = ["radius_earth", "mass_earth", "orbital_period_days", "planet_temp_k",
              "insolation_earth", "star_temp_k", "distance_ly"]

with tab_data:

    with st.container(border=True, key="card_preview"):
        s.card_header("Data preview", "Filtered planets", f"{len(filtered):,} ROWS")
        st.dataframe(filtered[PREVIEW_COLS], hide_index=True, height=400)
        st.download_button(
            "Download filtered data (CSV)",
            data=filtered.to_csv(index=False).encode("utf-8"),
            file_name="exoplanets_filtered.csv",
            mime="text/csv",
            icon=":material/download:",
        )

    with st.container(border=True, key="card_stats"):
        s.card_header("Summary statistics", "Key numeric columns", "DESCRIBE()", "info")
        st.dataframe(filtered[STATS_COLS].describe().T.round(2))

    with st.container(border=True, key="card_dictionary"):
        s.card_header("Data dictionary", "What each column means")
        dictionary = pd.DataFrame([
            ["planet_name", "Name of the planet", "—"],
            ["star_name", "Name of the star it orbits", "—"],
            ["discovery_method", "How the planet was found", "—"],
            ["discovery_year", "Year the discovery was published", "year"],
            ["planet_type", "Size category based on radius (Kepler mission ranges)", "—"],
            ["radius_earth", "Planet radius", "Earth = 1"],
            ["radius_measured", "True if the radius was measured, False if calculated from mass", "—"],
            ["mass_earth", "Planet mass (upper/lower limits removed)", "Earth = 1"],
            ["mass_quality", "Measured / Minimum estimate / Estimated from radius / Limit only", "—"],
            ["orbital_period_days", "Length of the planet's year", "days"],
            ["insolation_earth", "Energy received from its star", "Earth = 1"],
            ["planet_temp_k", "Estimated planet temperature", "Kelvin"],
            ["star_class", "Star type from its temperature (M, K, G, F, A)", "—"],
            ["distance_ly", "Distance from Earth", "light-years"],
            ["earth_like", "In the habitable zone and rocky-sized (simple screen)", "—"],
        ], columns=["Column", "Meaning", "Unit"])
        st.dataframe(dictionary, hide_index=True)