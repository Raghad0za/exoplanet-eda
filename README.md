# How Close Are We to Finding Another Earth?
### Exploratory Data Analysis & Interactive Dashboard of NASA's Confirmed Exoplanets

**Author:** Raghad Alasmari · Tuwaiq Academy, Unit 3 Final EDA Project

**Live dashboard:** _link coming soon_

**Dataset:** [NASA Exoplanet Archive – Planetary Systems Composite Parameters](https://exoplanetarchive.ipac.caltech.edu)

---

## About the project
This project explores all **6,445 confirmed exoplanets** (planets orbiting stars other than the Sun)
to answer one question: **how close are we to finding another Earth?**

It covers the full data analysis workflow: data loading, cleaning, exploratory data analysis,
insights, and an interactive Streamlit dashboard.

## Key insights
- **The radius valley:** small planets cluster at ~1.3 and ~2.5 Earth radii, with a gap at 1.6–2.0.
- **Detection bias:** Transit found 74% of all planets and mostly finds planets very close to their stars.
- **Data quality matters:** ~47% of masses and ~24% of radii were calculated, not measured.
- **Earth 2.0:** only **18 planets** with a measured size are rocky-sized and receive Earth-like energy.
  The nearest are Gliese 12 b and TRAPPIST-1 d, e and f, about 40 light-years away.

## Dashboard features
- **Filters:** discovery method, discovery year range, planet type, measured values only
- **Overview:** radius valley, discovery methods, planet types, data quality gauges
- **Discoveries:** discoveries per year by method, detection bias by orbital period
- **Earth 2.0 Finder:** define "Earth-like" with sliders and see matching planets
- **Data:** data preview, summary statistics, data dictionary, CSV download

## Project structure
```
exoplanet-eda/
├── .streamlit/config.toml # dashboard theme
├── app/
│ ├── app.py # Streamlit dashboard
│ ├── style.py # helper script: CSS, colors, reusable components
│ └── clean_data.csv # cleaned dataset used by the dashboard
├── data/
│ └── clean_data.csv # cleaned dataset (output of the notebook)
├── notebook/
│ └── exoplanet_eda.ipynb # full analysis: loading, cleaning, EDA, insights
├── report/figures/ # charts exported from the notebook
├── requirements.txt
└── README.md
```

## How to run it locally
1. Clone the repository and open the folder.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # Mac/Linux
   ```
3. Install the libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the dashboard from the main folder:
   ```bash
   streamlit run app/app.py
   ```

## Data source
The raw data was downloaded from the NASA Exoplanet Archive on **25 October 2026**
(Planetary Systems Composite Parameters table, all columns). The raw file (~49 MB) is not included
in this repository. To reproduce the analysis, download the same table as CSV and place it in `data/`.

## Tools
Python · pandas · NumPy · Matplotlib · seaborn · Plotly · Streamlit