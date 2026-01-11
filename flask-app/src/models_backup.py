from .app import db
from datetime import datetime
import secrets
import hashlib

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String(255), unique=True, nullable=False, default=lambda: secrets.token_urlsafe(32))
    api_secret_hash = db.Column(db.String(255), nullable=False)
    dashboard_token = db.Column(db.String(255), unique=True, nullable=False, default=lambda: secrets.token_urlsafe(32))
    ipfs_access_hash = db.Column(db.String(255), unique=True, nullable=False, default=lambda: secrets.token_urlsafe(48))  # Unique hash for IPFS cluster access control
    credit_balance_eur = db.Column(db.Numeric(16, 8), nullable=False, default=0.00)
    
    # Bandwidth management - IPFS Kubo Private and Public
    bandwidth_allowance_gb = db.Column(db.Numeric(10, 2), nullable=False, default=1.00)  # 1 GB free per month
    bandwidth_used_private_gb = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)  # IPFS Kubo Private usage
    bandwidth_used_public_gb = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)   # IPFS Kubo Public usage
    bandwidth_cycle_start = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    
    # Pay-as-you-go billing tracking
    last_pin_billing_date = db.Column(db.DateTime, nullable=True)  # For monthly IPFS Kubo storage billing
    last_backup_billing_date = db.Column(db.DateTime, nullable=True)  # For monthly backup service billing (legacy)

    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    #pins = db.relationship('Pin', backref='user', lazy=True)
    invoices = db.relationship('Invoice', backref='user', lazy=True)

    def set_api_secret(self, api_secret):
        self.api_secret_hash = hashlib.sha256(api_secret.encode('utf-8')).hexdigest()

    def check_api_secret(self, api_secret):
        return self.api_secret_hash == hashlib.sha256(api_secret.encode('utf-8')).hexdigest()

class Pin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cid = db.Column(db.String(255), nullable=False, index=True)
    file_name = db.Column(db.String(255), nullable=False)
    size_bytes = db.Column(db.BigInteger, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='queued') # e.g., 'queued', 'pinned', 'error', 'grace_period'
    is_private = db.Column(db.Boolean, default=False, nullable=False)
    ipfs_access_hash = db.Column(db.String(255), nullable=False, index=True)  # User's unique hash for IPFS cluster access validation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expire_at = db.Column(db.DateTime, nullable=True) # When the paid retention period ends
    grace_period_started_at = db.Column(db.DateTime, nullable=True) # Tracks the start of a grace period
    already_charged = db.Column(db.Boolean, default=False, nullable=False) # Track if upfront charge was already paid (for re-pinning)

    user = db.relationship('User', back_populates='pins')

class ClusterBackup(db.Model):
    """IPFS Cluster backup with PREPAID model (charged upfront)"""
    __tablename__ = 'cluster_backups'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cid = db.Column(db.String(255), nullable=False, index=True)
    file_name = db.Column(db.String(255), nullable=False)
    size_bytes = db.Column(db.BigInteger, nullable=False)
    replica_count = db.Column(db.Integer, nullable=False, default=1)  # 1, 2, or 3
    status = db.Column(db.String(50), nullable=False, default='active')  # active, grace_period, deleted
    ipfs_access_hash = db.Column(db.String(255), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expire_at = db.Column(db.DateTime, nullable=True)  # When the paid retention period ends (PREPAID)
    already_charged = db.Column(db.Boolean, default=False, nullable=False)  # Track if upfront charge was paid
    grace_period_started_at = db.Column(db.DateTime, nullable=True)
    
    user = db.relationship('User', backref='cluster_backups')


class ReplicaHistory(db.Model):
    """Track replica count changes for accurate mid-month billing"""
    __tablename__ = 'replica_history'
    id = db.Column(db.Integer, primary_key=True)
    backup_id = db.Column(db.Integer, db.ForeignKey('cluster_backups.id'), nullable=False)
    replica_count = db.Column(db.Integer, nullable=False)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    backup = db.relationship('ClusterBackup', back_populates='replica_history')


class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    payment_tx_id = db.Column(db.String(255), db.ForeignKey('payments.tx_id'))
    amount_eur = db.Column(db.Numeric(16, 8), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    tx_id = db.Column(db.String(255), unique=True, nullable=False)
    amount = db.Column(db.Numeric(16, 8), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    invoice = db.relationship('Invoice', backref='payment', uselist=False)
