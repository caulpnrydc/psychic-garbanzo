import boto3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-q", "--queue", help="URL for SQS Queue")
parser.add_argument("-o", "--out", help="Name for output file")
parser.add_argument("-b", "--bucket", help="s3 bucket name")

args = parser.parse_args()

queue_url = args.queue
backup_name = args.out
bucket = args.bucket

file = open(backup_name, 'a+')
sqs = boto3.client('sqs')

with open(backup_name) as f:
# Receive messages from sqs, write to json file, upload to s3

    response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'SentTimestamp'
                ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
                ],
            VisibilityTimeout=0,
            WaitTimeSeconds=0
            )

    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']
#file.write('%s' % message + '\n')
#file.close()
    f.write('%s' % message)

    s3up = boto3.resource('s3')
    s3up.Object(bucket,backup_name).upload_file(backup_name)


# Delete received messages from sqs queue

    sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
            )

