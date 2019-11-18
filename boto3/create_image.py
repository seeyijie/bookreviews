import boto3
import time

ec2 = boto3.client('ec2')
s3 = boto3.client('s3')

image_id = ""
def save_instance(ins, name, desc='My new instance'):
	res = ec2.create_image(InstanceId=ins, Name=name, Description=desc)
	image_id = res['ImageId']
	print("Created image: ",res['ImageId'])
	print("Waiting for it to be available...")

	# wait for it to be available
	available = 0
	while (not available):
		status = ec2.describe_images(ImageIds=[res['ImageId']])
		img = status['Images'][0]
		available = (img['State'] == 'available')
		time.sleep(1)

save_instance("i-02de5abf362ee63ed", "mongodb image", "save image from script")

