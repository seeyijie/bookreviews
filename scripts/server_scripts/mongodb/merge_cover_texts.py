import fire


def main(
    meta_json="meta_Kindle_Store.json",
    texts_csv="bookreviews/extra_data/kindle_cover_texts.csv",
    output_json="meta_new.json",
    sep=",",
):
    print("Merging csv with extracted book cover text into metadata json")
    asin2text = {}
    with open(texts_csv) as f:
        headers = f.readline().strip().split(sep)
        print("Csv headers:", headers)
        for line in f:
            asin, text = line.strip().split(sep)
            asin2text[asin] = text

    n_missing_asin = 0
    prefix = "{'asin': '"
    assert meta_json != output_json, "Output json path must be different!"
    with open(meta_json) as f, open(output_json, "w") as f2:
        for line in f:
            assert line.startswith(prefix)
            temp = line[len(prefix) :]
            asin = temp.split("'")[0]  # eg {'asin': 'B000FA5SHK', ...}\n

            if asin not in asin2text.keys():
                n_missing_asin += 1
                f2.write(line)
                continue

            new_field = "text: '{}', ".format(asin2text[asin])
            f2.write(line[0] + new_field + line[1:])
    print("Num asin found:", len(asin2text))
    print("Num missing asin:", n_missing_asin)


if __name__ == "__main__":
    fire.Fire(main)
