from flask import Blueprint, jsonify, request
from app.models.global_layer import Country, CountryNDC, CountryCarbonMarket, GlobalFramework, GlobalNews, GlobalTradeTrend

global_bp = Blueprint('global', __name__)


# --- Countries ---

@global_bp.route('/countries', methods=['GET'])
def get_countries():
    tier = request.args.get('tier')
    query = Country.query
    if tier:
        query = query.filter_by(readiness_tier=tier)
    return jsonify([c.to_dict() for c in query.all()])


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


# --- Frameworks ---

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


# --- News ---

@global_bp.route('/news', methods=['GET'])
def get_news():
    news = GlobalNews.query.order_by(GlobalNews.date.desc()).all()
    return jsonify([n.to_dict() for n in news])


@global_bp.route('/news/<string:news_id>', methods=['GET'])
def get_news_item(news_id):
    news = GlobalNews.query.filter_by(news_id=news_id).first_or_404()
    return jsonify(news.to_dict())


# --- Trade Trends ---

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
