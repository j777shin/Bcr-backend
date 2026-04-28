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
