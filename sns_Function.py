import boto3

sns = boto3.client('sns')
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:DataMaskingAlerts"

def send_sns_notification(status, message):
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject=f"Data Masking Job {status}"
    )
