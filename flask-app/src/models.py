from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String(255), unique=True, nullable=False)
    api_secret_hash = db.Column(db.String(255), nullable=False)
    dashboard_token = db.Column(db.String(255), unique=True, nullable=False)
    ipfs_access_hash = db.Column(db.String(255), unique=True, nullable=False)
    credit_balance_eur = db.Column(db.Numeric(16, 8), nullable=False, default=0.00)
    kubo_balance_eur = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    cluster_balance_eur = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    bandwidth_allowance_gb = db.Column(db.Numeric(10, 2), nullable=False, default=1.00)
    bandwidth_used_private_gb = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    bandwidth_used_public_gb = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    bandwidth_cycle_start = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    def set_api_secret(self, api_secret):
        self.api_secret_hash = generate_password_hash(f"{self.api_key}:{api_secret}")

    def check_api_secret(self, api_secret):
        return check_password_hash(self.api_secret_hash, f"{self.api_key}:{api_secret}")


class Pin(db.Model):
    __tablename__ = 'pins'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cid = db.Column(db.String(255), nullable=False, index=True)
    file_name = db.Column(db.String(255))
    size_bytes = db.Column(db.BigInteger, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')
    is_private = db.Column(db.Boolean, default=False, nullable=False)
    ipfs_access_hash = db.Column(db.String(255), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expire_at = db.Column(db.DateTime, nullable=True)
    already_charged = db.Column(db.Boolean, default=False, nullable=False)
    grace_period_started_at = db.Column(db.DateTime, nullable=True)
    retention_months = db.Column(db.Integer, default=1, nullable=False)


class ClusterBackup(db.Model):
    __tablename__ = 'cluster_backups'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cid = db.Column(db.String(255), nullable=False, index=True)
    file_name = db.Column(db.String(255), nullable=False)
    size_bytes = db.Column(db.BigInteger, nullable=False)
    replica_count = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.String(50), nullable=False, default='active')
    ipfs_access_hash = db.Column(db.String(255), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expire_at = db.Column(db.DateTime, nullable=True)
    already_charged = db.Column(db.Boolean, default=False, nullable=False)
    grace_period_started_at = db.Column(db.DateTime, nullable=True)


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tx_id = db.Column(db.String(255), unique=True, nullable=False)
    amount = db.Column(db.Numeric(16, 8), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)


class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    payment_tx_id = db.Column(db.String(255), db.ForeignKey('payments.tx_id'))
    amount_eur = db.Column(db.Numeric(16, 8), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)


class ReplicaHistory(db.Model):
    __tablename__ = 'replica_history'
    id = db.Column(db.Integer, primary_key=True)
    backup_id = db.Column(db.Integer, db.ForeignKey('cluster_backups.id'), nullable=False)
    replica_count = db.Column(db.Integer, nullable=False)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)
