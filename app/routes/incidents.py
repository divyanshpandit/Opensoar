from flask import Blueprint, request, jsonify
from app import db
from app.models import Incident
from flask_jwt_extended import jwt_required

incident_bp = Blueprint('incident', __name__, url_prefix='/api/incidents')

# Get all incidents
@incident_bp.route('/', methods=['GET'])
@jwt_required()
def get_all():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return jsonify([
        {
            'id': i.id,
            'title': i.title,
            'severity': i.severity,
            'status': i.status,
            'created_at': i.created_at.isoformat()
        } for i in incidents
    ]), 200

# Create a new incident
@incident_bp.route('/', methods=['POST'])
@jwt_required()
def create_incident():
    data = request.get_json()
    if not data.get('title') or not data.get('severity'):
        return jsonify({'msg': 'Title and severity are required'}), 400

    new_incident = Incident(
        title=data['title'],
        severity=data['severity'],
        status=data.get('status', 'Open')
    )
    db.session.add(new_incident)
    db.session.commit()
    return jsonify({'msg': 'Incident created'}), 201

# Update an incident
@incident_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_incident(id):
    incident = Incident.query.get_or_404(id)
    data = request.get_json()
    incident.title = data.get('title', incident.title)
    incident.severity = data.get('severity', incident.severity)
    incident.status = data.get('status', incident.status)
    db.session.commit()
    return jsonify({'msg': 'Incident updated'}), 200

# Delete an incident
@incident_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_incident(id):
    incident = Incident.query.get_or_404(id)
    db.session.delete(incident)
    db.session.commit()
    return jsonify({'msg': 'Incident deleted'}), 200
