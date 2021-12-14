from ..items import Item
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urlparse
from scrapy.exceptions import DropItem

class BennetspiderSpider(CrawlSpider):
    name = 'bennetSpider'
    allowed_domains = ['www.bennet.com']
    start_urls = ['http://www.bennet.com/']
    count = 0

    rules = (
        Rule(LinkExtractor(allow=[r'p/', r'c/']), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = Item()
        nome = response.css(".product-name__title::text").get()
        quantità =  response.css(".weight-price-info::text").get()
        if nome != None:
            try:
                item['nome'] = nome + quantità
            except:
                item['nome'] = nome
            item['prezzo'] = response.css(".c-product-price__amount b::text").get().replace('\xa0','')
            parsed_uri = urlparse(response.url)
            item['codice'] = parsed_uri.path.split('P_')[1].split('?list')[0]
            item['prezzo_non_scontato'] = response.css(".c-product-price__original b::text").get()
            self.count += 1
        else:
            DropItem(item)
        return item
