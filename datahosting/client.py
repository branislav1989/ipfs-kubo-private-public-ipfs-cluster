import requests
from typing import Optional, Dict, Any

class DataHostingClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://datahosting.company"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-KEY': api_key,
            'X-API-SECRET': api_secret
        })
    
    def upload_kubo(self, file_path: str, is_private: bool = False, retention_months: int = 1) -> Dict:
        """Upload file to IPFS Kubo"""
        with open(file_path, 'rb') as f:
            response = self.session.post(
                f'{self.base_url}/pin',
                files={'file': f},
                data={'is_private': str(is_private).lower(), 'retention_months': retention_months}
            )
        response.raise_for_status()
        return response.json()
    
    def upload_cluster(self, file_path: str, replica_count: int = 2) -> Dict:
        """Upload file to IPFS Cluster"""
        with open(file_path, 'rb') as f:
            response = self.session.post(
                f'{self.base_url}/cluster/upload',
                files={'file': f},
                data={'replica_count': replica_count}
            )
        response.raise_for_status()
        return response.json()
    
    def get_balance(self) -> Dict:
        """Get account balance"""
        response = self.session.get(f'{self.base_url}/dashboard/balance')
        response.raise_for_status()
        return response.json()
    
    def list_pins(self) -> list:
        """List Kubo pins"""
        response = self.session.get(f'{self.base_url}/pins')
        response.raise_for_status()
        return response.json()
    
    def list_cluster_backups(self) -> list:
        """List Cluster backups"""
        response = self.session.get(f'{self.base_url}/cluster/backups')
        response.raise_for_status()
        return response.json()
