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


def delete_bucket(bucket):
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
    print(run_shell("chmod 400 {}".format(path_out)))
    shutil.copyfile(keyfile, path_out)


def main(csv_aws_credentials, region="us-east-1"):
    creds = read_credentials(csv_aws_credentials)
    write_credentials(creds, region)

    # Upload book reviews and metadata to S3 bucket
    # This is temporary and should be replaced by ETL from databases (MySQL & MongoDB)
    s3 = boto3.resource("s3")
    print("All buckets:", list(s3.buckets.all()))
    user = creds["User name"]
    bucket_name = "{}-bucket-50043-group-datahoarders".format(user)
    bucket_name = bucket_name.lower()  # AWS only accepts lowercase
    bucket = create_bucket(s3, bucket_name, region)
    print("Bucket objects:", list(bucket.objects.all()))

    ec2 = boto3.resource("ec2")
    keypair = create_key_pair(ec2)
    keyfile = write_key(keypair)
    put_keyfile_in_ssh(keyfile)

    # Important: for a new user, the default IAM roles must be created
    # in order to launch a cluster
    run_shell("aws emr create-default-roles")

    with open("info.txt", "w") as f:
        f.write(str(dict(region=region, keyfile=keyfile, bucket_name=bucket_name)))


if __name__ == "__main__":
    fire.Fire(main)
