import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import Item
from urllib.parse import urlparse
from scrapy.exceptions import DropItem

class TigotaSpider(CrawlSpider):
    name = 'tigotaSpider'
    allowed_domains = ['tigota.it']
    start_urls = ['https://www.tigota.it/']

    rules = (
        Rule(LinkExtractor(allow = [r'it/'], restrict_xpaths = '//*[contains(concat( " ", @class, " " ), concat( " ", "main", " " ))]'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = Item()
            parsed_uri = urlparse(response.url)
            
            item['nome'] = response.css(".base::text").get()
            item['codice'] = parsed_uri.path[-6:]
            item['prezzo'] = response.css(".product-info-price .price::text").get().replace('\xa0','')
            try:
                item['prezzo_non_scontato'] = response.css(".product-info-price .old-price .price::text").get()
            except:
                item['prezzo_non_scontato'] = None
        except:
            DropItem(item)
        return item
