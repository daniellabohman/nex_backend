from flask import Blueprint, request, jsonify
from app.models import db, Scan, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from your_scanner_module import run_scan  # Assume you have a scanning function here

scan_bp = Blueprint('scan', __name__, url_prefix='/api')

# Start a scan for a URL
@scan_bp.route('/scan', methods=['POST'])
@jwt_required()
def scan():
    data = request.get_json()
    website_url = data.get('website_url')

    if not website_url:
        return jsonify({'message': 'Website URL is required'}), 400

    # Get the user id from JWT token
    user_id = get_jwt_identity()

    # Run the actual scan (using Playwright or Selenium)
    scan_result = run_scan(website_url)  # Assume this returns the scan result

    # Save scan result to database
    new_scan = Scan(
        user_id=user_id,
        website_url=website_url,
        scan_status='completed',
        issues_found=scan_result.get('issues'),
        cookies=scan_result.get('cookies'),
        privacy_policy_status=scan_result.get('privacy_policy_status')
    )
    db.session.add(new_scan)
    db.session.commit()

    return jsonify({'message': 'Scan completed successfully', 'scan_id': new_scan.id}), 201

# Fetch all scans for the current user
@scan_bp.route('/scans', methods=['GET'])
@jwt_required()
def get_scans():
    user_id = get_jwt_identity()
    scans = Scan.query.filter_by(user_id=user_id).all()
    return jsonify([scan.serialize() for scan in scans]), 200
