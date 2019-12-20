import subprocess
import time

import fire

import aws_setup
import make_cluster_scripts


def cli(
    csv_aws_credentials,
    image_id="ami-04b9e92b5572fa0d1",
    instance_type="t3.large",
    n_nodes_analytics=4,
):
    # Example: python3 call_master.py --csv_aws_credentials=path/to/csv
    # Default image_id refers to "Ubuntu Server 18.04 LTS (HVM), SSD Volume Type"
    # This is the ami for production backend, analytics backend uses Amazon Linux 2

    start = time.time()
    aws_setup.main(csv_aws_credentials)
    with open("info.txt") as f:
        dict_info = eval(f.read())
        keypair = dict_info["keyname"]

    make_cluster_scripts.main(num_nodes=n_nodes_analytics, instance_type=instance_type)
    subprocess.check_call(["./master.sh", keypair, image_id, instance_type])
    duration = (time.time() - start) / 60  # convert seconds to minutes
    print(f"time taken is {duration}")


if __name__ == "__main__":
    fire.Fire(cli)
