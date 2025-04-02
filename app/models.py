from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# User Model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    mobile_number = db.Column(db.String(20), unique=True, nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    company_address = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    scans = db.relationship('Scan', backref='user', lazy=True)
    documents = db.relationship('GeneratedDocument', backref='user', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)
    analyzes = db.relationship('Analyze', backref='user', lazy=True)
    checklists = db.relationship('Checklist', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Scan Model
class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    website_url = db.Column(db.String(255), nullable=False)
    scan_status = db.Column(db.String(50), default="pending")
    issues_found = db.Column(db.JSON, nullable=True)  # Issues such as cookie issues, policy issues, etc.
    cookies = db.Column(db.JSON, nullable=True)  # Store cookie data
    privacy_policy_status = db.Column(db.String(50), default="not_checked")  # Privacy policy check status
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Scan {self.id} for {self.website_url}>'


# Analyze Model (for AI-driven analysis)
class Analyze(db.Model):
    __tablename__ = 'analyzes'
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.Integer, db.ForeignKey('scan.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ai_feedback = db.Column(db.Text, nullable=True)  # AI feedback on privacy policy
    missing_elements = db.Column(db.JSON, nullable=True)  # Missing elements in the policy
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    scan = db.relationship('Scan', backref=db.backref('analyzes', lazy=True))
    user = db.relationship('User', back_populates='analyzes')

    def __repr__(self):
        return f'<Analyze {self.id} for Scan {self.scan_id}>'


# Generated Document Model (for AI-generated documents)
class GeneratedDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    document_url = db.Column(db.String(255), nullable=False)  # URL or file path for the generated document
    document_type = db.Column(db.String(50), nullable=False, default="privacy_policy")  # Type of document (e.g., privacy policy)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('generated_documents', lazy=True))

    def __repr__(self):
        return f'<GeneratedDocument {self.id} for User {self.user_id}>'


# Payment Model (for handling payments via Stripe)
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default="DKK")
    payment_status = db.Column(db.String(50), default="pending")  # Status like 'pending', 'completed', 'failed'
    stripe_charge_id = db.Column(db.String(255), unique=True, nullable=True)  # Stripe charge ID for the payment
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('payments', lazy=True))

    def __repr__(self):
        return f'<Payment {self.id} for User {self.user_id}>'


# Checklist Model (for GDPR, IT security, ESG guidelines, etc.)
class Checklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)  # Title of the checklist (e.g., "GDPR Compliance Checklist")
    description = db.Column(db.Text, nullable=True)  # Description or detailed instructions for the checklist
    steps = db.Column(db.JSON, nullable=False)  # Steps or items in the checklist
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('checklists', lazy=True))

    def __repr__(self):
        return f'<Checklist {self.title} for User {self.user_id}>'

