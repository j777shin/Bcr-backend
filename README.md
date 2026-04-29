# BCR Backend

Flask REST API for the Blue Carbon Readiness (BCR) Dashboard. Serves country-level Article 6 readiness data, blue carbon project pipeline, NDC tracker, and market intelligence.

## Stack

- **Python 3.13** · Flask 3.0 · Flask-SQLAlchemy · Flask-CORS
- **Database**: SQLite (`instance/bcr.db`)
- **Data source**: CSV files in `data/`

## Setup & Running

```bash
./start.sh
```

This script:
1. Creates/activates the virtual environment
2. Drops and recreates the database schema
3. Loads all CSV files from `data/`
4. Kills any existing process on port 5000
5. Starts the Flask dev server on `http://localhost:5000`

## Project Structure

```
Bcr-backend/
├── app/
│   ├── __init__.py          # App factory, db init, blueprint registration
│   ├── models/
│   │   ├── global_layer.py  # Country, NDC, Carbon Market, Framework, News, Ticker, Stats
│   │   ├── country_layer.py # Metrics, Dimensions, Checklists, Institutions, Agreements
│   │   └── project_layer.py # Project, Methodology, EcosystemTier
│   └── routes/
│       ├── global_routes.py  # /api/countries, /api/frameworks, /api/news, etc.
│       ├── country_routes.py # /api/countries/<code>/metrics, /dimensions, etc.
│       └── project_routes.py # /api/projects, /api/methodologies, /api/ecosystem-tiers
├── data/                    # CSV data files (loaded on every start)
├── seed.py                  # Schema init → calls load_data.py
├── load_data.py             # Upserts all CSVs into the database
├── run.py                   # Flask entry point (port 5000)
└── start.sh                 # One-command start script
```

---

## Database Schema

### Global Layer (`app/models/global_layer.py`)

#### `countries`
Article 6 readiness scores and world map coordinates for each country.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer PK | |
| `country_code` | String(3) unique | ISO 3-letter code (e.g. `IDN`) |
| `country_name` | String(100) | |
| `flag_emoji` | String(10) | |
| `readiness_score` | Integer | Overall 0–100 readiness score |
| `readiness_tier` | String(50) | `High readiness` / `Developing` / `Early stage` |
| `context_note` | String(200) | Short Art.6 status note |
| `dim_1_strategic` | Integer | I — Strategic Considerations (0–100) |
| `dim_2_legal` | Integer | II — Legal Foundations & Governance (0–100) |
| `dim_3_institutional` | Integer | III — Institutional Arrangements (0–100) |
| `dim_4_operational` | Integer | IV — Operational Procedures (0–100) |
| `dim_5_infrastructure` | Integer | V — Infrastructure (0–100) |
| `map_cx` | Float | SVG x-coordinate (viewBox 0 0 1200 560) |
| `map_cy` | Float | SVG y-coordinate |

#### `country_ndcs`
NDC versions and blue carbon commitments per country.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer PK | |
| `country_code` | String(3) FK → countries | |
| `ndc_version` | String(50) | e.g. `2nd NDC (2025)` |
| `blue_carbon_included` | Boolean | |
| `unconditional_ecosystems` | JSON | List of ecosystem names |
| `conditional_ecosystems` | JSON | List of ecosystem names |
| `unconditional_target_desc` | Text | |
| `conditional_target_desc` | Text | |
| `intervention_type` | String(50) | e.g. `Conservation + Restoration` |
| `target_type` | String(50) | `Both` / `Unconditional` / `Conditional` |
| `targets` | String(200) | Summary of GHG targets |
| `domestic_pricing` | String(100) | e.g. `ETS & Carbon Tax` |
| `market_status` | String(50) | e.g. `Operational` / `Planned` |

#### `country_carbon_markets`
Domestic carbon market status and price ranges.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer PK | |
| `country_code` | String(3) FK → countries | |
| `market_status` | String(100) | |
| `price_range_min` | Float | USD |
| `price_range_max` | Float | USD |
| `currency` | String(10) | |

#### `global_frameworks`
National and international carbon market regulatory frameworks.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer PK | |
| `framework_id` | String(50) unique | e.g. `FW-IDN-PR110` |
| `jurisdiction` | String(200) | |
| `title` | String(200) | |
| `description` | Text | |
| `status_date` | String(100) | |
| `category` | String(50) | Color hint: `blue` / `teal` / `orange` |

#### `global_news`
Market intelligence and news items.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer PK | |
| `news_id` | String(50) unique | e.g. `NEWS-IDN-SNDC2025` |
| `country_code` | String(3) nullable | Null = global news |
| `title` | String(200) | |
| `body` | Text | |
| `date` | String(50) | Display date string |
| `tags` | JSON | List of tag strings e.g. `["NDC","IDN"]` |

#### `global_trade_trends`
Blue carbon VCM volume and price data by year and ecosystem.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer PK | |
| `trend_id` | String(50) unique | e.g. `TT-2024-MNG` |
| `year` | Integer | |
| `ecosystem_category` | String(100) | e.g. `Mangrove Restoration` |
| `volume_traded_mt` | Float | Million tonnes CO₂ |
| `average_price_usd` | Float | USD per tonne |
| `data_source` | String(200) | |

#### `ticker_items`
Scrolling news ticker content.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer PK | |
| `ticker_id` | String(50) unique | |
| `text` | String(500) | |
| `order` | Integer | Display order (ascending) |

#### `global_stats`
Key metric values displayed in stat strips across the dashboard.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer PK | |
| `stat_key` | String(100) unique | e.g. `hero_mangrove_ha` |
| `stat_value` | String(50) | Display value e.g. `3.45M` |
| `stat_label` | String(200) | |
| `stat_sub` | String(200) | Sub-label |
| `color_hint` | String(50) | e.g. `leaf3` / `tide3` / `white` |

---

### Country Layer (`app/models/country_layer.py`)

#### `country_metrics`
Top-line stat cards on a country deep-dive page.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer PK | |
| `country_code` | String(3) FK → countries | |
| `metric_name` | String(100) | e.g. `Mangrove extent` |
| `metric_value` | String(100) | e.g. `3.45M ha` |
| `metric_subtext` | String(200) | |

#### `country_dimensions`
Article 6 Readiness Toolkit building block assessments per country.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer PK | |
| `country_code` | String(3) FK → countries | |
| `dimension_id` | String(5) | `i` / `ii` / `iii` / `iv` / `v` |
| `label` | String(50) | e.g. `I — Strategic` |
| `full_label` | String(100) | e.g. `I — Strategic Considerations` |
| `gate` | String(20) | `cleared` / `progress` / `pending` |
| `gate_text` | String(50) | e.g. `✓ Gate cleared` |
| `description` | Text | Full narrative assessment |

#### `country_checklists`
Granular checklist items within each readiness dimension.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer PK | |
| `country_code` | String(3) FK → countries | |
| `dimension_id` | String(5) | `i` – `v` |
| `item_label` | String(200) | |
| `status` | String(10) | `yes` / `partial` / `no` |

#### `country_ndc_targets`
Quantified NDC targets for specific ecosystem types.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer PK | |
| `country_code` | String(3) FK → countries | |
| `target_type` | String(100) | e.g. `Deforestation prevention` |
| `target_title` | String(200) | |
| `unconditional_val` | String(100) | Area/volume value |
| `unconditional_pct` | Integer | Percentage of target |
| `conditional_val` | String(100) | |
| `conditional_pct` | Integer | |

#### `country_institutions`
Key regulatory bodies, frameworks, and pricing mechanisms per country.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer PK | |
| `country_code` | String(3) FK → countries | |
| `role` | String(100) | e.g. `Governing framework` |
| `name` | String(200) | Institution or regulation name |
| `description` | Text | |

#### `ecosystem_recognitions`
Legal and MRV recognition status of blue carbon ecosystem types per country.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer PK | |
| `country_code` | String(3) FK → countries | |
| `ecosystem_type` | String(50) | e.g. `Mangroves` / `Seagrass` |
| `recognition_status` | String(50) | e.g. `Established` / `Emerging` |
| `details` | Text | |

#### `country_agreements`
Article 6 bilateral agreements and special arrangements.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer PK | |
| `agreement_id` | String(50) unique | e.g. `AGR-IDN-JPN-001` |
| `host_country_code` | String(3) FK → countries | |
| `agreement_type` | String(100) | e.g. `Article 6.2 Cooperative Approach` |
| `partner_entity` | String(200) | |
| `status` | String(50) | e.g. `Active` / `MoU Signed` |
| `date_signed` | String(50) | |
| `reference_link` | String(500) | |

---

### Project Layer (`app/models/project_layer.py`)

#### `projects`
Blue carbon project pipeline entries.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer PK | |
| `project_id` | String(50) unique | e.g. `PRJ-KEN-MIKOKO` |
| `project_name` | String(200) | |
| `location` | String(200) | |
| `status` | String(20) | `Active` / `Pipeline` |
| `tags` | JSON | e.g. `["Active","VCS","Art.6"]` |
| `area` | String(100) | Hectares (display string) |
| `methodology` | String(200) | |
| `ecosystem_type` | String(50) | `Mangroves` / `Seagrass` / `Tidal Marshes` / `Energy` |
| `vintage` | String(50) | Credit vintage year or `—` |
| `credits` | String(50) | Credits issued (display string) |
| `registry` | String(200) | e.g. `Verra VCS` |
| `description` | Text | |
| `checks` | JSON | List of verification/status strings |
| `price` | String(100) | Display price string |
| `rating_agency` | String(100) | |
| `rating_score` | String(10) | |
| `status_category` | String(20) | `Active` / `Pipeline` / `listed` |

#### `methodologies`
Carbon methodology registry (VCS, Gold Standard, CDM, etc.).

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer PK | |
| `methodology_id` | String(50) unique | e.g. `VM0053` |
| `standard` | String(100) | e.g. `Verra (VCS)` |
| `description` | Text | |
| `ecosystem_focus` | String(200) | |
| `activity_type` | String(100) | e.g. `Restoration & conservation` |
| `recognition` | String(50) | `International` / `Primarily domestic` |
| `is_current` | Boolean | False = legacy/deprecated |

#### `ecosystem_tiers`
IPCC/VCM ecosystem classification tiers.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer PK | |
| `tier_name` | String(50) unique | e.g. `Tier 1 — Established` |
| `ecosystems` | String(200) | Ecosystem types in this tier |
| `ghg_impact` | String(100) | |
| `long_term_storage` | String(100) | |
| `ipcc_accounting` | String(50) | |
| `vcm_readiness` | String(100) | |

---

## API Endpoints

All routes are prefixed with `/api`.

### Global

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/summary` | All `global_stats` keyed by `stat_key` |
| GET | `/ticker` | Ticker items ordered by `order` |
| GET | `/countries` | All countries, sorted by readiness score desc. Query: `?tier=` |
| GET | `/countries/<code>` | Single country |
| GET | `/countries/<code>/ndc` | NDC record for country |
| GET | `/countries/<code>/carbon-markets` | Carbon market records |
| GET | `/ndc-tracker` | Joined NDC + country view. Query: `?market=operational&target=&ecosystem=` |
| GET | `/frameworks` | All frameworks. Query: `?category=` |
| GET | `/frameworks/<id>` | Single framework |
| GET | `/news` | All news. Query: `?country=&tag=` |
| GET | `/news/<id>` | Single news item |
| GET | `/trade-trends` | Trade trend data. Query: `?year=&ecosystem=` |

### Country Deep-Dive

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/countries/<code>/metrics` | Stat cards |
| GET | `/countries/<code>/dimensions` | Art.6 readiness dimensions |
| GET | `/countries/<code>/checklist` | Checklist items. Query: `?dimension=i` |
| GET | `/countries/<code>/ndc-targets` | Quantified NDC targets |
| GET | `/countries/<code>/institutions` | Institutions and regulations |
| GET | `/countries/<code>/ecosystem-recognition` | Ecosystem recognition status |
| GET | `/countries/<code>/agreements` | Bilateral agreements. Query: `?type=` |

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/projects` | All projects. Query: `?status=&ecosystem=&location=` |
| GET | `/projects/<id>` | Single project |
| GET | `/methodologies` | All methodologies. Query: `?recognition=` |
| GET | `/methodologies/<id>` | Single methodology |
| GET | `/ecosystem-tiers` | All ecosystem tiers |
| GET | `/ecosystem-tiers/<name>` | Single tier |

---

## Data Files (`data/`)

CSV files are loaded (upserted) on every `./start.sh` run via `load_data.py`.

| File | Table | Key |
|------|-------|-----|
| `01_countries_update.csv` | `countries` | `country_code` |
| `02_country_ndcs_update.csv` | `country_ndcs` | `country_code` (replace) |
| `03_country_metrics_idn.csv` | `country_metrics` | `country_code + metric_name` |
| `04_country_ndc_targets_idn.csv` | `country_ndc_targets` | `country_code + target_type` |
| `05_country_carbon_markets_update.csv` | `country_carbon_markets` | `country_code` |
| `06_country_institutions_idn.csv` | `country_institutions` | `country_code + name` |
| `07_country_agreements_idn.csv` | `country_agreements` | `agreement_id` |
| `08_ecosystem_recognitions_idn.csv` | `ecosystem_recognitions` | `country_code + ecosystem_type` |
| `09_global_frameworks_idn.csv` | `global_frameworks` | `framework_id` |
| `10_global_news_idn.csv` | `global_news` | `news_id` |
| `11_global_stats_new.csv` | `global_stats` | `stat_key` |
| `12_ticker_items_new.csv` | `ticker_items` | `ticker_id` |
| `13_projects_idn_energy.csv` | `projects` | `project_id` |

To add new data: create a new CSV and add a loader in `load_data.py`.
