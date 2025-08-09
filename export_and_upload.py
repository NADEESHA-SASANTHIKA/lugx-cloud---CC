import boto3
import subprocess
from datetime import datetime

# S3 settings
bucket_name = 'lugx-clickhouse-export'
s3_key = f'clickhouse-exports/events_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
local_file = '/tmp/events.csv'

# Run ClickHouse export inside the pod
print("Exporting data from ClickHouse...")
pod_name = subprocess.getoutput('kubectl get pod -l app=clickhouse -o jsonpath="{.items[0].metadata.name}"')
cmd = f'kubectl exec -i {pod_name} -- clickhouse-client --query="SELECT * FROM analytics.events FORMAT CSV" > {local_file}'
subprocess.run(cmd, shell=True, check=True)

# Upload to S3
print("Uploading to S3...")
s3 = boto3.client('s3')
s3.upload_file(local_file, bucket_name, s3_key)
print(f"✅ Uploaded {s3_key} to S3 bucket {bucket_name}")
