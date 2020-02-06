# Import needed functions and call needed python files
import scrapy
import json
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from ..items import DataItem

# Spider class
class LoginSpider(scrapy.Spider):
    # Name of spider
    name = "LoginSpider"
    #URL where dated is located
    start_urls = ["http://www.starcitygames.com/buylist/"]

    # Login function
    def parse(self, response):
        # Login using email and password than proceed to after_login function
        return scrapy.FormRequest.from_response(
        response,
        formcss='#existing_users form',
        formdata={'ex_usr_email': 'jackb@openworldinc.com', 'ex_usr_pass': 'CAB43-825bD'},
        callback=self.after_login
        )


    # Function to barse buylist website
    def after_login(self, response):
        # Loop through website and get all the ID numbers for each category of card and plug into the end of the below
        # URL then go to parse data function
        for category_id in response.xpath('//select[@id="bl-category-options"]/option/@value').getall():
            yield scrapy.Request(
                    url="http://www.starcitygames.com/buylist/search?search-type=category&id={category_id}".format(category_id=category_id),
                    callback=self.parse_data,
                    )
    # Function to parse JSON dasta
    def parse_data(self, response):
        # Declare variables
        jsonreponse = json.loads(response.body_as_unicode())
        # Call DataItem class from items.py
        items = DataItem()

        # Scrape category name
        items['Category'] = jsonreponse['search']
        # Loop where other data is located
        for result in jsonreponse['results']:
            # Inside this loop, run through loop until all data is scraped
            for index in range(len(result)):
                # Scrape the rest of needed data
                items['Card_Name'] = result[index]['name']
                items['Condition'] = result[index]['condition']
                items['Rarity'] = result[index]['rarity']
                items['Foil'] = result[index]['foil']
                items['Language'] = result[index]['language']
                items['Buy_Price'] = result[index]['price']
                # Return all data
                yield items
