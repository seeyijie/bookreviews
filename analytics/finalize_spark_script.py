# Inserts bucket details into spark_app.py
# Requires aws_setup.py to be run first to write info.txt

if __name__ == "__main__":
    with open("info.txt") as f:
        dict_info = eval(f.read())
    bucket_name = dict_info["bucket_name"]
    with open("my_spark_app.py") as f:
        content = f.read()
    content = content.replace(
        "bucket_name = None", "bucket_name = '{}'".format(bucket_name)
    )
    with open("my_spark_app.py", "w") as f:
        f.write(content)
