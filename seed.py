"""
Populate the database with all BCR Dashboard data.
Usage: python seed.py
"""
from app import create_app, db
from app.models.global_layer import (
    Country, CountryNDC, CountryCarbonMarket,
    GlobalFramework, GlobalNews, GlobalTradeTrend,
    TickerItem, GlobalStat,
)
from app.models.country_layer import (
    CountryMetric, CountryDimension, CountryChecklist,
    CountryNDCTarget, CountryInstitution,
    EcosystemRecognition, CountryAgreement,
)
from app.models.project_layer import Project, Methodology, EcosystemTier


def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # ── Ticker ───────────────────────────────────────────────────────────

        tickers = [
            TickerItem(ticker_id='T1', order=1, text="PR 110/2025 operationalizes Indonesia's ITMO export pathway via ministerial authorization"),
            TickerItem(ticker_id='T2', order=2, text='VM0033 deprecated in Indonesia since 2023 — VM0053 now mandatory for all new projects'),
            TickerItem(ticker_id='T3', order=3, text='IDXCarbon exchange stabilizes at ~$4/tonne — below international blue carbon benchmarks'),
            TickerItem(ticker_id='T4', order=4, text='Indonesia targets international carbon market entry by 2027'),
            TickerItem(ticker_id='T5', order=5, text='South Korea absent from Article 6 readiness rankings — transparency gap flagged'),
            TickerItem(ticker_id='T6', order=6, text='ICVCM CCP label increasingly required by institutional Art.6 buyers'),
            TickerItem(ticker_id='T7', order=7, text='MOMAF Reg 1/2025 specifically governs blue carbon ecosystems for domestic & international markets'),
        ]
        db.session.add_all(tickers)

        # ── Global Stats ─────────────────────────────────────────────────────

        stats = [
            # Hero section
            GlobalStat(stat_key='hero_countries', stat_value='18', stat_label='Countries tracked', stat_sub='blue carbon potential', color_hint='leaf3'),
            GlobalStat(stat_key='hero_mangrove_ha', stat_value='3.44M', stat_label='Indonesia mangrove ha', stat_sub='20% of global total', color_hint='tide3'),
            GlobalStat(stat_key='hero_high_readiness', stat_value='4', stat_label='High readiness', stat_sub='countries ≥ 75%', color_hint='white'),
            GlobalStat(stat_key='hero_avg_price', stat_value='$18', stat_label='Avg blue C premium', stat_sub='USD / tonne CO₂', color_hint='white'),
            # Global section stat strip
            GlobalStat(stat_key='global_countries_total', stat_value='47', stat_label='Countries in Art.6.4 participation tracker', stat_sub=None, color_hint='white'),
            GlobalStat(stat_key='high_readiness_count', stat_value='4', stat_label='High readiness (≥75%)', stat_sub=None, color_hint='leaf3'),
            GlobalStat(stat_key='developing_count', stat_value='7', stat_label='Developing (40–74%)', stat_sub=None, color_hint='amber3'),
            GlobalStat(stat_key='early_stage_count', stat_value='7', stat_label='Early stage / no data', stat_sub=None, color_hint='coral3'),
            # Projects section
            GlobalStat(stat_key='projects_total', stat_value='47', stat_label='Total projects', stat_sub='tracked globally', color_hint='white'),
            GlobalStat(stat_key='projects_mangroves', stat_value='38', stat_label='Mangroves', stat_sub='projects in pipeline', color_hint='leaf3'),
            GlobalStat(stat_key='projects_tidal', stat_value='6', stat_label='Tidal Marshes', stat_sub='projects in pipeline', color_hint='tide3'),
            GlobalStat(stat_key='projects_seagrass', stat_value='3', stat_label='Seagrass', stat_sub='projects in pipeline', color_hint='amber3'),
            GlobalStat(stat_key='projects_avg_price', stat_value='$18', stat_label='Avg price', stat_sub='blue C premium (VCM)', color_hint='white'),
        ]
        db.session.add_all(stats)

        # ── Countries (all NDC tracker entries + WorldMap countries) ─────────
        # SVG viewBox: 0 0 1200 560; coords are (cx, cy) in SVG units.
        # Approximate pixel positions derived from country locations.

        countries = [
            Country(
                country_code='IDN', country_name='Indonesia', flag_emoji='🇮🇩',
                readiness_score=84, readiness_tier='High readiness',
                context_note='Art.6.2 · Art.6.4',
                dim_1_strategic=88, dim_2_legal=92, dim_3_institutional=82,
                dim_4_operational=72, dim_5_infrastructure=78,
                map_cx=966.0, map_cy=268.0,
            ),
            Country(
                country_code='KEN', country_name='Kenya', flag_emoji='🇰🇪',
                readiness_score=76, readiness_tier='High readiness',
                context_note='Art.6.2',
                dim_1_strategic=78, dim_2_legal=80, dim_3_institutional=72,
                dim_4_operational=74, dim_5_infrastructure=68,
                map_cx=660.0, map_cy=276.0,
            ),
            Country(
                country_code='BRA', country_name='Brazil', flag_emoji='🇧🇷',
                readiness_score=58, readiness_tier='Developing',
                context_note=None,
                dim_1_strategic=62, dim_2_legal=55, dim_3_institutional=60,
                dim_4_operational=58, dim_5_infrastructure=52,
                map_cx=310.0, map_cy=355.0,
            ),
            Country(
                country_code='VNM', country_name='Vietnam', flag_emoji='🇻🇳',
                readiness_score=48, readiness_tier='Developing',
                context_note=None,
                dim_1_strategic=52, dim_2_legal=45, dim_3_institutional=48,
                dim_4_operational=50, dim_5_infrastructure=40,
                map_cx=926.0, map_cy=210.0,
            ),
            Country(
                country_code='AUS', country_name='Australia', flag_emoji='🇦🇺',
                readiness_score=77, readiness_tier='High readiness',
                context_note=None,
                dim_1_strategic=80, dim_2_legal=82, dim_3_institutional=75,
                dim_4_operational=72, dim_5_infrastructure=74,
                map_cx=1055.0, map_cy=385.0,
            ),
            Country(
                country_code='CHN', country_name='China', flag_emoji='🇨🇳',
                readiness_score=62, readiness_tier='Developing',
                context_note=None,
                dim_1_strategic=68, dim_2_legal=65, dim_3_institutional=60,
                dim_4_operational=60, dim_5_infrastructure=58,
                map_cx=870.0, map_cy=170.0,
            ),
            Country(
                country_code='KOR', country_name='South Korea', flag_emoji='🇰🇷',
                readiness_score=60, readiness_tier='Developing',
                context_note='Art.6 transparency gap flagged',
                dim_1_strategic=55, dim_2_legal=65, dim_3_institutional=62,
                dim_4_operational=60, dim_5_infrastructure=58,
                map_cx=968.0, map_cy=158.0,
            ),
            Country(
                country_code='JPN', country_name='Japan', flag_emoji='🇯🇵',
                readiness_score=75, readiness_tier='High readiness',
                context_note=None,
                dim_1_strategic=78, dim_2_legal=80, dim_3_institutional=74,
                dim_4_operational=70, dim_5_infrastructure=72,
                map_cx=1018.0, map_cy=162.0,
            ),
            Country(
                country_code='COL', country_name='Colombia', flag_emoji='🇨🇴',
                readiness_score=66, readiness_tier='Developing',
                context_note=None,
                dim_1_strategic=70, dim_2_legal=65, dim_3_institutional=65,
                dim_4_operational=68, dim_5_infrastructure=58,
                map_cx=298.0, map_cy=352.0,
            ),
            Country(
                country_code='PHL', country_name='Philippines', flag_emoji='🇵🇭',
                readiness_score=54, readiness_tier='Developing',
                context_note=None,
                dim_1_strategic=58, dim_2_legal=52, dim_3_institutional=55,
                dim_4_operational=50, dim_5_infrastructure=48,
                map_cx=996.0, map_cy=238.0,
            ),
            Country(
                country_code='SYC', country_name='Seychelles', flag_emoji='🇸🇨',
                readiness_score=38, readiness_tier='Early stage',
                context_note=None,
                dim_1_strategic=42, dim_2_legal=38, dim_3_institutional=35,
                dim_4_operational=38, dim_5_infrastructure=32,
                map_cx=700.0, map_cy=295.0,
            ),
            Country(
                country_code='GBR', country_name='United Kingdom', flag_emoji='🇬🇧',
                readiness_score=78, readiness_tier='High readiness',
                context_note=None,
                dim_1_strategic=82, dim_2_legal=85, dim_3_institutional=76,
                dim_4_operational=74, dim_5_infrastructure=72,
                map_cx=488.0, map_cy=108.0,
            ),
            Country(
                country_code='CRI', country_name='Costa Rica', flag_emoji='🇨🇷',
                readiness_score=65, readiness_tier='Developing',
                context_note=None,
                dim_1_strategic=70, dim_2_legal=65, dim_3_institutional=62,
                dim_4_operational=62, dim_5_infrastructure=58,
                map_cx=258.0, map_cy=285.0,
            ),
            Country(
                country_code='BLZ', country_name='Belize', flag_emoji='🇧🇿',
                readiness_score=58, readiness_tier='Developing',
                context_note=None,
                dim_1_strategic=60, dim_2_legal=58, dim_3_institutional=55,
                dim_4_operational=58, dim_5_infrastructure=50,
                map_cx=248.0, map_cy=260.0,
            ),
            Country(
                country_code='SGP', country_name='Singapore', flag_emoji='🇸🇬',
                readiness_score=65, readiness_tier='Developing',
                context_note=None,
                dim_1_strategic=68, dim_2_legal=70, dim_3_institutional=65,
                dim_4_operational=62, dim_5_infrastructure=58,
                map_cx=952.0, map_cy=302.0,
            ),
            Country(
                country_code='NOR', country_name='Norway', flag_emoji='🇳🇴',
                readiness_score=70, readiness_tier='Developing',
                context_note=None,
                dim_1_strategic=72, dim_2_legal=75, dim_3_institutional=70,
                dim_4_operational=65, dim_5_infrastructure=68,
                map_cx=524.0, map_cy=85.0,
            ),
            Country(
                country_code='CAN', country_name='Canada', flag_emoji='🇨🇦',
                readiness_score=72, readiness_tier='Developing',
                context_note=None,
                dim_1_strategic=76, dim_2_legal=74, dim_3_institutional=72,
                dim_4_operational=68, dim_5_infrastructure=70,
                map_cx=185.0, map_cy=115.0,
            ),
            Country(
                country_code='MEX', country_name='Mexico', flag_emoji='🇲🇽',
                readiness_score=62, readiness_tier='Developing',
                context_note=None,
                dim_1_strategic=65, dim_2_legal=62, dim_3_institutional=60,
                dim_4_operational=62, dim_5_infrastructure=58,
                map_cx=215.0, map_cy=242.0,
            ),
            Country(
                country_code='CHL', country_name='Chile', flag_emoji='🇨🇱',
                readiness_score=60, readiness_tier='Developing',
                context_note=None,
                dim_1_strategic=62, dim_2_legal=62, dim_3_institutional=58,
                dim_4_operational=58, dim_5_infrastructure=55,
                map_cx=278.0, map_cy=440.0,
            ),
            Country(
                country_code='EUU', country_name='EU', flag_emoji='🇪🇺',
                readiness_score=72, readiness_tier='Developing',
                context_note=None,
                dim_1_strategic=75, dim_2_legal=78, dim_3_institutional=72,
                dim_4_operational=68, dim_5_infrastructure=70,
                map_cx=532.0, map_cy=118.0,
            ),
            Country(
                country_code='FJI', country_name='Fiji', flag_emoji='🇫🇯',
                readiness_score=35, readiness_tier='Early stage',
                context_note=None,
                dim_1_strategic=38, dim_2_legal=35, dim_3_institutional=32,
                dim_4_operational=35, dim_5_infrastructure=28,
                map_cx=1112.0, map_cy=348.0,
            ),
            Country(
                country_code='BGD', country_name='Bangladesh', flag_emoji='🇧🇩',
                readiness_score=30, readiness_tier='Early stage',
                context_note=None,
                dim_1_strategic=32, dim_2_legal=30, dim_3_institutional=28,
                dim_4_operational=30, dim_5_infrastructure=25,
                map_cx=820.0, map_cy=212.0,
            ),
            Country(
                country_code='THA', country_name='Thailand', flag_emoji='🇹🇭',
                readiness_score=42, readiness_tier='Early stage',
                context_note=None,
                dim_1_strategic=45, dim_2_legal=42, dim_3_institutional=40,
                dim_4_operational=42, dim_5_infrastructure=38,
                map_cx=900.0, map_cy=228.0,
            ),
            Country(
                country_code='ZAF', country_name='South Africa', flag_emoji='🇿🇦',
                readiness_score=58, readiness_tier='Developing',
                context_note=None,
                dim_1_strategic=60, dim_2_legal=60, dim_3_institutional=55,
                dim_4_operational=58, dim_5_infrastructure=52,
                map_cx=628.0, map_cy=402.0,
            ),
            Country(
                country_code='BHS', country_name='Bahamas', flag_emoji='🇧🇸',
                readiness_score=42, readiness_tier='Early stage',
                context_note=None,
                dim_1_strategic=45, dim_2_legal=42, dim_3_institutional=40,
                dim_4_operational=40, dim_5_infrastructure=38,
                map_cx=262.0, map_cy=242.0,
            ),
            Country(
                country_code='MDV', country_name='Maldives', flag_emoji='🇲🇻',
                readiness_score=32, readiness_tier='Early stage',
                context_note=None,
                dim_1_strategic=35, dim_2_legal=32, dim_3_institutional=30,
                dim_4_operational=30, dim_5_infrastructure=28,
                map_cx=802.0, map_cy=282.0,
            ),
            Country(
                country_code='PLW', country_name='Palau', flag_emoji='🇵🇼',
                readiness_score=30, readiness_tier='Early stage',
                context_note=None,
                dim_1_strategic=32, dim_2_legal=28, dim_3_institutional=28,
                dim_4_operational=30, dim_5_infrastructure=25,
                map_cx=1038.0, map_cy=270.0,
            ),
            Country(
                country_code='GAB', country_name='Gabon', flag_emoji='🇬🇦',
                readiness_score=35, readiness_tier='Early stage',
                context_note=None,
                dim_1_strategic=38, dim_2_legal=35, dim_3_institutional=32,
                dim_4_operational=35, dim_5_infrastructure=28,
                map_cx=558.0, map_cy=318.0,
            ),
        ]
        db.session.add_all(countries)
        db.session.flush()

        # ── Country NDCs ──────────────────────────────────────────────────────

        ndcs = [
            CountryNDC(country_code='IDN', ndc_version='2nd NDC (2025)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Mangroves', 'Seagrass'],
                       conditional_ecosystems=['Mangroves', 'Seagrass'],
                       target_type='Both', domestic_pricing='ETS & Carbon Tax', market_status='Operational'),
            CountryNDC(country_code='BRA', ndc_version='NDC 3.0 (2025)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Mangroves', 'Corals'],
                       conditional_ecosystems=[],
                       target_type='Unconditional', domestic_pricing='ETS (in dev.)', market_status='Under development'),
            CountryNDC(country_code='KEN', ndc_version='NDC 3.0 (2025)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Mangroves', 'Seagrass'],
                       conditional_ecosystems=['Mangroves', 'Seagrass'],
                       target_type='Both', domestic_pricing='Carbon market regs', market_status='Operational'),
            CountryNDC(country_code='VNM', ndc_version='Updated (2022)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Mangroves', 'Seagrass'],
                       conditional_ecosystems=['Mangroves', 'Seagrass'],
                       target_type='Both', domestic_pricing='ETS (planned)', market_status='Pilot / Planned'),
            CountryNDC(country_code='AUS', ndc_version='Updated (2022)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Mangroves', 'Saltmarsh', 'Seagrass'],
                       conditional_ecosystems=[],
                       target_type='Unconditional', domestic_pricing='Safeguard Mechanism', market_status='Operational'),
            CountryNDC(country_code='CHN', ndc_version='Updated (2021)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Mangroves', 'Seagrass'],
                       conditional_ecosystems=[],
                       target_type='Unconditional', domestic_pricing='National ETS', market_status='Operational (2025+)'),
            CountryNDC(country_code='KOR', ndc_version='2035 NDC (2025)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Coastal wetlands'],
                       conditional_ecosystems=[],
                       target_type='Unconditional', domestic_pricing='K-ETS', market_status='Operational'),
            CountryNDC(country_code='JPN', ndc_version='Updated (2021)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Seagrass', 'Mangroves'],
                       conditional_ecosystems=[],
                       target_type='Unconditional', domestic_pricing='GX-ETS', market_status='Pilot / Operational'),
            CountryNDC(country_code='COL', ndc_version='NDC 3.0 (2025)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Mangroves', 'Peatlands'],
                       conditional_ecosystems=['Mangroves', 'Peatlands'],
                       target_type='Both', domestic_pricing='Carbon Tax', market_status='Operational'),
            CountryNDC(country_code='PHL', ndc_version='Updated (2021)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Mangroves'],
                       conditional_ecosystems=['Mangroves'],
                       target_type='Conditional', domestic_pricing='ETS (planned)', market_status='Under development'),
            CountryNDC(country_code='SYC', ndc_version='Updated (2021)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Seagrass', 'Mangroves'],
                       conditional_ecosystems=[],
                       target_type='Unconditional', domestic_pricing='None', market_status='No market'),
            CountryNDC(country_code='GBR', ndc_version='NDC 3.0 (2025)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Saltmarshes'],
                       conditional_ecosystems=[],
                       target_type='Unconditional', domestic_pricing='UK ETS', market_status='Operational'),
            CountryNDC(country_code='CRI', ndc_version='NDC 2025–2035',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Mangroves', 'Peatlands'],
                       conditional_ecosystems=[],
                       target_type='Unconditional', domestic_pricing='Carbon Tax', market_status='Operational'),
            CountryNDC(country_code='BLZ', ndc_version='Updated (2021)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Mangroves', 'Seagrass'],
                       conditional_ecosystems=[],
                       target_type='Unconditional', domestic_pricing='Carbon Market Regs', market_status='Operational'),
            CountryNDC(country_code='SGP', ndc_version='Updated (2022)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Coastal'],
                       conditional_ecosystems=[],
                       target_type='Unconditional', domestic_pricing='Carbon Tax', market_status='Operational'),
            CountryNDC(country_code='NOR', ndc_version='Updated (2022)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Kelp', 'Seagrass'],
                       conditional_ecosystems=[],
                       target_type='Unconditional', domestic_pricing='Carbon Tax', market_status='Operational'),
            CountryNDC(country_code='CAN', ndc_version='NDC 3.0 (2025)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Coastal ecosystems'],
                       conditional_ecosystems=[],
                       target_type='Unconditional', domestic_pricing='Output-Based Pricing', market_status='Operational'),
            CountryNDC(country_code='MEX', ndc_version='NDC 3.0 (2025)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Mangroves'],
                       conditional_ecosystems=['Mangroves'],
                       target_type='Both', domestic_pricing='ETS (pilot)', market_status='Operational / Pilot'),
            CountryNDC(country_code='CHL', ndc_version='Updated (2020)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Coastal wetlands'],
                       conditional_ecosystems=[],
                       target_type='Unconditional', domestic_pricing='Carbon Tax', market_status='Operational'),
            CountryNDC(country_code='EUU', ndc_version='NDC 3.0 (2025)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Coastal wetlands'],
                       conditional_ecosystems=[],
                       target_type='Unconditional', domestic_pricing='EU ETS', market_status='Operational'),
            CountryNDC(country_code='FJI', ndc_version='Updated (2020)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Mangroves', 'Seagrass'],
                       conditional_ecosystems=['Mangroves', 'Seagrass'],
                       target_type='Conditional', domestic_pricing='None', market_status='No market'),
            CountryNDC(country_code='BGD', ndc_version='Updated (2021)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Mangroves'],
                       conditional_ecosystems=['Mangroves'],
                       target_type='Both', domestic_pricing='None', market_status='No market'),
            CountryNDC(country_code='THA', ndc_version='Updated (2022)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Mangroves'],
                       conditional_ecosystems=['Mangroves'],
                       target_type='Both', domestic_pricing='Carbon Tax (planned)', market_status='Planned'),
            CountryNDC(country_code='ZAF', ndc_version='Updated (2021)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Coastal wetlands'],
                       conditional_ecosystems=['Coastal wetlands'],
                       target_type='Both', domestic_pricing='Carbon Tax', market_status='Operational'),
            CountryNDC(country_code='BHS', ndc_version='Updated (2022)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Mangroves', 'Seagrass'],
                       conditional_ecosystems=[],
                       target_type='Unconditional', domestic_pricing='Carbon Credit Act', market_status='Operational'),
            CountryNDC(country_code='MDV', ndc_version='Updated (2020)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Corals', 'Mangroves'],
                       conditional_ecosystems=['Corals', 'Mangroves'],
                       target_type='Both', domestic_pricing='None', market_status='No market'),
            CountryNDC(country_code='PLW', ndc_version='NDC 3.0 (2026)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Mangroves', 'Seagrass'],
                       conditional_ecosystems=[],
                       target_type='Unconditional', domestic_pricing='None', market_status='No market'),
            CountryNDC(country_code='GAB', ndc_version='NDC 3.0 (2025)',
                       blue_carbon_included=True,
                       unconditional_ecosystems=['Mangroves'],
                       conditional_ecosystems=[],
                       target_type='Unconditional', domestic_pricing='None', market_status='No market'),
        ]
        db.session.add_all(ndcs)

        # ── Carbon Markets ────────────────────────────────────────────────────

        carbon_markets = [
            CountryCarbonMarket(country_code='IDN', market_status='Active ETS', price_range_min=3.0, price_range_max=6.0, currency='USD'),
            CountryCarbonMarket(country_code='KEN', market_status='In Development', price_range_min=None, price_range_max=None, currency='USD'),
            CountryCarbonMarket(country_code='AUS', market_status='Operational', price_range_min=18.0, price_range_max=30.0, currency='USD'),
            CountryCarbonMarket(country_code='GBR', market_status='Operational', price_range_min=30.0, price_range_max=50.0, currency='GBP'),
            CountryCarbonMarket(country_code='JPN', market_status='Pilot / Operational', price_range_min=10.0, price_range_max=25.0, currency='USD'),
            CountryCarbonMarket(country_code='COL', market_status='Operational', price_range_min=5.0, price_range_max=10.0, currency='USD'),
            CountryCarbonMarket(country_code='NOR', market_status='Operational', price_range_min=50.0, price_range_max=90.0, currency='EUR'),
            CountryCarbonMarket(country_code='CAN', market_status='Operational', price_range_min=40.0, price_range_max=60.0, currency='CAD'),
            CountryCarbonMarket(country_code='EUU', market_status='Operational', price_range_min=55.0, price_range_max=85.0, currency='EUR'),
        ]
        db.session.add_all(carbon_markets)

        # ── Global Frameworks ─────────────────────────────────────────────────

        frameworks = [
            GlobalFramework(
                framework_id='FW-IDN-PR110',
                jurisdiction='Indonesia',
                title='PR 110/2025 — ITMO authorization pathway',
                description='Operationalizes Article 6.2 export via ministerial authorization. Blue carbon projects must comply with domestic registry requirements.',
                status_date='Dec 2025',
                category='blue',
            ),
            GlobalFramework(
                framework_id='FW-IDN-MOMAF',
                jurisdiction='Indonesia',
                title='MOMAF Reg 1/2025 — Blue carbon governance',
                description='Specifically addresses mangrove, seagrass, and tidal wetland carbon projects for domestic and international markets.',
                status_date='Jan 2025',
                category='teal',
            ),
            GlobalFramework(
                framework_id='FW-KEN-CCA',
                jurisdiction='Kenya',
                title='Climate Change Act amendments',
                description='Establishes registry framework for NDC-compatible carbon credits. Blue carbon pilot projects underway in coastal zones.',
                status_date='Nov 2024',
                category='orange',
            ),
        ]
        db.session.add_all(frameworks)

        # ── Global News ───────────────────────────────────────────────────────

        news = [
            GlobalNews(
                news_id='NEWS-IDX-001',
                country_code=None,
                title='IDXCarbon stabilizes at $4/tonne — below international benchmarks',
                body='Domestic pricing reflects early market stage. International blue carbon credits trade at $15-25/tonne premium.',
                date='Apr 2026',
                tags=['ID', 'MKT'],
            ),
            GlobalNews(
                news_id='NEWS-ICVCM-001',
                country_code=None,
                title='ICVCM CCP label increasingly required by institutional buyers',
                body='Major Article 6 buyers now requiring Core Carbon Principles label for transaction approval.',
                date='Mar 2026',
                tags=['GLOBAL'],
            ),
            GlobalNews(
                news_id='NEWS-KOR-001',
                country_code=None,
                title='South Korea absent from Article 6 readiness rankings',
                body='Transparency gap flagged by international observers. No public data on ITMO framework development.',
                date='Feb 2026',
                tags=['WARN'],
            ),
            GlobalNews(
                news_id='NEWS-IDN-VM0033-001',
                country_code='IDN',
                title='VM0033 deprecated in Indonesia — VM0053 now mandatory',
                body='VM0033 is no longer accepted in Indonesia since 2023. All new projects must use VM0053, paired with VMD0052 for additionality. Projects using VM0033 cannot receive ministerial authorization for ITMO export.',
                date='2023',
                tags=['WARN', 'IDN'],
            ),
        ]
        db.session.add_all(news)

        # ── Trade Trends ──────────────────────────────────────────────────────

        trade_trends = [
            GlobalTradeTrend(trend_id='TT-2021-MNG', year=2021, ecosystem_category='Mangrove Restoration', volume_traded_mt=0.8, average_price_usd=14.5, data_source='Ecosystem Marketplace 2022'),
            GlobalTradeTrend(trend_id='TT-2022-MNG', year=2022, ecosystem_category='Mangrove Restoration', volume_traded_mt=1.2, average_price_usd=16.0, data_source='Ecosystem Marketplace 2023'),
            GlobalTradeTrend(trend_id='TT-2023-MNG', year=2023, ecosystem_category='Mangrove Restoration', volume_traded_mt=1.9, average_price_usd=18.2, data_source='Ecosystem Marketplace 2024'),
            GlobalTradeTrend(trend_id='TT-2024-MNG', year=2024, ecosystem_category='Mangrove Restoration', volume_traded_mt=2.7, average_price_usd=21.0, data_source='Nature Finance 2025'),
            GlobalTradeTrend(trend_id='TT-2022-SEA', year=2022, ecosystem_category='Seagrass Conservation', volume_traded_mt=0.1, average_price_usd=22.0, data_source='Ecosystem Marketplace 2023'),
            GlobalTradeTrend(trend_id='TT-2023-SEA', year=2023, ecosystem_category='Seagrass Conservation', volume_traded_mt=0.3, average_price_usd=25.5, data_source='Ecosystem Marketplace 2024'),
            GlobalTradeTrend(trend_id='TT-2024-SEA', year=2024, ecosystem_category='Seagrass Conservation', volume_traded_mt=0.6, average_price_usd=28.0, data_source='Nature Finance 2025'),
            GlobalTradeTrend(trend_id='TT-2023-SAL', year=2023, ecosystem_category='Salt Marsh Restoration', volume_traded_mt=0.05, average_price_usd=19.0, data_source='Ecosystem Marketplace 2024'),
            GlobalTradeTrend(trend_id='TT-2024-SAL', year=2024, ecosystem_category='Salt Marsh Restoration', volume_traded_mt=0.12, average_price_usd=20.5, data_source='Nature Finance 2025'),
        ]
        db.session.add_all(trade_trends)

        # ── Country Layer — Indonesia ─────────────────────────────────────────

        metrics = [
            CountryMetric(country_code='IDN', metric_name='Mangrove extent', metric_value='3.44M ha', metric_subtext='largest in the world'),
            CountryMetric(country_code='IDN', metric_name='Domestic carbon price', metric_value='~$4/t', metric_subtext='IDXCarbon, late 2024'),
            CountryMetric(country_code='IDN', metric_name='Active methodology', metric_value='VM0053', metric_subtext='VM0033 deprecated 2023'),
            CountryMetric(country_code='IDN', metric_name='ITMO target', metric_value='2027', metric_subtext='official market entry goal'),
            # Kenya basic metrics
            CountryMetric(country_code='KEN', metric_name='Mangrove extent', metric_value='61,000 ha', metric_subtext='along Indian Ocean coast'),
            CountryMetric(country_code='KEN', metric_name='Active projects', metric_value='3', metric_subtext='VCM verified'),
        ]
        db.session.add_all(metrics)

        dimensions = [
            CountryDimension(
                country_code='IDN', dimension_id='i',
                label='I — Strategic', full_label='I — Strategic Considerations',
                gate='cleared', gate_text='✓ Gate cleared',
                description="Indonesia's 2nd NDC (2025) explicitly commits to Art.6.2 bilateral cooperation and Art.6.4 participation, with blue carbon ecosystems (mangroves 3.44M ha, seagrass) named as priority sectors. The national strategy defines both unconditional and conditional pathways, and IDXCarbon provides a domestic pricing anchor for ITMO benchmarking.",
            ),
            CountryDimension(
                country_code='IDN', dimension_id='ii',
                label='II — Legal', full_label='II — Legal Foundations & Governance',
                gate='cleared', gate_text='✓ Gate cleared',
                description="Ministry of Environment and Forestry (KLHK) is formally designated as Indonesia's Designated National Authority (DNA). Presidential Regulation No. 110/2025 governs the Corresponding Adjustment mechanism and ITMO authorization. MOMAF Regulation 1/2025 specifically addresses blue carbon ecosystems — mangroves and seagrass — for domestic and international carbon markets.",
            ),
            CountryDimension(
                country_code='IDN', dimension_id='iii',
                label='III — Institutional', full_label='III — Institutional Arrangements',
                gate='cleared', gate_text='✓ Gate cleared',
                description="KLHK's DNA office is operational with a dedicated carbon trading unit. Inter-ministerial coordination spans KLHK, Ministry of Finance, MOMAF, and Bappenas. IDXCarbon operates Indonesia's domestic ETS platform. The FPIC framework is mandatory for all blue carbon project areas, with community benefit-sharing required under regulation.",
            ),
            CountryDimension(
                country_code='IDN', dimension_id='iv',
                label='IV — Operational', full_label='IV — Operational Procedures',
                gate='cleared', gate_text='✓ Mostly cleared',
                description="Letter of Authorization (LoA) for ITMO export is regulated via MoF Regulation No. 6/2026. A Mutual Recognition Agreement (MRA) with Japan operationalizes accounting adjustments for bilateral Art.6.2 transactions. VM0053 is the mandatory methodology for all Indonesian blue carbon projects (VM0033 deprecated 2023).",
            ),
            CountryDimension(
                country_code='IDN', dimension_id='v',
                label='V — Infrastructure', full_label='V — Infrastructure',
                gate='progress', gate_text='→ Operational',
                description="Indonesia operates dual registries — SRN-PPI tracks NDC actions at sector level, while SRUK tracks granular carbon unit issuance, transfer, and retirement for Art.6. The national MRV system under KLHK includes satellite monitoring for mangrove extent. Indonesia's first Biennial Transparency Report (BTR1) was submitted in 2024, demonstrating transparency framework compliance.",
            ),
        ]
        db.session.add_all(dimensions)

        checklists = [
            # Dimension I — Strategic
            CountryChecklist(country_code='IDN', dimension_id='i', item_label='2nd NDC (2025) submitted — blue carbon explicitly included', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='i', item_label='Art.6.2 bilateral cooperation strategy active', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='i', item_label='Art.6.4 participation confirmed', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='i', item_label='Domestic carbon pricing: IDXCarbon ETS operational', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='i', item_label='CORSIA eligibility pathway assessed', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='i', item_label='ITMO export volume ceiling — Joint Ministerial Decision Jun 2026', status='partial'),
            # Dimension II — Legal
            CountryChecklist(country_code='IDN', dimension_id='ii', item_label='DNA designated: Ministry of Environment (KLHK)', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='ii', item_label='PR 110/2025: CA mechanism & ITMO authorization enacted', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='ii', item_label='MOMAF Reg 1/2025: Blue carbon governance framework', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='ii', item_label='LoA pathway legally established', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='ii', item_label='Revenue-sharing regulation in place', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='ii', item_label='Mangroves legally recognized for carbon credits', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='ii', item_label='Seagrass carbon framework: interim guidelines, standard pending', status='partial'),
            # Dimension III — Institutional
            CountryChecklist(country_code='IDN', dimension_id='iii', item_label='DNA office functions: KLHK carbon trading unit active', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='iii', item_label='Inter-agency coordination: KLHK, MoF, MOMAF, Bappenas', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='iii', item_label='IDXCarbon: Domestic ETS exchange operational', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='iii', item_label='FPIC framework: mandatory for blue carbon project areas', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='iii', item_label='Community benefit-sharing: regulation in place', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='iii', item_label='Local VVB capacity: limited — international VVBs engaged', status='partial'),
            # Dimension IV — Operational
            CountryChecklist(country_code='IDN', dimension_id='iv', item_label='LoA process: Regulated under MoF Regulation No. 6/2026', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='iv', item_label='ITMO authorization: Ministerial approval pathway defined', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='iv', item_label='Corresponding Adjustment: PR 110/2025 procedure established', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='iv', item_label='MRA with Japan: Mutual Recognition Agreement for accounting', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='iv', item_label='Approved methodology: VM0053 (VMD0052 for additionality)', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='iv', item_label='Sector ITMO supply allocation ceiling: Jun 2026 deadline', status='partial'),
            # Dimension V — Infrastructure
            CountryChecklist(country_code='IDN', dimension_id='v', item_label='SRUK registry: Art.6 unit registry launched & operational', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='v', item_label='SRN-PPI registry: NDC progress tracking operational', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='v', item_label='National MRV system: KLHK system active', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='v', item_label='Satellite monitoring: Mangrove extent coverage', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='v', item_label='BTR1 submitted (2024): Transparency framework met', status='yes'),
            CountryChecklist(country_code='IDN', dimension_id='v', item_label='Art.6.4 unit registration pathway: In progress', status='partial'),
        ]
        db.session.add_all(checklists)

        ndc_targets = [
            CountryNDCTarget(
                country_code='IDN',
                target_type='Deforestation prevention',
                target_title='Preventing mangrove loss',
                unconditional_val='111K ha', unconditional_pct=70,
                conditional_val='158K ha', conditional_pct=100,
            ),
            CountryNDCTarget(
                country_code='IDN',
                target_type='Degradation prevention',
                target_title='Protecting mangrove quality',
                unconditional_val='63K ha', unconditional_pct=40,
                conditional_val='88K ha', conditional_pct=56,
            ),
            CountryNDCTarget(
                country_code='IDN',
                target_type='Ecosystem restoration',
                target_title='Active mangrove replanting',
                unconditional_val='17.2K ha', unconditional_pct=11,
                conditional_val='36.8K ha', conditional_pct=23,
            ),
            # Kenya
            CountryNDCTarget(
                country_code='KEN',
                target_type='Conservation',
                target_title='Coastal mangrove conservation',
                unconditional_val='61K ha', unconditional_pct=50,
                conditional_val='61K ha', conditional_pct=100,
            ),
        ]
        db.session.add_all(ndc_targets)

        institutions = [
            # Indonesia (6 cards from IndonesiaSection.tsx)
            CountryInstitution(
                country_code='IDN', role='Governing framework', name='PR 110/2025',
                description='Replaces PR 98/2021. Covers CA mechanism, ITMO authorization, SRUK registry, and carbon allocation ceilings for 2026–30.',
            ),
            CountryInstitution(
                country_code='IDN', role='Marine authority', name='MOMAF Reg 1/2025',
                description='Governs blue carbon ecosystems (mangroves, seagrass) for domestic & international markets via carbon trading and RBP.',
            ),
            CountryInstitution(
                country_code='IDN', role='Registry systems', name='SRN-PPI + SRUK',
                description='Dual-layer registry: SRN-PPI tracks NDC actions, SRUK tracks granular carbon unit issuance, transfer, and retirement.',
            ),
            CountryInstitution(
                country_code='IDN', role='Carbon certificate', name='SPE-GRK / SPEI',
                description="Indonesia's official GHG reduction certificate. Used across domestic compliance, international trading, RBP, and Art.6.4.",
            ),
            CountryInstitution(
                country_code='IDN', role='Domestic pricing', name='NEK / IDXCarbon ETS',
                description='Hybrid: cap-and-trade (PTBAE-PU) + carbon tax. Expanding from coal power to other sectors including blue carbon.',
            ),
            CountryInstitution(
                country_code='IDN', role='Supply ceiling', name='Carbon allocation 2026',
                description='Sector-specific ITMO supply limits due by Joint Ministerial Decision in June 2026 for the 2026–30 period.',
            ),
            # Kenya
            CountryInstitution(
                country_code='KEN', role='Designated National Authority', name='NEMA',
                description='National Environment Management Authority acts as DNA under the Climate Change Act 2023 amendment.',
            ),
        ]
        db.session.add_all(institutions)

        eco_recognitions = [
            EcosystemRecognition(country_code='IDN', ecosystem_type='Mangroves', recognition_status='Established', details='Fully recognized under national law with legally defined emission factors and MRV protocols.'),
            EcosystemRecognition(country_code='IDN', ecosystem_type='Seagrass', recognition_status='Emerging', details='Interim guidelines published; national standard pending finalization under MOMAF.'),
            EcosystemRecognition(country_code='IDN', ecosystem_type='Tidal Wetlands', recognition_status='Emerging', details='Covered under MOMAF Reg 1/2025 alongside mangroves and seagrass.'),
            EcosystemRecognition(country_code='KEN', ecosystem_type='Mangroves', recognition_status='Established', details='Recognized under national REDD+ framework and AFOLU accounting.'),
            EcosystemRecognition(country_code='KEN', ecosystem_type='Seagrass', recognition_status='Emerging', details='Pilot recognition under national blue carbon registry program.'),
        ]
        db.session.add_all(eco_recognitions)

        agreements = [
            CountryAgreement(
                agreement_id='AGR-IDN-VERRA-001',
                host_country_code='IDN',
                agreement_type='Special Agreement',
                partner_entity='Verra',
                status='Active',
                date_signed='2022-05-01',
                reference_link='https://verra.org/verra-and-indonesia-sign-mou-on-carbon-markets/',
            ),
            CountryAgreement(
                agreement_id='AGR-IDN-WB-001',
                host_country_code='IDN',
                agreement_type='Article 6 Bilateral Tracker',
                partner_entity='World Bank (cooperative approaches)',
                status='Active',
                date_signed=None,
                reference_link='https://carbonpricingdashboard.worldbank.org/credits/cooperative-approaches',
            ),
            CountryAgreement(
                agreement_id='AGR-IDN-JPN-001',
                host_country_code='IDN',
                agreement_type='Article 6.2 Cooperative Approach',
                partner_entity='Japan (MRA for accounting)',
                status='Authorized',
                date_signed='2024-08-20',
                reference_link='https://www.meti.go.jp/',
            ),
            CountryAgreement(
                agreement_id='AGR-IDN-SGP-001',
                host_country_code='IDN',
                agreement_type='Article 6.2 Cooperative Approach',
                partner_entity='Singapore',
                status='MoU Signed',
                date_signed='2023-11-10',
                reference_link='https://www.nea.gov.sg/',
            ),
            CountryAgreement(
                agreement_id='AGR-KEN-WB-001',
                host_country_code='KEN',
                agreement_type='Special Agreement',
                partner_entity='World Bank (REDD+)',
                status='Active',
                date_signed='2021-09-15',
                reference_link='https://www.worldbank.org/',
            ),
        ]
        db.session.add_all(agreements)

        # ── Project Layer ─────────────────────────────────────────────────────

        projects = [
            Project(
                project_id='PRJ-KEN-MIKOKO',
                project_name='Mikoko Pamoja',
                location='Kenya, Gazi Bay',
                status='Active',
                tags=['Active', 'VCS', 'Art.6'],
                ecosystem_type='Mangroves',
                area='117',
                vintage='2024',
                methodology='VM0033',
                credits='2,458',
                registry='Verra VCS',
                description='Community-based mangrove conservation and restoration. First blue carbon project in Africa. Strong social co-benefits and Art.6 pilot candidate.',
                checks=['Community ownership verified', 'MRV systems operational', 'Art.6 pre-approval pathway'],
                price=None,
                rating_agency=None,
                rating_score=None,
                status_category='Active',
            ),
            Project(
                project_id='PRJ-IDN-TAHURA',
                project_name='Tahura Ngurah Rai Mangrove',
                location='Indonesia, Bali',
                status='Active',
                tags=['Active', 'VM0053'],
                ecosystem_type='Mangroves',
                area='1,373',
                vintage='2025',
                methodology='VM0053',
                credits='—',
                registry='SRN Indonesia / IDXCarbon',
                description="Large-scale mangrove protection and restoration in Bali. Aligned with Indonesia's domestic registry and ITMO pathway under PR 110/2025. Source: IDX Carbon Exchange (idxcarbon.co.id).",
                checks=['SRN registered', 'VM0053 compliance', 'MOMAF approval pending'],
                price=None,
                rating_agency=None,
                rating_score=None,
                status_category='Active',
            ),
            Project(
                project_id='PRJ-COL-CISPATA',
                project_name='Cispatá Bay Restoration',
                location='Colombia, Caribbean',
                status='Pipeline',
                tags=['Pipeline', 'VCS'],
                ecosystem_type='Mangroves',
                area='11,084',
                vintage='—',
                methodology='VM0053',
                credits='—',
                registry='Verra VCS',
                description='One of the largest blue carbon projects in development. Combines mangrove restoration with seagrass protection. REDD+ experience applied to blue carbon.',
                checks=['Baseline assessment complete', 'Community consultation ongoing', 'Registry pre-approval'],
                price=None,
                rating_agency=None,
                rating_score=None,
                status_category='Pipeline',
            ),
            Project(
                project_id='PRJ-IND-SUNDARBANS',
                project_name='Livelihoods Sundarbans',
                location='India, West Bengal',
                status='Active',
                tags=['Active'],
                ecosystem_type='Mangroves',
                area='5,880',
                vintage='2023',
                methodology='VM0033',
                credits='18,240',
                registry='Plan Vivo',
                description="Mangrove restoration with strong livelihood focus. Limited Art.6 readiness due to India's early-stage national framework.",
                checks=['Plan Vivo certified', 'Social impact verified', 'Art.6 pathway unclear'],
                price=None,
                rating_agency=None,
                rating_score=None,
                status_category='Active',
            ),
            Project(
                project_id='PRJ-IDN-WAKATOBI',
                project_name='Wakatobi Seagrass Conservation',
                location='Indonesia, Southeast Sulawesi',
                status='Pipeline',
                tags=['Pipeline', 'VCS'],
                ecosystem_type='Seagrass',
                area='8,200',
                vintage='—',
                methodology='VM0033',
                credits='—',
                registry='Verra VCS',
                description="Early-stage seagrass conservation project in Wakatobi National Park, one of the world's most biodiverse marine areas. Pending national seagrass MRV standard approval under MOMAF. Carbon potential informed by Indonesian seagrass soil carbon datasets.",
                checks=['Feasibility study complete', 'Awaiting national seagrass MRV standard', 'MOMAF engagement initiated'],
                price=None,
                rating_agency=None,
                rating_score=None,
                status_category='Pipeline',
            ),
            Project(
                project_id='PRJ-PHL-PALAWAN',
                project_name='Palawan Seagrass Blue Carbon Pilot',
                location='Philippines, Palawan',
                status='Pipeline',
                tags=['Pipeline'],
                ecosystem_type='Seagrass',
                area='5,200',
                vintage='—',
                methodology='VM0033',
                credits='—',
                registry='Verra VCS',
                description="Pilot project aiming to generate the Philippines' first seagrass carbon credits, in partnership with IUCN and local government units. Informed by global seagrass carbon potential data (Alongi et al. 2016).",
                checks=['IUCN partnership confirmed', 'Baseline mapping underway', 'National framework pending'],
                price=None,
                rating_agency=None,
                rating_score=None,
                status_category='Pipeline',
            ),
            Project(
                project_id='PRJ-USA-CHESAPEAKE',
                project_name='Chesapeake Bay Tidal Marsh Restoration',
                location='USA, Virginia',
                status='Active',
                tags=['Active'],
                ecosystem_type='Tidal Marshes',
                area='3,400',
                vintage='2023',
                methodology='VM0033',
                credits='12,800',
                registry='Gold Standard',
                description='Large-scale tidal saltmarsh restoration project combining hydrological management with community resilience. Generating verified Gold Standard credits with strong co-benefits for coastal protection and waterfowl habitat.',
                checks=['Gold Standard certified', 'Hydrological restoration complete', 'SD co-benefits verified'],
                price=None,
                rating_agency=None,
                rating_score=None,
                status_category='Active',
            ),
            Project(
                project_id='PRJ-KEN-COAST',
                project_name='Kenya Coast Tidal Wetland',
                location='Kenya, Mombasa County',
                status='Pipeline',
                tags=['Pipeline', 'Art.6'],
                ecosystem_type='Tidal Marshes',
                area='2,100',
                vintage='—',
                methodology='VM0033',
                credits='—',
                registry='Verra VCS',
                description="Tidal wetland restoration along Kenya's Indian Ocean coast, co-developed with local fishing communities. Art.6 pilot candidate under Kenya's emerging carbon market regulations.",
                checks=['Community FPIC process initiated', 'Baseline assessment underway', 'Art.6 pre-feasibility complete'],
                price=None,
                rating_agency=None,
                rating_score=None,
                status_category='Pipeline',
            ),
        ]
        db.session.add_all(projects)

        # ── Methodologies ─────────────────────────────────────────────────────

        methodologies = [
            Methodology(methodology_id='VM0053', standard='Verra (VCS)',
                        description='Restoration & conservation of tidal wetlands and seagrasses. Current mandatory standard for Indonesia.',
                        ecosystem_focus='Mangroves, seagrasses, tidal wetlands',
                        activity_type='Restoration & conservation (current)', recognition='International', is_current=True),
            Methodology(methodology_id='VM0033', standard='Verra (VCS)',
                        description='Methodology for tidal wetland and seagrass restoration. Legacy — deprecated in Indonesia since 2023.',
                        ecosystem_focus='Mangroves, salt marshes, seagrasses',
                        activity_type='Restoration & creation (legacy)', recognition='International', is_current=False),
            Methodology(methodology_id='VM0007', standard='Verra (VCS)',
                        description='REDD+ methodology for avoided deforestation applicable to mangrove and wetland conservation.',
                        ecosystem_focus='Mangroves, tidal wetlands, peatlands',
                        activity_type='REDD+ / Avoided loss', recognition='International', is_current=True),
            Methodology(methodology_id='GS-SMM', standard='Gold Standard',
                        description='Gold Standard sustainable mangrove management methodology emphasizing community co-benefits.',
                        ecosystem_focus='Mangroves',
                        activity_type='Sustainable management', recognition='International', is_current=True),
            Methodology(methodology_id='PV-COASTAL', standard='Plan Vivo',
                        description='Community-led coastal ecosystem restoration under the Plan Vivo standard.',
                        ecosystem_focus='Mangroves, seagrasses, salt marshes',
                        activity_type='Community-led restoration', recognition='International', is_current=True),
            Methodology(methodology_id='AR-AM0014', standard='CDM (UNFCCC)',
                        description='CDM afforestation and reforestation methodology applicable to mangrove planting activities.',
                        ecosystem_focus='Mangroves',
                        activity_type='Afforestation & reforestation', recognition='International', is_current=True),
            Methodology(methodology_id='ACR-RESTORATION', standard='American Carbon Registry',
                        description='U.S. coastal and deltaic wetland restoration via hydrological management.',
                        ecosystem_focus='U.S. coastal/deltaic wetlands',
                        activity_type='Hydrological management', recognition='Primarily domestic', is_current=True),
            Methodology(methodology_id='AUS-TIDAL', standard='Australia ACCU',
                        description='Australian methodology for tidal re-introduction to restore mangroves and salt marshes.',
                        ecosystem_focus='Mangroves, salt marshes',
                        activity_type='Tidal re-introduction', recognition='Primarily domestic', is_current=True),
            Methodology(methodology_id='JCM-J-BLUE', standard='Japan JCM',
                        description="Japan's Joint Crediting Mechanism blue carbon methodology for marine forestation.",
                        ecosystem_focus='Kelp, seaweed, seagrass',
                        activity_type='Marine forestation', recognition='Primarily domestic', is_current=True),
            Methodology(methodology_id='CCER-14-002', standard='China CCER',
                        description='China CCER methodology for mangrove afforestation activities.',
                        ecosystem_focus='Mangroves',
                        activity_type='Mangrove afforestation', recognition='Primarily domestic', is_current=True),
        ]
        db.session.add_all(methodologies)

        # ── Ecosystem Tiers ───────────────────────────────────────────────────

        ecosystem_tiers = [
            EcosystemTier(
                tier_name='Tier 1 — Established',
                ecosystems='Mangroves · Salt Marshes · Seagrass',
                ghg_impact='High GHG impact & long-term storage',
                long_term_storage='Centuries to millennia',
                ipcc_accounting='Included in national inventories',
                vcm_readiness='High — proven MRV methodology stack',
            ),
            EcosystemTier(
                tier_name='Tier 2 — Emerging',
                ecosystems='Tidal Flats · Benthic Sediments · Macroalgae',
                ghg_impact='Uncertain sequestration rates',
                long_term_storage='Decades (variable)',
                ipcc_accounting='Not IPCC-included (tidal flats, macroalgae)',
                vcm_readiness='Low–Medium — weak / limited MRV systems',
            ),
            EcosystemTier(
                tier_name='Tier 3 — Nascent',
                ecosystems='Coral Reefs · Oyster Reefs · Phytoplankton · Marine Fauna',
                ghg_impact='Low or negative net GHG impact',
                long_term_storage='Short-term or negligible',
                ipcc_accounting='Not IPCC-included',
                vcm_readiness='Not VCM eligible — no approved methodology',
            ),
        ]
        db.session.add_all(ecosystem_tiers)

        db.session.commit()
        print('✓ Database seeded successfully.')
        print(f'  Countries:      {len(countries)}')
        print(f'  NDC records:    {len(ndcs)}')
        print(f'  Ticker items:   {len(tickers)}')
        print(f'  Global stats:   {len(stats)}')
        print(f'  Frameworks:     {len(frameworks)}')
        print(f'  News items:     {len(news)}')
        print(f'  Projects:       {len(projects)}')
        print(f'  Methodologies:  {len(methodologies)}')
        print(f'  Eco tiers:      {len(ecosystem_tiers)}')


if __name__ == '__main__':
    seed()
