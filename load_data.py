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
    EcosystemRecognition, CountryAgreement,
)
from app.models.project_layer import Project

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
                      'dim_3_institutional', 'dim_4_operational', 'dim_5_infrastructure'):
            v = _int(row.get(field))
            if v is not None:
                setattr(rec, field, v)
        v = _float(row.get('map_cx'))
        if v is not None:
            rec.map_cx = v
        v = _float(row.get('map_cy'))
        if v is not None:
            rec.map_cy = v
    return len(rows)


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


def load_ecosystem_recognitions():
    rows = _csv('08_ecosystem_recognitions_idn.csv')
    for row in rows:
        code, eco = row['country_code'], row['ecosystem_type']
        rec = EcosystemRecognition.query.filter_by(country_code=code, ecosystem_type=eco).first()
        if not rec:
            rec = EcosystemRecognition(country_code=code, ecosystem_type=eco)
            db.session.add(rec)
        if _str(row.get('recognition_status')):
            rec.recognition_status = row['recognition_status']
        if _str(row.get('details')):
            rec.details = row['details']
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
        if rec.map_cx is None:
            v = _float(row.get('map_cx'))
            if v is not None:
                rec.map_cx = v
        if rec.map_cy is None:
            v = _float(row.get('map_cy'))
            if v is not None:
                rec.map_cy = v
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


def load_projects():
    rows = _csv('13_projects_idn_energy.csv')
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


# ── Entry point ───────────────────────────────────────────────────────────────

LOADERS = [
    ('01_countries_update.csv',          load_countries),
    ('02_country_ndcs_update.csv',       load_country_ndcs),
    ('03_country_metrics_idn.csv',       load_country_metrics),
    ('04_country_ndc_targets_idn.csv',   load_ndc_targets),
    ('05_country_carbon_markets_update.csv', load_carbon_markets),
    ('06_country_institutions_idn.csv',  load_institutions),
    ('07_country_agreements_idn.csv',    load_agreements),
    ('08_ecosystem_recognitions_idn.csv', load_ecosystem_recognitions),
    ('09_global_frameworks_idn.csv',     load_global_frameworks),
    ('10_global_news_idn.csv',           load_global_news),
    ('11_global_stats_new.csv',          load_global_stats),
    ('12_ticker_items_new.csv',          load_ticker_items),
    ('13_projects_idn_energy.csv',       load_projects),
    ('14_countries_ref.csv',             load_countries_ref),
    ('15_country_metrics_ref.csv',       load_country_metrics_ref),
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
