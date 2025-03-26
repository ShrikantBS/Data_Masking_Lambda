import boto3
import pandas as pd
import psycopg2
import re
from faker import Faker
import os

fake = Faker()
s3 = boto3.client('s3')

# Environment variables for DB credentials (stored in AWS Secrets Manager or Lambda env variables)
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = "mydatabase"
S3_BUCKET = "masked-data-exports"

# Masking functions
def mask_email(email):
    return fake.email()

def mask_credit_card(card_number):
    return re.sub(r"\d", "*", card_number[:-4]) + card_number[-4:]

def mask_data(df):
    df["name"] = df["name"].apply(lambda x: fake.name())
    df["email"] = df["email"].apply(mask_email)
    df["credit_card"] = df["credit_card"].apply(mask_credit_card)
    return df

def lambda_handler(event, context):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME)
        df = pd.read_sql("SELECT id, name, email, credit_card FROM users", conn)
        conn.close()

        # Apply masking
        df = mask_data(df)

        # Save to CSV and upload to S3
        file_name = f"masked_data_{pd.Timestamp.now().date()}.csv"
        df.to_csv(f"/tmp/{file_name}", index=False)
        s3.upload_file(f"/tmp/{file_name}", S3_BUCKET, file_name)

        return {
            "status": "Success",
            "file_uploaded": file_name
        }

    except Exception as e:
        return {
            "status": "Failed",
            "error": str(e)
        }
