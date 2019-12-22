import os
import fire
import boto3
import string
import random
import shutil


def gen_random_string(length=32):
    vocab = string.ascii_letters + string.digits
    return "".join([random.choice(vocab) for _ in range(length)])


def create_key_pair(ec2):
    name = "keypair_" + gen_random_string()
    print("Creating key pair:", repr(name))
    return ec2.create_key_pair(KeyName=name)


def read_credentials(csv_file, sep=","):
    with open(csv_file) as f:
        headers = f.readline().strip().split(sep)
        values = f.readline().strip().split(sep)
    assert len(headers) == len(values)
    print("Headers:", headers)
    return {h: v for h, v in zip(headers, values)}


def write_credentials(creds, region):
    folder = os.path.expanduser("~/.aws")
    if not os.path.exists(folder):
        os.mkdir(folder)

    with open(os.path.join(folder, "credentials"), "w") as f:
        f.write("[default]\n")
        f.write("aws_access_key_id = {}\n".format(creds["Access key ID"]))
        f.write("aws_secret_access_key = {}\n".format(creds["Secret access key"]))

    with open(os.path.join(folder, "config"), "w") as f:
        f.write("[default]\n")
        f.write("region={}\n".format(region))


def write_bucket_info(bucket_name):
    assert type(bucket_name) == str
    assert bucket_name != ""
    folder = os.path.expanduser("~/.aws")
    with open(os.path.join(folder, "info.txt"), "w") as f:
        f.write(bucket_name)


def upload_file(bucket, filepath, overwrite=False):
    objects = {obj.key: obj for obj in bucket.objects.all()}
    key = os.path.basename(filepath)
    if key in objects.keys():
        if not overwrite:
            print("Object already exists, skipping")
            return objects[key]

    bucket.upload_file(filepath, key)
    objects = {obj.key: obj for obj in bucket.objects.all()}
    return objects[key]


def delete_bucket_helper(bucket):
    print("Deleting bucket:", bucket.name)
    to_delete = {"Objects": [{"Key": obj.key for obj in bucket.objects.all()}]}
    bucket.delete_objects(Delete=to_delete)
    return bucket.delete()


def create_bucket(s3, name, region):
    print("Creating bucket:", name, region)
    bucket = s3.Bucket(name)
    bucket.create()
    return bucket


def run_shell(command):
    print("Shell command:", command)
    return os.popen(command).read()


def write_key(keypair):
    keyfile = keypair.name + ".pem"
    with open(keyfile, "w") as f:
        f.write(keypair.key_material)
    print(run_shell("chmod 400 {}".format(keyfile)))
    with open(keyfile) as f:
        print("Key material preview:\n", f.read()[:100])

    return keyfile


def put_keyfile_in_ssh(keyfile):
    folder = os.path.expanduser("~/.ssh")
    if not os.path.exists(folder):
        os.mkdir(folder)
    path_out = os.path.join(folder, keyfile)
    shutil.copyfile(keyfile, path_out)
    print(run_shell("chmod 400 {}".format(path_out)))
    return path_out


def make_valid_bucket_name(bucket_name):
    # https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-s3-bucket-naming-requirements.html
    whitelist = string.ascii_lowercase + string.digits + "." + "-"
    bucket_name = bucket_name.lower()
    bucket_name = "".join([c for c in bucket_name if c in whitelist])
    return bucket_name


def import_results_from_bucket():
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
                print("Downloaded:", obj.key)


def delete_bucket():
    s3 = boto3.resource("s3")
    with open("info.txt") as f:
        bucket_name = eval(f.read())["bucket_name"]
    bucket = s3.Bucket(bucket_name)
    delete_bucket_helper(bucket)


def main(csv_aws_credentials, region="us-east-1"):
    creds = read_credentials(csv_aws_credentials)
    write_credentials(creds, region)

    # Upload book reviews and metadata to S3 bucket
    # This is temporary and should be replaced by ETL from databases (MySQL & MongoDB)
    s3 = boto3.resource("s3")
    # print("All buckets:", list(s3.buckets.all()))
    user = creds["User name"]
    bucket_name = "{}-bucket-50043-group-datahoarders".format(user)
    bucket_name = make_valid_bucket_name(bucket_name)
    bucket = create_bucket(s3, bucket_name, region)
    write_bucket_info(bucket_name)
    print("Bucket objects:", list(bucket.objects.all()))

    ec2 = boto3.resource("ec2")
    keypair = create_key_pair(ec2)
    keyfile = write_key(keypair)
    keyfile = put_keyfile_in_ssh(keyfile)

    # Important: for a new user, the default IAM roles must be created
    # in order to launch a cluster
    run_shell("aws emr create-default-roles")

    dict_info = dict(
        region=region, keyfile=keyfile, keyname=keypair.name, bucket_name=bucket_name
    )
    with open("info.txt", "w") as f:
        f.write(str(dict_info))


if __name__ == "__main__":
    fire.Fire()
