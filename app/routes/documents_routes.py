from flask import Blueprint, request, jsonify
from app.models import db, GeneratedDocument

document_bp = Blueprint('documents', __name__, url_prefix='/api')

# API Endpoint: Hent alle dokumenter

@document_bp.route('/documents', methods=['GET'])
def get_documents():
    documents = GeneratedDocument.query.all()
    result = [
        {'id': doc.id, 'user_id': doc.user_id, 'document_url': doc.document_url, 'created_at': doc.created_at}
        for doc in documents
    ]
    return jsonify(result), 200
