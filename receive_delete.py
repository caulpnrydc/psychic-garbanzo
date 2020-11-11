import boto3
import argparse
from jaeger_client import Config
import logging
import time


def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.WARNING)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
    )

    return config.initialize_tracer()

tracer = init_tracer('sqs-empty')


# Receive messages from sqs, write to json file, upload to s3
def receive_message(sqs_queue):
    with tracer.start_span('receive-message') as span:
        sqs = boto3.client('sqs')

        span.set_tag('sqs_queue', queue_url)
        span.log_kv({'event': 'string-format', 'value': queue_url})

        with tracer.start_span('receive-message', child_of=span) as span2:
            span2.set_tag('receive-msg', queue_url)
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
            span.log_kv({'event': 'string-format', 'receipt': receipt_handle})
            
            with tracer.start_span('receive-message', child_of=span2) as span3:
                span3.set_tag('write-to-file', backup_name)
                file.write('%s' % message + '\n')
                file.close()
                span.log_kv({'event': 'string-format', 'file': backup_name})

                with tracer.start_span('receive-message', child_of=span3) as span4:
                    span4.set_tag('upload-s3', bucket)
                    s3up = boto3.resource('s3')
                    s3up.Object(bucket,backup_name).upload_file(backup_name)
                    span.log_kv({'event': 'string-format', 'bucket': bucket})

                    # Delete received messages from sqs queue
                    with tracer.start_span('receive-message', child_of=span4) as span5:
                        span5.set_tag('delete-msg', queue_url)
                        span.log_kv({'event': 'string-format', 'value': 'Delete'})
                        span.log_kv({'event': 'string-format', 'queue': queue_url})
                        sqs.delete_message(
                                QueueUrl=queue_url,
                                ReceiptHandle=receipt_handle
                                )

parser = argparse.ArgumentParser()
parser.add_argument("-q", "--queue", help="URL for SQS Queue")
parser.add_argument("-o", "--out", help="Name for output file")
parser.add_argument("-b", "--bucket", help="s3 bucket name")

args = parser.parse_args()

queue_url = args.queue
backup_name = args.out
bucket = args.bucket

file = open(backup_name, 'a')

receive_message(queue_url)

time.sleep(2)
tracer.close()