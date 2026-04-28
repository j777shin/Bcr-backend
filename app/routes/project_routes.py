from flask import Blueprint, jsonify, request
from app.models.project_layer import Project, Methodology, EcosystemTier

project_bp = Blueprint('project', __name__)


# --- Projects ---

@project_bp.route('/projects', methods=['GET'])
def get_projects():
    status = request.args.get('status')
    ecosystem = request.args.get('ecosystem')
    location = request.args.get('location')

    query = Project.query
    if status:
        query = query.filter_by(status=status)
    if ecosystem:
        query = query.filter_by(ecosystem_type=ecosystem)
    if location:
        query = query.filter(Project.location.ilike(f'%{location}%'))

    return jsonify([p.to_dict() for p in query.all()])


@project_bp.route('/projects/<string:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    return jsonify(project.to_dict())


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
