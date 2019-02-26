import boto3
from config import S3_BUCKET, S3_KEY, S3_SECRET
from flask import session

def _get_s3_client():
    if S3_KEY and S3_SECRET:
        return boto3.client(
            's3',
            aws_access_key_id=S3_KEY,
            aws_secret_access_key=S3_SECRET
        )
    else:
        return boto3.client('s3')

def _get_s3_resource():
    if S3_KEY and S3_SECRET:
        return boto3.resource(
            's3',
            aws_access_key_id=S3_KEY,
            aws_secret_access_key=S3_SECRET
        )
    else:
        return boto3.resource('s3')

def get_bucket():
    s3_resource = _get_s3_resource()
    if 'bucket' in session:
        bucket = session['bucket']
    else:
        bucket = S3_BUCKET
    return s3_resource.Bucket(bucket)

def get_detail_bucket_list():
    objects = dict()
    client = boto3.client('s3')

    bucket_list = get_bucket().objects.all()

    for item in bucket_list:
        response = client.get_object_tagging(
            Bucket=S3_BUCKET,
            Key=item.key
        )

        objects[item.key] = response

    return objects

def get_buckets_list():
    client = boto3.client('s3')
    return client.list_buckets().get('Buckets')

def add_tags_to_object(fileName, url, classifier, breed):
    tagging= []
    tagging.append({'Key': 'type', 'Value': classifier })
    tagging.append({'Key': 'breed', 'Value': breed })
    tagset =  {'TagSet' : tagging}

    client = boto3.client('s3')
    client.put_object_tagging(Bucket=S3_BUCKET, Key=fileName, Tagging=tagset)

    r = client.get_object_tagging(Bucket=S3_BUCKET, Key=fileName)
    print('get tags returned %s' % r)
