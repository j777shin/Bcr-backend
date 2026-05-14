# BCR Backend

Flask REST API for the Blue Carbon Readiness (BCR) Dashboard. Serves country-level Article 6 readiness data, blue carbon project economics, NDC tracker, and market intelligence.

## Stack

- **Python 3.13** / Flask 3.0 / Flask-SQLAlchemy / Flask-CORS
- **Database**: SQLite (`instance/bcr.db`)
- **Data source**: CSV files in `data/`

## Project Structure

```
Bcr-backend/
├── app/
│   ├── __init__.py          # App factory, db init, blueprint registration
│   ├── models/
│   │   ├── global_layer.py  # Country, NDC, Carbon Market, Framework, News, Stats
│   │   ├── country_layer.py # Metrics, Dimensions, Checklists, Institutions, Agreements
│   │   └── project_layer.py # Project, ProjectCost, Methodology, EcosystemTier
│   └── routes/
│       ├── global_routes.py  # /api/countries, /api/frameworks, /api/news, etc.
│       ├── country_routes.py # /api/countries/<code>/metrics, /dimensions, etc.
│       └── project_routes.py # /api/projects, /api/methodologies, /api/ecosystem-tiers
├── data/                    # CSV data files (loaded on every start)
├── seed.py                  # Schema init + data loading orchestrator
├── load_data.py             # CSV upsert logic with type converters
├── extract_project_costs.py # Extracts CAPEX/OPEX cost model from Excel
├── run.py                   # Flask entry point (default port 5050)
├── start.sh                 # One-command start script
└── requirements.txt         # Python dependencies
```

## Quick Start

```bash
./start.sh
```

This script will:
1. Create and activate a Python virtual environment
2. Install dependencies from `requirements.txt`
3. Drop and recreate the database schema
4. Load all CSV files from `data/`
5. Start the Flask dev server on `http://localhost:5050`

The port is configurable via the `PORT` environment variable.

### Manual Commands

```bash
python seed.py          # Initialize database + load data
python load_data.py     # Load CSV data only
python run.py           # Run Flask server only
```

## API Documentation

All routes are prefixed with `/api`. Responses are JSON.

### Global

| Method | Endpoint | Description | Query Params |
|--------|----------|-------------|--------------|
| GET | `/summary` | Global stats keyed by `stat_key` | |
| GET | `/ticker` | Scrolling ticker items | |
| GET | `/countries` | All countries sorted by readiness score | `?tier=` |
| GET | `/ndc-tracker` | Joined NDC + country + carbon market view | `?market=` `?target=` `?ecosystem=` |
| GET | `/frameworks` | Regulatory frameworks | `?category=` |
| GET | `/news` | Market news | `?country=` `?tag=` |

### Country Deep-Dive

| Method | Endpoint | Description | Query Params |
|--------|----------|-------------|--------------|
| GET | `/countries/<code>/metrics` | Top-line stat cards | |
| GET | `/countries/<code>/dimensions` | Article 6 readiness dimensions | |
| GET | `/countries/<code>/checklist` | Checklist items per dimension | `?dimension=` |
| GET | `/countries/<code>/ndc-targets` | Quantified NDC targets | |
| GET | `/countries/<code>/institutions` | Regulatory bodies & frameworks | |
| GET | `/countries/<code>/agreements` | Bilateral Article 6 agreements | `?type=` |

### Projects

| Method | Endpoint | Description | Query Params |
|--------|----------|-------------|--------------|
| GET | `/registered-projects` | Blue carbon project pipeline | `?status=` `?ecosystem=` |
| GET | `/projects` | Project CAPEX/OPEX cost model | `?ecosystem=` `?activity=` `?activity_type=` `?size=` `?country_code=` |
| GET | `/methodologies` | Carbon methodology registry | `?recognition=` |
| GET | `/ecosystem-tiers` | IPCC/VCM ecosystem classification | |

## Data Files

CSV files in `data/` are loaded on every `./start.sh` run. Key mappings:

| File | Target Table |
|------|-------------|
| `01_countries_update.csv` | `countries` |
| `02_country_ndcs_update.csv` | `country_ndcs` |
| `03_country_metrics_idn.csv` | `country_metrics` |
| `04_country_ndc_targets_idn.csv` | `country_ndc_targets` |
| `05_country_carbon_markets_update.csv` | `country_carbon_markets` |
| `06_country_institutions_idn.csv` | `country_institutions` |
| `07_country_agreements_idn.csv` | `country_agreements` |
| `09_global_frameworks_idn.csv` | `global_frameworks` |
| `10_global_news_idn.csv` | `global_news` |
| `11_global_stats_new.csv` | `global_stats` |
| `12_ticker_items_new.csv` | `ticker_items` |
| `13_projects_idn_bluecarbon.csv` | `projects` |
| `14_countries_ref.csv` | `countries` (merge) |
| `15_country_metrics_ref.csv` | `country_metrics` (merge) |
| `16_project_costs_ref.csv` | `project_costs` |
| `17_country_dimensions_idn.csv` | `country_dimensions` |
| `18_country_checklists_idn.csv` | `country_checklists` |

To add new data, create a CSV in `data/` and add a loader function in `load_data.py`.

## Deployment

This app runs natively with Python. No Docker configuration is included.

```bash
# Production-like setup
pip install -r requirements.txt
python seed.py
PORT=5050 python run.py
```

For production, consider placing Flask behind a WSGI server (e.g. Gunicorn) and a reverse proxy (e.g. Nginx).
