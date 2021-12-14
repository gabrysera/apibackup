import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import Item
from urllib.parse import urlparse
from scrapy.exceptions import DropItem
import re

class AcquaesaponeSpider(CrawlSpider):
    name = 'acquaesaponeSpider'
    allowed_domains = ['acquaesapone.gospesa.it']
    start_urls = ['https://acquaesapone.gospesa.it/']

    rules = (
        Rule(LinkExtractor(deny = ['content/']), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = Item()
            parsed_uri = urlparse(response.url)
            # /path1/path2
            cod = re.findall(r'\d+', parsed_uri.path.split('/')[2])[0]
            item['nome'] = response.css(".tvproduct-content-title::text").get()
            item['codice'] = cod
            item['prezzo'] = response.css(".tvcurrent-price::text").get().replace('\xa0','')
            try:
                item['prezzo_non_scontato'] = response.css(".regular-price::text").get()
            except:
                item['prezzo_non_scontato'] = None
        except:
            DropItem(item)
        return item
