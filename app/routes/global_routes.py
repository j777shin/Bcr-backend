from flask import Blueprint, jsonify, request
from app import db
from app.models.global_layer import (
    Country, CountryNDC, CountryCarbonMarket,
    GlobalFramework, GlobalNews, GlobalTradeTrend,
    TickerItem, GlobalStat,
)

global_bp = Blueprint('global', __name__)


# ── Summary ──────────────────────────────────────────────────────────────────

@global_bp.route('/summary', methods=['GET'])
def get_summary():
    stats = GlobalStat.query.all()
    return jsonify({s.stat_key: s.to_dict() for s in stats})


# ── Ticker ────────────────────────────────────────────────────────────────────

@global_bp.route('/ticker', methods=['GET'])
def get_ticker():
    items = TickerItem.query.order_by(TickerItem.order).all()
    return jsonify([i.to_dict() for i in items])


# ── Countries ─────────────────────────────────────────────────────────────────

@global_bp.route('/countries', methods=['GET'])
def get_countries():
    tier = request.args.get('tier')
    query = Country.query
    if tier:
        query = query.filter_by(readiness_tier=tier)
    return jsonify([c.to_dict() for c in query.order_by(Country.readiness_score.desc().nullslast()).all()])


@global_bp.route('/countries/<string:country_code>', methods=['GET'])
def get_country(country_code):
    country = Country.query.filter_by(country_code=country_code.upper()).first_or_404()
    return jsonify(country.to_dict())


@global_bp.route('/countries/<string:country_code>/ndc', methods=['GET'])
def get_country_ndc(country_code):
    ndc = CountryNDC.query.filter_by(country_code=country_code.upper()).first_or_404()
    return jsonify(ndc.to_dict())


@global_bp.route('/countries/<string:country_code>/carbon-markets', methods=['GET'])
def get_country_carbon_markets(country_code):
    markets = CountryCarbonMarket.query.filter_by(country_code=country_code.upper()).all()
    return jsonify([m.to_dict() for m in markets])


# ── NDC Tracker (joined view) ─────────────────────────────────────────────────

@global_bp.route('/ndc-tracker', methods=['GET'])
def get_ndc_tracker():
    filter_market = request.args.get('market')
    filter_target = request.args.get('target')
    filter_eco = request.args.get('ecosystem')

    ndcs = CountryNDC.query.all()
    results = []
    for ndc in ndcs:
        country = Country.query.filter_by(country_code=ndc.country_code).first()
        if not country:
            continue
        eco = list(dict.fromkeys(
            (ndc.unconditional_ecosystems or []) + (ndc.conditional_ecosystems or [])
        ))
        row = {
            'country_code': country.country_code,
            'country': country.country_name,
            'flag': country.flag_emoji,
            'ndc': ndc.ndc_version,
            'eco': eco,
            'target': ndc.target_type,
            'market': ndc.domestic_pricing,
            'mkt_status': ndc.market_status,
        }
        # Server-side filtering
        if filter_market and filter_market == 'operational':
            if 'Operational' not in (ndc.market_status or ''):
                continue
        if filter_target and filter_target != row['target'].lower():
            continue
        if filter_eco:
            if not any(filter_eco.lower() in e.lower() for e in eco):
                continue
        results.append(row)

    return jsonify(results)


# ── Frameworks ────────────────────────────────────────────────────────────────

@global_bp.route('/frameworks', methods=['GET'])
def get_frameworks():
    category = request.args.get('category')
    query = GlobalFramework.query
    if category:
        query = query.filter_by(category=category)
    return jsonify([f.to_dict() for f in query.all()])


@global_bp.route('/frameworks/<string:framework_id>', methods=['GET'])
def get_framework(framework_id):
    framework = GlobalFramework.query.filter_by(framework_id=framework_id).first_or_404()
    return jsonify(framework.to_dict())


# ── News ──────────────────────────────────────────────────────────────────────

@global_bp.route('/news', methods=['GET'])
def get_news():
    country_code = request.args.get('country')
    tag = request.args.get('tag')

    query = GlobalNews.query
    if country_code:
        query = query.filter_by(country_code=country_code.upper())
    else:
        # Default: return global news (country_code is null) + all country news
        pass
    news_items = query.order_by(GlobalNews.date.desc()).all()

    if tag:
        news_items = [n for n in news_items if tag in (n.tags or [])]

    return jsonify([n.to_dict() for n in news_items])


@global_bp.route('/news/<string:news_id>', methods=['GET'])
def get_news_item(news_id):
    news = GlobalNews.query.filter_by(news_id=news_id).first_or_404()
    return jsonify(news.to_dict())


# ── Trade Trends ──────────────────────────────────────────────────────────────

@global_bp.route('/trade-trends', methods=['GET'])
def get_trade_trends():
    year = request.args.get('year', type=int)
    ecosystem = request.args.get('ecosystem')

    query = GlobalTradeTrend.query
    if year:
        query = query.filter_by(year=year)
    if ecosystem:
        query = query.filter_by(ecosystem_category=ecosystem)

    return jsonify([t.to_dict() for t in query.order_by(GlobalTradeTrend.year).all()])
