# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    """questa classe è utilizzata dalla classe dello spider per definire il dizionario di elementi che verranno presi dalla pagina web.
    con scrapy.Field() indichiamo che le variabili potranno essere di ogni subclass della classe Field (nel nostro caso quasi sempre String).
    lo stesso vale per tutte le altre classi di questo file.
    """    
    nome = scrapy.Field()
    codice = scrapy.Field()
    prezzo = scrapy.Field()
    prezzo_non_scontato = scrapy.Field()
    pass

