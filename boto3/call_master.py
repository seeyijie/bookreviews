import subprocess
import fire

# python3 call_master.py --keypair=50043-east1-keypair --image_id=ami-04b9e92b5572fa0d1 --instance_type=t2.micro
def cli(keypair, image_id, instance_type):
    subprocess.check_call(['./master.sh', keypair, image_id, instance_type])

if __name__ == '__main__':
  fire.Fire(cli)