# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_javascript project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

# Name of project
BOT_NAME = 'scrapy_javascript'

# Module where spider is
SPIDER_MODULES = ['scrapy_javascript.spiders']
# Mode where to create new spiders
NEWSPIDER_MODULE = 'scrapy_javascript.spiders'

# Obey robots.txt rules set by website, disable to not be detected as web scraper
ROBOTSTXT_OBEY = False
# The path of the csv file that contains the proxies/user agnets paired with URLs
PROXY_CSV_FILE = "proxies.csv"

# The downloader middleware is a framework of hooks into Scrapy's request/response processing.
# It's a light, low-level system for globally altering Scrapy's requests and responses. 
DOWNLOADER_MIDDLEWARES = {
        # This middleware enables working with sites that require cookies, such as those that use sessions. 
        # It keeps track of cookies sent by web servers, and send them back on subsequent requests (from that spider), just like web browsers do.
        'scrapy_splash.SplashCookiesMiddleware': 723,
         
        'scrapy_splash.SplashMiddleware': 725,
        # This middleware allows compressed (gzip, deflate) traffic to be sent/received from web sites.
        # This middleware also supports decoding brotli-compressed responses, provided brotlipy is installed.
        'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# URL that splash server is running on, must be activated to use splash
SPLASH_URL = 'http://localhost:8050'
# The class used to detect and filter duplicate requests
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# This middleware provides low-level cache to all HTTP requests and responses. It has to be combined with a cache storage backend as well as a cache policy.
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# The maximum number of concurrent (ie. simultaneous) requests that will be performed by the Scrapy downloader (default: 16)

CONCURRENT_ITEMS = 1
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# If enabled, Scrapy will wait a random amount of time (between 0.5 * DOWNLOAD_DELAY and 1.5 * DOWNLOAD_DELAY) while fetching requests from the same website.
RANDOMIZE_DOWNLOAD_DELAY = True
# Delay between scraping webpages
DOWNLOAD_DELAY = 10 
# The download delay setting will honor only one of:
# Number of concurrent requests made to one URL(enabled)
CONCURRENT_REQUESTS_PER_DOMAIN = 1 
# Number of concurrent requests made to one IP(disabled)
#CONCURRENT_REQUESTS_PER_IP = 1


# Disable cookies (enabled by default)
# Whether to enable the cookies middleware. If disabled, no cookies will be sent to web servers.
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
# A boolean which specifies if the telnet console will be enabled (provided its extension is also enabled)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
        'Referer': 'https://www.trollandtoad.com/magic-the-gathering/1041'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'scrapy_javascript.middlewares.ScrapyJavascriptSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'scrapy_javascript.middlewares.ScrapyJavascriptDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'scrapy_javascript.pipelines.ScrapyJavascriptPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# This is an extension for automatically throttling crawling speed based on load of both the Scrapy server and the website you are crawling.
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 15
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

