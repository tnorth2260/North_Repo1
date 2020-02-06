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
    name = 'splash_spider'
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

    # Function to parse needed data
    def parse(self, response):
        
        # For loop to run through html code until all needed data is scraped
        for data in response.css('div.card > div.row'):
            # import items from items.py
            item = DataItem()
            # Scrape Category name
            item["Category"] = data.css("div.col-12.prod-cat a::text").get()
            # Scrape card name
            item["Card_Name"]  = data.css("a.card-text::text").get()
            # For loop to run through all the buying information needed, skips first row
            for buying_option in data.css('div.buying-options-table div.row')[1:]:
                # Scrape seller, condition,stock, and price
                item["Seller"] = buying_option.css('div.row.align-center.py-2.m-auto > div.col-3.text-center.p-1 > img::attr(title)').get()
                if item["Seller"] == "PRE ORDER":
                    item["Seller"] = "TrollAndToad Com"
                item["Condition"] = buying_option.css("div.col-3.text-center.p-1::text").get()
                Quantity = buying_option.xpath('.//select[@name="qtyToBuy"]/option[last()]/@value').get()
                # Determine the highest number in the quantity drop down list to get remaining stock and if 0 output Out of Stock
                if Quantity == "0":
                    item["Stock"] = "Out of Stock"
                # If not 0 output greatest number in drop down list
                else:
                    item["Stock"] = "In Stock: " + Quantity + " Left"
                item["Price"] = buying_option.css("div.col-2.text-center.p-1::text").get()
                # Return data
                yield item

        # Find next page
        next_page_number = response.xpath('//div[div[.="Next Page"]][not(contains(@class, "hide"))]/@data-page').get()
        # If it exists and there is a next page enter if statement
        if next_page_number:
            # Go to next page and continue to top of fucntion to scrape next page
            yield scrapy.FormRequest.from_response(
                    response=response,
                    method="POST",
                    formid="category_form",
                    formdata={
                        'page-no': next_page_number,
                        },
                    callback=self.parse
                    )
