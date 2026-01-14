"""
Bandwidth tracking and charging module for IPFS Kubo
Tracks bandwidth usage and charges based on private/public network
"""

from decimal import Decimal
from .models import db, User
from datetime import datetime

# Pricing constants (should match routes.py)
PRICE_PER_GB_BANDWIDTH_PRIVATE = Decimal("0.02")  # €0.02/GB
PRICE_PER_GB_BANDWIDTH_PUBLIC = Decimal("0.10")   # €0.10/GB
FREE_BANDWIDTH_GB_PER_MONTH = Decimal("1.00")     # 1 GB free
BYTES_PER_GB = 1024 * 1024 * 1024


def track_bandwidth_usage(user_id, bytes_transferred, is_private):
    """
    Track bandwidth usage and charge user's credit balance.
    
    Args:
        user_id: User ID
        bytes_transferred: Number of bytes transferred
        is_private: True if private network, False if public
    
    Returns:
        dict: {
            "success": bool,
            "charged_amount": Decimal,
            "free_bandwidth_used": Decimal,
            "paid_bandwidth_used": Decimal,
            "new_balance": Decimal
        }
    """
    user = User.query.get(user_id)
    if not user:
        return {"success": False, "error": "User not found"}
    
    gb_transferred = Decimal(bytes_transferred) / Decimal(BYTES_PER_GB)
    
    # Calculate total bandwidth used this cycle
    total_used = user.bandwidth_used_private_gb + user.bandwidth_used_public_gb
    
    # Calculate free bandwidth remaining
    free_remaining = max(Decimal("0"), FREE_BANDWIDTH_GB_PER_MONTH - total_used)
    
    # Apply free bandwidth first
    free_used = min(gb_transferred, free_remaining)
    paid_used = gb_transferred - free_used
    
    # Calculate charge
    if paid_used > 0:
        if is_private:
            charge = paid_used * PRICE_PER_GB_BANDWIDTH_PRIVATE
        else:
            charge = paid_used * PRICE_PER_GB_BANDWIDTH_PUBLIC
        
        # Deduct from balance
        user.credit_balance_eur -= charge
    else:
        charge = Decimal("0")
    
    # Update usage tracking
    if is_private:
        user.bandwidth_used_private_gb += gb_transferred
    else:
        user.bandwidth_used_public_gb += gb_transferred
    
    db.session.commit()
    
    return {
        "success": True,
        "charged_amount": charge,
        "free_bandwidth_used": free_used,
        "paid_bandwidth_used": paid_used,
        "new_balance": user.credit_balance_eur,
        "total_bandwidth_used": total_used + gb_transferred
    }


def reset_bandwidth_cycle(user_id):
    """
    Reset bandwidth usage counters for a new billing cycle (monthly).
    Should be called monthly via cron job.
    """
    user = User.query.get(user_id)
    if not user:
        return False
    
    user.bandwidth_used_private_gb = Decimal("0")
    user.bandwidth_used_public_gb = Decimal("0")
    user.bandwidth_cycle_start = datetime.utcnow()
    db.session.commit()
    
    return True


def check_bandwidth_allowance(user_id, bytes_needed):
    """
    Check if user has enough bandwidth allowance (free + credit balance).
    
    Args:
        user_id: User ID
        bytes_needed: Bytes needed for download
    
    Returns:
        dict: {
            "allowed": bool,
            "reason": str (if not allowed),
            "estimated_cost": Decimal
        }
    """
    user = User.query.get(user_id)
    if not user:
        return {"allowed": False, "reason": "User not found"}
    
    gb_needed = Decimal(bytes_needed) / Decimal(BYTES_PER_GB)
    
    # Calculate free bandwidth remaining
    total_used = user.bandwidth_used_private_gb + user.bandwidth_used_public_gb
    free_remaining = max(Decimal("0"), FREE_BANDWIDTH_GB_PER_MONTH - total_used)
    
    # If within free allowance, always allow
    if gb_needed <= free_remaining:
        return {
            "allowed": True,
            "estimated_cost": Decimal("0"),
            "using_free_bandwidth": True
        }
    
    # Calculate cost for paid bandwidth (assume worst case - public pricing)
    paid_needed = gb_needed - free_remaining
    estimated_cost = paid_needed * PRICE_PER_GB_BANDWIDTH_PUBLIC
    
    # Check if user has enough balance
    if user.credit_balance_eur < estimated_cost:
        return {
            "allowed": False,
            "reason": "Insufficient credits for bandwidth",
            "estimated_cost": estimated_cost,
            "current_balance": user.credit_balance_eur,
            "required_balance": estimated_cost
        }
    
    return {
        "allowed": True,
        "estimated_cost": estimated_cost,
        "using_free_bandwidth": False
    }
