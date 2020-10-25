import boto3
import argparse

#create sqs client
sqs = boto3.client('sqs')

parser = argparse.ArgumentParser()
parser.add_argument("-q", "--queue", help="url of sqs queue")

args = parser.parse_args()

queue_url= args.queue

# send message to sqs - sample json msgs

response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=1,
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

