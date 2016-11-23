import random

import boto3


def transcode_on_boto3(input_key):


    pipeline_id = '1479421321140-03pscz'

    preset_id = '1351620000001-500050'

    # All outputs will have this prefix prepended to their output key.
    output_key_prefix = '/'

    # Region where you setup your AWS resources.
    region_name = 'us-west-2'

    client = boto3.client('elastictranscoder', region_name = region_name)

    random_prefix = str(random.randrange(200))
    output_key = random_prefix + input_key + "_dash"
    playlist_name  = random_prefix + "playlist_"+input_key



    response = client.create_job(

        PipelineId=pipeline_id,

        Input={
            'Key': input_key,
            'FrameRate': 'auto',
            'Resolution': 'auto',
            'AspectRatio': 'auto',
            'Interlaced': 'auto',
            'Container': 'auto',
        },

        Output={
            'Key': output_key,
            'ThumbnailPattern': output_key+'_{count}',
            'PresetId': preset_id,
            'SegmentDuration': '1',
        },

        # OutputKeyPrefix=output_key_prefix,
        Playlists=[
            {
                'Name': playlist_name,
                'Format': 'MPEG-DASH',

                'OutputKeys': [
                    output_key,
                ]
            },
        ],
    )
    print(response)
    return output_key, playlist_name+'.mpd', output_key+'_00001.png'
