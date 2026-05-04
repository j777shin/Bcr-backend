from flask import Blueprint, jsonify, request
from app.models.project_layer import ProjectCost, Methodology, EcosystemTier

project_bp = Blueprint('project', __name__)


# --- Projects (CAPEX/OPEX cost-model variations) ---

@project_bp.route('/projects', methods=['GET'])
def get_projects():
    ecosystem = request.args.get('ecosystem')
    activity = request.args.get('activity')
    activity_type = request.args.get('activity_type')
    size = request.args.get('size')
    country_code = request.args.get('country_code')

    query = ProjectCost.query
    if ecosystem:
        query = query.filter_by(ecosystem=ecosystem)
    if activity:
        query = query.filter_by(activity=activity)
    if activity_type:
        query = query.filter_by(activity_type=activity_type)
    if size:
        query = query.filter_by(project_size_filter=size)
    if country_code:
        query = query.filter_by(country_code=country_code)

    return jsonify([{'id': p.id, **p.to_dict()} for p in query.all()])


@project_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = ProjectCost.query.filter_by(id=project_id).first_or_404()
    return jsonify({'id': project.id, **project.to_dict()})


# --- Methodologies ---

@project_bp.route('/methodologies', methods=['GET'])
def get_methodologies():
    recognition = request.args.get('recognition')
    query = Methodology.query
    if recognition:
        query = query.filter_by(recognition=recognition)
    return jsonify([m.to_dict() for m in query.all()])


@project_bp.route('/methodologies/<string:methodology_id>', methods=['GET'])
def get_methodology(methodology_id):
    methodology = Methodology.query.filter_by(methodology_id=methodology_id).first_or_404()
    return jsonify(methodology.to_dict())


# --- Ecosystem Tiers ---

@project_bp.route('/ecosystem-tiers', methods=['GET'])
def get_ecosystem_tiers():
    tiers = EcosystemTier.query.all()
    return jsonify([t.to_dict() for t in tiers])


@project_bp.route('/ecosystem-tiers/<string:tier_name>', methods=['GET'])
def get_ecosystem_tier(tier_name):
    tier = EcosystemTier.query.filter_by(tier_name=tier_name).first_or_404()
    return jsonify(tier.to_dict())
