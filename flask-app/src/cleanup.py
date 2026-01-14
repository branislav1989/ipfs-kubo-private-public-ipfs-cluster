from .app import create_app
from .models import db, User, Pin, ClusterBackup
from datetime import datetime, timedelta
import subprocess

def unpin_cid(cid):
    """Executes the ipfs-cluster-ctl pin rm command."""
    try:
        subprocess.run(["ipfs-cluster-ctl", "pin", "rm", cid], check=True, capture_output=True, text=True)
        print(f"Successfully unpinned CID: {cid}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error unpinning CID {cid}: {e.stderr if hasattr(e, 'stderr') else e}")
        return False

def repin_cid(cid):
    """Executes the ipfs-cluster-ctl pin add command."""
    try:
        subprocess.run(["ipfs-cluster-ctl", "pin", "add", cid], check=True, capture_output=True, text=True)
        print(f"Successfully re-pinned CID: {cid}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error re-pinning CID {cid}: {e.stderr if hasattr(e, 'stderr') else e}")
        return False

def manage_pin_expiration():
    """
    Manages automatic unpinning of pins that reached their retention period (expire_at).
    - Unpins files when expire_at date is reached
    - Deletes pin records from database
    """
    print("Starting pin expiration management...")
    
    # Find all pins where expire_at has passed
    now = datetime.utcnow()
    expired_pins = Pin.query.filter(Pin.status == 'pinned', Pin.expire_at <= now).all()
    
    for pin in expired_pins:
        print(f"Pin {pin.cid} retention period expired (expire_at: {pin.expire_at}). Unpinning and deleting.")
        if unpin_cid(pin.cid):
            db.session.delete(pin)
        else:
            print(f"Failed to unpin {pin.cid}, but will delete record anyway.")
            db.session.delete(pin)
    
    db.session.commit()
    print("Pin expiration management finished.")


def manage_pin_grace_periods():
    """
    Manages the grace period for pins when user balance reaches zero.
    - Initiates grace period if user balance is <= 0.
    - Re-pins content if user adds credit during grace period (FREE).
    - Deletes user + all data after 7 days grace period.
    """
    print("Starting pin grace period management...")
    
    # 1. Handle users with depleted credit
    users_with_no_credit = User.query.filter(User.credit_balance_eur <= 0).all()
    for user in users_with_no_credit:
        active_pins = Pin.query.filter_by(user_id=user.id, status='pinned').all()
        for pin in active_pins:
            print(f"User {user.id} has no credit. Moving pin {pin.cid} to grace period.")
            if unpin_cid(pin.cid):
                pin.status = 'grace_period'
                pin.grace_period_started_at = datetime.utcnow()
                db.session.add(pin)

    # 2. Handle users in grace period who have re-added credit (FREE re-pinning)
    pins_in_grace_period = Pin.query.filter_by(status='grace_period').all()
    for pin in pins_in_grace_period:
        if pin.user.credit_balance_eur > 0:
            print(f"User {pin.user.id} has added credit. Re-pinning {pin.cid} (FREE - already paid).")
            if repin_cid(pin.cid):
                pin.status = 'pinned'
                pin.grace_period_started_at = None # Clear the grace period start time
                # NOTE: already_charged remains True, no additional charge for re-pinning
                db.session.add(pin)

    # 3. Handle expired grace periods (7 days) - DELETE USER + ALL DATA
    grace_period_limit = datetime.utcnow() - timedelta(days=7)
    expired_pins = Pin.query.filter(Pin.status == 'grace_period', Pin.grace_period_started_at <= grace_period_limit).all()
    
    # Track users to delete (users with expired grace periods)
    users_to_delete = set()
    for pin in expired_pins:
        print(f"Grace period for pin {pin.cid} has expired. Will delete user {pin.user_id} and all data.")
        users_to_delete.add(pin.user_id)
        # The content is already unpinned, so we just delete the database record.
        db.session.delete(pin)
    
    # Delete entire user accounts after 7 days grace period
    for user_id in users_to_delete:
        user = User.query.get(user_id)
        if user:
            print(f"Deleting user {user_id} and all associated data (7 days grace period expired).")
            # Delete all user's pins (cascade should handle this, but explicit is safer)
            Pin.query.filter_by(user_id=user_id).delete()
            # Delete user invoices
            from .models import Invoice
            Invoice.query.filter_by(user_id=user_id).delete()
            # Delete user account
            db.session.delete(user)
        
    db.session.commit()
    print("Pin grace period management finished.")

# NOTE: charge_monthly_pin_storage() REMOVED
# IPFS Kubo uses PREPAID model - charges upfront when file is pinned
# No monthly billing needed for pin storage


def charge_monthly_backup_storage():
    """
    Charges users for their total stored private backup data on a monthly basis.
    """
    print("Starting monthly backup billing...")
    
    from decimal import Decimal
    
    # Configuration constants from routes
    PRICE_PER_GB_MONTH_EUR_BACKUP = Decimal("0.0156")
    BYTES_PER_GB = Decimal(1024 * 1024 * 1024)
    
    # Find users who haven't been billed in the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    users_to_bill = User.query.filter(
        (User.last_backup_billing_date == None) | (User.last_backup_billing_date <= thirty_days_ago)
    ).all()

    for user in users_to_bill:
        total_size_bytes = db.session.query(db.func.sum(Backup.size_bytes)).filter_by(user_id=user.id, status='active').scalar()
        
        if total_size_bytes is None or total_size_bytes == 0:
            # No active backups, just update billing date to prevent re-checking for 30 days
            user.last_backup_billing_date = datetime.utcnow()
            print(f"User {user.id} has no active backups. Billing date updated.")
            continue

        total_size_gb = Decimal(total_size_bytes) / BYTES_PER_GB
        monthly_cost = total_size_gb * PRICE_PER_GB_MONTH_EUR_BACKUP
        
        print(f"Billing User {user.id} for {total_size_gb:.4f} GB of backup storage. Cost: €{monthly_cost:.4f}")
        
        user.credit_balance_eur -= monthly_cost
        user.last_backup_billing_date = datetime.utcnow()
        db.session.add(user)

    db.session.commit()
    print("Monthly backup billing finished.")


def reset_monthly_bandwidth():
    """
    Reset bandwidth usage counters for all users (runs monthly).
    Resets bandwidth_used_private_gb and bandwidth_used_public_gb to 0.
    Users get 1 GB free bandwidth per month.
    """
    print("Starting monthly bandwidth reset...")
    
    from datetime import timedelta
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    # Find users whose bandwidth cycle started more than 30 days ago
    users_to_reset = User.query.filter(
        (User.bandwidth_cycle_start == None) | (User.bandwidth_cycle_start <= thirty_days_ago)
    ).all()
    
    for user in users_to_reset:
        print(f"Resetting bandwidth for user {user.id}")
        user.bandwidth_used_private_gb = 0.00
        user.bandwidth_used_public_gb = 0.00
        user.bandwidth_cycle_start = datetime.utcnow()
        db.session.add(user)
    
    db.session.commit()
    print(f"Monthly bandwidth reset finished. Reset {len(users_to_reset)} users.")


def manage_cluster_backup_expiration():
    """
    Manages automatic deletion of IPFS Cluster backups that reached their retention period.
    PREPAID model - no billing, just delete expired backups.
    """
    print("Starting cluster backup expiration management...")
    from .models import ClusterBackup
    
    # Find all backups where expire_at has passed
    now = datetime.utcnow()
    expired_backups = ClusterBackup.query.filter(
        ClusterBackup.status == 'active',
        ClusterBackup.expire_at <= now
    ).all()
    
    for backup in expired_backups:
        print(f"Cluster backup {backup.id} ({backup.file_name}) retention period expired. Deleting.")
        try:
            # Unpin from IPFS cluster
            ipfs_unpin_cmd = ["ipfs-cluster-ctl", "pin", "rm", backup.cid]
            subprocess.run(ipfs_unpin_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to unpin {backup.cid}, but will delete record anyway: {e}")
        
        # Delete from database
        db.session.delete(backup)
    
    db.session.commit()
    print(f"Cluster backup expiration management finished. Deleted {len(expired_backups)} backups.")


def run_cleanup():
    """Main function to run all cleanup tasks."""
    app = create_app()
    with app.app_context():
        manage_pin_expiration()              # Unpin IPFS Kubo files after retention period
        manage_cluster_backup_expiration()   # Delete IPFS Cluster backups after retention period (PREPAID)
        manage_pin_grace_periods()           # Handle grace period when balance=0 (7 days, then delete user)
        reset_monthly_bandwidth()            # Reset bandwidth counters monthly (1 GB free per month)
        charge_monthly_backup_storage()      # Monthly billing for backup service (legacy)
        # Note: NO monthly billing for IPFS Kubo or IPFS Cluster - both are PREPAID

if __name__ == "__main__":
    run_cleanup()