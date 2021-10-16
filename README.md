# Python S3 Queue purging and storing of deleted messages

<p>With this script you can purge an AWS SQS queue of the messages currently sitting in it and back them up to an S3 bucket for analysis. The original purpose of this was to clear any messages not able to be played successfully in an SQS Deadletter Queue.</p>


<p>This was also used as a demo process for the implementation of Jaeger Tracing as an APM tracing application. This is still in it's own branch at the moment.</p>

<p>Demo implementation of Jaeger Tracing can be found <a href=https://github.com/kris-bunney/psychic-garbanzo/tree/jaeger-tracing>Here</a></p>