import scrapy
import time
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from scrapy import Selector

global list_of_dictionaries
list_of_dictionaries = []

class SpideySpider(scrapy.Spider):
    name = 'spidey'
    allowed_domains = ['www.google.com']
    start_urls = ['https://www.google.com/']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63'

    ua = UserAgent()

    def __init__(self):
        self.options = ChromeOptions()
        self.options.add_argument("--disable-blink-features")
        self.options.add_argument("start-maximized")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--incognito')
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--use-fake-ui-for-media-stream")
        self.options.add_argument(
            f'--user-agent={self.ua.chrome}')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=self.options)

    def get_liq_values(self,symbol,liquidations,value_liquidated,avg_liquidation_value):
        return{
            'symbol' : symbol,
            'liquidations' : liquidations,
            'value_liquidated' : value_liquidated,
            'avg_liquidation_value' : avg_liquidation_value
        }


    def parse(self,response):
        global list_of_dictionaries
        self.driver.get('https://liquidation.wtf/')
        time.sleep(3)
        
        resp = Selector(text = self.driver.page_source)
        
        for x in resp.xpath('//div[@class="w-full"]/div/table/tbody/tr'):
            symbol = x.xpath('.//td/span/text()').get()
            liquidations = x.xpath('.//td[2]/div/text()').get()
            value_liquidated = x.xpath('.//td[3]/div/text()').get()
            avg_liquidation_value = x.xpath('.//td[5]/div/text()').get()
                        
            try:
                avg_liquidation_value = avg_liquidation_value.replace('$', '')
                avg_liquidation_value = avg_liquidation_value.replace(',', '')
                avg_liquidation_value = float(avg_liquidation_value)
            except:
                avg_liquidation_value = 0
                
            single_pair = self.get_liq_values(symbol,liquidations,value_liquidated,avg_liquidation_value)
            list_of_dictionaries.append(single_pair)
            
        self.driver.quit()
        
    
def WebCrawler():
    process = CrawlerProcess()
    process.crawl(SpideySpider)
    process.start()
    return list_of_dictionaries