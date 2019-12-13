from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import time
from collections import Counter
from functools import partial
from operator import add

from pyspark import ml
from pyspark.sql import SparkSession, utils

# __future__ imports necessary in case EC2 Linux AMI does not have python3


class Timer(object):
    def __init__(self, name, decimals=1):
        self.name = name
        self.decimals = decimals

    def __enter__(self):
        print("Start timer:", self.name)
        self.start = time.time()

    def __exit__(self, type, value, traceback):
        duration = time.time() - self.start
        duration = round(duration, self.decimals)
        print("Ended timer: {}: {} s".format(self.name, duration))


def map_fn_pearsonr(pair):
    x, y = pair
    return [
        ("n", 1),
        ("xy", x * y),
        ("x", x),
        ("y", y),
        ("x_square", x ** 2),
        ("y_square", y ** 2),
    ]


def apply_pearsonr_formula(result_list):
    """
  r = top / bottom, where n = number of total xy pairs
  top = n*sum(xy)-sum(x)-sum(y)
  bottom = sqrt(n*sum(x^2)-sum(x)^2) * sqrt(n*sum(y^2)-sum(y)^2
  """
    sums = {key: value for key, value in result_list}
    assert set(sums.keys()) == {"n", "xy", "x", "y", "x_square", "y_square"}

    top = (sums["n"] * sums["xy"]) - (sums["x"] * sums["y"])
    bottom_left = ((sums["n"] * sums["x_square"]) - sums["x"] ** 2) ** 0.5
    bottom_right = ((sums["n"] * sums["y_square"]) - sums["y"] ** 2) ** 0.5
    return top / (bottom_left * bottom_right)


def map_reduce_pearsonr(rdd):
    rdd = rdd.flatMap(map_fn_pearsonr)
    rdd = rdd.reduceByKey(add)
    return apply_pearsonr_formula(rdd.collect())


def tokenize(text):
    return text.strip().lower().split()


def get_length(text):
    return len(tokenize(text))


def pearson_price_vs_review_length(_df_meta, _df_reviews):
    _df_meta = _df_meta.select(["asin", "price"])
    _df_reviews = _df_reviews.select(["asin", "reviewText"])
    df = _df_meta.join(_df_reviews, on="asin", how="inner")
    df = df.drop("asin")
    df = df.dropna()

    rdd = df.rdd  # (price, reviewText)
    rdd = rdd.mapValues(get_length)  # (price, reviewLength)
    with Timer("Map reduce pearson correlation"):
        val_pearson = map_reduce_pearsonr(rdd)
    print("Correlation value:", val_pearson)
    with open("results_pearson.txt", "w") as f:
        f.write(str(val_pearson))


def map_fn_tf(pair):
    doc_id, text = pair
    counts = Counter(tokenize(text))
    total = sum(counts.values())
    return [((doc_id, tok), c / total) for tok, c in counts.items()]


def map_fn_df(pair):
    (doc_id, tok), tf = pair
    return tok, 1


def map_reduce_tfidf(rdd):
    rdd = rdd.flatMap(map_fn_tf)
    rdd.cache()
    with Timer("Term frequency"):
        tf = rdd.collect()

    rdd = rdd.map(map_fn_df)
    rdd = rdd.reduceByKey(add)
    with Timer("Doc frequency"):
        df = rdd.collect()

    print("TF tuples:", tf[:10])
    print("DF tuples:", df[:10])
    return tf, df


def get_rdd_text(df, col_text):
    def map_fn(pair):
        row, idx = pair
        return idx, row[col_text]

    df = df.select([col_text]).dropna()
    rdd = df.rdd
    # rdd = rdd.map(str)
    rdd = rdd.zipWithIndex()
    rdd = rdd.map(map_fn)
    return rdd


def tuples2dict(tuples):
    keys = [k for k, v in tuples]
    assert len(keys) == len(set(keys))
    return {k: v for k, v in tuples}


# def get_tfidf(tf, df):
#     with Timer("Get TF-IDF"):
#         print("len(df):", len(df))
#         print("len(tf):", len(tf))
#         with Timer("tuples2dict, doc_ids, n_docs"):
#             df = tuples2dict(df)
#             doc_ids = set([d for (d, tok), freq in tf])
#             n_docs = len(doc_ids)
#
#         tfidf = {d: {} for d in doc_ids}
#         with Timer("tfidf[d][tok] = freq * math.log(n_docs / df[tok])"):
#             for (d, tok), freq in tf:
#                 tfidf[d][tok] = freq * math.log(n_docs / df[tok])
#
#     return tfidf


def get_tfidf_multi(dfs, inputCol, outputCol="tfidf"):
    assert type(dfs) == list
    tokenizer = ml.feature.Tokenizer(inputCol=inputCol, outputCol="token")
    hasher = ml.feature.HashingTF(inputCol="token", outputCol="hash_tf")
    idf = ml.feature.IDF(inputCol="hash_tf", outputCol=outputCol)
    pipeline = ml.Pipeline(stages=[tokenizer, hasher, idf])
    pipeline = pipeline.fit(dfs[0])  # Assume first is df_trn
    return [pipeline.transform(df) for df in dfs]


def get_tfidf(df, inputCol):
    df = df.select([inputCol]).dropna()
    df = get_tfidf_multi([df], inputCol)[0]
    return df


def show_tfidf(tfidf, n_show=10, decimals=4):
    print("Showing first {} TF-IDF results:".format(n_show))
    for doc_id in list(tfidf.keys())[:n_show]:
        print({k: round(v, decimals) for k, v in tfidf[doc_id].items()})


def tfidf_review_text(_df_reviews):
    with Timer("TFIDF for reviewText"):
        # _df_reviews = _df_reviews.sample(withReplacement=False, fraction=0.1, seed=42)
        # rdd = get_rdd_text(_df_reviews, col_text="reviewText")
        # tf, df = map_reduce_tfidf(rdd)
        # tfidf = get_tfidf(tf, df)
        # show_tfidf(tfidf)

        df = get_tfidf(_df_reviews, "reviewText")
        df = df.select(["token", "tfidf"])
        show_df(df, 10)

        # with Timer("Write TFIDF results"):
        #   cols_new = []
        #   for c in df.columns:
        #     c_new = c + "_string"
        #     df = df.withColumn(c_new, df[c].cast("string"))
        #     cols_new.append(c_new)
        #   df = df.select(cols_new)
        #   df.write.csv("results_tfidf.csv", header=True)


def load_data(bucket, fname):
    name, ftype = fname.split(".")
    read_fn = {
        "csv": partial(spark.read.csv, header=True, inferSchema=True),
        "json": spark.read.json,
    }[ftype]
    path_hdfs = os.path.join("hdfs:", fname)
    path_s3 = os.path.join(bucket, fname)
    with Timer("Read S3 Bucket"):
        df = read_fn(path_s3)
    if ftype == "csv":
        read_fn = partial(spark.read.csv, header=True, schema=df.schema)

    try:
        return read_fn(path_hdfs)

    except utils.AnalysisException as e:
        print("HDFS file not found:", e)

        with Timer("Write HDFS"):
            try:
                if ftype == "csv":
                    df.write.csv(path_hdfs, header=True)
                elif ftype == "json":
                    df.write.json(path_hdfs)
            except utils.AnalysisException as e:
                print("HDFS write error:", e)

        with Timer("Read HDFS"):
            return read_fn(path_hdfs)


def show_df(df, n_show):
    rows = df.take(n_show)
    for r in rows:
        print(r)


if __name__ == "__main__":
    with Timer("My spark script"):
        spark = SparkSession.builder.master("local[*]").getOrCreate()

        bucket_name = ""  # Should be overwritten by finalize_spark_script.py
        bucket = "s3a://" + bucket_name
        df_reviews = load_data(bucket, "kindle_reviews.csv")
        df_meta = load_data(bucket, "meta_Kindle_Store.json")

        print("Meta:", show_df(df_meta, 10))
        print("Review:", show_df(df_reviews, 10))

        pearson_price_vs_review_length(df_meta, df_reviews)
        tfidf_review_text(df_reviews)

    assert False  # For debugging, this exposes script printouts
