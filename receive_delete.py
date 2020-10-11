import boto3


queue_url = "<SQS_QUEUE_HERE>"
backup_name = "<Filename>"


file = open(backup_name, 'a')
sqs = boto3.client('sqs')


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
print('Receiving and saving messages')
file.write('%s' % message + '\n')
file.close()

s3up = boto3.resource('s3')
print('Starting file upload to S3 bucket...')
s3up.Object('<S3_BUCKET_HERE>',backup_name).upload_file(backup_name)


# Delete received messages from sqs queue

sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
        )

