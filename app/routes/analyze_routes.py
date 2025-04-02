from flask import Blueprint, request, jsonify
from app.models import db, Analyze, Scan, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from your_bert_model import analyze_privacy_policy  # Assume this is your AI model function

analyze_bp = Blueprint('analyze', __name__, url_prefix='/api')

# Perform AI-driven analysis of a scan's privacy policy
@analyze_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze():
    data = request.get_json()
    scan_id = data.get('scan_id')

    if not scan_id:
        return jsonify({'message': 'Scan ID is required'}), 400

    # Get the user id from JWT token
    user_id = get_jwt_identity()

    scan = Scan.query.get(scan_id)
    if not scan or scan.user_id != user_id:
        return jsonify({'message': 'Scan not found or not authorized'}), 404

    # Run the AI analysis on the scan's privacy policy
    analysis_result = analyze_privacy_policy(scan.privacy_policy_status)

    # Store the analysis results in the database
    new_analysis = Analyze(
        scan_id=scan.id,
        user_id=user_id,
        ai_feedback=analysis_result.get('feedback'),
        missing_elements=analysis_result.get('missing_elements')
    )
    db.session.add(new_analysis)
    db.session.commit()

    return jsonify({'message': 'Analysis completed successfully', 'analysis_id': new_analysis.id}), 201
