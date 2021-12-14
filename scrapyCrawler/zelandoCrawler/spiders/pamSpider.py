import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import Item
from urllib.parse import urlparse
from scrapy.exceptions import DropItem

class PamSpider(CrawlSpider):
    name = 'pamSpider'
    allowed_domains = ['pamacasa.pampanorama.it']
    start_urls = ['http://pamacasa.pampanorama.it/']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    count = 0

    def parse_item(self, response):
        try:
            item = Item()
            parsed_uri = urlparse(response.url)
            item['nome'] = parsed_uri.path.replace('/prodotto/','').replace('-',' ')[:-6].replace('\n','').replace('\r','') + response.css(".product-size.between::text").get().replace('\n','').replace('\r','').replace(' ','')
            item['codice'] = parsed_uri.path.replace('/prodotto/','').replace('-',' ')[-6:]
            item['prezzo'] = response.css("span.price::text").get().replace('\n','').replace('\r','').replace(' ','')
            try:
                item['prezzo_non_scontato'] = response.css(".old-price::text").get()
            except:
                item['prezzo_non_scontato'] = None
            self.count += 1
        except:
            DropItem(item)
        return item

