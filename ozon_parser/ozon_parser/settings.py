BOT_NAME = "ozon_parser"

SPIDER_MODULES = ["ozon_parser.spiders"]
NEWSPIDER_MODULE = "ozon_parser.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

ROTATING_PROXY_LIST = [
   '85.26.146.169:80',
   '95.66.138.21:8880',
   '95.84.166.138:8080',
   '176.192.65.34:5020',
   '185.42.228.66:1080',
   '109.94.182.9:4145',
   '213.184.153.66:8080',
   '109.94.182.128:4145',
   '46.29.116.6:4145',
   '82.146.45.136:3128',
   '77.39.8.165:3629',
   '91.238.2.30:3128',
   '91.205.131.110:53339',
   '46.47.197.210:3128',
   '176.197.144.158:4153',
   '212.220.13.98:4153',
   '95.143.12.201:60505',
   '80.242.56.115:3128',
   '85.113.55.123:8080',
]

DOWNLOADER_MIDDLEWARES = {
   'ozon_parser.middlewares.SeleniumMiddleWare': 1,
   'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
   'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}

PRODUCT_COUNT = 100