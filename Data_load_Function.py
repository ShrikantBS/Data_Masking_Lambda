import boto3
import snowflake.connector
import pandas as pd

s3 = boto3.client("s3")

SNOWFLAKE_CONN = {
    "user": "my_user",
    "password": "my_password",
    "account": "my_account"
}

def lambda_handler(event, context):
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        file_name = record['s3']['object']['key']
        
        # Download file from S3
        s3.download_file(bucket_name, file_name, f"/tmp/{file_name}")
        df = pd.read_csv(f"/tmp/{file_name}")

        # Load into Snowflake
        conn = snowflake.connector.connect(**SNOWFLAKE_CONN)
        for _, row in df.iterrows():
            sql = f"INSERT INTO masked_users (name, email, credit_card) VALUES ('{row['name']}', '{row['email']}', '{row['credit_card']}')"
            conn.cursor().execute(sql)
        
        conn.close()
        return {"status": "Success"}
