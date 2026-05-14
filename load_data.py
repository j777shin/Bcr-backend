"""
Upsert all CSV files from data/ into the database.
Files are processed in filename order. Run after seed.py.
Usage: python load_data.py
"""
import csv
import json
import os

from app import create_app, db
from app.models.global_layer import (
    Country, CountryNDC, CountryCarbonMarket,
    GlobalFramework, GlobalNews, TickerItem, GlobalStat,
)
from app.models.country_layer import (
    CountryMetric, CountryNDCTarget, CountryInstitution,
    CountryAgreement,
    CountryDimension, CountryChecklist,
)
from app.models.project_layer import Project, ProjectCost

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def _float(v):
    if not v or v.strip() in ('', 'None'):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def _int(v):
    if not v or v.strip() in ('', 'None'):
        return None
    try:
        return int(float(v))
    except ValueError:
        return None


def _bool(v):
    if not v:
        return None
    return v.strip().lower() in ('true', '1', 'yes')


def _list(v):
    """Parse JSON array string or fall back to comma-split."""
    if not v or not v.strip():
        return []
    try:
        result = json.loads(v)
        return result if isinstance(result, list) else [result]
    except (json.JSONDecodeError, ValueError):
        return [x.strip() for x in v.split(',') if x.strip()]


def _str(v):
    """Return stripped string or None for empty/missing values."""
    if v is None:
        return None
    s = v.strip()
    return s if s else None


def _csv(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        print(f'  ! {filename} not found, skipping.')
        return []
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


# ── Loaders ───────────────────────────────────────────────────────────────────

def load_countries():
    rows = _csv('01_countries_update.csv')
    for row in rows:
        rec = Country.query.filter_by(country_code=row['country_code']).first()
        if not rec:
            rec = Country(country_code=row['country_code'])
            db.session.add(rec)
        if _str(row.get('country_name')):
            rec.country_name = row['country_name']
        if _str(row.get('flag_emoji')):
            rec.flag_emoji = row['flag_emoji']
        if _str(row.get('readiness_tier')):
            rec.readiness_tier = row['readiness_tier']
        if 'context_note' in row:
            rec.context_note = _str(row['context_note'])
        for field in ('readiness_score', 'dim_1_strategic', 'dim_2_legal',
                      'dim_3_institutional', 'dim_4_operational', 'dim_5_infrastructure',
                      'caas_a_legal', 'caas_b_mrv', 'caas_c_finance',
                      'caas_d_social', 'caas_e_registry'):
            v = _int(row.get(field))
            if v is not None:
                setattr(rec, field, v)
        for flag in ('flag_dna_appointed', 'flag_pr_submitted',
                     'flag_ndc_blue_carbon', 'flag_bilateral_a6_2',
                     'flag_market_operational'):
            if flag in row:
                rec_val = _bool(row.get(flag))
                if rec_val is not None:
                    setattr(rec, flag, rec_val)
        cc = _int(row.get('components_count'))
        if cc is not None:
            rec.components_count = cc
    return len(rows)


_ISO3_TO_ISO2 = {
    'IDN':'ID','BRA':'BR','KEN':'KE','VNM':'VN','AUS':'AU','USA':'US','CHN':'CN',
    'SYC':'SC','GBR':'GB','CRI':'CR','KOR':'KR','FJI':'FJ','BHS':'BS','MEX':'MX',
    'COL':'CO','PAN':'PA','PHL':'PH','CHL':'CL','BGD':'BD','VUT':'VU','BLZ':'BZ',
    'ZAF':'ZA','THA':'TH','CPV':'CV','DOM':'DO','GAB':'GA','NAM':'NA','JOR':'JO',
    'MHL':'MH','PLW':'PW','SGP':'SG','JPN':'JP','EUU':'EU','ISL':'IS','FRA':'FR',
    'NOR':'NO','CAN':'CA','TON':'TO','MDV':'MV',
}


def _flag_emoji(iso3: str) -> str | None:
    iso2 = _ISO3_TO_ISO2.get((iso3 or '').upper())
    if not iso2 or len(iso2) != 2:
        return None
    return ''.join(chr(ord(c) - ord('A') + 0x1F1E6) for c in iso2.upper())


def load_country_ndcs():
    rows = _csv('02_country_ndcs_update.csv')
    for row in rows:
        code = row['country_code']
        CountryNDC.query.filter_by(country_code=code).delete()
        db.session.add(CountryNDC(
            country_code=code,
            ndc_version=_str(row.get('ndc_version')),
            blue_carbon_included=_bool(row.get('blue_carbon_included')),
            unconditional_ecosystems=_list(row.get('unconditional_ecosystems', '')),
            conditional_ecosystems=_list(row.get('conditional_ecosystems', '')),
            unconditional_target_desc=_str(row.get('unconditional_target_desc')),
            conditional_target_desc=_str(row.get('conditional_target_desc')),
            intervention_type=_str(row.get('intervention_type')),
            target_type=_str(row.get('target_type')),
            targets=_str(row.get('targets')),
            domestic_pricing=_str(row.get('domestic_pricing')),
            market_status=_str(row.get('market_status')),
        ))
        # Ensure the joined Country row has a flag_emoji so the NDC tracker
        # renders correctly for non-DNA-appointed countries (USA, AUS, JPN, …)
        # whose row is currently created from 14_countries_ref only.
        country = Country.query.filter_by(country_code=code).first()
        if country and not country.flag_emoji:
            f = _flag_emoji(code)
            if f:
                country.flag_emoji = f
    return len(rows)


def load_country_metrics():
    rows = _csv('03_country_metrics_idn.csv')
    for row in rows:
        code, name = row['country_code'], row['metric_name']
        rec = CountryMetric.query.filter_by(country_code=code, metric_name=name).first()
        if not rec:
            rec = CountryMetric(country_code=code, metric_name=name)
            db.session.add(rec)
        rec.metric_value = _str(row.get('metric_value')) or rec.metric_value
        rec.metric_subtext = _str(row.get('metric_subtext')) or rec.metric_subtext
    return len(rows)


def load_ndc_targets():
    rows = _csv('04_country_ndc_targets_idn.csv')
    for row in rows:
        code, ttype = row['country_code'], row['target_type']
        rec = CountryNDCTarget.query.filter_by(country_code=code, target_type=ttype).first()
        if not rec:
            rec = CountryNDCTarget(country_code=code, target_type=ttype)
            db.session.add(rec)
        if _str(row.get('target_title')):
            rec.target_title = row['target_title']
        rec.unconditional_val = _str(row.get('unconditional_val')) or rec.unconditional_val
        rec.conditional_val = _str(row.get('conditional_val')) or rec.conditional_val
        v = _int(row.get('unconditional_pct'))
        if v is not None:
            rec.unconditional_pct = v
        v = _int(row.get('conditional_pct'))
        if v is not None:
            rec.conditional_pct = v
    return len(rows)


def load_carbon_markets():
    rows = _csv('05_country_carbon_markets_update.csv')
    for row in rows:
        code = row['country_code']
        rec = CountryCarbonMarket.query.filter_by(country_code=code).first()
        if not rec:
            rec = CountryCarbonMarket(country_code=code)
            db.session.add(rec)
        if _str(row.get('market_status')):
            rec.market_status = row['market_status']
        if _str(row.get('currency')):
            rec.currency = row['currency']
        v = _float(row.get('price_range_min'))
        if v is not None:
            rec.price_range_min = v
        v = _float(row.get('price_range_max'))
        if v is not None:
            rec.price_range_max = v
    return len(rows)


def load_institutions():
    rows = _csv('06_country_institutions_idn.csv')
    for row in rows:
        code, name = row['country_code'], row['name']
        rec = CountryInstitution.query.filter_by(country_code=code, name=name).first()
        if not rec:
            rec = CountryInstitution(country_code=code, name=name)
            db.session.add(rec)
        if _str(row.get('role')):
            rec.role = row['role']
        if _str(row.get('description')):
            rec.description = row['description']
    return len(rows)


def load_agreements():
    rows = _csv('07_country_agreements_idn.csv')
    for row in rows:
        aid = row['agreement_id']
        rec = CountryAgreement.query.filter_by(agreement_id=aid).first()
        if not rec:
            rec = CountryAgreement(agreement_id=aid, host_country_code=row['host_country_code'])
            db.session.add(rec)
        if _str(row.get('agreement_type')):
            rec.agreement_type = row['agreement_type']
        if _str(row.get('partner_entity')):
            rec.partner_entity = row['partner_entity']
        if _str(row.get('status')):
            rec.status = row['status']
        rec.date_signed = _str(row.get('date_signed'))
        if _str(row.get('reference_link')):
            rec.reference_link = row['reference_link']
    return len(rows)


def load_global_frameworks():
    rows = _csv('09_global_frameworks_idn.csv')
    for row in rows:
        fid = row['framework_id']
        rec = GlobalFramework.query.filter_by(framework_id=fid).first()
        if not rec:
            rec = GlobalFramework(framework_id=fid)
            db.session.add(rec)
        if _str(row.get('jurisdiction')):
            rec.jurisdiction = row['jurisdiction']
        if _str(row.get('title')):
            rec.title = row['title']
        if _str(row.get('description')):
            rec.description = row['description']
        if _str(row.get('status_date')):
            rec.status_date = row['status_date']
        if _str(row.get('category')):
            rec.category = row['category']
    return len(rows)


def load_global_news():
    rows = _csv('10_global_news_idn.csv')
    for row in rows:
        nid = row['news_id']
        rec = GlobalNews.query.filter_by(news_id=nid).first()
        if not rec:
            rec = GlobalNews(news_id=nid)
            db.session.add(rec)
        rec.country_code = _str(row.get('country_code'))
        if _str(row.get('title')):
            rec.title = row['title']
        if _str(row.get('body')):
            rec.body = row['body']
        if _str(row.get('date')):
            rec.date = row['date']
        rec.tags = _list(row.get('tags', ''))
    return len(rows)


def load_global_stats():
    rows = _csv('11_global_stats_new.csv')
    for row in rows:
        key = row['stat_key']
        rec = GlobalStat.query.filter_by(stat_key=key).first()
        if not rec:
            rec = GlobalStat(stat_key=key)
            db.session.add(rec)
        if _str(row.get('stat_value')):
            rec.stat_value = row['stat_value']
        if _str(row.get('stat_label')):
            rec.stat_label = row['stat_label']
        rec.stat_sub = _str(row.get('stat_sub'))
        if _str(row.get('color_hint')):
            rec.color_hint = row['color_hint']
    return len(rows)


def load_ticker_items():
    rows = _csv('12_ticker_items_new.csv')
    for row in rows:
        tid = row['ticker_id']
        rec = TickerItem.query.filter_by(ticker_id=tid).first()
        if not rec:
            rec = TickerItem(ticker_id=tid)
            db.session.add(rec)
        if _str(row.get('text')):
            rec.text = row['text']
        v = _int(row.get('order'))
        if v is not None:
            rec.order = v
    return len(rows)


def load_countries_ref():
    rows = _csv('14_countries_ref.csv')
    for row in rows:
        code = row['country_code']
        rec = Country.query.filter_by(country_code=code).first()
        if not rec:
            rec = Country(country_code=code)
            db.session.add(rec)
        if not rec.country_name and _str(row.get('country_name')):
            rec.country_name = row['country_name']
    return len(rows)


def load_country_metrics_ref():
    rows = _csv('15_country_metrics_ref.csv')
    added = 0
    for row in rows:
        code, name = row['country_code'], row['metric_name']
        if not CountryMetric.query.filter_by(country_code=code, metric_name=name).first():
            db.session.add(CountryMetric(
                country_code=code,
                metric_name=name,
                metric_value=_str(row.get('metric_value')),
                metric_subtext=_str(row.get('metric_subtext')),
            ))
            added += 1
    return added


def load_country_dimensions():
    rows = _csv('17_country_dimensions_idn.csv')
    for row in rows:
        code, dim = row['country_code'], row['dimension_id']
        rec = CountryDimension.query.filter_by(country_code=code, dimension_id=dim).first()
        if not rec:
            rec = CountryDimension(country_code=code, dimension_id=dim)
            db.session.add(rec)
        for field in ('label', 'full_label', 'gate', 'gate_text', 'description'):
            v = _str(row.get(field))
            if v is not None:
                setattr(rec, field, v)
    return len(rows)


def load_country_checklists():
    rows = _csv('18_country_checklists_idn.csv')
    # Replace-per-country so re-runs don't leave stale items.
    seen_countries = set()
    for row in rows:
        code = row['country_code']
        if code not in seen_countries:
            CountryChecklist.query.filter_by(country_code=code).delete()
            seen_countries.add(code)
        db.session.add(CountryChecklist(
            country_code=code,
            dimension_id=_str(row.get('dimension_id')),
            item_label=_str(row.get('item_label')),
            status=_str(row.get('status')),
        ))
    return len(rows)


def load_projects():
    rows = _csv('13_projects_idn_bluecarbon.csv')
    for row in rows:
        pid = row['project_id']
        rec = Project.query.filter_by(project_id=pid).first()
        if not rec:
            rec = Project(project_id=pid)
            db.session.add(rec)
        for field in ('project_name', 'location', 'status', 'area', 'methodology',
                      'ecosystem_type', 'vintage', 'credits', 'registry',
                      'description', 'price', 'rating_agency', 'rating_score', 'status_category'):
            v = _str(row.get(field))
            if v is not None:
                setattr(rec, field, v)
        rec.tags = _list(row.get('tags', ''))
        rec.checks = _list(row.get('checks', ''))
    return len(rows)


PROJECT_COST_FLOAT_FIELDS = (
    'project_size_ha', 'country_size_ha', 'base_size',
    'total_cost_npv', 'total_cost', 'total_weighted_cost_npv', 'total_weighted_cost',
    'capex_npv', 'capex', 'opex_npv', 'opex',
    'country_abatement_potential', 'project_abatement_potential',
    'cost_per_tco2e', 'cost_per_tco2e_npv',
    'feasibility_analysis_npv', 'feasibility_analysis',
    'conservation_planning_npv', 'conservation_planning',
    'data_collection_npv', 'data_collection',
    'community_representation_npv', 'community_representation',
    'blue_carbon_project_planning_npv', 'blue_carbon_project_planning',
    'establishing_carbon_rights_npv', 'establishing_carbon_rights',
    'validation_npv', 'validation',
    'implementation_labor_npv', 'implementation_labor',
    'monitoring_maintenance_npv', 'monitoring_maintenance',
    'community_benefit_npv', 'community_benefit',
    'carbon_standard_fees_npv', 'carbon_standard_fees',
    'baseline_reassessment_npv', 'baseline_reassessment',
    'mrv_npv', 'mrv',
    'long_term_project_operating_npv', 'long_term_project_operating',
    'initial_price_assumption', 'leftover_after_opex', 'leftover_after_opex_npv',
    'total_revenue', 'total_revenue_npv', 'credits_issued',
    'monitoring_npv', 'maintenance_npv', 'monitoring', 'maintenance',
)

PROJECT_COST_STR_FIELDS = (
    'country', 'country_code', 'ecosystem', 'activity', 'activity_type',
    'project_size_filter', 'price_type', 'project_name',
)


def load_project_costs():
    rows = _csv('16_project_costs_ref.csv')
    for row in rows:
        key = dict(
            country_code=_str(row.get('country_code')),
            ecosystem=_str(row.get('ecosystem')),
            activity=_str(row.get('activity')),
            activity_type=_str(row.get('activity_type')),
            project_size_filter=_str(row.get('project_size_filter')),
        )
        if not all(key.values()):
            continue
        rec = ProjectCost.query.filter_by(**key).first()
        if not rec:
            rec = ProjectCost(**key)
            db.session.add(rec)
        for field in PROJECT_COST_STR_FIELDS:
            if field in key:
                continue
            v = _str(row.get(field))
            if v is not None:
                setattr(rec, field, v)
        for field in PROJECT_COST_FLOAT_FIELDS:
            v = _float(row.get(field))
            if v is not None:
                setattr(rec, field, v)
    return len(rows)


# ── Entry point ───────────────────────────────────────────────────────────────

LOADERS = [
    ('01_countries_update.csv',          load_countries),
    ('02_country_ndcs_update.csv',       load_country_ndcs),
    ('03_country_metrics_idn.csv',       load_country_metrics),
    ('04_country_ndc_targets_idn.csv',   load_ndc_targets),
    ('05_country_carbon_markets_update.csv', load_carbon_markets),
    ('06_country_institutions_idn.csv',  load_institutions),
    ('07_country_agreements_idn.csv',    load_agreements),
    ('09_global_frameworks_idn.csv',     load_global_frameworks),
    ('10_global_news_idn.csv',           load_global_news),
    ('11_global_stats_new.csv',          load_global_stats),
    ('12_ticker_items_new.csv',          load_ticker_items),
    ('13_projects_idn_bluecarbon.csv',   load_projects),
    ('14_countries_ref.csv',             load_countries_ref),
    ('15_country_metrics_ref.csv',       load_country_metrics_ref),
    ('16_project_costs_ref.csv',         load_project_costs),
    ('17_country_dimensions_idn.csv',    load_country_dimensions),
    ('18_country_checklists_idn.csv',    load_country_checklists),
]


def load_all():
    app = create_app()
    with app.app_context():
        total = 0
        for filename, loader in LOADERS:
            n = loader()
            if n:
                print(f'  ✓ {filename}: {n} rows')
            total += n
        db.session.commit()
        print(f'✓ Data loaded: {total} rows across {len(LOADERS)} files.')


if __name__ == '__main__':
    load_all()
