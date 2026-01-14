"""
IPFS Cluster Backup Billing Module
Daily cost calculation with replica tracking
NO managed fee - only storage × replicas × days
"""

from decimal import Decimal
from datetime import datetime, timedelta
from .models import db, User, ClusterBackup, ReplicaHistory

# Pricing constants
DAILY_RATE_PER_GB = Decimal("0.0005125")  # €0.0005125/GB/day
AVERAGE_DAYS_PER_MONTH = Decimal("30.4375")  # Average days in a month


def calculate_backup_cost(backup, from_date, to_date):
    """
    Calculate cost for a backup between two dates, accounting for replica changes.
    
    Args:
        backup: ClusterBackup object
        from_date: Start date for billing period
        to_date: End date for billing period
    
    Returns:
        Decimal: Total cost for the period
    """
    total_cost = Decimal("0")
    size_gb = Decimal(backup.size_bytes) / Decimal(1024 * 1024 * 1024)
    
    # Get all replica changes in this period
    replica_changes = ReplicaHistory.query.filter(
        ReplicaHistory.backup_id == backup.id,
        ReplicaHistory.changed_at >= from_date,
        ReplicaHistory.changed_at <= to_date
    ).order_by(ReplicaHistory.changed_at).all()
    
    # If no replica changes, use current replica count for entire period
    if not replica_changes:
        days = (to_date - from_date).total_seconds() / 86400
        total_cost = size_gb * Decimal(backup.replica_count) * DAILY_RATE_PER_GB * Decimal(days)
        return total_cost
    
    # Calculate cost for each period between replica changes
    current_date = from_date
    current_replicas = backup.replica_count
    
    # Start with the replica count before any changes
    first_change = replica_changes[0]
    if first_change.changed_at > from_date:
        # Find what the replica count was before first change
        prev_history = ReplicaHistory.query.filter(
            ReplicaHistory.backup_id == backup.id,
            ReplicaHistory.changed_at < from_date
        ).order_by(ReplicaHistory.changed_at.desc()).first()
        
        if prev_history:
            current_replicas = prev_history.replica_count
        else:
            current_replicas = 1  # Default starting replica count
    
    for change in replica_changes:
        # Calculate cost from current_date to change date
        days = (change.changed_at - current_date).total_seconds() / 86400
        period_cost = size_gb * Decimal(current_replicas) * DAILY_RATE_PER_GB * Decimal(days)
        total_cost += period_cost
        
        # Update for next period
        current_date = change.changed_at
        current_replicas = change.replica_count
    
    # Calculate cost from last change to end date
    days = (to_date - current_date).total_seconds() / 86400
    period_cost = size_gb * Decimal(current_replicas) * DAILY_RATE_PER_GB * Decimal(days)
    total_cost += period_cost
    
    return total_cost


def charge_monthly_cluster_backups():
    """
    Monthly billing for IPFS Cluster backups.
    Charges based on daily usage with replica tracking.
    NO managed fee - only storage costs.
    """
    print("Starting monthly IPFS Cluster backup billing...")
    
    now = datetime.utcnow()
    thirty_days_ago = now - timedelta(days=30)
    
    # Find all active backups that haven't been billed in last 30 days
    backups_to_bill = ClusterBackup.query.filter(
        ClusterBackup.status == 'active',
        db.or_(
            ClusterBackup.last_billed_at == None,
            ClusterBackup.last_billed_at <= thirty_days_ago
        )
    ).all()
    
    if not backups_to_bill:
        print("No backups to bill this month.")
        return
    
    # Group by user
    user_costs = {}
    for backup in backups_to_bill:
        # Determine billing period
        if backup.last_billed_at:
            from_date = backup.last_billed_at
        else:
            from_date = backup.created_at
        
        to_date = now
        
        # Calculate cost for this backup
        cost = calculate_backup_cost(backup, from_date, to_date)
        
        if backup.user_id not in user_costs:
            user_costs[backup.user_id] = Decimal("0")
        user_costs[backup.user_id] += cost
        
        # Update last_billed_at
        backup.last_billed_at = now
        db.session.add(backup)
        
        print(f"  Backup {backup.id}: {backup.file_name}")
        print(f"    Size: {backup.size_bytes / (1024**3):.2f} GB")
        print(f"    Replicas: {backup.replica_count}")
        print(f"    Period: {from_date} to {to_date}")
        print(f"    Cost: €{cost:.2f}")
    
    # Charge each user
    for user_id, total_cost in user_costs.items():
        user = User.query.get(user_id)
        if user:
            print(f"\nCharging User {user_id}: €{total_cost:.2f}")
            user.credit_balance_eur -= total_cost
            db.session.add(user)
    
    db.session.commit()
    print(f"\nMonthly IPFS Cluster backup billing finished. Billed {len(user_costs)} users.")


def get_estimated_monthly_cost(user_id):
    """
    Calculate estimated monthly cost for a user's active backups.
    Shows what they would pay if billed today.
    
    Args:
        user_id: User ID
    
    Returns:
        dict: {
            "total_estimated_cost": Decimal,
            "backups": [
                {
                    "id": int,
                    "file_name": str,
                    "size_gb": Decimal,
                    "replica_count": int,
                    "estimated_cost": Decimal
                }
            ]
        }
    """
    backups = ClusterBackup.query.filter_by(user_id=user_id, status='active').all()
    
    if not backups:
        return {
            "total_estimated_cost": Decimal("0"),
            "backups": []
        }
    
    now = datetime.utcnow()
    total_cost = Decimal("0")
    backup_details = []
    
    for backup in backups:
        # Calculate from last billing or creation
        if backup.last_billed_at:
            from_date = backup.last_billed_at
        else:
            from_date = backup.created_at
        
        cost = calculate_backup_cost(backup, from_date, now)
        total_cost += cost
        
        size_gb = Decimal(backup.size_bytes) / Decimal(1024 * 1024 * 1024)
        
        backup_details.append({
            "id": backup.id,
            "file_name": backup.file_name,
            "size_gb": float(size_gb),
            "replica_count": backup.replica_count,
            "estimated_cost": float(cost),
            "days_since_last_bill": (now - from_date).days
        })
    
    return {
        "total_estimated_cost": float(total_cost),
        "backups": backup_details
    }


def update_replica_count(backup_id, new_replica_count):
    """
    Update replica count for a backup and record change in history.
    
    Args:
        backup_id: ClusterBackup ID
        new_replica_count: New replica count (1, 2, or 3)
    
    Returns:
        bool: Success
    """
    if new_replica_count not in [1, 2, 3]:
        return False
    
    backup = ClusterBackup.query.get(backup_id)
    if not backup:
        return False
    
    # Record the change in history
    history = ReplicaHistory(
        backup_id=backup_id,
        replica_count=new_replica_count,
        changed_at=datetime.utcnow()
    )
    db.session.add(history)
    
    # Update current replica count
    backup.replica_count = new_replica_count
    db.session.add(backup)
    
    db.session.commit()
    return True
