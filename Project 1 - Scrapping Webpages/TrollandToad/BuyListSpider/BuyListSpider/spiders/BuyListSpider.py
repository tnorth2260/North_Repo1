# Import from other python files and scrapy files and the needed csv file containing all URLs/proxies/ua
import csv
import scrapy
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from ..items import DataItem
##########################          SPALSHSPIDER.PY OVERVIEW      #####################################################
# process the csv file so the url + ip address + useragent pairs are the same as defined in the file
# returns a list of dictionaries, example:
# [ {'url': 'http://www.starcitygames.com/catalog/category/Rivals%20of%20Ixalan',
#    'ip': 'http://204.152.114.244:8050',
#    'ua': "Mozilla/5.0 (BlackBerry; U; BlackBerry 9320; en-GB) AppleWebKit/534.11"},
#    ...
# ]
# plus python file also scrapes all URLs returning needed info and goes to all apges associated with URL by clicking next button

# Function to read csv file that contains URLs that are paried with proxies and user agents
def process_csv(csv_file):
    # Initialize data
    data = []
    # Initialize reader
    reader = csv.reader(csv_file)
    next(reader)

    # While inside csv file and not at end of csv file
    for fields in reader:

        # Set URL
        if fields[0] != "":
            url = fields[0]
        else:
            continue # skip the whole row if the url column is empty
        #Set proxy and pair with correct URL
        if fields[1] != "":
            ip = "http://" + fields[1] + ":8050" # adding http and port because this is the needed scheme
        # Set user agent and pair with correct URL
        if fields[2] != "":
            useragent = fields[2]
        # Put all three together
        data.append({"url": url, "ip": ip, "ua": useragent})
    # Return URL paried with ua and proxy
    return data

# Spider class
class MySpider(Spider):
    # Name of Spider
    name = 'BuyListSpider'
    # getting all the url + ip address + useragent pairs then request them
    
    def start_requests(self):
        # get the file path of the csv file that contains the pairs from the settings.py
        with open(self.settings["PROXY_CSV_FILE"], mode="r") as csv_file:
            # requests is a list of dictionaries like this -> {url: str, ua: str, ip: str}
            
            requests = process_csv(csv_file)
            for req in requests:
                # Return needed url with set delay of 3 seconds
                yield SplashRequest(url=req["url"], callback=self.parse, args={"wait": 3},
                    # Pair with user agent specified in csv file
                    headers={"User-Agent": req["ua"]},
                    # Sets splash_url to whatever the current proxy that goes with current URL  is instead of actual splash url
                    splash_url = req["ip"],
                    )

    # Scraping function that will scrape URLs for specified information
    def parse(self, response):
        #  Initialize item to function GameItem located in items.py, will be called multiple times
        item = DataItem()
        # Extract card category from URL using html code from website that identifies the category.  Will be outputted before rest of data
        for data in response.css('tr.ng-scope'):
            # Use xpath to get set names
            item["Set"] = data.xpath(".//td[1]/a/text()").get()
            #If set is equal to none use different xpath to get set name
            if item["Set"] == None:
               item["Set"] = data.xpath(".//td[1]/span/text()").get()
               # If set is still equal to none use different xpath to get set name
               if item["Set"] == None:
                   item["Set"] = data.xpath(".//td[1]/text()").get()
            # Use xpath to get card name
            item["Card_Name"]  = data.xpath(".//td[2]/a/text()").get()
            # If none use different xpath to get card name
            if item["Card_Name"] == None:
                item["Card_Name"] = data.xpath(".//td[2]/span/text()").get()
            # Use xpath to get remainder of needed data
            item["Condition"] = data.xpath('.//td[3]/text()').get()
            item["Quantity"] = data.xpath('.//td[5]/span/text()').get()
            item["Buy_Price"] = data.xpath('.//td[4]/span/text()').get()
            # Return values
            yield item
