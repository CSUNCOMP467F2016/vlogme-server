import boto.elastictranscoder

import hashlib
import json
import multiprocessing
import time


def set_transcoder_job(input_key):

    pipeline_id = '1479421321140-03pscz'

    # This is the URL of the SQS queue
    #
    sqs_queue_url = 'video_decoding'

    # This is the name of the input key that you would like to transcode.
    input_key = input_key

    # This will generate a 480p 16:9 mp4 output.
    preset_id = '1351620000001-000061'

    # All outputs will have this prefix prepended to their output key.
    output_key_prefix = 'lower_quality/'

    # Region where you setup your AWS resources.
    region = 'us-west-2'
    response=create_elastic_transcoder_job(input_key,pipeline_id,output_key_prefix, preset_id)
    return response

def create_elastic_transcoder_job(input_key, pipeline_id,output_key_prefix, preset_id):
    region ='us-west-2'
    # Setup the job input using the provided input key.
    job_input = { 'Key' : input_key }

    # Setup the job output using the provided input key to generate an output key.
    job_output_lq = {
        'Key' : hashlib.sha256(input_key.encode('utf-8')).hexdigest(),
        'ThumbnailPattern':str(input_key) + '_thumb_{count}',
        'PresetId' : preset_id,
    }



    # Create a job on the specified pipeline and return the job ID.
    create_job_request = {
        'pipeline_id' : pipeline_id,
        'input_name' : job_input,
        'output_key_prefix' : output_key_prefix,
        'outputs' : [ job_output_lq ],
    }
    transcoder_connection = boto.elastictranscoder.connect_to_region(region)
    return transcoder_connection.create_job(**create_job_request)['Job']['Id']
