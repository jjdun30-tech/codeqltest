# test/hardcoded_aws_key.py
import boto3

# Vulnerable: hardcoded AWS access key & secret
AWS_ACCESS_KEY_ID = "AKIAEXAMPLEACCESSKEY12345"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def list_s3_buckets():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    resp = s3.list_buckets()
    return [b["Name"] for b in resp.get("Buckets", [])]

if __name__ == "__main__":
    print(list_s3_buckets())
