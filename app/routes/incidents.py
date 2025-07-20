from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Incident, User

incident_bp = Blueprint('incident', __name__, url_prefix='/api/incidents')


# GET /api/incidents/ - Fetch all incidents with optional filters
@incident_bp.route('/', methods=['GET'])
@jwt_required()
def get_all():
    severity = request.args.get('severity')
    status = request.args.get('status')
    title = request.args.get('title')

    query = Incident.query

    if severity:
        query = query.filter_by(severity=severity)
    if status:
        query = query.filter_by(status=status)
    if title:
        query = query.filter(Incident.title.ilike(f"%{title}%"))

    incidents = query.order_by(Incident.created_at.desc()).all()

    return jsonify([{
        'id': i.id,
        'title': i.title,
        'severity': i.severity,
        'status': i.status,
        'created_at': i.created_at.isoformat(),
        'assigned_to': i.assigned_to.username if i.assigned_to else None,
        'assigned_to_id': i.assigned_to_id,
        'priority': i.priority,
        'tags': i.tags,
        'notes': i.notes
    } for i in incidents])


# POST /api/incidents/ - Create a new incident
@incident_bp.route('/', methods=['POST'])
@jwt_required()
def create_incident():
    data = request.get_json()
    if not data.get('title') or not data.get('severity'):
        return jsonify({'msg': 'Title and severity required'}), 400

    incident = Incident(
        title=data['title'],
        severity=data['severity'],
        status=data.get('status', 'Open'),
        assigned_to_id=data.get('assigned_to_id'),  # ✅ Correct field name
        priority=data.get('priority'),
        tags=data.get('tags'),
        notes=data.get('notes')
    )
    db.session.add(incident)
    db.session.commit()
    return jsonify({'msg': 'Incident created'}), 201


# PUT /api/incidents/<id> - Update an existing incident
@incident_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_incident(id):
    incident = Incident.query.get_or_404(id)
    data = request.get_json()

    incident.title = data.get('title', incident.title)
    incident.severity = data.get('severity', incident.severity)
    incident.status = data.get('status', incident.status)
    incident.assigned_to_id = data.get('assigned_to_id', incident.assigned_to_id)
    incident.priority = data.get('priority', incident.priority)
    incident.tags = data.get('tags', incident.tags)
    incident.notes = data.get('notes', incident.notes)

    db.session.commit()
    return jsonify({'msg': 'Incident updated'}), 200


# DELETE /api/incidents/<id> - Delete an incident
@incident_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_incident(id):
    incident = Incident.query.get_or_404(id)
    db.session.delete(incident)
    db.session.commit()
    return jsonify({'msg': 'Incident deleted'}), 200
