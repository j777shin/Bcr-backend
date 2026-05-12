from app import db


class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_code = db.Column(db.String(3), unique=True, nullable=False, index=True)
    country_name = db.Column(db.String(100), nullable=False)
    flag_emoji = db.Column(db.String(10))
    readiness_score = db.Column(db.Integer, nullable=True)
    readiness_tier = db.Column(db.String(50))
    context_note = db.Column(db.String(200))
    # 5 building blocks (UNFCCC / NDC Partnership Article 6 Readiness Toolkit)
    dim_1_strategic = db.Column(db.Integer)
    dim_2_legal = db.Column(db.Integer)
    dim_3_institutional = db.Column(db.Integer)
    dim_4_operational = db.Column(db.Integer)
    dim_5_infrastructure = db.Column(db.Integer)
    # CAAS Article Six Investment Readiness Index — 5 dimensions
    # A: legally do it? · B: measure & verify? · C: financed & sold? ·
    # D: socially & environmentally credible? · E: issued & tracked?
    caas_a_legal = db.Column(db.Integer)
    caas_b_mrv = db.Column(db.Integer)
    caas_c_finance = db.Column(db.Integer)
    caas_d_social = db.Column(db.Integer)
    caas_e_registry = db.Column(db.Integer)
    # ── Real binary readiness indicators (5; primary sources only) ──────────
    # All sourced; see DATA.md for the per-flag provenance.
    flag_dna_appointed       = db.Column(db.Boolean, default=False)
    flag_pr_submitted        = db.Column(db.Boolean, default=False)
    flag_ndc_blue_carbon     = db.Column(db.Boolean, default=False)
    flag_bilateral_a6_2      = db.Column(db.Boolean, default=False)
    flag_market_operational  = db.Column(db.Boolean, default=False)
    components_count         = db.Column(db.Integer, default=0)  # 0–5; precomputed
    # Aliases kept for backwards compatibility with earlier UI code.
    dna_appointed = db.Column(db.Boolean, default=False)
    pr_submitted = db.Column(db.Boolean, default=False)
    # SVG map coordinates (viewBox 0 0 1200 560) — legacy stylized map
    map_cx = db.Column(db.Float, nullable=True)
    map_cy = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {
            'country_code': self.country_code,
            'country_name': self.country_name,
            'flag_emoji': self.flag_emoji,
            'readiness_score': self.readiness_score,
            'readiness_tier': self.readiness_tier,
            'context_note': self.context_note,
            'dim_1_strategic': self.dim_1_strategic,
            'dim_2_legal': self.dim_2_legal,
            'dim_3_institutional': self.dim_3_institutional,
            'dim_4_operational': self.dim_4_operational,
            'dim_5_infrastructure': self.dim_5_infrastructure,
            'caas_a_legal': self.caas_a_legal,
            'caas_b_mrv': self.caas_b_mrv,
            'caas_c_finance': self.caas_c_finance,
            'caas_d_social': self.caas_d_social,
            'caas_e_registry': self.caas_e_registry,
            'flag_dna_appointed': bool(self.flag_dna_appointed),
            'flag_pr_submitted': bool(self.flag_pr_submitted),
            'flag_ndc_blue_carbon': bool(self.flag_ndc_blue_carbon),
            'flag_bilateral_a6_2': bool(self.flag_bilateral_a6_2),
            'flag_market_operational': bool(self.flag_market_operational),
            'components_count': self.components_count or 0,
            'dna_appointed': bool(self.dna_appointed or self.flag_dna_appointed),
            'pr_submitted': bool(self.pr_submitted or self.flag_pr_submitted),
            'map_cx': self.map_cx,
            'map_cy': self.map_cy,
        }


class CountryNDC(db.Model):
    __tablename__ = 'country_ndcs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_code = db.Column(db.String(3), db.ForeignKey('countries.country_code'), nullable=False, index=True)
    ndc_version = db.Column(db.String(50))
    blue_carbon_included = db.Column(db.Boolean)
    unconditional_ecosystems = db.Column(db.JSON)
    conditional_ecosystems = db.Column(db.JSON)
    unconditional_target_desc = db.Column(db.Text)
    conditional_target_desc = db.Column(db.Text)
    intervention_type = db.Column(db.String(50))
    target_type = db.Column(db.String(50))
    targets = db.Column(db.String(200))
    domestic_pricing = db.Column(db.String(100))
    market_status = db.Column(db.String(50))

    def to_dict(self):
        return {
            'country_code': self.country_code,
            'ndc_version': self.ndc_version,
            'blue_carbon_included': self.blue_carbon_included,
            'unconditional_ecosystems': self.unconditional_ecosystems or [],
            'conditional_ecosystems': self.conditional_ecosystems or [],
            'unconditional_target_desc': self.unconditional_target_desc,
            'conditional_target_desc': self.conditional_target_desc,
            'intervention_type': self.intervention_type,
            'target_type': self.target_type,
            'targets': self.targets,
            'domestic_pricing': self.domestic_pricing,
            'market_status': self.market_status,
        }


class CountryCarbonMarket(db.Model):
    __tablename__ = 'country_carbon_markets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_code = db.Column(db.String(3), db.ForeignKey('countries.country_code'), nullable=False, index=True)
    market_status = db.Column(db.String(100))
    price_range_min = db.Column(db.Float)
    price_range_max = db.Column(db.Float)
    currency = db.Column(db.String(10))

    def to_dict(self):
        return {
            'country_code': self.country_code,
            'market_status': self.market_status,
            'price_range_min': self.price_range_min,
            'price_range_max': self.price_range_max,
            'currency': self.currency,
        }


class GlobalFramework(db.Model):
    __tablename__ = 'global_frameworks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    framework_id = db.Column(db.String(50), unique=True, nullable=False)
    jurisdiction = db.Column(db.String(200))
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    status_date = db.Column(db.String(100))
    category = db.Column(db.String(50))

    def to_dict(self):
        return {
            'framework_id': self.framework_id,
            'jurisdiction': self.jurisdiction,
            'title': self.title,
            'description': self.description,
            'status_date': self.status_date,
            'category': self.category,
        }


class GlobalNews(db.Model):
    __tablename__ = 'global_news'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    news_id = db.Column(db.String(50), unique=True, nullable=False)
    country_code = db.Column(db.String(3), nullable=True)  # null = global news
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    date = db.Column(db.String(50))
    tags = db.Column(db.JSON)

    def to_dict(self):
        return {
            'news_id': self.news_id,
            'country_code': self.country_code,
            'title': self.title,
            'body': self.body,
            'date': self.date,
            'tags': self.tags or [],
        }


class GlobalTradeTrend(db.Model):
    __tablename__ = 'global_trade_trends'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trend_id = db.Column(db.String(50), unique=True, nullable=False)
    year = db.Column(db.Integer)
    ecosystem_category = db.Column(db.String(100))
    volume_traded_mt = db.Column(db.Float)
    average_price_usd = db.Column(db.Float)
    data_source = db.Column(db.String(200))

    def to_dict(self):
        return {
            'trend_id': self.trend_id,
            'year': self.year,
            'ecosystem_category': self.ecosystem_category,
            'volume_traded_mt': self.volume_traded_mt,
            'average_price_usd': self.average_price_usd,
            'data_source': self.data_source,
        }


class TickerItem(db.Model):
    __tablename__ = 'ticker_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticker_id = db.Column(db.String(50), unique=True, nullable=False)
    text = db.Column(db.String(500), nullable=False)
    order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'ticker_id': self.ticker_id,
            'text': self.text,
            'order': self.order,
        }


class GlobalStat(db.Model):
    __tablename__ = 'global_stats'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stat_key = db.Column(db.String(100), unique=True, nullable=False)
    stat_value = db.Column(db.String(50))
    stat_label = db.Column(db.String(200))
    stat_sub = db.Column(db.String(200))
    color_hint = db.Column(db.String(50))  # e.g. 'leaf3', 'tide3', 'white'

    def to_dict(self):
        return {
            'stat_key': self.stat_key,
            'stat_value': self.stat_value,
            'stat_label': self.stat_label,
            'stat_sub': self.stat_sub,
            'color_hint': self.color_hint,
        }
