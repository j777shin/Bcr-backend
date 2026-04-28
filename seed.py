"""
Run once to populate the database with sample BCR data.
Usage: python seed.py
"""
from app import create_app, db
from app.models.global_layer import Country, CountryNDC, CountryCarbonMarket, GlobalFramework, GlobalNews, GlobalTradeTrend
from app.models.country_layer import CountryMetric, CountryChecklist, CountryNDCTarget, CountryInstitution, EcosystemRecognition, CountryAgreement
from app.models.project_layer import Project, Methodology, EcosystemTier


def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # ── Global Layer ─────────────────────────────────────────────────────

        countries = [
            Country(
                country_code='IDN',
                country_name='Indonesia',
                flag_emoji='🇮🇩',
                readiness_score=78,
                readiness_tier='High readiness',
                context_note='Art.6.2 · Art.6.4',
                dim_a_legal=82,
                dim_b_tech=75,
                dim_c_comm=80,
                dim_d_social=70,
                dim_e_reg=85,
            ),
            Country(
                country_code='KEN',
                country_name='Kenya',
                flag_emoji='🇰🇪',
                readiness_score=61,
                readiness_tier='Developing',
                context_note='Art.6.2',
                dim_a_legal=65,
                dim_b_tech=58,
                dim_c_comm=60,
                dim_d_social=62,
                dim_e_reg=55,
            ),
            Country(
                country_code='PHL',
                country_name='Philippines',
                flag_emoji='🇵🇭',
                readiness_score=54,
                readiness_tier='Developing',
                context_note='Art.6.4',
                dim_a_legal=58,
                dim_b_tech=52,
                dim_c_comm=55,
                dim_d_social=50,
                dim_e_reg=48,
            ),
            Country(
                country_code='BGD',
                country_name='Bangladesh',
                flag_emoji='🇧🇩',
                readiness_score=38,
                readiness_tier='Early stage',
                context_note=None,
                dim_a_legal=40,
                dim_b_tech=35,
                dim_c_comm=38,
                dim_d_social=42,
                dim_e_reg=30,
            ),
            Country(
                country_code='SLB',
                country_name='Solomon Islands',
                flag_emoji='🇸🇧',
                readiness_score=None,
                readiness_tier='No data',
                context_note=None,
                dim_a_legal=None,
                dim_b_tech=None,
                dim_c_comm=None,
                dim_d_social=None,
                dim_e_reg=None,
            ),
        ]
        db.session.add_all(countries)
        db.session.flush()

        ndcs = [
            CountryNDC(
                country_code='IDN',
                ndc_version='Second NDC (2025)',
                blue_carbon_included=True,
                unconditional_ecosystems=['Mangroves', 'Seagrass'],
                conditional_ecosystems=['Salt Marshes'],
                unconditional_target_desc='Reduce emissions by 31.89% by 2030 through conservation of 3.44M ha of mangroves.',
                conditional_target_desc='Reduce emissions by 43.20% with international support, including blue carbon restoration.',
                intervention_type='Both',
                target_type='Both',
                targets='31.89% unconditional / 43.20% conditional by 2030',
                domestic_pricing='ETS & Carbon Tax',
                market_status='Operational',
            ),
            CountryNDC(
                country_code='KEN',
                ndc_version='Updated NDC (2020)',
                blue_carbon_included=True,
                unconditional_ecosystems=['Mangroves'],
                conditional_ecosystems=['Seagrass', 'Salt Marshes'],
                unconditional_target_desc='Unconditional 32% emission reduction by 2030 with mangrove conservation as a co-benefit.',
                conditional_target_desc='Additional 50% reduction conditional on international finance.',
                intervention_type='Mitigation',
                target_type='Both',
                targets='32% unconditional / 50% conditional by 2030',
                domestic_pricing='None',
                market_status='In Development',
            ),
            CountryNDC(
                country_code='PHL',
                ndc_version='Updated NDC (2021)',
                blue_carbon_included=True,
                unconditional_ecosystems=['Mangroves'],
                conditional_ecosystems=['Seagrass'],
                unconditional_target_desc='75% emission reduction from 2020 baseline; blue carbon included under AFOLU sector.',
                conditional_target_desc='Full 75% contingent on technology transfer and climate finance.',
                intervention_type='Both',
                target_type='Both',
                targets='75% total by 2030 (2.71% unconditional)',
                domestic_pricing='None',
                market_status='In Development',
            ),
        ]
        db.session.add_all(ndcs)

        carbon_markets = [
            CountryCarbonMarket(country_code='IDN', market_status='Active ETS', price_range_min=5.0, price_range_max=12.0, currency='USD'),
            CountryCarbonMarket(country_code='KEN', market_status='In Development', price_range_min=3.0, price_range_max=8.0, currency='USD'),
            CountryCarbonMarket(country_code='PHL', market_status='In Development', price_range_min=None, price_range_max=None, currency='USD'),
        ]
        db.session.add_all(carbon_markets)

        frameworks = [
            GlobalFramework(
                framework_id='FW-IDN-001',
                jurisdiction='Indonesia · Presidential Regulation',
                title='PR 110/2025',
                description='Presidential Regulation 110/2025 establishes the legal basis for blue carbon project registration, MRV requirements, and Article 6 authorization within Indonesia.',
                status_date='Enacted Feb 2025',
                category='blue',
            ),
            GlobalFramework(
                framework_id='FW-VERRA-001',
                jurisdiction='Verra · Global Standard',
                title='VM0033 v2.1',
                description='Verra Methodology VM0033 covers tidal wetland and seagrass restoration with updated emission factor tables and permanence requirements.',
                status_date='Updated Jan 2024',
                category='green',
            ),
            GlobalFramework(
                framework_id='FW-UNFCCC-001',
                jurisdiction='UNFCCC · Article 6',
                title='Paris Agreement Art. 6.4 Mechanism',
                description='The Article 6.4 Supervisory Body approved carbon removal methodologies including blue carbon in November 2024, opening a new compliance pathway.',
                status_date='Approved Nov 2024',
                category='teal',
            ),
            GlobalFramework(
                framework_id='FW-KEN-001',
                jurisdiction='Kenya · Climate Change Act',
                title='Kenya Climate Change Act 2023 Amendment',
                description='Amendment introduces a carbon market regulatory framework and designates the National Environment Management Authority (NEMA) as the designated national authority.',
                status_date='Enacted Mar 2023',
                category='orange',
            ),
        ]
        db.session.add_all(frameworks)

        news = [
            GlobalNews(
                news_id='NEWS-001',
                title='Indonesia issues first Art.6.2 authorization for blue carbon credits',
                body='Indonesia\'s Ministry of Environment and Forestry issued its first bilateral authorization under Article 6.2 of the Paris Agreement for mangrove carbon credits, marking a milestone in the country\'s blue carbon market.',
                date='2025-03-15',
                tags=['Authorization', 'Art.6.2', 'Indonesia'],
            ),
            GlobalNews(
                news_id='NEWS-002',
                title='IPCC releases updated emission factors for seagrass ecosystems',
                body='The IPCC Wetlands Supplement has been updated with new emission factor tables for seagrass meadows, increasing confidence in MRV for blue carbon projects in tropical regions.',
                date='2025-02-20',
                tags=['Methodology', 'IPCC', 'Seagrass'],
            ),
            GlobalNews(
                news_id='NEWS-003',
                title='Alert: Verra suspends two mangrove projects pending MRV audit',
                body='Verra has temporarily suspended credit issuance for two mangrove conservation projects in Southeast Asia pending a third-party MRV audit following satellite monitoring discrepancies.',
                date='2025-01-10',
                tags=['Alert', 'Verra', 'MRV'],
            ),
            GlobalNews(
                news_id='NEWS-004',
                title='Kenya launches national blue carbon registry pilot',
                body='The Kenya Carbon Markets Taskforce launched a pilot national registry for blue carbon assets, covering mangrove projects along the Kenyan coast, in partnership with the World Bank REDD+ program.',
                date='2024-12-05',
                tags=['Registry', 'Kenya', 'Pilot'],
            ),
        ]
        db.session.add_all(news)

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

        # ── Country Layer ─────────────────────────────────────────────────────

        metrics = [
            # Indonesia
            CountryMetric(country_code='IDN', metric_name='Mangrove extent', metric_value='3.44M ha', metric_subtext='largest in the world', dimension_id='A', dimension_name='Legal & governance', gate_status='Gate cleared', description='Indonesia holds the world\'s largest mangrove area, providing a critical foundation for blue carbon project development.'),
            CountryMetric(country_code='IDN', metric_name='MRV capacity', metric_value='National system', metric_subtext='KLHK operational', dimension_id='B', dimension_name='Technical & MRV', gate_status='Gate cleared', description='Indonesia\'s Ministry of Environment and Forestry operates a national MRV system with satellite monitoring integration.'),
            CountryMetric(country_code='IDN', metric_name='Active projects', metric_value='12', metric_subtext='VCM + Art.6', dimension_id='C', dimension_name='Commercial', gate_status='Gate cleared', description='Twelve active projects across VCM and Article 6 pathways, with combined pipeline exceeding 5M tCO2e annually.'),
            CountryMetric(country_code='IDN', metric_name='Community benefit', metric_value='85%', metric_subtext='projects with FPIC', dimension_id='D', dimension_name='Social & community', gate_status='Gate cleared', description='85% of registered projects include FPIC processes and community benefit-sharing arrangements.'),
            CountryMetric(country_code='IDN', metric_name='Registry status', metric_value='Operational', metric_subtext='SRN integrated', dimension_id='E', dimension_name='Registry', gate_status='Gate cleared', description='Indonesia\'s national registry (SRN) is operational and linked to the UNFCCC transparency framework.'),
            # Kenya
            CountryMetric(country_code='KEN', metric_name='Mangrove extent', metric_value='61,000 ha', metric_subtext='along Indian Ocean coast', dimension_id='A', dimension_name='Legal & governance', gate_status='Gate cleared', description='Kenya\'s mangroves are concentrated along the coast in Lamu, Kilifi, and Mombasa counties.'),
            CountryMetric(country_code='KEN', metric_name='MRV capacity', metric_value='Developing', metric_subtext='pilot systems active', dimension_id='B', dimension_name='Technical & MRV', gate_status='Pending', description='Kenya is developing national MRV capacity with support from the World Bank and GIZ.'),
        ]
        db.session.add_all(metrics)

        checklists = [
            # Indonesia - Dimension A
            CountryChecklist(country_code='IDN', dimension_id='A', item_label='DNA active & capable', status='Yes'),
            CountryChecklist(country_code='IDN', dimension_id='A', item_label='Blue carbon legally recognized', status='Yes'),
            CountryChecklist(country_code='IDN', dimension_id='A', item_label='Article 6 authorization framework enacted', status='Yes'),
            CountryChecklist(country_code='IDN', dimension_id='A', item_label='Land tenure clarity for project areas', status='Partial'),
            # Indonesia - Dimension B
            CountryChecklist(country_code='IDN', dimension_id='B', item_label='National MRV system operational', status='Yes'),
            CountryChecklist(country_code='IDN', dimension_id='B', item_label='Satellite monitoring coverage', status='Yes'),
            CountryChecklist(country_code='IDN', dimension_id='B', item_label='Validated emission factors', status='Yes'),
            CountryChecklist(country_code='IDN', dimension_id='B', item_label='Third-party verification capacity', status='Partial'),
            # Indonesia - Dimension E
            CountryChecklist(country_code='IDN', dimension_id='E', item_label='National registry operational', status='Yes'),
            CountryChecklist(country_code='IDN', dimension_id='E', item_label='UNFCCC transparency linkage', status='Yes'),
            CountryChecklist(country_code='IDN', dimension_id='E', item_label='Double-counting prevention mechanism', status='Yes'),
            # Kenya - Dimension A
            CountryChecklist(country_code='KEN', dimension_id='A', item_label='DNA active & capable', status='Yes'),
            CountryChecklist(country_code='KEN', dimension_id='A', item_label='Blue carbon legally recognized', status='Partial'),
            CountryChecklist(country_code='KEN', dimension_id='A', item_label='Article 6 authorization framework enacted', status='No'),
            CountryChecklist(country_code='KEN', dimension_id='A', item_label='Land tenure clarity for project areas', status='Partial'),
        ]
        db.session.add_all(checklists)

        ndc_targets = [
            CountryNDCTarget(country_code='IDN', target_type='Deforestation prevention', target_title='Mangrove deforestation halt', unconditional_val='1.72M tCO2e/yr', unconditional_pct=60, conditional_val='2.58M tCO2e/yr', conditional_pct=90),
            CountryNDCTarget(country_code='IDN', target_type='Restoration', target_title='Degraded mangrove restoration', unconditional_val='180,000 ha', unconditional_pct=45, conditional_val='400,000 ha', conditional_pct=100),
            CountryNDCTarget(country_code='KEN', target_type='Deforestation prevention', target_title='Coastal mangrove conservation', unconditional_val='0.34M tCO2e/yr', unconditional_pct=50, conditional_val='0.68M tCO2e/yr', conditional_pct=100),
        ]
        db.session.add_all(ndc_targets)

        institutions = [
            CountryInstitution(country_code='IDN', role='Designated National Authority', name='Ministry of Environment and Forestry (KLHK)', description='Responsible for authorizing blue carbon projects under Article 6 and managing the national MRV system.'),
            CountryInstitution(country_code='IDN', role='Registry Operator', name='SRN (National Climate Registry)', description='Hosts the national registry for all carbon credit transactions and tracks corresponding adjustments.'),
            CountryInstitution(country_code='IDN', role='Standard Body', name='Indonesia Carbon Exchange (IDXCarbon)', description='Operates the domestic carbon trading platform integrated with the national ETS.'),
            CountryInstitution(country_code='KEN', role='Designated National Authority', name='National Environment Management Authority (NEMA)', description='Acts as DNA for international carbon market activities under the Climate Change Act 2023 amendment.'),
            CountryInstitution(country_code='KEN', role='Policy Lead', name='Kenya Carbon Markets Taskforce', description='Inter-ministerial body coordinating Kenya\'s carbon market policy and registry pilot.'),
        ]
        db.session.add_all(institutions)

        eco_recognitions = [
            EcosystemRecognition(country_code='IDN', ecosystem_type='Mangroves', recognition_status='Established', details='Mangroves are fully recognized under national law as carbon sinks with legally defined emission factors and MRV protocols.'),
            EcosystemRecognition(country_code='IDN', ecosystem_type='Seagrass', recognition_status='Emerging', details='Seagrass recognition is progressing; KLHK has published interim guidelines pending national standard finalization.'),
            EcosystemRecognition(country_code='IDN', ecosystem_type='Salt Marshes', recognition_status='Not Recognized', details='Salt marshes have limited coverage in Indonesia and are not yet included in national carbon accounting frameworks.'),
            EcosystemRecognition(country_code='KEN', ecosystem_type='Mangroves', recognition_status='Established', details='Mangroves are recognized under Kenya\'s national REDD+ framework and AFOLU accounting.'),
            EcosystemRecognition(country_code='KEN', ecosystem_type='Seagrass', recognition_status='Emerging', details='Seagrass meadows in Lamu and Mombasa are being piloted under the national blue carbon registry.'),
        ]
        db.session.add_all(eco_recognitions)

        agreements = [
            CountryAgreement(agreement_id='AGR-IDN-JPN-001', host_country_code='IDN', agreement_type='Article 6 Cooperative Approach', partner_entity='Japan', status='Authorized', date_signed='2024-08-20', reference_link='https://www.meti.go.jp/'),
            CountryAgreement(agreement_id='AGR-IDN-SIN-001', host_country_code='IDN', agreement_type='Article 6 Cooperative Approach', partner_entity='Singapore', status='MoU Signed', date_signed='2023-11-10', reference_link='https://www.nea.gov.sg/'),
            CountryAgreement(agreement_id='AGR-IDN-VERRA-001', host_country_code='IDN', agreement_type='Special Agreement', partner_entity='Verra', status='Active', date_signed='2022-05-01', reference_link='https://verra.org/'),
            CountryAgreement(agreement_id='AGR-KEN-WB-001', host_country_code='KEN', agreement_type='Special Agreement', partner_entity='World Bank (REDD+)', status='Active', date_signed='2021-09-15', reference_link='https://www.worldbank.org/'),
        ]
        db.session.add_all(agreements)

        # ── Project Layer ─────────────────────────────────────────────────────

        projects = [
            Project(
                project_id='PRJ-IDN-001',
                project_name='Katingan Mentaya Mangrove & Peat Conservation',
                location='Central Kalimantan, Indonesia',
                status='Active',
                tags=['VCM', 'Mangroves', 'Conservation'],
                area='149,800 ha',
                methodology='VM0007 v1.6',
                ecosystem_type='Mangroves',
                price='USD 18/tCO2e',
                first_issued='2018-03-01',
                description='One of the world\'s largest tropical peatland and mangrove conservation projects, protecting critical habitat and delivering verified carbon credits under the VCS standard.',
                rating_agency='BeZero Carbon',
                rating_score='AA',
                label='MRV operational',
                status_category='Success',
            ),
            Project(
                project_id='PRJ-IDN-002',
                project_name='Sulawesi Mangrove Restoration Art.6',
                location='South Sulawesi, Indonesia',
                status='Active',
                tags=['Art.6', 'Mangroves', 'Restoration'],
                area='22,000 ha',
                methodology='VM0033 v2.1',
                ecosystem_type='Mangroves',
                price='USD 24/tCO2e',
                first_issued='2023-07-15',
                description='Art.6.2 authorized mangrove restoration project delivering corresponding adjustment credits to Japan under the bilateral Indonesia-Japan agreement.',
                rating_agency='Sylvera',
                rating_score='BBB',
                label='Art.6 authorized',
                status_category='Success',
            ),
            Project(
                project_id='PRJ-KEN-001',
                project_name='Gazi Bay Mangrove Restoration',
                location='Kwale County, Kenya',
                status='Active',
                tags=['VCM', 'Mangroves', 'Community'],
                area='460 ha',
                methodology='VM0033 v2.1',
                ecosystem_type='Mangroves',
                price='USD 12/tCO2e',
                first_issued='2020-06-01',
                description='Community-led mangrove restoration project in Gazi Bay, Kenya, generating verified carbon credits and supporting local livelihoods through benefit-sharing.',
                rating_agency='BeZero Carbon',
                rating_score='BBB',
                label='Community benefit plan active',
                status_category='Success',
            ),
            Project(
                project_id='PRJ-PHL-001',
                project_name='Palawan Seagrass Blue Carbon Pilot',
                location='Palawan, Philippines',
                status='Pipeline',
                tags=['VCM', 'Seagrass', 'Pilot'],
                area='5,200 ha',
                methodology='VM0033 v2.1',
                ecosystem_type='Seagrass',
                price='TBD',
                first_issued='Expected 2026',
                description='Pilot project aiming to generate the first seagrass carbon credits in the Philippines, under development with IUCN and local government support.',
                rating_agency=None,
                rating_score=None,
                label='Feasibility study underway',
                status_category='Info',
            ),
            Project(
                project_id='PRJ-IDN-003',
                project_name='Raja Ampat Seagrass Conservation',
                location='West Papua, Indonesia',
                status='Pipeline',
                tags=['VCM', 'Seagrass', 'Conservation'],
                area='8,000 ha',
                methodology='VM0033 v2.1',
                ecosystem_type='Seagrass',
                price='TBD',
                first_issued='Expected 2025',
                description='Early-stage seagrass conservation project in the Coral Triangle; pending national seagrass MRV standard approval.',
                rating_agency=None,
                rating_score=None,
                label='Awaiting national standard',
                status_category='Warning',
            ),
        ]
        db.session.add_all(projects)

        methodologies = [
            Methodology(
                methodology_id='VM0033',
                standard='Verra (VCS)',
                description='VM0033 covers tidal wetland and seagrass restoration activities, providing standardized emission factors and accounting for soil carbon, biomass, and methane emissions.',
                ecosystem_focus='Mangroves, Seagrass, Salt Marshes',
                activity_type='Restoration & Conservation',
                recognition='International',
            ),
            Methodology(
                methodology_id='VM0007',
                standard='Verra (VCS)',
                description='VM0007 addresses avoided deforestation in REDD+ projects and is widely applied to mangrove conservation with peatland co-benefits.',
                ecosystem_focus='Mangroves',
                activity_type='Conservation (REDD+)',
                recognition='International',
            ),
            Methodology(
                methodology_id='GS-TIDAL',
                standard='Gold Standard',
                description='Gold Standard tidal wetland methodology emphasizing community co-benefits, safeguards, and integrated SDG reporting alongside carbon accounting.',
                ecosystem_focus='Mangroves, Salt Marshes',
                activity_type='Restoration & Conservation',
                recognition='International',
            ),
            Methodology(
                methodology_id='JCM-BLU-001',
                standard='Japan JCM',
                description='Japan\'s Joint Crediting Mechanism methodology for blue carbon activities, primarily used in bilateral Art.6 cooperation with Southeast Asian partners.',
                ecosystem_focus='Mangroves, Seagrass',
                activity_type='Conservation & Restoration',
                recognition='Primarily Domestic',
            ),
        ]
        db.session.add_all(methodologies)

        ecosystem_tiers = [
            EcosystemTier(
                tier_name='Established',
                ecosystems='Mangroves',
                ghg_impact='High (up to 1,000 tCO2e/ha)',
                long_term_storage='Centuries to millennia',
                ipcc_accounting='Included',
                vcm_readiness='Active market — multiple methodologies',
            ),
            EcosystemTier(
                tier_name='Emerging',
                ecosystems='Seagrass, Salt Marshes',
                ghg_impact='Moderate (50–300 tCO2e/ha)',
                long_term_storage='Decades to centuries',
                ipcc_accounting='Included',
                vcm_readiness='Growing — limited methodologies',
            ),
            EcosystemTier(
                tier_name='Nascent',
                ecosystems='Kelp Forests, Macroalgae',
                ghg_impact='Low to moderate (variable)',
                long_term_storage='Short-term (seasonal)',
                ipcc_accounting='Not included',
                vcm_readiness='Pre-market — experimental only',
            ),
        ]
        db.session.add_all(ecosystem_tiers)

        db.session.commit()
        print('Database seeded successfully.')


if __name__ == '__main__':
    seed()
