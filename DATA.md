# DATA.md — Dataset Reference

This document describes every dataset in the BCR backend: its source, CSV file, database table, API endpoint, frontend consumer, and field-level definitions.

---

## Overview

| # | CSV File | DB Table | Source | API Endpoint | Frontend Component |
|---|----------|----------|--------|--------------|-------------------|
| 01 | `01_countries_update.csv` | `countries` | Sourced + synthesised | `GET /countries` | GlobalSection, WorldMap |
| 02 | `02_country_ndcs_update.csv` | `country_ndcs` | Sourced | (internal to `/ndc-tracker`) | NDCTrackerSection |
| 03 | `03_country_metrics_idn.csv` | `country_metrics` | Synthesised | `GET /countries/{code}/metrics` | IndonesiaSection |
| 04 | `04_country_ndc_targets_idn.csv` | `country_ndc_targets` | Sourced | `GET /countries/{code}/ndc-targets` | IndonesiaSection |
| 05 | `05_country_carbon_markets_update.csv` | `country_carbon_markets` | Sourced | (internal to `/ndc-tracker`) | NDCTrackerSection |
| 06 | `06_country_institutions_idn.csv` | `country_institutions` | Sourced | `GET /countries/{code}/institutions` | IndonesiaSection |
| 07 | `07_country_agreements_idn.csv` | `country_agreements` | Sourced | `GET /countries/{code}/agreements` | StandardsSection |
| 09 | `09_global_frameworks_idn.csv` | `global_frameworks` | Sourced | `GET /frameworks` | GlobalSection |
| 10 | `10_global_news_idn.csv` | `global_news` | Synthesised | `GET /news` | GlobalSection, IndonesiaSection |
| 11 | `11_global_stats_new.csv` | `global_stats` | Synthesised | `GET /summary` | Hero, GlobalSection, ProjectsSection |
| 12 | `12_ticker_items_new.csv` | `ticker_items` | Synthesised | `GET /ticker` | Ticker |
| 13 | `13_projects_idn_bluecarbon.csv` | `projects` | Sourced | `GET /registered-projects` | ProjectsSection |
| 14 | `14_countries_ref.csv` | `countries` (merge) | Reference | (merged into `/countries`) | — |
| 15 | `15_country_metrics_ref.csv` | `country_metrics` (merge) | Synthesised | (merged into `/countries/{code}/metrics`) | — |
| 16 | `16_project_costs_ref.csv` | `project_costs` | Sourced (workbook) | `GET /projects` | ProjectsSection |
| 17 | `17_country_dimensions_idn.csv` | `country_dimensions` | Sourced | `GET /countries/{code}/dimensions` | IndonesiaSection |
| 18 | `18_country_checklists_idn.csv` | `country_checklists` | Sourced | `GET /countries/{code}/checklist` | IndonesiaSection |

**Joined view:** `GET /ndc-tracker` joins `country_ndcs` + `countries` + `country_carbon_markets` server-side.

---

## 01 — Countries (`countries`)

**CSV:** `01_countries_update.csv` (127 rows)
**Generator:** `scripts/generate_127_countries.py`
**Source:** UNFCCC Article 6.4 Designated National Authority list (127 Parties with DNA appointed, as of 9 Apr 2026). Binary flags from primary sources listed below; UNFCCC building-block scores curated for Indonesia only; CAAS scores curated for Indonesia + synthesised for 38 NDC-tracker peers.

**API:** `GET /countries` (list), with optional `?tier=` filter
**Frontend:** GlobalSection (stat strip, top countries), WorldMap (choropleth)

| Field | Type | Description |
|-------|------|-------------|
| `country_code` | string | ISO 3166-1 alpha-3 code (e.g. `IDN`) |
| `country_name` | string | Common English name |
| `flag_emoji` | string | Unicode flag emoji |
| `readiness_score` | int\|null | 0–100, derived as `components_count * 20` |
| `readiness_tier` | string | `High readiness` (5/5), `Developing` (3–4), `Early stage` (0–2) |
| `context_note` | string\|null | Short description of country's Article 6 posture |
| `dim_1_strategic` | int\|null | UNFCCC Building Block I — Strategic Considerations (0–100) |
| `dim_2_legal` | int\|null | UNFCCC Building Block II — Legal & Regulatory |
| `dim_3_institutional` | int\|null | UNFCCC Building Block III — Institutional Arrangements |
| `dim_4_operational` | int\|null | UNFCCC Building Block IV — Operational Systems |
| `dim_5_infrastructure` | int\|null | UNFCCC Building Block V — Market Infrastructure |
| `caas_a_legal` | int\|null | CAAS Investment Readiness — A: Legal framework |
| `caas_b_mrv` | int\|null | CAAS Investment Readiness — B: MRV capacity |
| `caas_c_finance` | int\|null | CAAS Investment Readiness — C: Finance & market access |
| `caas_d_social` | int\|null | CAAS Investment Readiness — D: Social & environmental safeguards |
| `caas_e_registry` | int\|null | CAAS Investment Readiness — E: Registry & tracking |
| `flag_dna_appointed` | bool | DNA appointed for Art.6.4 — Source: UNFCCC |
| `flag_pr_submitted` | bool | Participation Requirements submitted — Source: UNFCCC Art.6.4 Supervisory Body (~47 countries, heuristic) |
| `flag_ndc_blue_carbon` | bool | Blue carbon referenced in NDC — Source: supplementary research note (curated subset) |
| `flag_bilateral_a6_2` | bool | Bilateral Art.6.2 cooperative approach signed — Source: public bilateral roster |
| `flag_market_operational` | bool | Domestic carbon market operational — Source: ICAP / World Bank + supplementary research |
| `components_count` | int | Sum of the five `flag_*` fields (0–5) |

**Supplementary merge:** `14_countries_ref.csv` (249 rows) adds `country_name` for ISO codes not in the 127-country universe (needed so the NDC tracker can display non-DNA countries).

---

## 02 — Country NDCs (`country_ndcs`)

**CSV:** `02_country_ndcs_update.csv` (39 rows)
**Generator:** `scripts/generate_ndc_table.py`
**Source:** Curated 38-country NDC table from *Blue Carbon Dashboard Supplementary Information* document. Each row is one country's NDC submission with blue-carbon scope.

**API:** No direct endpoint. Consumed internally by `GET /ndc-tracker` (joined with `countries` + `country_carbon_markets`).
**Frontend:** NDCTrackerSection (via joined `/ndc-tracker` response)

| Field | Type | Description |
|-------|------|-------------|
| `country_code` | string | ISO alpha-3, FK to `countries` |
| `ndc_version` | string | NDC submission identifier (e.g. `2nd NDC (submitted 24 Oct 2025)`) |
| `blue_carbon_included` | bool | Whether NDC explicitly includes blue carbon |
| `unconditional_ecosystems` | JSON array | Ecosystems under unconditional target (e.g. `["Mangroves","Seagrass"]`) |
| `conditional_ecosystems` | JSON array | Ecosystems under conditional target |
| `unconditional_target_desc` | text | Description of unconditional target |
| `conditional_target_desc` | text | Description of conditional target |
| `intervention_type` | string | e.g. `Conservation + Restoration` |
| `target_type` | string | `Unconditional`, `Conditional`, or `Both` |
| `targets` | string | Quantitative target summary |
| `domestic_pricing` | string | Domestic carbon pricing instrument description |
| `market_status` | string | `Operational`, `Developing`, `Unknown` |

---

## 03 — Country Metrics (`country_metrics`)

**CSV:** `03_country_metrics_idn.csv` (25 rows) + `15_country_metrics_ref.csv` (1326 rows, merge)
**Source:** Synthesised key statistics for the country deep-dive page. IDN-specific file has curated values; ref file provides additional countries.

**API:** `GET /countries/{code}/metrics`
**Frontend:** IndonesiaSection (4 stat cards)

| Field | Type | Description |
|-------|------|-------------|
| `country_code` | string | ISO alpha-3, FK to `countries` |
| `metric_name` | string | Display label (e.g. `Mangrove Area`) |
| `metric_value` | string | Formatted value (e.g. `3.45M ha`) |
| `metric_subtext` | string | Explanatory subtext |

---

## 04 — Country NDC Targets (`country_ndc_targets`)

**CSV:** `04_country_ndc_targets_idn.csv` (4 rows)
**Source:** Sourced from Indonesia's 2nd NDC submission. Mangrove restoration/conservation targets with unconditional vs conditional progress.

**API:** `GET /countries/{code}/ndc-targets`
**Frontend:** IndonesiaSection (NDC target cards with progress bars)

| Field | Type | Description |
|-------|------|-------------|
| `country_code` | string | ISO alpha-3, FK to `countries` |
| `target_type` | string | Target category (e.g. `Mangrove Restoration`) |
| `target_title` | string | Display title |
| `unconditional_val` | string | Unconditional target value (formatted) |
| `unconditional_pct` | int | Unconditional progress percentage (0–100) |
| `conditional_val` | string | Conditional target value (formatted) |
| `conditional_pct` | int | Conditional progress percentage (0–100) |

---

## 05 — Country Carbon Markets (`country_carbon_markets`)

**CSV:** `05_country_carbon_markets_update.csv` (32 rows)
**Source:** Sourced from ICAP, World Bank Carbon Pricing Dashboard, and supplementary research.

**API:** No direct endpoint. Consumed internally by `GET /ndc-tracker` (joined with `country_ndcs` to provide price and market status).
**Frontend:** NDCTrackerSection (price column, market status)

| Field | Type | Description |
|-------|------|-------------|
| `country_code` | string | ISO alpha-3, FK to `countries` |
| `market_status` | string | e.g. `Operational`, `Developing` |
| `price_range_min` | float\|null | Low end of carbon price range (local currency) |
| `price_range_max` | float\|null | High end of carbon price range |
| `currency` | string\|null | Currency code (e.g. `USD`, `IDR`) |

---

## 06 — Country Institutions (`country_institutions`)

**CSV:** `06_country_institutions_idn.csv` (9 rows)
**Source:** Sourced from Indonesian government publications and UNFCCC submissions. Institutional mapping for Article 6 roles.

**API:** `GET /countries/{code}/institutions`
**Frontend:** IndonesiaSection (institutional mapping cards)

| Field | Type | Description |
|-------|------|-------------|
| `country_code` | string | ISO alpha-3, FK to `countries` |
| `role` | string | Institutional role (e.g. `Designated National Authority`, `Focal Point`) |
| `name` | string | Organisation name |
| `description` | text | Role description and responsibilities |

---

## 07 — Country Agreements (`country_agreements`)

**CSV:** `07_country_agreements_idn.csv` (4 rows)
**Source:** Sourced from public bilateral cooperative-approach registries and government announcements. Indonesia-specific.

**API:** `GET /countries/{code}/agreements` with optional `?type=` filter
**Frontend:** StandardsSection (bilateral agreement cards, first 2 displayed)

| Field | Type | Description |
|-------|------|-------------|
| `agreement_id` | string | Unique identifier |
| `host_country_code` | string | ISO alpha-3, FK to `countries` |
| `agreement_type` | string | e.g. `Bilateral Art.6.2`, `MOU` |
| `partner_entity` | string | Partner country or organisation |
| `status` | string | e.g. `Signed`, `In negotiation` |
| `date_signed` | string\|null | Date signed (free-form) |
| `reference_link` | string\|null | URL to source document |

---

## 09 — Global Frameworks (`global_frameworks`)

**CSV:** `09_global_frameworks_idn.csv` (8 rows)
**Source:** Sourced from UNFCCC decisions, national legislation, and carbon market regulatory frameworks.

**API:** `GET /frameworks` with optional `?category=` filter
**Frontend:** GlobalSection (frameworks table, categorised by color)

| Field | Type | Description |
|-------|------|-------------|
| `framework_id` | string | Unique identifier |
| `jurisdiction` | string | Jurisdiction scope (e.g. `UNFCCC`, `Indonesia`) |
| `title` | string | Framework or regulation title |
| `description` | text | Summary of the framework |
| `status_date` | string | Status with date (e.g. `Adopted Dec 2024`) |
| `category` | string | Display category — `blue`, `teal`, `orange`, `green` |

---

## 10 — Global News (`global_news`)

**CSV:** `10_global_news_idn.csv` (6 rows)
**Source:** Synthesised intelligence updates based on real events. Curated for dashboard demonstration.

**API:** `GET /news` with optional `?country=` and `?tag=` filters
**Frontend:** GlobalSection (news feed), IndonesiaSection (WARN alert box)

| Field | Type | Description |
|-------|------|-------------|
| `news_id` | string | Unique identifier |
| `country_code` | string\|null | ISO alpha-3 (null = global news) |
| `title` | string | Headline |
| `body` | text | Full text |
| `date` | string | Date string (e.g. `2025-04-09`) |
| `tags` | JSON array | Tag codes: `ID`, `MKT`, `GLOBAL`, `WARN`, `IDN` |

---

## 11 — Global Stats (`global_stats`)

**CSV:** `11_global_stats_new.csv` (16 rows)
**Source:** Synthesised headline statistics for the hero section and global overview. Values derived from primary data (e.g. UNFCCC country count, Indonesia mangrove area).

**API:** `GET /summary` (returns keyed `Record<stat_key, GlobalStat>`)
**Frontend:** Hero (4 headline stats), GlobalSection (stat strip), ProjectsSection

| Field | Type | Description |
|-------|------|-------------|
| `stat_key` | string | Lookup key (e.g. `hero_countries`, `hero_mangrove_ha`) |
| `stat_value` | string | Display value (e.g. `127`, `3.45M`) |
| `stat_label` | string | Label text |
| `stat_sub` | string\|null | Subtitle / source note |
| `color_hint` | string\|null | CSS color token (e.g. `leaf3`, `tide3`, `white`) |

---

## 12 — Ticker Items (`ticker_items`)

**CSV:** `12_ticker_items_new.csv` (7 rows)
**Source:** Synthesised scrolling news items for the dashboard ticker bar.

**API:** `GET /ticker` (ordered by `order`)
**Frontend:** Ticker (animated scrolling banner)

| Field | Type | Description |
|-------|------|-------------|
| `ticker_id` | string | Unique identifier |
| `text` | string | Ticker text content |
| `order` | int | Display sort order |

---

## 13 — Registered Projects (`projects`)

**CSV:** `13_projects_idn_bluecarbon.csv` (7 rows)
**Source:** Sourced from Verra VCS registry, Plan Vivo, JCM (Japan), and SRN (Indonesia national registry). Real blue carbon projects in Indonesia.

**API:** `GET /registered-projects` with optional `?ecosystem=` and `?status=` filters
**Frontend:** ProjectsSection (project cards grid)

| Field | Type | Description |
|-------|------|-------------|
| `project_id` | string | Unique identifier |
| `project_name` | string | Project title |
| `location` | string | Geographic location |
| `status` | string | e.g. `Registered`, `Under validation` |
| `tags` | JSON array | Tag labels (e.g. `["Verra","Mangrove"]`) |
| `area` | string\|null | Project area in hectares (display string) |
| `methodology` | string\|null | Applied methodology ID |
| `ecosystem_type` | string | `Mangrove`, `Seagrass`, `Salt marsh` |
| `vintage` | string\|null | Credit vintage year |
| `credits` | string\|null | Credits issued (display string) |
| `registry` | string\|null | Registry name (e.g. `Verra VCS`) |
| `description` | text\|null | Project description |
| `checks` | JSON array | Validation check labels |
| `price` | string\|null | Market price (display string) |
| `rating_agency` | string\|null | Rating provider name |
| `rating_score` | string\|null | Rating score |
| `status_category` | string\|null | Color category: `operational`, `developing`, `unknown` |

---

## 16 — Project Costs (`project_costs`)

**CSV:** `16_project_costs_ref.csv` (444 rows)
**Extractor:** `extract_project_costs.py` reads from `data/ref/Carbon-Cost Data Upload.xlsm` (Projects sheet)
**Source:** Sourced from the Carbon-Cost workbook — a financial model producing CAPEX/OPEX estimates for blue carbon project variations by country, ecosystem, activity, and size.

**API:** `GET /projects` with optional `?ecosystem=`, `?activity=`, `?activity_type=`, `?size=`, `?country_code=` filters
**Frontend:** ProjectsSection (cost-model table, expandable breakdowns, stats strip)

**Key fields:**

| Field | Type | Description |
|-------|------|-------------|
| `country` | string | Country name |
| `country_code` | string | ISO alpha-3 |
| `ecosystem` | string | `Mangrove`, `Salt marsh`, `Seagrass` |
| `activity` | string | `Conservation` or `Restoration` |
| `activity_type` | string | e.g. `Planting`, `Hydrology`, `Hybrid`, `Avoided loss` |
| `project_size_filter` | string | `Small`, `Medium`, `Large` |
| `project_size_ha` | float\|null | Project area in hectares |
| `price_type` | string | Price scenario applied |
| `country_size_ha` | float\|null | Total country ecosystem area |
| `base_size` | float\|null | Base size used in model |
| `project_name` | string | Descriptive project name |

**Aggregate cost fields** (each has nominal and `_npv` variant):

| Field | Description |
|-------|-------------|
| `capex` / `capex_npv` | Total capital expenditure |
| `opex` / `opex_npv` | Total operating expenditure |
| `total_cost` / `total_cost_npv` | CAPEX + OPEX |
| `total_weighted_cost` / `total_weighted_cost_npv` | Weighted total cost |
| `cost_per_tco2e` / `cost_per_tco2e_npv` | Unit abatement cost ($/tCO2e) |
| `country_abatement_potential` | Country-level abatement potential (tCO2e) |
| `project_abatement_potential` | Project-level abatement potential (tCO2e) |

**14 cost-component line items** (each has nominal and `_npv` variant):

| Field | Description |
|-------|-------------|
| `feasibility_analysis` | Feasibility study costs |
| `conservation_planning` | Conservation planning |
| `data_collection` | Baseline data collection |
| `community_representation` | Community engagement & FPIC |
| `blue_carbon_project_planning` | Blue carbon project design |
| `establishing_carbon_rights` | Carbon rights establishment |
| `validation` | Third-party validation |
| `implementation_labor` | Implementation labour |
| `monitoring_maintenance` | Monitoring & maintenance (combined) |
| `community_benefit` | Community benefit sharing |
| `carbon_standard_fees` | Carbon standard listing/issuance fees |
| `baseline_reassessment` | Baseline reassessment |
| `mrv` | Measurement, reporting & verification |
| `long_term_project_operating` | Long-term operating costs |

**Revenue fields:**

| Field | Type | Description |
|-------|------|-------------|
| `initial_price_assumption` | float\|null | Carbon price assumption ($/tCO2e) |
| `credits_issued` | float\|null | Total credits issued over project lifetime |
| `total_revenue` / `total_revenue_npv` | float\|null | Projected revenue |
| `leftover_after_opex` / `leftover_after_opex_npv` | float\|null | Revenue minus OPEX |
| `monitoring` / `monitoring_npv` | float\|null | Monitoring cost (split) |
| `maintenance` / `maintenance_npv` | float\|null | Maintenance cost (split) |

---

## 17 — Country Dimensions (`country_dimensions`)

**CSV:** `17_country_dimensions_idn.csv` (5 rows)
**Source:** Sourced from UNFCCC/NDC Partnership Article 6 Readiness Toolkit. Five building blocks assessed for Indonesia.

**API:** `GET /countries/{code}/dimensions`
**Frontend:** IndonesiaSection (radar chart, dimension tabs with progress bars)

| Field | Type | Description |
|-------|------|-------------|
| `country_code` | string | ISO alpha-3, FK to `countries` |
| `dimension_id` | string | `i`, `ii`, `iii`, `iv`, `v` |
| `label` | string | Short label (e.g. `I -- Strategic`) |
| `full_label` | string | Full label (e.g. `I -- Strategic Considerations`) |
| `gate` | string | Gate status: `cleared`, `progress`, `pending` |
| `gate_text` | string | Display text (e.g. `Gate cleared`) |
| `description` | text | Detailed description of the dimension |

---

## 18 — Country Checklists (`country_checklists`)

**CSV:** `18_country_checklists_idn.csv` (26 rows)
**Source:** Sourced from UNFCCC Article 6 Readiness Toolkit checklist items, assessed for Indonesia per dimension.

**API:** `GET /countries/{code}/checklist` with optional `?dimension=` filter
**Frontend:** IndonesiaSection (checklist items within dimension tabs)

| Field | Type | Description |
|-------|------|-------------|
| `country_code` | string | ISO alpha-3, FK to `countries` |
| `dimension_id` | string | Links to `country_dimensions.dimension_id` |
| `item_label` | string | Checklist item description |
| `status` | string | `yes`, `partial`, `no` |

---

## Methodology & Ecosystem Tiers

These two tables are seeded directly in `seed.py` (hardcoded), not from CSV files.

### Methodologies (`methodologies`)

**API:** `GET /methodologies` with optional `?recognition=` filter
**Frontend:** StandardsSection (methodology table)

| Field | Type | Description |
|-------|------|-------------|
| `methodology_id` | string | Standard methodology ID (e.g. `VM0007`) |
| `standard` | string | Issuing standard (e.g. `Verra VCS`, `Gold Standard`, `Plan Vivo`) |
| `description` | text | Methodology description |
| `ecosystem_focus` | string | Target ecosystem(s) |
| `activity_type` | string | Activity scope |
| `recognition` | string | `International` or `Domestic` |
| `is_current` | bool | `true` if active, `false` if deprecated |

### Ecosystem Tiers (`ecosystem_tiers`)

**API:** `GET /ecosystem-tiers`
**Frontend:** StandardsSection (3-column tier cards)

| Field | Type | Description |
|-------|------|-------------|
| `tier_name` | string | `Ready`, `Developing`, `Frontier` |
| `ecosystems` | string | Ecosystems in this tier |
| `ghg_impact` | string | GHG impact assessment |
| `long_term_storage` | string | Long-term carbon storage capacity |
| `ipcc_accounting` | string | IPCC accounting readiness |
| `vcm_readiness` | string | Voluntary carbon market readiness |

---

## NDC Tracker (Joined View)

**API:** `GET /ndc-tracker` with optional `?market=`, `?target=`, `?ecosystem=` filters
**Frontend:** NDCTrackerSection

This endpoint is not backed by a single table. It joins three tables server-side:

1. `country_ndcs` — NDC version, ecosystems, target type, market status
2. `countries` — country name, flag emoji, country code
3. `country_carbon_markets` — price range, currency

**Response fields:**

| Field | Source Table | Description |
|-------|-------------|-------------|
| `country_code` | `countries` | ISO alpha-3 |
| `country` | `countries` | Country name |
| `flag` | `countries` | Flag emoji |
| `ndc` | `country_ndcs` | NDC version string |
| `eco` | `country_ndcs` | Deduplicated ecosystem list |
| `target` | `country_ndcs` | Target type |
| `market` | `country_ndcs` | Domestic pricing instrument |
| `mkt_status` | `country_ndcs` | Market status |
| `price_min` | `country_carbon_markets` | Price range low |
| `price_max` | `country_carbon_markets` | Price range high |
| `currency` | `country_carbon_markets` | Currency code |

---

## Reference Files

| File | Purpose |
|------|---------|
| `data/ref/Carbon-Cost Data Upload.xlsm` | Source workbook for project cost model; extracted by `extract_project_costs.py` into `16_project_costs_ref.csv` |
| `data/ref/Carbon-Cost Data Upload_v1_UNMODIFIED.xlsm` | Original unmodified workbook (archive) |
| `data/ref/country_centroids.csv` | Country centroid coordinates (reference, not loaded) |
| `data/ref/data_ingestion_project_scorecard.xlsm` | Project scorecard workbook (reference, not loaded) |

---

## Data Flow

```
CSV files (data/*.csv)
    |
    v
load_data.py (upsert into SQLite)
    |
    v
SQLite DB (instance/bcr.db)
    |
    v
Flask API (app/routes/*.py)
    |
    v
Frontend (Bcrdashboard/src/api.ts -> components)
```

**Seeding:** `python seed.py` drops all tables, recreates schema, runs `extract_project_costs.py`, then calls `load_data.load_all()`.

**Regenerating source CSVs:**
- `python scripts/generate_127_countries.py` -> `01_countries_update.csv`
- `python scripts/generate_ndc_table.py` -> `02_country_ndcs_update.csv`
- `python extract_project_costs.py` -> `16_project_costs_ref.csv`

---

## Synthetic Dataset Generation Scripts

Both scripts live in `scripts/` and produce CSVs into `data/`. They are self-contained (no external API calls) — all source data is hard-coded in-file from curated documents.

### `scripts/generate_127_countries.py` → `01_countries_update.csv`

**What it does:** Builds the 127-row countries table from hard-coded primary-source data.

**Logic:**

1. **Country universe** — A literal list of 127 country names (UNFCCC Article 6.4 DNA-appointed Parties, Apr 2026).

2. **ISO-3 lookup** — Maps each name to an ISO alpha-3 code using `14_countries_ref.csv` as a lookup table, with manual overrides for non-standard names (e.g. `'Bahamas (The)' → 'BHS'`).

3. **Five binary flags** — Each country is scored against five hard-coded sets of ISO codes:
   - `flag_dna_appointed` — always `true` (all 127 are DNA-appointed)
   - `flag_pr_submitted` — all African DNA parties + Indonesia (47 total, heuristic)
   - `flag_ndc_blue_carbon` — ~39 countries with blue carbon in their NDC (curated set)
   - `flag_bilateral_a6_2` — ~35 countries with Art.6.2 bilateral agreements (curated set)
   - `flag_market_operational` — ~31 countries with an operational domestic carbon market (curated set)

4. **Derived fields:**
   - `components_count` = sum of the five flags (0–5)
   - `readiness_score` = `components_count * 20` (0–100)
   - `readiness_tier` = `High readiness` (5), `Developing` (3–4), `Early stage` (0–2)
   - `context_note` = human-readable summary built from the active flags

5. **Dimension scores** — Two score sets, written only for select countries:
   - **UNFCCC building blocks** (5 dimensions, 0–100) — curated for Indonesia only
   - **CAAS investment readiness** (5 dimensions, 0–100) — curated for Indonesia, synthesised for 38 NDC-tracker peer countries via a hard-coded `CAAS_SYNTH` dict; all other countries left blank

6. **Flag emoji** — Computed from ISO-3 → ISO-2 mapping using Unicode regional indicator math.

7. **Output** — Writes all rows as a CSV with `csv.DictWriter`.

### `scripts/generate_ndc_table.py` → `02_country_ndcs_update.csv`

**What it does:** Builds the 38-row NDC tracker table from a hard-coded list of tuples.

**Logic:**

1. **Source data** — A single `NDC` list of 38 tuples, each containing:
   `(country_code, ndc_version, ecosystems[], unconditional_desc, conditional_desc, intervention_type, target_type, targets, domestic_pricing, market_status)`

2. **Row construction** — For each tuple:
   - `blue_carbon_included` is always `True` (every entry in this table has blue carbon in its NDC)
   - `unconditional_ecosystems` and `conditional_ecosystems` are both set to the same ecosystem list, JSON-serialised
   - All other fields map directly from the tuple

3. **Output** — Writes rows with `csv.DictWriter` into the CSV.

### `extract_project_costs.py` → `16_project_costs_ref.csv`

Extracts cost-model data from `data/ref/Carbon-Cost Data Upload.xlsm` (Excel workbook). Unlike the two scripts above, this reads from an external file rather than hard-coded data. See **§16 — Project Costs** for field details.
