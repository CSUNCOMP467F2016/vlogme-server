import boto3

def add_video_file_for_encoding(bucket_name, file_name, author):
    sqs = boto3.resource('sqs', region_name = "us-west-2")
    queue = sqs.get_queue_by_name(QueueName='video_decoding')

    response=queue.send_message(MessageBody='encode me', MessageAttributes={
            'filename': {
                'StringValue': file_name,
                'DataType': 'String'},
            'bucket_name': {
                'StringValue': bucket_name,
                'DataType': 'String'},
            'author': {
                'StringValue': author,
                'DataType': 'String'},
            })
    print(response)

add_video_file_for_encoding('buk1', 'fil1', 'auth1')