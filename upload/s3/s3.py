import boto3
import time

BUCKET_NAME='comp467originals'
s3 = boto3.resource('s3')

def upload_original_to_s3(file_object, user):
    username = user.username

    extension = file_object.name.split('.')[-1]
    s3_filename = "{}_{}.{}".format(username,int(time.time()),extension)
    put_result=s3.Object(BUCKET_NAME, s3_filename).put(Body=file_object.file.read())

    return (BUCKET_NAME, s3_filename)