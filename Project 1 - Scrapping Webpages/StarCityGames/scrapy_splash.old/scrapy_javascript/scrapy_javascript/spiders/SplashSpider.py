import csv
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from ..items import GameItem


# process the csv file so the url + ip address + useragent pairs are the same as defined in the file
# returns a list of dictionaries, example:
# [ {'url': 'http://www.starcitygames.com/catalog/category/Rivals%20of%20Ixalan',
#    'ip': 'http://204.152.114.244:8050',
#    'ua': "Mozilla/5.0 (BlackBerry; U; BlackBerry 9320; en-GB) AppleWebKit/534.11"},
#    ...
# ]
def process_csv(csv_file):
    data = []
    reader = csv.reader(csv_file)
    next(reader)
    for fields in reader:
        if fields[0] != "":
            url = fields[0]
        else:
            continue # skip the whole row if the url column is empty
        if fields[1] != "":
            ip = "http://" + fields[1] + ":8050" # adding http and port because this is the needed scheme
        if fields[2] != "":
            useragent = fields[2]
        data.append({"url": url, "ip": ip, "ua": useragent})
    return data


class MySpider(Spider):
    name = 'splash_spider'  # Name of Spider

    # notice that we don't need to define start_urls
    # just make sure to get all the urls you want to scrape inside start_requests function

    # getting all the url + ip address + useragent pairs then request them
    def start_requests(self):

        # get the file path of the csv file that contains the pairs rom the settings.py
        with open(self.settings["PROXY_CSV_FILE"], mode="r") as csv_file:
            # requests is a list of dictionaries like this -> {url: str, ua: str, ip: str}
            requests = process_csv(csv_file)

        for req in requests:
            # no need to create custom middlewares
            # just pass useragent using the headers param, and pass proxy using the meta param
            yield SplashRequest(url=req["url"], callback=self.parse, args={"wait": 3},
                                headers={"User-Agent": req["ua"]},
                                meta={"proxy": (req["ip"])})

    # Scraping
    def parse(self, response):
        item = GameItem()
        for game in response.css("tr"):
            # Card Name
            item["card_name"] = game.css("a.card_popup::text").extract_first()
            yield item

