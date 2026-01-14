from datahosting import DataHostingClient

# Get credentials from https://datahosting.company/register
client = DataHostingClient(
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET"
)

# Upload file
result = client.upload_kubo("example.txt", retention_months=6)
print(f"Uploaded! CID: {result['cid']}")
