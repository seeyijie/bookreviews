import os
import subprocess
import fire
import time
import aws_setup

def cli(csv_aws_credentials, image_id, instance_type):
    # eg python3 call_master.py --csv_aws_credentials=path/to/csv --image_id=ami-04b9e92b5572fa0d1 --instance_type=t2.micro
    start = time.time()
    aws_setup.main(csv_aws_credentials)
    with open("info.txt") as f:
        info_dict = eval(f.read())
        keyfile = info_dict["keyfile"]
        keypair = os.path.basename(keyfile).split(".")[0]  # eg "/root/.ssh/key.pem"

    subprocess.check_call(["./master.sh", keypair, image_id, instance_type])
    duration = (time.time() - start) / 60  # convert seconds to minutes
    print(f"time taken is {duration}")


if __name__ == "__main__":
    fire.Fire(cli)
