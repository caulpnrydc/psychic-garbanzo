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

def send_message(sqs_queue):
    with tracer.start_span('send-message') as span:
        #create sqs client
        sqs = boto3.client('sqs')

        span.set_tag('sqs-queue', queue_url)
        span.log_kv({'event': 'string-format', 'value': queue_url})

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
        span.log_kv({'event': 'print'})

parser = argparse.ArgumentParser()
parser.add_argument("-q", "--queue", help="url of sqs queue")

args = parser.parse_args()

queue_url= args.queue
send_message(queue_url)

time.sleep(2)
tracer.close()