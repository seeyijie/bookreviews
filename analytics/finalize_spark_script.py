import fire


def main(spark_script):
    # Inserts bucket details into spark_script
    # Requires aws_setup.py to be run first to write info.txt
    with open("info.txt") as f:
        dict_info = eval(f.read())
    bucket_name = dict_info["bucket_name"]
    with open(spark_script) as f:
        content = f.read()
    content = content.replace(
        'bucket_name = ""', 'bucket_name = "{}"'.format(bucket_name)
    )
    with open(spark_script, "w") as f:
        f.write(content)


if __name__ == "__main__":
    fire.Fire(main)
