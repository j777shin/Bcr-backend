from app import db


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.String(50), unique=True, nullable=False)
    project_name = db.Column(db.String(200))
    location = db.Column(db.String(200))
    status = db.Column(db.String(20))
    tags = db.Column(db.JSON)
    area = db.Column(db.String(100))      # hectares as display string
    methodology = db.Column(db.String(200))
    ecosystem_type = db.Column(db.String(50))
    vintage = db.Column(db.String(50))    # credit vintage year or "—"
    credits = db.Column(db.String(50))    # credits issued, e.g. "2,458" or "—"
    registry = db.Column(db.String(200))  # registry name, e.g. "Verra VCS"
    description = db.Column(db.Text)
    checks = db.Column(db.JSON)           # list of check strings
    price = db.Column(db.String(100))
    rating_agency = db.Column(db.String(100))
    rating_score = db.Column(db.String(10))
    status_category = db.Column(db.String(20))

    def to_dict(self):
        return {
            'project_id': self.project_id,
            'project_name': self.project_name,
            'location': self.location,
            'status': self.status,
            'tags': self.tags or [],
            'area': self.area,
            'methodology': self.methodology,
            'ecosystem_type': self.ecosystem_type,
            'vintage': self.vintage,
            'credits': self.credits,
            'registry': self.registry,
            'description': self.description,
            'checks': self.checks or [],
            'price': self.price,
            'rating_agency': self.rating_agency,
            'rating_score': self.rating_score,
            'status_category': self.status_category,
        }


class ProjectCost(db.Model):
    """Project-level CAPEX/OPEX cost model output (from Carbon-Cost workbook,
    Projects sheet). Keyed by country/ecosystem/activity/activity_type/size."""
    __tablename__ = 'project_costs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    country = db.Column(db.String(100))
    country_code = db.Column(db.String(10), index=True)
    ecosystem = db.Column(db.String(50), index=True)
    activity = db.Column(db.String(50), index=True)
    activity_type = db.Column(db.String(50))
    project_size_filter = db.Column(db.String(20))
    project_size_ha = db.Column(db.Float)
    price_type = db.Column(db.String(50))
    country_size_ha = db.Column(db.Float)
    base_size = db.Column(db.Float)
    project_name = db.Column(db.String(255), index=True)

    total_cost_npv = db.Column(db.Float)
    total_cost = db.Column(db.Float)
    total_weighted_cost_npv = db.Column(db.Float)
    total_weighted_cost = db.Column(db.Float)
    capex_npv = db.Column(db.Float)
    capex = db.Column(db.Float)
    opex_npv = db.Column(db.Float)
    opex = db.Column(db.Float)
    country_abatement_potential = db.Column(db.Float)
    project_abatement_potential = db.Column(db.Float)
    cost_per_tco2e = db.Column(db.Float)
    cost_per_tco2e_npv = db.Column(db.Float)

    feasibility_analysis_npv = db.Column(db.Float)
    feasibility_analysis = db.Column(db.Float)
    conservation_planning_npv = db.Column(db.Float)
    conservation_planning = db.Column(db.Float)
    data_collection_npv = db.Column(db.Float)
    data_collection = db.Column(db.Float)
    community_representation_npv = db.Column(db.Float)
    community_representation = db.Column(db.Float)
    blue_carbon_project_planning_npv = db.Column(db.Float)
    blue_carbon_project_planning = db.Column(db.Float)
    establishing_carbon_rights_npv = db.Column(db.Float)
    establishing_carbon_rights = db.Column(db.Float)
    validation_npv = db.Column(db.Float)
    validation = db.Column(db.Float)
    implementation_labor_npv = db.Column(db.Float)
    implementation_labor = db.Column(db.Float)
    monitoring_maintenance_npv = db.Column(db.Float)
    monitoring_maintenance = db.Column(db.Float)
    community_benefit_npv = db.Column(db.Float)
    community_benefit = db.Column(db.Float)
    carbon_standard_fees_npv = db.Column(db.Float)
    carbon_standard_fees = db.Column(db.Float)
    baseline_reassessment_npv = db.Column(db.Float)
    baseline_reassessment = db.Column(db.Float)
    mrv_npv = db.Column(db.Float)
    mrv = db.Column(db.Float)
    long_term_project_operating_npv = db.Column(db.Float)
    long_term_project_operating = db.Column(db.Float)

    initial_price_assumption = db.Column(db.Float)
    leftover_after_opex = db.Column(db.Float)
    leftover_after_opex_npv = db.Column(db.Float)
    total_revenue = db.Column(db.Float)
    total_revenue_npv = db.Column(db.Float)
    credits_issued = db.Column(db.Float)
    monitoring_npv = db.Column(db.Float)
    maintenance_npv = db.Column(db.Float)
    monitoring = db.Column(db.Float)
    maintenance = db.Column(db.Float)

    __table_args__ = (
        db.UniqueConstraint(
            'country_code', 'ecosystem', 'activity',
            'activity_type', 'project_size_filter',
            name='uq_project_cost_variation',
        ),
    )

    def to_dict(self):
        cols = [c.name for c in self.__table__.columns if c.name != 'id']
        return {c: getattr(self, c) for c in cols}


class Methodology(db.Model):
    __tablename__ = 'methodologies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    methodology_id = db.Column(db.String(50), unique=True, nullable=False)
    standard = db.Column(db.String(100))
    description = db.Column(db.Text)
    ecosystem_focus = db.Column(db.String(200))
    activity_type = db.Column(db.String(100))
    recognition = db.Column(db.String(50))
    is_current = db.Column(db.Boolean, default=True)  # False = legacy/deprecated

    def to_dict(self):
        return {
            'methodology_id': self.methodology_id,
            'standard': self.standard,
            'description': self.description,
            'ecosystem_focus': self.ecosystem_focus,
            'activity_type': self.activity_type,
            'recognition': self.recognition,
            'is_current': self.is_current,
        }


class EcosystemTier(db.Model):
    __tablename__ = 'ecosystem_tiers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tier_name = db.Column(db.String(50), unique=True, nullable=False)
    ecosystems = db.Column(db.String(200))
    ghg_impact = db.Column(db.String(100))
    long_term_storage = db.Column(db.String(100))
    ipcc_accounting = db.Column(db.String(50))
    vcm_readiness = db.Column(db.String(100))

    def to_dict(self):
        return {
            'tier_name': self.tier_name,
            'ecosystems': self.ecosystems,
            'ghg_impact': self.ghg_impact,
            'long_term_storage': self.long_term_storage,
            'ipcc_accounting': self.ipcc_accounting,
            'vcm_readiness': self.vcm_readiness,
        }
