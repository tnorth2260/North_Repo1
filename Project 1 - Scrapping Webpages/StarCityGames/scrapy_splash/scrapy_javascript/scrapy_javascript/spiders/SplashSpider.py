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
            for i, req in enumerate(requests):
                x = len(requests) - i
                # Return needed url with set delay of 3 seconds
                yield SplashRequest(url=req["url"], callback=self.parse, args={"wait": 3},
                    # Pair with user agent specified in csv file
                    headers={"User-Agent": req["ua"]},
                    # Sets splash_url to whatever the current proxy that goes with current URL  is instead of actual splash url
                    splash_url = req["ip"],
                    priority = x,
                    meta={'priority': x}  # <- check here!!
                    )

    # Scraping function that will scrape URLs for specified information
    def parse(self, response):
        #  Initialize item to function GameItem located in items.py, will be called multiple times
        item = DataItem()
        # Initialize saved_name
        saved_name = ""
        # Extract card category from URL using html code from website that identifies the category.  Will be outputted before rest of data
        item["Category"] = response.css("span.titletext::text").get()
        # For loop to loop through HTML code until all necessary data has been scraped
        for data in response.css("tr[class^=deckdbbody]"):
            # Initialize saved_name to the extracted card name
            saved_name  = data.css("a.card_popup::text").get() or saved_name
            # Now call item and set equal to saved_name and strip leading '\n' from output
            item["Card_Name"] = saved_name.strip()
            # Check to see if output is null, in the case that there are two different conditions for one card
            if item["Card_Name"] != None:
                # If not null than store value in saved_name
                saved_name = item["Card_Name"].strip()
            # If null then set null value to previous card name since if there is a null value you should have the same card name twice    
            else:
                item["Card_Name"] = saved_name
            # Call item again in order to extract the condition, stock, and price using the corresponding html code from the website
            item["Condition"] = data.css("td[class^=deckdbbody].search_results_7 a::text").get()
            item["Stock"] = data.css("td[class^=deckdbbody].search_results_8::text").get()
            item["Price"] = data.css("td[class^=deckdbbody].search_results_9::text").get()
            if item["Price"] == None:
                item["Price"] = data.css("td[class^=deckdbbody].search_results_9 span[style*='color:red']::text").get()

            # Return values
            yield item
            # Finds next page button
            priority = response.meta['priority']
            next_page = response.xpath('//a[contains(., "- Next>>")]/@href').get()
            # If it exists and there is a next page enter if statement
            if next_page is not None:
                # Go to next page
                yield response.follow(next_page, self.parse, priority=priority, meta={'priority': priority})
