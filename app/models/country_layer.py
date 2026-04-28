from app import db


class CountryMetric(db.Model):
    """Top-level stat cards shown on the country deep-dive page."""
    __tablename__ = 'country_metrics'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_code = db.Column(db.String(3), db.ForeignKey('countries.country_code'), nullable=False, index=True)
    metric_name = db.Column(db.String(100))
    metric_value = db.Column(db.String(100))
    metric_subtext = db.Column(db.String(200))

    def to_dict(self):
        return {
            'country_code': self.country_code,
            'metric_name': self.metric_name,
            'metric_value': self.metric_value,
            'metric_subtext': self.metric_subtext,
        }


class CountryDimension(db.Model):
    """One row per Article 6 Readiness Toolkit building block per country."""
    __tablename__ = 'country_dimensions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_code = db.Column(db.String(3), db.ForeignKey('countries.country_code'), nullable=False, index=True)
    dimension_id = db.Column(db.String(5))   # 'i', 'ii', 'iii', 'iv', 'v'
    label = db.Column(db.String(50))         # 'I — Strategic'
    full_label = db.Column(db.String(100))   # 'I — Strategic Considerations'
    gate = db.Column(db.String(20))          # 'cleared', 'pending', 'progress'
    gate_text = db.Column(db.String(50))     # '✓ Gate cleared'
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            'country_code': self.country_code,
            'dimension_id': self.dimension_id,
            'label': self.label,
            'full_label': self.full_label,
            'gate': self.gate,
            'gate_text': self.gate_text,
            'description': self.description,
        }


class CountryChecklist(db.Model):
    __tablename__ = 'country_checklists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_code = db.Column(db.String(3), db.ForeignKey('countries.country_code'), nullable=False, index=True)
    dimension_id = db.Column(db.String(5))   # 'i', 'ii', 'iii', 'iv', 'v'
    item_label = db.Column(db.String(200))
    status = db.Column(db.String(10))        # 'yes', 'partial', 'no'

    def to_dict(self):
        return {
            'country_code': self.country_code,
            'dimension_id': self.dimension_id,
            'item_label': self.item_label,
            'status': self.status,
        }


class CountryNDCTarget(db.Model):
    __tablename__ = 'country_ndc_targets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_code = db.Column(db.String(3), db.ForeignKey('countries.country_code'), nullable=False, index=True)
    target_type = db.Column(db.String(100))
    target_title = db.Column(db.String(200))
    unconditional_val = db.Column(db.String(100))
    unconditional_pct = db.Column(db.Integer)
    conditional_val = db.Column(db.String(100))
    conditional_pct = db.Column(db.Integer)

    def to_dict(self):
        return {
            'country_code': self.country_code,
            'target_type': self.target_type,
            'target_title': self.target_title,
            'unconditional_val': self.unconditional_val,
            'unconditional_pct': self.unconditional_pct,
            'conditional_val': self.conditional_val,
            'conditional_pct': self.conditional_pct,
        }


class CountryInstitution(db.Model):
    __tablename__ = 'country_institutions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_code = db.Column(db.String(3), db.ForeignKey('countries.country_code'), nullable=False, index=True)
    role = db.Column(db.String(100))
    name = db.Column(db.String(200))
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            'country_code': self.country_code,
            'role': self.role,
            'name': self.name,
            'description': self.description,
        }


class EcosystemRecognition(db.Model):
    __tablename__ = 'ecosystem_recognitions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_code = db.Column(db.String(3), db.ForeignKey('countries.country_code'), nullable=False, index=True)
    ecosystem_type = db.Column(db.String(50))
    recognition_status = db.Column(db.String(50))
    details = db.Column(db.Text)

    def to_dict(self):
        return {
            'country_code': self.country_code,
            'ecosystem_type': self.ecosystem_type,
            'recognition_status': self.recognition_status,
            'details': self.details,
        }


class CountryAgreement(db.Model):
    __tablename__ = 'country_agreements'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    agreement_id = db.Column(db.String(50), unique=True, nullable=False)
    host_country_code = db.Column(db.String(3), db.ForeignKey('countries.country_code'), nullable=False, index=True)
    agreement_type = db.Column(db.String(100))
    partner_entity = db.Column(db.String(200))
    status = db.Column(db.String(50))
    date_signed = db.Column(db.String(50))
    reference_link = db.Column(db.String(500))

    def to_dict(self):
        return {
            'agreement_id': self.agreement_id,
            'host_country_code': self.host_country_code,
            'agreement_type': self.agreement_type,
            'partner_entity': self.partner_entity,
            'status': self.status,
            'date_signed': self.date_signed,
            'reference_link': self.reference_link,
        }
