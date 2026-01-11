"""
Customer Dashboard Routes
"""
from flask import Blueprint, render_template, request, jsonify
from src.models import db, User, Pin, Payment, ClusterBackup
from decimal import Decimal
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
def customer_dashboard():
    """
    Customer billing dashboard
    Access via: https://datahosting.company/dashboard?token=DASHBOARD_TOKEN
    """
    import requests
    import logging
    
    # Get dashboard token from query string
    token = request.args.get('token')
    
    if not token:
        return jsonify({
            "error": "Missing dashboard token",
            "usage": "Access via: /dashboard?token=YOUR_DASHBOARD_TOKEN"
        }), 401
    
    # Find user by dashboard token
    user = User.query.filter_by(dashboard_token=token).first()
    
    if not user:
        return jsonify({"error": "Invalid dashboard token"}), 401
    
    # Get user's pins (IPFS Kubo)
    pins = Pin.query.filter_by(user_id=user.id).order_by(Pin.created_at.desc()).all()
    
    # Get user's cluster backups
    cluster_backups = ClusterBackup.query.filter_by(user_id=user.id).order_by(ClusterBackup.created_at.desc()).all()
    
    # Calculate total storage (Kubo pins)
    total_storage_bytes = sum(pin.size_bytes for pin in pins)
    total_storage_gb = float(total_storage_bytes) / (1024 ** 3)
    
    # Calculate total cluster backup storage
    total_cluster_bytes = sum(backup.size_bytes for backup in cluster_backups)
    total_cluster_gb = float(total_cluster_bytes) / (1024 ** 3)
    
    # Calculate daily and monthly cluster costs
    daily_cluster_cost = Decimal("0")
    monthly_cluster_cost = Decimal("0")
    cluster_backups_with_info = []
    grace_period_backups = []
    
    for backup in cluster_backups:
        size_gb = Decimal(backup.size_bytes) / Decimal(1024 ** 3)
        monthly_cost = size_gb * backup.replica_count * Decimal("0.0156")
        daily_cost = monthly_cost / 30
        
        if backup.status in ['active', 'grace_period']:
            daily_cluster_cost += daily_cost
            monthly_cluster_cost += monthly_cost
            
            # Calculate days remaining until expiration
            if backup.expire_at:
                days_remaining = (backup.expire_at - datetime.utcnow()).days
                if days_remaining < 0:
                    days_remaining = 0
            else:
                days_remaining = None
            
            backup_info = {
                'backup': backup,
                'daily_cost': float(daily_cost),
                'monthly_cost': float(monthly_cost),
                'days_remaining': days_remaining
            }
            
            if backup.status == 'grace_period':
                # Calculate grace period days left
                grace_days_elapsed = (datetime.utcnow() - backup.updated_at).days
                grace_days_left = max(0, 7 - grace_days_elapsed)
                backup_info['grace_days_left'] = grace_days_left
                grace_period_backups.append(backup_info)
            else:
                cluster_backups_with_info.append(backup_info)
    
    # Calculate how many days current balance can sustain all backups
    if daily_cluster_cost > 0:
        days_balance_lasts = int(user.credit_balance_eur / daily_cluster_cost)
        months_balance_lasts = float(user.credit_balance_eur / monthly_cluster_cost)
    else:
        days_balance_lasts = 999999  # Infinite (no active backups)
        months_balance_lasts = 999
    
    # Calculate end of current month
    from calendar import monthrange
    now = datetime.utcnow()
    days_in_month = monthrange(now.year, now.month)[1]
    days_until_month_end = days_in_month - now.day
    cost_until_month_end = float(daily_cluster_cost * days_until_month_end)
    
    # Calculate how much to add to reach end of month
    if cost_until_month_end > float(user.credit_balance_eur):
        amount_to_add_for_month = cost_until_month_end - float(user.credit_balance_eur)
    else:
        amount_to_add_for_month = 0
    
    # Get recent pins (last 10)
    recent_pins = pins[:10]
    
    # Get recent cluster backups (last 10)
    recent_cluster_backups = cluster_backups[:10]
    
    # Get payment history
    recent_payments = Payment.query.filter_by(user_id=user.id).order_by(Payment.created_at.desc()).limit(10).all()
    
    # Generate Bitcoin payment address via SatSale
    btc_address = None
    btc_qr_url = None
    payment_amount = 10  # Default suggested amount in EUR
    
    try:
        # Create a payment request with SatSale
        webhook_url = f"http://localhost:5003/webhook/satsale?user_id={user.id}"
        satsale_url = f"http://localhost:5004/api/createpayment?amount={payment_amount}&currency=EUR&method=onchain&w_url={webhook_url}"
        
        response = requests.get(satsale_url, timeout=5)
        
        if response.status_code == 200:
            invoice_data = response.json()
            if 'invoice' in invoice_data:
                invoice = invoice_data['invoice']
                btc_address = invoice.get('address')
                btc_amount = invoice.get('btc_value')
                invoice_uuid = invoice.get('uuid')
                
                # Generate QR code URL
                if btc_address:
                    btc_qr_url = f"http://localhost:5004/static/qr_codes/{invoice_uuid}.png"
                    logging.info(f"Generated Bitcoin address {btc_address} for user {user.id}")
            else:
                logging.warning(f"No invoice in SatSale response: {invoice_data}")
        else:
            logging.error(f"SatSale returned status {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to connect to SatSale: {e}")
        btc_address = "Service temporarily unavailable. Please try refreshing the page."
    except Exception as e:
        logging.error(f"Error generating Bitcoin address: {e}")
        btc_address = "Error generating payment address"
    
    # Render dashboard template
    return render_template('dashboard.html',
        user=user,
        total_storage_gb=total_storage_gb,
        total_files=len(pins),
        recent_pins=recent_pins,
        total_cluster_gb=total_cluster_gb,
        total_cluster_backups=len([b for b in cluster_backups if b.status in ['active', 'grace_period']]),
        cluster_backups_with_info=cluster_backups_with_info,
        grace_period_backups=grace_period_backups,
        daily_cluster_cost=float(daily_cluster_cost),
        monthly_cluster_cost=float(monthly_cluster_cost),
        days_balance_lasts=days_balance_lasts,
        months_balance_lasts=months_balance_lasts,
        cost_until_month_end=cost_until_month_end,
        amount_to_add_for_month=amount_to_add_for_month,
        days_until_month_end=days_until_month_end,
        recent_payments=recent_payments,
        btc_address=btc_address,
        btc_qr_url=btc_qr_url,
        payment_amount=payment_amount
    )


@dashboard_bp.route('/dashboard/stats', methods=['GET'])
def dashboard_stats():
    """
    API endpoint for dashboard statistics
    Returns JSON with user stats
    """
    token = request.args.get('token')
    
    if not token:
        return jsonify({"error": "Missing dashboard token"}), 401
    
    user = User.query.filter_by(dashboard_token=token).first()
    
    if not user:
        return jsonify({"error": "Invalid dashboard token"}), 401
    
    # Get user's pins
    pins = Pin.query.filter_by(user_id=user.id).all()
    
    # Calculate statistics
    total_storage_bytes = sum(pin.size_bytes for pin in pins)
    total_storage_gb = float(total_storage_bytes) / (1024 ** 3)
    
    # Count file types
    public_files = sum(1 for pin in pins if not pin.is_private)
    private_files = sum(1 for pin in pins if pin.is_private)
    
    # Storage by type
    public_storage = sum(pin.size_bytes for pin in pins if not pin.is_private) / (1024 ** 3)
    private_storage = sum(pin.size_bytes for pin in pins if pin.is_private) / (1024 ** 3)
    
    # Calculate estimated monthly cost
    storage_cost = Decimal(total_storage_gb) * Decimal("0.07")
    
    # Estimate bandwidth cost (using average)
    avg_bandwidth_cost = (
        (user.bandwidth_used_private_gb * Decimal("0.02")) +
        (user.bandwidth_used_public_gb * Decimal("0.10"))
    )
    
    estimated_monthly_cost = float(storage_cost + avg_bandwidth_cost)
    
    return jsonify({
        "balance": {
            "current_eur": float(user.credit_balance_eur),
            "low_balance_warning": float(user.credit_balance_eur) < 1.0
        },
        "storage": {
            "total_gb": round(total_storage_gb, 2),
            "public_gb": round(public_storage, 2),
            "private_gb": round(private_storage, 2),
            "total_files": len(pins),
            "public_files": public_files,
            "private_files": private_files
        },
        "bandwidth": {
            "private_used_gb": float(user.bandwidth_used_private_gb),
            "public_used_gb": float(user.bandwidth_used_public_gb),
            "free_allowance_gb": float(user.bandwidth_allowance_gb),
            "cycle_start": user.bandwidth_cycle_start.isoformat() if user.bandwidth_cycle_start else None
        },
        "costs": {
            "storage_monthly_eur": float(storage_cost),
            "bandwidth_current_eur": float(avg_bandwidth_cost),
            "estimated_monthly_total_eur": estimated_monthly_cost
        },
        "account": {
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "api_key": user.api_key
        }
    })


@dashboard_bp.route('/dashboard/files', methods=['GET'])
def dashboard_files():
    """
    API endpoint to list all user files
    """
    token = request.args.get('token')
    
    if not token:
        return jsonify({"error": "Missing dashboard token"}), 401
    
    user = User.query.filter_by(dashboard_token=token).first()
    
    if not user:
        return jsonify({"error": "Invalid dashboard token"}), 401
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    # Get user's pins with pagination
    pagination = Pin.query.filter_by(user_id=user.id).order_by(Pin.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    files = []
    for pin in pagination.items:
        files.append({
            "cid": pin.cid,
            "file_name": pin.file_name,
            "size_bytes": pin.size_bytes,
            "size_mb": round(pin.size_bytes / (1024 ** 2), 2),
            "is_private": pin.is_private,
            "status": pin.status,
            "created_at": pin.created_at.isoformat() if pin.created_at else None,
            "expire_at": pin.expire_at.isoformat() if pin.expire_at else None,
            "url": f"https://ipfs.datahosting.company/ipfs/{pin.cid}" if not pin.is_private else f"https://private.datahosting.company/ipfs/{pin.cid}"
        })
    
    return jsonify({
        "files": files,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    })


@dashboard_bp.route('/dashboard/payments', methods=['GET'])
def dashboard_payments():
    """
    API endpoint to list payment history
    """
    token = request.args.get('token')
    
    if not token:
        return jsonify({"error": "Missing dashboard token"}), 401
    
    user = User.query.filter_by(dashboard_token=token).first()
    
    if not user:
        return jsonify({"error": "Invalid dashboard token"}), 401
    
    # Get payment history
    payments = Payment.query.filter_by(user_id=user.id).order_by(Payment.created_at.desc()).limit(50).all()
    
    payment_list = []
    for payment in payments:
        payment_list.append({
            "tx_id": payment.tx_id,
            "amount_eur": float(payment.amount),
            "status": payment.status,
            "created_at": payment.created_at.isoformat() if payment.created_at else None
        })
    
    return jsonify({
        "payments": payment_list,
        "total_payments": len(payment_list)
    })
