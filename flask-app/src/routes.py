from flask import Blueprint, jsonify, request, current_app, render_template
from .models import db, User, Pin, ClusterBackup, Payment, Invoice, ReplicaHistory # Added Backup import
from .ipfs_access_control import validate_ipfs_access, verify_pin_ownership
import secrets
import subprocess
import os
from decimal import Decimal
from datetime import datetime, timedelta
from functools import wraps

# Authentication decorator
def require_auth(f):
    """Decorator to require API key and secret authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        api_secret = request.headers.get('X-API-SECRET')
        
        if not api_key or not api_secret:
            return jsonify({"error": "Missing API credentials"}), 401
        
        user = User.query.filter_by(api_key=api_key).first()
        if not user or not user.check_api_secret(api_secret):
            return jsonify({"error": "Invalid API credentials"}), 401
        
        return f(user, *args, **kwargs)
    return decorated_function


main = Blueprint('main', __name__)

# --- Configuration ---
# IPFS Kubo Pricing with Retention Options (OPTION A - Discount for Commitment)
# Pricing is the SAME for both private and public (simplified model)
KUBO_PRICING = {
    "private": {
        1: {"price_per_gb_month": Decimal("0.10"), "bandwidth_overage": Decimal("0.08"), "discount": "0%"},
        2: {"price_per_gb_month": Decimal("0.09"), "bandwidth_overage": Decimal("0.08"), "discount": "10%"},
        6: {"price_per_gb_month": Decimal("0.07"), "bandwidth_overage": Decimal("0.08"), "discount": "30%"},
        12: {"price_per_gb_month": Decimal("0.05"), "bandwidth_overage": Decimal("0.08"), "discount": "50%"}
    },
    "public": {
        1: {"price_per_gb_month": Decimal("0.10"), "bandwidth_overage": Decimal("0.08"), "discount": "0%"},
        2: {"price_per_gb_month": Decimal("0.09"), "bandwidth_overage": Decimal("0.08"), "discount": "10%"},
        6: {"price_per_gb_month": Decimal("0.07"), "bandwidth_overage": Decimal("0.08"), "discount": "30%"},
        12: {"price_per_gb_month": Decimal("0.05"), "bandwidth_overage": Decimal("0.08"), "discount": "50%"}
    }
}

FREE_BANDWIDTH_GB_PER_MONTH = Decimal("5.00")     # 5 GB free bandwidth per customer per month
ALLOWED_RETENTION_MONTHS = [1, 2, 6, 12]

# Legacy pricing for backward compatibility
PRICE_PER_GB_MONTH_EUR_PINNING = Decimal("0.07")  # Old default
PRICE_PER_GB_BANDWIDTH_PRIVATE = Decimal("0.02")  # Old bandwidth pricing
PRICE_PER_GB_BANDWIDTH_PUBLIC = Decimal("0.10")   # Old bandwidth pricing

# Backup Service Pricing (separate service, not IPFS Kubo)
PRICE_PER_GB_MONTH_EUR_BACKUP = Decimal("0.0156") # For Backup Service (legacy)

BYTES_PER_GB = 1024 * 1024 * 1024

# --- Authentication Decorator ---
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        api_secret = request.headers.get('X-API-SECRET')
        if not api_key or not api_secret:
            return jsonify({"error": "API key and secret are required"}), 401
        
        user = User.query.filter_by(api_key=api_key).first()
        
        # Use the updated check_api_secret method
        if not user or not user.check_api_secret(api_secret):
            return jsonify({"error": "Invalid API key or secret"}), 401
        
        request.user = user
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def index():
    """Homepage with integrated Terms of Service"""
    return render_template('homepage.html')

@main.route('/terms')
def terms_of_service():
    """Full Terms of Service page"""
    return render_template('terms_of_service.html')

@main.route('/robots.txt')
def robots():
    """Robots.txt for SEO"""
    from flask import send_from_directory
    return send_from_directory('static', 'robots.txt', mimetype='text/plain')

@main.route('/sitemap.xml')
def sitemap():
    """Sitemap.xml for SEO"""
    from flask import send_from_directory
    return send_from_directory('static', 'sitemap.xml', mimetype='application/xml')

@main.route('/api')
def api_root():
    return jsonify({"status": "API is running"}), 200

@main.route('/api/welcome-data', methods=['GET'])
def welcome_data():
    """
    API endpoint for welcome page to fetch user credentials and payment address
    """
    token = request.args.get('token')
    if not token:
        return jsonify({"error": "Token required"}), 400
    
    user = User.query.filter_by(dashboard_token=token).first()
    if not user:
        return jsonify({"error": "Invalid token"}), 404
    
    # Generate payment address via SatSale
    bitcoin_address = None
    payment_uri = None
    qr_code_url = None
    
    try:
        import requests
        satsale_response = requests.get(
            "http://localhost:8000/api/createpayment",
            params={
                "amount": 10,
                "currency": "EUR",
                "method": "onchain",
                "w_url": f"http://localhost:5003/webhook/satsale?user_id={user.api_key}"
            },
            timeout=10
        )
        if satsale_response.status_code == 200:
            payment_data = satsale_response.json()
            # SatSale returns address nested in 'invoice' key
            invoice_data = payment_data.get("invoice", {})
            bitcoin_address = invoice_data.get("address")
            payment_uri = payment_data.get("payment_uri")
            qr_code_url = f"http://localhost:8000/api/qr/{bitcoin_address}" if bitcoin_address else None
    except Exception as e:
        bitcoin_address = "Error generating address"
    
    return jsonify({
        "credentials": {
            "api_key": user.api_key,
            "api_secret": "HIDDEN - Check registration response",
            "dashboard_token": user.dashboard_token,
            "ipfs_access_hash": user.ipfs_access_hash
        },
        "payment": {
            "bitcoin_address": bitcoin_address,
            "payment_uri": payment_uri,
            "qr_code_url": qr_code_url
        },
        "balance": {
            "kubo_balance": str(user.kubo_balance_eur),
            "cluster_balance": str(user.cluster_balance_eur)
        }
    }), 200

@main.route('/api/balance', methods=['GET'])
def check_balance():
    """
    Check user balance by dashboard token
    """
    token = request.args.get('token')
    if not token:
        return jsonify({"error": "Token required"}), 400
    
    user = User.query.filter_by(dashboard_token=token).first()
    if not user:
        return jsonify({"error": "Invalid token"}), 404
    
    return jsonify({
        "balance": str(user.kubo_balance_eur + user.cluster_balance_eur),
        "kubo_balance": str(user.kubo_balance_eur),
        "cluster_balance": str(user.cluster_balance_eur)
    }), 200

@main.route('/api/pricing', methods=['GET'])
def get_pricing():
    """Get current pricing structure for IPFS Kubo pinning"""
    pricing_info = {
        "ipfs_kubo": {
            "note": "Same pricing for both private and public access",
            "private": {
                "1_month": {
                    "price_per_gb_month": str(KUBO_PRICING["private"][1]["price_per_gb_month"]),
                    "bandwidth_overage": str(KUBO_PRICING["private"][1]["bandwidth_overage"]),
                    "discount": KUBO_PRICING["private"][1]["discount"],
                    "use_case": "Testing, demos"
                },
                "2_months": {
                    "price_per_gb_month": str(KUBO_PRICING["private"][2]["price_per_gb_month"]),
                    "bandwidth_overage": str(KUBO_PRICING["private"][2]["bandwidth_overage"]),
                    "discount": KUBO_PRICING["private"][2]["discount"],
                    "use_case": "Small websites"
                },
                "6_months": {
                    "price_per_gb_month": str(KUBO_PRICING["private"][6]["price_per_gb_month"]),
                    "bandwidth_overage": str(KUBO_PRICING["private"][6]["bandwidth_overage"]),
                    "discount": KUBO_PRICING["private"][6]["discount"],
                    "use_case": "Medium projects (30% savings!)"
                },
                "12_months": {
                    "price_per_gb_month": str(KUBO_PRICING["private"][12]["price_per_gb_month"]),
                    "bandwidth_overage": str(KUBO_PRICING["private"][12]["bandwidth_overage"]),
                    "discount": KUBO_PRICING["private"][12]["discount"],
                    "use_case": "Large projects - Best Value! (50% savings!)"
                }
            },
            "public": {
                "1_month": {
                    "price_per_gb_month": str(KUBO_PRICING["public"][1]["price_per_gb_month"]),
                    "bandwidth_overage": str(KUBO_PRICING["public"][1]["bandwidth_overage"]),
                    "discount": KUBO_PRICING["public"][1]["discount"],
                    "use_case": "Testing"
                },
                "2_months": {
                    "price_per_gb_month": str(KUBO_PRICING["public"][2]["price_per_gb_month"]),
                    "bandwidth_overage": str(KUBO_PRICING["public"][2]["bandwidth_overage"]),
                    "discount": KUBO_PRICING["public"][2]["discount"],
                    "use_case": "Public websites"
                },
                "6_months": {
                    "price_per_gb_month": str(KUBO_PRICING["public"][6]["price_per_gb_month"]),
                    "bandwidth_overage": str(KUBO_PRICING["public"][6]["bandwidth_overage"]),
                    "discount": KUBO_PRICING["public"][6]["discount"],
                    "use_case": "CDN usage (30% savings!)"
                },
                "12_months": {
                    "price_per_gb_month": str(KUBO_PRICING["public"][12]["price_per_gb_month"]),
                    "bandwidth_overage": str(KUBO_PRICING["public"][12]["bandwidth_overage"]),
                    "discount": KUBO_PRICING["public"][12]["discount"],
                    "use_case": "Long-term CDN - Best Value! (50% savings!)"
                }
            }
        },
        "free_bandwidth_per_month_gb": str(FREE_BANDWIDTH_GB_PER_MONTH),
        "allowed_retention_months": ALLOWED_RETENTION_MONTHS,
        "currency": "EUR",
        "comparison": {
            "pinata_storage_price": "€0.14/GB/month",
            "you_are_cheaper_by": "29-64% depending on retention period"
        }
    }
    return jsonify(pricing_info), 200

@main.route('/register', methods=['POST', 'GET'])
def register():
    """
    Creates a new user and returns their credentials with IPFS access hash.
    GET: Shows terms acceptance form or welcome page (with ?welcome=token)
    POST: Creates account (implies terms acceptance)
    """
    
    # If GET request with welcome parameter, show welcome page
    if request.method == 'GET' and request.args.get('welcome'):
        return render_template('welcome.html', token=request.args.get('welcome'))
    
    # If GET request without welcome, show registration form
    if request.method == 'GET':
        return render_template('register_form.html')
    
    # POST request - create account
    try:
        api_secret = secrets.token_urlsafe(32)
        
        # Explicitly generate all required fields
        new_user = User()
        new_user.api_key = secrets.token_urlsafe(32)
        new_user.dashboard_token = secrets.token_urlsafe(32)
        new_user.ipfs_access_hash = secrets.token_urlsafe(48)
        
        # Now set the secret (uses api_key)
        new_user.set_api_secret(api_secret)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Build dashboard URL
        dashboard_url = f"https://datahosting.company/dashboard?token={new_user.dashboard_token}"
        welcome_url = f"https://datahosting.company/register?welcome={new_user.dashboard_token}"
        
        # Generate Bitcoin payment address immediately via SatSale
        bitcoin_address = None
        payment_uri = None
        qr_code_url = None
        
        try:
            import requests
            satsale_response = requests.get(
                "http://localhost:8000/api/createpayment",
                params={
                    "amount": 10,
                    "currency": "EUR",
                    "method": "onchain",
                    "w_url": f"http://localhost:5003/webhook/satsale?user_id={new_user.api_key}"
                },
                timeout=10
            )
            if satsale_response.status_code == 200:
                payment_data = satsale_response.json()
                # SatSale returns address nested in 'invoice' key
                invoice_data = payment_data.get("invoice", {})
                bitcoin_address = invoice_data.get("address")
                payment_uri = payment_data.get("payment_uri")
                qr_code_url = f"http://localhost:8000/api/qr/{bitcoin_address}" if bitcoin_address else None
        except Exception as payment_error:
            # Log error but don't fail registration
            import logging
            logging.error(f"Failed to generate payment address: {payment_error}")
            bitcoin_address = "ERROR - Visit dashboard for payment address"
        
        # Check if request wants HTML (from web form) or JSON (from API)
        accept_header = request.headers.get('Accept', '')
        is_web_request = 'text/html' in accept_header or request.form.get('web_form') == 'true'
        
        if is_web_request:
            # Redirect to welcome page for web users
            from flask import redirect
            return redirect(welcome_url)
        
        # Return JSON for API users with Bitcoin address included
        return jsonify({
            "success": True,
            "message": "Account created successfully!",
            "credentials": {
                "api_key": new_user.api_key,
                "api_secret": api_secret,
                "dashboard_token": new_user.dashboard_token,
                "ipfs_access_hash": new_user.ipfs_access_hash
            },
            "payment": {
                "bitcoin_address": bitcoin_address,
                "payment_uri": payment_uri,
                "qr_code_url": qr_code_url,
                "recommended_amount": "€10 to start (any amount works)",
                "note": "Send Bitcoin to this address to add credits"
            },
            "important": "⚠️ SAVE THESE CREDENTIALS NOW - They cannot be recovered!",
            "next_steps": {
                "1": f"💰 SEND BITCOIN NOW to: {bitcoin_address}",
                "2": "Recommended: €10+ to start (minimum €5)",
                "3": f"Check payment status: {dashboard_url}",
                "4": "Once payment confirms (usually 10-60 min), start uploading!",
                "5": "Or visit welcome page: {welcome_url}"
            },
            "dashboard_url": dashboard_url,
            "welcome_url": welcome_url,
            "api_documentation": "https://datahosting.company/",
            "pricing": {
                "storage_1month": "€0.10/GB",
                "storage_12months": "€0.05/GB (50% discount!)",
                "bandwidth_overage": "€0.08/GB",
                "free_bandwidth": "5 GB per month"
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create user", "details": str(e)}), 500

@main.route('/api/pins', methods=['POST'])
@require_api_key
def create_pin():
    """Handles file pinning, billing, and database recording for the Pinning Service."""
    user = request.user

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        retention_months = int(request.form.get('retention_months', 1))
        if retention_months not in ALLOWED_RETENTION_MONTHS:
            return jsonify({
                "error": f"retention_months must be one of {ALLOWED_RETENTION_MONTHS}",
                "allowed_values": ALLOWED_RETENTION_MONTHS
            }), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid retention_months format"}), 400

    is_private = request.form.get('private', 'false').lower() == 'true'

    temp_dir = os.path.join(os.path.dirname(current_app.root_path), 'temp_uploads')
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, file.filename)
    file.save(temp_path)
    
    file_size_bytes = os.path.getsize(temp_path)
    if file_size_bytes == 0:
        os.remove(temp_path)
        return jsonify({"error": "Cannot pin an empty file"}), 400

    file_size_gb = Decimal(file_size_bytes) / Decimal(BYTES_PER_GB)
    
    # NEW RETENTION-BASED PRICING: Get price based on retention and privacy
    access_type = "private" if is_private else "public"
    pricing = KUBO_PRICING[access_type][retention_months]
    price_per_gb_month = pricing["price_per_gb_month"]
    
    # PREPAID MODEL: Calculate upfront cost for entire retention period
    upfront_cost = file_size_gb * price_per_gb_month * retention_months
    
    # Use Kubo balance for IPFS Kubo pinning
    if user.kubo_balance_eur < upfront_cost:
        os.remove(temp_path)
        return jsonify({
            "error": "Insufficient credits in Kubo balance",
            "required_credits": str(upfront_cost),
            "current_kubo_balance": str(user.kubo_balance_eur),
            "pricing_details": {
                "file_size_gb": str(file_size_gb),
                "price_per_gb_month": str(price_per_gb_month),
                "retention_months": retention_months,
                "access_type": access_type
            }
        }), 402

    try:
        ipfs_add_cmd = ["ipfs", "add", "-Q", temp_path]
        result = subprocess.run(ipfs_add_cmd, capture_output=True, text=True, check=True)
        cid = result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        os.remove(temp_path)
        return jsonify({"error": "Failed to add file to IPFS node", "details": str(e)}), 500
    finally:
        os.remove(temp_path)

    try:
        # PREPAID MODEL: Charge upfront for entire retention period from Kubo balance
        user.kubo_balance_eur -= upfront_cost
        expire_at = datetime.utcnow() + timedelta(days=30 * retention_months)

        new_pin = Pin(
            user_id=user.id,
            cid=cid,
            file_name=file.filename,
            size_bytes=file_size_bytes,
            status='queued',
            is_private=is_private,
            ipfs_access_hash=user.ipfs_access_hash,  # Store user's unique hash for access validation
            expire_at=expire_at,
            already_charged=True,  # Mark as already charged to avoid double charging on re-pin
            retention_months=retention_months  # Store retention period
        )
        db.session.add(new_pin)

        ipfs_pin_cmd = ["ipfs-cluster-ctl", "pin", "add", cid]
        subprocess.run(ipfs_pin_cmd, check=True)
        
        new_pin.status = 'pinned'
        db.session.commit()

        return jsonify({
            "message": "File pinned successfully!",
            "cid": cid,
            "cost_charged": str(upfront_cost),
            "retention_months": retention_months,
            "pricing_tier": access_type,
            "price_per_gb_month": str(price_per_gb_month),
            "new_kubo_balance_eur": str(user.kubo_balance_eur),
            "free_bandwidth_per_month": str(FREE_BANDWIDTH_GB_PER_MONTH)
        }), 201

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        db.session.rollback()
        return jsonify({"error": "Failed to pin CID to cluster", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@main.route('/api/backups', methods=['POST'])
@require_api_key
def create_backup():
    """Handles file backups, billing, and database recording for the Backup Service."""
    user = request.user

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        retention_months = int(request.form.get('retention_months', 1))
        if not (1 <= retention_months <= 12):
            return jsonify({"error": "retention_months must be between 1 and 12"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid retention_months format"}), 400

    # Backups are always private by default as per requirements
    is_private = True

    temp_dir = os.path.join(os.path.dirname(current_app.root_path), 'temp_uploads')
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, file.filename)
    file.save(temp_path)
    
    file_size_bytes = os.path.getsize(temp_path)
    if file_size_bytes == 0:
        os.remove(temp_path)
        return jsonify({"error": "Cannot backup an empty file"}), 400

    # PAY-AS-YOU-GO CHANGE: Check for any positive balance instead of upfront cost.
    if user.credit_balance_eur <= 0:
        os.remove(temp_path)
        return jsonify({
            "error": "Insufficient credits. Please add funds to your account to back up files.",
            "current_balance": str(user.credit_balance_eur)
        }), 402

    try:
        # Add to IPFS to get CID
        ipfs_add_cmd = ["ipfs", "add", "-Q", temp_path]
        result = subprocess.run(ipfs_add_cmd, capture_output=True, text=True, check=True)
        cid = result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        os.remove(temp_path)
        return jsonify({"error": "Failed to add file to IPFS node for backup", "details": str(e)}), 500
    finally:
        os.remove(temp_path) # Clean up temp file

    try:
        # PAY-AS-YOU-GO CHANGE: Do not deduct cost upfront.
        # user.credit_balance_eur -= cost

        # Create Backup record
        new_backup = Backup(
            user_id=user.id,
            cid=cid,
            file_name=file.filename,
            size_bytes=file_size_bytes,
            status='active',
            is_private=is_private,
            retention_months=retention_months
        )
        db.session.add(new_backup)

        # Pin to cluster
        ipfs_pin_cmd = ["ipfs-cluster-ctl", "pin", "add", cid]
        subprocess.run(ipfs_pin_cmd, check=True)
        
        db.session.commit()

        return jsonify({
            "message": "File backup initiated successfully! Storage costs will be deducted monthly.",
            "cid": cid,
            "estimated_monthly_cost_eur": str((Decimal(file_size_bytes) / Decimal(BYTES_PER_GB)) * PRICE_PER_GB_MONTH_EUR_BACKUP)
        }), 201

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        db.session.rollback()
        return jsonify({"error": "Failed to pin CID to cluster for backup", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred during backup creation", "details": str(e)}), 500

@main.route('/api/backups/cancel', methods=['POST'])
@require_api_key
def cancel_backup_service():
    """Triggers a 7-day grace period for the user's backup service."""
    user = request.user

    if user.grace_period_ends_at is None:
        user.grace_period_ends_at = datetime.utcnow() + timedelta(days=7)
        db.session.commit()
        return jsonify({
            "message": "Backup service cancellation initiated. All backups and your account will be deleted in 7 days if no new activity/payment is made.",
            "grace_period_ends_at": user.grace_period_ends_at.isoformat()
        }), 200
    else:
        return jsonify({"message": "Grace period already active or initiated."}), 200


@main.route('/api/ipfs/validate', methods=['POST'])
def validate_access():
    """
    Validate IPFS access hash and CID ownership.
    Used by IPFS cluster or gateway to verify user has paid for access.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    ipfs_access_hash = data.get('ipfs_access_hash')
    cid = data.get('cid')
    
    if not ipfs_access_hash or not cid:
        return jsonify({"error": "ipfs_access_hash and cid are required"}), 400
    
    # Validate access
    validation = validate_ipfs_access(ipfs_access_hash, cid)
    
    if validation["valid"]:
        return jsonify({
            "valid": True,
            "user_id": validation["user_id"],
            "is_private": validation["is_private"],
            "file_size_bytes": validation["file_size_bytes"]
        }), 200
    else:
        return jsonify({
            "valid": False,
            "reason": validation["reason"]
        }), 403


# ========================================================================
# IPFS CLUSTER BACKUP ENDPOINTS
# ========================================================================

@main.route('/api/cluster/backup', methods=['POST'])
@require_auth
def create_cluster_backup(user):
    """
    Create IPFS Cluster backup with replica count.
    PREPAID MODEL: Customer chooses duration, charged upfront.
    """
    from .models import ClusterBackup, ReplicaHistory
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Get replica count (default: 1)
    replica_count = int(request.form.get('replica_count', 1))
    if replica_count not in [1, 2, 3]:
        return jsonify({"error": "replica_count must be 1, 2, or 3"}), 400
    
    # MONTHLY DEDUCTION MODEL: No retention_days needed
    # Customer adds balance, system deducts monthly until balance runs out
    # Optional: max_retention_days as safety limit
    max_retention_days = request.form.get('max_retention_days', None)
    if max_retention_days:
        try:
            max_retention_days = int(max_retention_days)
            if max_retention_days < 1 or max_retention_days > 365:
                return jsonify({"error": "max_retention_days must be between 1 and 365"}), 400
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid max_retention_days"}), 400
    
    # Save temp file
    temp_path = os.path.join('/tmp', secrets.token_hex(16))
    file.save(temp_path)
    
    try:
        file_size_bytes = os.path.getsize(temp_path)
        file_size_gb = Decimal(file_size_bytes) / Decimal(1024 * 1024 * 1024)
        
        # MONTHLY DEDUCTION: Calculate costs but don't charge upfront
        monthly_cost = file_size_gb * replica_count * PRICE_PER_GB_MONTH_EUR_BACKUP
        daily_cost = monthly_cost / 30
        
        # Check if user has any balance to start
        if user.credit_balance_eur <= 0:
            os.remove(temp_path)
            return jsonify({
                "error": "Insufficient credits. Please add funds to create cluster backup.",
                "monthly_cost": str(monthly_cost),
                "recommendation": "Add at least €10 to start using cluster backups"
            }), 402
        
        # Calculate how long current balance will last
        months_balance_lasts = float(user.credit_balance_eur / monthly_cost) if monthly_cost > 0 else 999
        days_balance_lasts = int(user.credit_balance_eur / daily_cost) if daily_cost > 0 else 99999
        
        # Add to IPFS cluster
        ipfs_add_cmd = ["ipfs", "add", "-q", temp_path]
        result = subprocess.run(ipfs_add_cmd, capture_output=True, text=True, check=True)
        cid = result.stdout.strip()
        
        # Pin to cluster with replication factor
        ipfs_pin_cmd = ["ipfs-cluster-ctl", "pin", "add", "--replication-min", str(replica_count), 
                        "--replication-max", str(replica_count), cid]
        subprocess.run(ipfs_pin_cmd, check=True)
        
        # MONTHLY DEDUCTION: No upfront charge, will be deducted monthly
        # Balance is checked, but not deducted now
        
        # Calculate optional expiration date
        expire_at = None
        if max_retention_days:
            expire_at = datetime.utcnow() + timedelta(days=max_retention_days)
        
        # Create backup record
        new_backup = ClusterBackup(
            user_id=user.id,
            cid=cid,
            file_name=file.filename,
            size_bytes=file_size_bytes,
            replica_count=replica_count,
            status='active',
            ipfs_access_hash=user.ipfs_access_hash,
            expire_at=expire_at,  # None = runs until balance depletes
            already_charged=False  # Will be charged monthly
        )
        db.session.add(new_backup)
        db.session.commit()
        
        os.remove(temp_path)
        
        # Calculate end of current month
        from calendar import monthrange
        now = datetime.utcnow()
        days_until_month_end = monthrange(now.year, now.month)[1] - now.day
        cost_until_month_end = daily_cost * days_until_month_end
        
        return jsonify({
            "message": "Cluster backup created! Monthly charges will be deducted from your balance.",
            "cid": cid,
            "file_name": file.filename,
            "size_gb": float(file_size_gb),
            "replica_count": replica_count,
            "billing_info": {
                "monthly_cost": str(monthly_cost),
                "daily_cost": str(daily_cost),
                "current_balance": str(user.credit_balance_eur),
                "balance_lasts": f"{months_balance_lasts:.1f} months ({days_balance_lasts} days)",
                "next_charge_date": "1st of next month",
                "cost_until_month_end": str(cost_until_month_end),
                "grace_period": "7 days after balance reaches €0"
            },
            "important": "Charged monthly on 1st. When balance hits €0, you have 7 days grace period to add credits before backup is deleted.",
            "expire_at": expire_at.isoformat() if expire_at else "Runs until balance depleted or manually deleted"
        }), 201
        
    except subprocess.CalledProcessError as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({"error": "Failed to create backup", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({"error": "Failed to create backup", "details": str(e)}), 500


@main.route('/api/cluster/backup/<int:backup_id>/replicas', methods=['PUT'])
@require_auth
def update_backup_replicas(user, backup_id):
    """
    Update replica count for an existing backup.
    Cost is prorated based on days with each replica count.
    """
    from .models import ClusterBackup
    from .cluster_billing import update_replica_count
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    new_replica_count = data.get('replica_count')
    if new_replica_count not in [1, 2, 3]:
        return jsonify({"error": "replica_count must be 1, 2, or 3"}), 400
    
    # Verify ownership
    backup = ClusterBackup.query.filter_by(id=backup_id, user_id=user.id).first()
    if not backup:
        return jsonify({"error": "Backup not found"}), 404
    
    if backup.status != 'active':
        return jsonify({"error": f"Backup is not active (status: {backup.status})"}), 400
    
    # Update replica count in IPFS cluster
    try:
        ipfs_pin_cmd = ["ipfs-cluster-ctl", "pin", "add", "--replication-min", str(new_replica_count),
                        "--replication-max", str(new_replica_count), backup.cid]
        subprocess.run(ipfs_pin_cmd, check=True)
        
        # Update database and record change
        if update_replica_count(backup_id, new_replica_count):
            return jsonify({
                "message": f"Replica count updated to {new_replica_count}",
                "backup_id": backup_id,
                "new_replica_count": new_replica_count,
                "billing_info": "Cost will be prorated based on days with each replica count."
            }), 200
        else:
            return jsonify({"error": "Failed to update replica count"}), 500
            
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to update replicas in cluster", "details": str(e)}), 500


@main.route('/api/cluster/backups', methods=['GET'])
@require_auth
def list_cluster_backups(user):
    """
    List all IPFS Cluster backups for the authenticated user.
    Shows current estimated costs.
    """
    from .models import ClusterBackup
    from .cluster_billing import get_estimated_monthly_cost
    
    backups = ClusterBackup.query.filter_by(user_id=user.id).all()
    
    backup_list = []
    for backup in backups:
        size_gb = Decimal(backup.size_bytes) / Decimal(1024 * 1024 * 1024)
        backup_list.append({
            "id": backup.id,
            "cid": backup.cid,
            "file_name": backup.file_name,
            "size_gb": float(size_gb),
            "replica_count": backup.replica_count,
            "status": backup.status,
            "created_at": backup.created_at.isoformat(),
            "last_billed_at": backup.last_billed_at.isoformat() if backup.last_billed_at else None
        })
    
    # Get estimated costs
    cost_info = get_estimated_monthly_cost(user.id)
    
    return jsonify({
        "backups": backup_list,
        "total_backups": len(backup_list),
        "estimated_monthly_cost": cost_info["total_estimated_cost"],
        "cost_details": cost_info["backups"],
        "current_balance": str(user.credit_balance_eur)
    }), 200


@main.route('/api/cluster/backup/<int:backup_id>', methods=['DELETE'])
@require_auth
def delete_cluster_backup(user, backup_id):
    """
    Delete IPFS Cluster backup.
    User will be charged for actual days stored (prorated).
    """
    from .models import ClusterBackup
    
    backup = ClusterBackup.query.filter_by(id=backup_id, user_id=user.id).first()
    if not backup:
        return jsonify({"error": "Backup not found"}), 404
    
    try:
        # Unpin from cluster
        ipfs_unpin_cmd = ["ipfs-cluster-ctl", "pin", "rm", backup.cid]
        subprocess.run(ipfs_unpin_cmd, check=True)
        
        # Delete from database
        db.session.delete(backup)
        db.session.commit()
        
        return jsonify({
            "message": "Backup deleted successfully",
            "info": "You will be charged for actual days stored at next billing cycle."
        }), 200
        
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to delete backup", "details": str(e)}), 500


# ========================================================================
# SATSALE WEBHOOK INTEGRATION
# ========================================================================

@main.route('/webhook/satsale', methods=['POST', 'GET'])
def satsale_webhook():
    """
    SatSale webhook endpoint for Bitcoin payments.
    Converts BTC payment to EUR and adds to user balance.
    """
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("Received SatSale webhook")
    
    # SatSale can send GET or POST
    data = {}
    if request.method == 'POST':
        if request.is_json:
            data = request.json
        else:
            data = request.form.to_dict()
    # GET parameters (SatSale often uses GET)
    data.update(request.args.to_dict())
    
    logger.info(f"Webhook data: {data}")
    
    # Extract payment details
    tx_id = data.get('id') or data.get('tx_id')
    amount_btc = data.get('btc_value') or data.get('amount')
    fiat_value_eur = data.get('fiat_value') or data.get('value')
    user_api_key = data.get('user_id') or data.get('api_key')  # Pass api_key in SatSale config
    
    # Validation
    if not all([tx_id, amount_btc, fiat_value_eur, user_api_key]):
        logger.error("Missing required payment data")
        return jsonify({
            "status": "error",
            "message": "Missing required fields: tx_id, amount_btc, fiat_value_eur, user_api_key"
        }), 400
    
    try:
        # Find user by API key
        user = User.query.filter_by(api_key=user_api_key).first()
        if not user:
            logger.error(f"User not found with api_key: {user_api_key}")
            return jsonify({"status": "error", "message": "User not found"}), 404
        
        # Check if payment already processed (prevent double-charging)
        from .models import Payment
        existing_payment = Payment.query.filter_by(tx_id=tx_id).first()
        if existing_payment:
            logger.warning(f"Payment {tx_id} already processed")
            return jsonify({"status": "success", "message": "Payment already processed"}), 200
        
        # Add credits to user balance (EUR)
        # FIXED: Add to kubo_balance_eur (for IPFS Kubo storage) instead of credit_balance_eur
        credit_amount = Decimal(str(fiat_value_eur))
        user.kubo_balance_eur += credit_amount
        
        # Record payment in database
        new_payment = Payment(
            tx_id=tx_id,
            user_id=user.id,
            amount=Decimal(str(amount_btc)),
            status='completed'
        )
        db.session.add(new_payment)
        
        # Create invoice record
        from .models import Invoice
        new_invoice = Invoice(
            user_id=user.id,
            payment_tx_id=tx_id,
            amount_eur=credit_amount
        )
        db.session.add(new_invoice)
        
        db.session.commit()
        
        logger.info(f"Payment {tx_id} processed successfully for user {user.id}. Added €{credit_amount}")
        
        return jsonify({
            "status": "success",
            "message": "Payment processed successfully",
            "user_id": user.id,
            "amount_eur": str(credit_amount),
            "new_balance": str(user.credit_balance_eur)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@main.route('/health/ipfs', methods=['GET'])
def ipfs_health():
    """
    Check IPFS node and cluster health.
    """
    health_status = {
        "ipfs_node": "unknown",
        "ipfs_cluster": "unknown",
        "swarm_peers": 0,
        "cluster_peers": 0,
        "errors": []
    }
    
    # Check IPFS node
    try:
        result = subprocess.run(["ipfs", "id"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            health_status["ipfs_node"] = "healthy"
        else:
            health_status["ipfs_node"] = "unhealthy"
            health_status["errors"].append("IPFS node not responding")
    except Exception as e:
        health_status["ipfs_node"] = "error"
        health_status["errors"].append(f"IPFS node error: {str(e)}")
    
    # Check swarm peers
    try:
        result = subprocess.run(["ipfs", "swarm", "peers"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            health_status["swarm_peers"] = len(result.stdout.strip().split('\n'))
    except Exception as e:
        health_status["errors"].append(f"Swarm check error: {str(e)}")
    
    # Check IPFS cluster
    try:
        result = subprocess.run(["ipfs-cluster-ctl", "peers", "ls"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            health_status["ipfs_cluster"] = "healthy"
            health_status["cluster_peers"] = len(result.stdout.strip().split('\n'))
        else:
            health_status["ipfs_cluster"] = "unhealthy"
            health_status["errors"].append("IPFS cluster not responding")
    except Exception as e:
        health_status["ipfs_cluster"] = "error"
        health_status["errors"].append(f"IPFS cluster error: {str(e)}")
    
    # Determine overall status
    if health_status["ipfs_node"] == "healthy" and health_status["ipfs_cluster"] == "healthy":
        overall_status = "healthy"
        status_code = 200
    elif health_status["ipfs_node"] == "healthy" or health_status["ipfs_cluster"] == "healthy":
        overall_status = "degraded"
        status_code = 200
    else:
        overall_status = "unhealthy"
        status_code = 503
    
    health_status["overall_status"] = overall_status
    
    return jsonify(health_status), status_code

