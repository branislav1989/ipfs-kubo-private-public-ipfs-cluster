"""
IPFS Access Control Module
Validates user's ipfs_access_hash before allowing IPFS cluster operations
Prevents billing evasion by ensuring all IPFS access goes through billing system
"""

from .models import db, User, Pin
from flask import jsonify


def validate_ipfs_access(ipfs_access_hash, cid):
    """
    Validate if a user has permission to access a specific CID.
    
    Args:
        ipfs_access_hash: User's unique IPFS access hash
        cid: Content identifier to access
    
    Returns:
        dict: {
            "valid": bool,
            "user_id": int (if valid),
            "is_private": bool (if valid),
            "reason": str (if invalid)
        }
    """
    # Check if hash exists
    user = User.query.filter_by(ipfs_access_hash=ipfs_access_hash).first()
    if not user:
        return {
            "valid": False,
            "reason": "Invalid IPFS access hash"
        }
    
    # Check if user has positive balance
    if user.credit_balance_eur <= 0:
        return {
            "valid": False,
            "reason": "Insufficient credits. Please add funds to your account."
        }
    
    # Check if pin exists and belongs to this user
    pin = Pin.query.filter_by(cid=cid, ipfs_access_hash=ipfs_access_hash).first()
    if not pin:
        return {
            "valid": False,
            "reason": "CID not found or access denied"
        }
    
    # Check if pin is active (not in grace period or expired)
    if pin.status != 'pinned':
        return {
            "valid": False,
            "reason": f"Pin is not active (status: {pin.status})"
        }
    
    return {
        "valid": True,
        "user_id": user.id,
        "is_private": pin.is_private,
        "pin_id": pin.id,
        "file_size_bytes": pin.size_bytes
    }


def get_user_by_ipfs_hash(ipfs_access_hash):
    """
    Get user by IPFS access hash.
    
    Args:
        ipfs_access_hash: User's unique IPFS access hash
    
    Returns:
        User object or None
    """
    return User.query.filter_by(ipfs_access_hash=ipfs_access_hash).first()


def list_user_pins_by_hash(ipfs_access_hash):
    """
    List all active pins for a user by their IPFS access hash.
    
    Args:
        ipfs_access_hash: User's unique IPFS access hash
    
    Returns:
        list: List of Pin objects
    """
    return Pin.query.filter_by(
        ipfs_access_hash=ipfs_access_hash,
        status='pinned'
    ).all()


def verify_pin_ownership(ipfs_access_hash, cid):
    """
    Verify that a CID belongs to the user with the given IPFS access hash.
    
    Args:
        ipfs_access_hash: User's unique IPFS access hash
        cid: Content identifier
    
    Returns:
        bool: True if user owns the pin, False otherwise
    """
    pin = Pin.query.filter_by(
        ipfs_access_hash=ipfs_access_hash,
        cid=cid
    ).first()
    
    return pin is not None
