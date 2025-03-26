## 🚀 Automating Data Masking & Export with AWS Lambda
---
## 📌 Overview of Serverless Data Masking Pipeline
#### Lambda extracts data from a database (PostgreSQL, MySQL, DynamoDB).
#### Data is masked in Lambda using Python (Faker, Regex).
#### Masked data is stored in AWS S3 or sent to Snowflake/Redshift.
#### S3 triggers another Lambda function to load data into analytics systems.
#### (Optional) SNS or Slack notifications for monitoring.
---
##  Architecture
#### 🔹 Trigger: AWS EventBridge (runs Lambda every X hours/days).
#### 🔹 Lambda Function: Extracts & masks data.
#### 🔹 Storage: S3 Bucket for masked data storage.
#### 🔹 Data Warehouse Integration: Snowflake, Redshift, RDS, or DynamoDB.
#### 🔹 Notifications: SNS/Slack alert on job success or failure.
