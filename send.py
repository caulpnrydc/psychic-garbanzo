import boto3

#create sqs client
sqs = boto3.client('sqs')

queue_url='<SQS_QUEUE_HERE>'

# send message to sqs - sample json msgs

response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'The Whistler'
                },
            'Author': {
                'DataType': 'String',
                'StringValue': 'John Grisham'
                },
            'WeeksOn': {
                'DataType': 'Number',
                'StringValue': '6'
                }
            },
        MessageBody=(
            'Information about current NY Times fiction bestseller for week of 12/11/2016.')
        )

print(response['MessageId'])

