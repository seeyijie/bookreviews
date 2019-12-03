import subprocess
import fire

# TODO: test entering t2.micro without quotation marks
def cli(keypair, image_id="ami-0d5d9d301c853a04a", instance_type="t2.micro"):
    subprocess.check_call(['./master.sh', keypair, image_id, instance_type])

if __name__ == '__main__':
  fire.Fire(cli)