from flask import Blueprint, jsonify, request
from app.models.country_layer import (
    CountryMetric, CountryChecklist, CountryNDCTarget,
    CountryInstitution, EcosystemRecognition, CountryAgreement,
)

country_bp = Blueprint('country', __name__)


@country_bp.route('/countries/<string:country_code>/metrics', methods=['GET'])
def get_metrics(country_code):
    dimension_id = request.args.get('dimension')
    query = CountryMetric.query.filter_by(country_code=country_code.upper())
    if dimension_id:
        query = query.filter_by(dimension_id=dimension_id.upper())
    return jsonify([m.to_dict() for m in query.all()])


@country_bp.route('/countries/<string:country_code>/checklist', methods=['GET'])
def get_checklist(country_code):
    dimension_id = request.args.get('dimension')
    query = CountryChecklist.query.filter_by(country_code=country_code.upper())
    if dimension_id:
        query = query.filter_by(dimension_id=dimension_id.upper())
    return jsonify([i.to_dict() for i in query.all()])


@country_bp.route('/countries/<string:country_code>/ndc-targets', methods=['GET'])
def get_ndc_targets(country_code):
    targets = CountryNDCTarget.query.filter_by(country_code=country_code.upper()).all()
    return jsonify([t.to_dict() for t in targets])


@country_bp.route('/countries/<string:country_code>/institutions', methods=['GET'])
def get_institutions(country_code):
    institutions = CountryInstitution.query.filter_by(country_code=country_code.upper()).all()
    return jsonify([i.to_dict() for i in institutions])


@country_bp.route('/countries/<string:country_code>/ecosystem-recognition', methods=['GET'])
def get_ecosystem_recognition(country_code):
    recognitions = EcosystemRecognition.query.filter_by(country_code=country_code.upper()).all()
    return jsonify([r.to_dict() for r in recognitions])


@country_bp.route('/countries/<string:country_code>/agreements', methods=['GET'])
def get_agreements(country_code):
    agreement_type = request.args.get('type')
    query = CountryAgreement.query.filter_by(host_country_code=country_code.upper())
    if agreement_type:
        query = query.filter_by(agreement_type=agreement_type)
    return jsonify([a.to_dict() for a in query.all()])
