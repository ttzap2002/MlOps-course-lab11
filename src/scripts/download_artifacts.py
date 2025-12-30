import boto3
import os
from settings import Settings

def download_artifacts(settings: Settings):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(settings.s3_bucket)

    for obj in bucket.objects.filter(Prefix=settings.s3_model_dir):
        target_path = obj.key

        if obj.key.endswith("/"):
            continue

        directory = os.path.dirname(target_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        try:
            bucket.download_file(obj.key, str(target_path))
        except Exception as e:
            print(f"Failed to download file {obj.key}: {e}")



