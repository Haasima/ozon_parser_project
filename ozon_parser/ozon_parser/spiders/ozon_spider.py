from scrapy_selenium import SeleniumRequest
from scrapy import Spider, signals
from .urls import BASE_URL, BASE_URL_PARAMS_SORTING, CATEGORY_URL, API_URL, API_URL_PARAMS
from ozon_parser.settings import PRODUCT_COUNT
from .utils import parse_os_from_json
import pandas as pd
import json

class OzonSpider(Spider):
    name = "ozon"
    allowed_domains = ['ozon.ru']
   
    products_urls = []
    products_os = []

    def start_requests(self):
        url = f"{BASE_URL}{CATEGORY_URL}{BASE_URL_PARAMS_SORTING}"
        self.logger.info(f'URL: {url}')
        yield SeleniumRequest(url=url, callback=self.parse_urls, wait_time=5)

    def parse_urls(self, response):
        xpath = '//a[contains(@href, "smartfon") and contains(@href, "/product/") and not(contains(@href, "podstavka")) and not(contains(@href, "chehol"))]/@href'
        links = response.xpath(xpath).extract()

        for i in links:
            if i not in self.products_urls:
                self.products_urls.append(i)

        if len(self.products_urls) >= PRODUCT_COUNT:
            for product_url in self.products_urls[:PRODUCT_COUNT]:
                self.logger.info(f"PRODUCT URL: {product_url}")
                yield SeleniumRequest(url=f"{API_URL}{product_url}{API_URL_PARAMS}", callback=self.parse_product, wait_time=5)
        else:
            try:
                current_page = int(response.url.split("?page=")[1].split("&")[0])
            except:
                current_page = 1

            next_page = current_page + 1

            next_page_url = f"{BASE_URL}/category/telefony-i-smart-chasy-15501/?page={next_page}&sorting=rating"
            print(next_page)

            yield SeleniumRequest(url=next_page_url, callback=self.parse_urls, wait_time=5)
        
    def parse_product(self, response):
        response_ = response.css('pre::text').get()
        if response_:
            response_json = json.loads(response_)
            os = parse_os_from_json(data_json=response_json)
            self.products_os.append(os)
            print(f"Data: {os}; Len urls: {len(self.products_urls)}; Len OS: {len(self.products_os)}")

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(OzonSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        data = pd.Series(self.products_os).value_counts()

        with open("data.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(data.to_json()))