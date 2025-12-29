import boto3

from settings import Settings

def download_artifacts(settings: Settings):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(settings.s3_bucket)

    for obj in bucket.objects.filter(Prefix=settings.s3_model_dir):
        target_path = obj.key

        if obj.key.endswith("/"):
            continue

        bucket.download_file(obj.key, str(target_path))


