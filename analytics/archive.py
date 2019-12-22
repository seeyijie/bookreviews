import string
import boto3
import random


def gen_random_string(length=32):
    vocab = string.ascii_letters + string.digits
    return "".join([random.choice(vocab) for _ in range(length)])


def create_key_pair(ec2):
    name = "keypair_" + gen_random_string()
    print("Creating key pair:", repr(name))
    return ec2.create_key_pair(KeyName=name)


def create_vpc(ec2):
    existing = list(ec2.vpcs.all())
    if len(existing) > 0:
        print("Returning existing vpc")
        return existing[0]
    else:
        return ec2.create_vpc(CidrBlock="10.0.0.0/16")


def create_subnet(vpc):
    existing = list(vpc.subnets.all())
    if len(existing) > 0:
        print("Returning existing subnet")
        return existing[0]
    else:
        return vpc.create_subnet(CidrBlock="10.0.0.0/16")


def create_internet_gateway(ec2, vpc):
    existing = list(vpc.internet_gateways.all())
    if len(existing) > 0:
        print("Returning existing internet gateway")
        return existing[0]
    else:
        return ec2.create_internet_gateway()


def attach_gateway(vpc, igw):
    for _igw in vpc.internet_gateways.all():
        if _igw.id == igw.id:
            print("Returning existing attached igw")
            return igw
    return vpc.attach_internet_gateway(InternetGatewayId=igw.id)


def create_instances(
    ec2,
    key_pair_name,
    subnet,
    n_instances=2,
    ami="ami-04b9e92b5572fa0d1",
    i_type="t2.micro",
):
    # Default AMI is Ubuntu Server 18.04 LTS (HVM), SSD Volume Type
    instances = [i for i in ec2.instances.all() if i.state["Name"] == "running"]
    if len(instances) >= n_instances:
        print("Returning existing instances:", n_instances)
        instances = instances[:n_instances]
    else:
        instances = ec2.create_instances(
            ImageId=ami,
            MinCount=n_instances,
            MaxCount=n_instances,
            InstanceType=i_type,
            KeyName=key_pair_name,
        )
    print("Instances:", instances)
    return instances


def delete_instances(instances):
    print("Terminating instances:", instances)
    for i in instances:
        i.terminate()


def check_cluster_terminated(cluster_dict):
    # "TERMINATED", "TERMINATING" etc
    state = cluster_dict["Status"]["State"]
    return "TERMINAT" in state


def delete_cluster(emr, cluster_id):
    print("Deleting cluster:", cluster_id)
    return emr.terminate_job_flows(JobFlowIds=[cluster_id])


def get_all_clusters(emr, show_terminated=False):
    clusters = []
    for cluster_dict in emr.list_clusters()["Clusters"]:
        if check_cluster_terminated(cluster_dict) and not show_terminated:
            continue
        clusters.append(cluster_dict)
    return clusters


def create_cluster(
    emr,
    key_pair_name,
    subnet=None,
    bootstrap_actions=[],
    num_core_nodes=2,
    apps=("Hadoop", "Spark", "Livy"),
):
    assert type(bootstrap_actions) == list
    instance_dict = {
        "InstanceGroups": [
            {
                "Name": "Master nodes",
                "Market": "SPOT",
                "InstanceRole": "MASTER",
                "InstanceType": "m4.large",
                "InstanceCount": 1,
            },
            {
                "Name": "Slave nodes",
                "Market": "SPOT",
                "InstanceRole": "CORE",
                "InstanceType": "m4.large",
                "InstanceCount": num_core_nodes,
            },
        ],
        "Ec2KeyName": key_pair_name,
        "KeepJobFlowAliveWhenNoSteps": True,
        "TerminationProtected": False,
    }
    if subnet is not None:
        instance_dict["Ec2SubnetId"] = subnet.id

    response = emr.run_job_flow(
        Name="my_cluster",
        ReleaseLabel="emr-5.28.0",
        Applications=[{"Name": a} for a in apps],
        Instances=instance_dict,
        VisibleToAllUsers=True,
        JobFlowRole="EMR_EC2_DefaultRole",
        ServiceRole="EMR_DefaultRole",
        BootstrapActions=bootstrap_actions,
    )
    cluster_id = response["JobFlowId"]
    print("Created cluster:", cluster_id)
    return cluster_id


def main():
    ec2 = boto3.resource("ec2")
    keypair = create_key_pair(ec2)

    # Not necessary to create new vpc, can get default one with
    # subnet, igw and route table already setup
    subnet = create_subnet(create_vpc(ec2))

    instances = create_instances(ec2, keypair.name, subnet)
    delete_instances(instances)

    # Important: for a new user, the default IAM roles must be created (aws emr create-default-roles)
    emr = boto3.client("emr")
    # EMR notebook requirements: EC2-VPC, EMR >= 5.18.0, (Hadoop, Spark, and Livy)
    print("All clusters:", get_all_clusters(emr))
    cluster_id = create_cluster(emr, keypair.name, subnet)
    delete_cluster(emr, cluster_id)
