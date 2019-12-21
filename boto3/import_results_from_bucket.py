# Get exported results from S3 bucket
import boto3
import os

if __name__ == "__main__":
    s3 = boto3.resource("s3")
    with open("info.txt") as f:
        bucket_name = eval(f.read())["bucket_name"]
    bucket = s3.Bucket(bucket_name)
    print("All bucket objects:", list(bucket.objects.all()))

    for obj in bucket.objects.all():
        for name in ["tfidf.csv", "pearsonr.csv"]:
            if not os.path.isdir(name):
                os.mkdir(name)
            if obj.key.startswith(name):
                bucket.download_file(Key=obj.key, Filename=obj.key)
