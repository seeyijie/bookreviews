import requests
import lxml.html
from typing import List
import time
import csv
import models.Title as AsinTitle
from application import db
from sqlalchemy.exc import IntegrityError

Response = requests.models.Response


class Scraper:
    def create_URL(self, asin_list: List[str]) -> List[str]:
        url_list = []
        for asin in asin_list:
            url = "https://www.amazon.com/s?k={}".format(asin)
            url_list.append(url)

        return url_list

    def get_response(self, url_list: str, upper_limit: int, lower_limit: int = 0) -> List[Response]:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/39.0.2171.95 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1"
        }

        print("Upper Limit set at %s (inclusive)" % upper_limit)
        print("Lower Limit set at %s (inclusive)" % lower_limit)

        res_list = []
        for index in range(lower_limit, upper_limit + 1):
            print("Getting response object #{}".format(index))
            res = requests.get(url_list[index], headers=headers)
            res_list.append(res)

        print("Length of response list is: " + str(len(res_list)))

        return res_list

    def scrape(self, res_list: List[Response], asin_list: List[str], fileout: str, err_logs: str):
        index_dict = {}
        for index, res in enumerate(res_list):
            print("Scraping from response object #{}".format(index))
            try:
                doc = lxml.html.fromstring(res.text)
                title = doc.xpath("//*[@class='a-size-medium a-color-base a-text-normal']/text()")[0]
                index_dict[title] = asin_list[index]

                asin_title = AsinTitle(asin_list[index], title)
                db.session.add(asin_title)
                db.session.commit()

                title.replace(',', '|')

                with open(fileout, mode="a") as fout:
                    csv_writer = csv.writer(fout, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow([title, asin_list[index]])

            except IntegrityError as err:
                # print("IntegrityError on Index {}".format(index))
                db.session.rollback()
                with open(err_logs, mode="a") as err_log:
                    err_log.write("ASIN: " + str(asin_list[index]) + " | Trace: " + "Key is already in database" + "\n")

            except Exception as e:
                # print(e)
                # print("Unhandled error on Index {}".format(index))
                # print("ASIN: " + asin_list[index])
                db.session.rollback()
                with open(err_logs, mode="a") as err_log:
                    err_log.write("ASIN: " + asin_list[index] + " | " + "Trace: " + str(e) + "\n")


def load_list(filein: str):
    asin_list = []
    with open(filein, mode="r") as fin:
        text = fin.readlines()
        for asin in text:
            asin_list.append(asin.strip("\n").strip("\""))

    print("ASIN List is " + str(len(asin_list)))
    return asin_list

# start = time.time()
# scraper = Scraper()
# LIMIT = 5
# asin_list = load_list("/home/yijie/Desktop/results.csv")
# print(len(asin_list))
# url_list = scraper.create_URL(asin_list)
# res_list = scraper.get_response(url_list, upper_limit=LIMIT, lower_limit=0)
# scraper.scrape(res_list, asin_list, limit=LIMIT, fileout="/home/yijie/Desktop/title_to_asin.csv",
#                err_logs="/home/yijie/Desktop/err_logs.txt")
#
# elapsed_time = time.time() - start
# print("Duration: {}".format(elapsed_time))
