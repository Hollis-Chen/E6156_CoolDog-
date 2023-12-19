import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    ses_client = boto3.client('ses')
    sender = "wenzhengxuan@gmail.com"
    recipient = "zw2851@columbia.edu"
    subject = "New Paper Added"
    body = event['Records'][0]['Sns']['Message']

    try:
        response = ses_client.send_email(
            Source=sender,
            Destination={'ToAddresses': [recipient]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
        return response
    except ClientError as e:
        print(e.response['Error']['Message'])
        raise e
