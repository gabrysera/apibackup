from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import Item
from scrapy.exceptions import DropItem
from urllib.parse import urlparse



class CarrefourSpider(CrawlSpider):
    """class CarrefourSpider:
    classe principale dello spider:
    definisce come lo spider deve agire su un sito (o un gruppo di siti), incluso anche come come estrarre altri link dai siti di partenza 
    (i.e. follow links) e come estrarre le informazioni desiderate (i.e. scraping items). 

    Args:
        CrawlSpider(requisito): 
            è lo spider piu utilizzato per seguire link da una pagina generando un effetto a cascata, seguendo tutti gli URL 
            selezionati dalle rules che gli vengono specificate.

        name(requisito): 
            Stringa che definisce il nome dello spider.Il nome dello spider comporta come lo spider viene collocato da scrapy, 
            di conseguenza deve essere unico. Comunque è possibile generare piu' instancedello stesso spider.

        allowed_domains(opzionale):
            Una lista di stringhe contenenti i dominii sui quali lo spider ha il permesso di agire. Tutte le richieste
            per URLS che non appartengono a un dominio di questa lista verranno scartate. In questo caso il dominio specificato è quello del
            carrefour per evitare che lo spider vada a visitare tutti i siti di tutte le pagine collegate a quelle visitate e non si concentri
            sul crawling dei prodotti carrefour
        
        start_urls(opzionale): 
            lista di URLS che , nel caso in cui lo spider viene chiamato dalla command line e nessun URL viene specificato, allora lo spider utilizza
            questa lista come link di partenza per il crawling.

        custom_settings(opzionale):
            Un dizionario di impostazioni che verranno sovrascritte dalla configurazione a livello di progetto (settings.py file) durante 
            l'esecuzione di questo spider. Deve essere definito come attributo di classe poiché le impostazioni vengono aggiornate prima dell'istanza.
            In questo caso l'impostazione ITEM_PIPELINES, che si occupa di processare le informazioni scaricate dallo spider, specifica che 
            dovra' appunto ptocessare queste informazioni utilizzando la classe CarrefourCrawlerPipeline nel file pipelines.py

        rules(opzionale): 
            Che è un elenco di uno (o più) oggetti Regola. Ogni Regola definisce un determinato comportamento per la scansione del sito. 
            Gli oggetti regole sono descritti di seguito. Se più regole corrispondono allo stesso collegamento, verrà utilizzata la prima, 
            in base all'ordine in cui sono definite in questo attributo. Nel nostro esempio abbiamo solo una rule che determina di seguire i
            link trovati (follow = true) ed in particolare di seguire i link i cui url assoluti matchano con 'p/' o 'spesa-online/',
            (allow = [r'p/',r'spesa-online/']) e una volta seguiti chiamare il metodo specificato (callback = 'parse_item') 
            passandogli la response ottenuta dal link seguito ( in poche parole l'html della pagina da cui poi prendere informazioni)
    """    

    name = 'carrefourSpider'
    allowed_domains = ['www.carrefour.it']
    start_urls = ['https://www.carrefour.it/spesa-online']

    custom_settings = {
        'ITEM_PIPELINES': {'zelandoCrawler.pipelines.Pipeline': 300},
    }

    rules = (
        Rule(LinkExtractor(allow = [r'p/',r'spesa-online/']), callback='parse_item', follow=True),
    )

    count = 0

    def parse_item(self, response):
        """ Il metodo parse_item è responsabile dell'elaborazione della risposta e della restituzione dei dati raccolti e/o più URL da seguire.
            per prima cosa richiama classe CarrefourItem per specificare che il nostro item sara' un dictionary definito nella classe CarrefourItem.
            dopodichè controlla con un if il nome del prodotto: se il nome è null allora significa che stiamo prendendo dati da una pagina che non 
            ha un prodotto, quindi droppiamo l'item. le informazioni dei prodotti vengono specificate tramite i css selector dell'html 
            delle pagine desiderate: Solitamente nello stesso sito, per i prodotti i css selector sono sempre gli stessi.

        Args:
            response (Response): the response to parse
            more on Response Object: https://docs.scrapy.org/en/latest/topics/request-response.html#scrapy.http.Response

        Returns:
            [type not defined]: must return an iterable of Request and/or item objects.
            more on item object: https://docs.scrapy.org/en/latest/topics/items.html#topics-items
        """       

        item = Item()
        name = response.css('.product-description::text').get()
        if name != None:
            item['nome'] = name
            item['prezzo'] = response.css('.value::text').get().replace('\n','')
            parsed_uri = urlparse(response.url)
            item['codice'] = parsed_uri.path.split('/')[-1].replace('html','')
            try:
                item['prezzo_non_scontato'] = response.css('.list .value::text').get().replace('\n','')
            except:
                item['prezzo_non_scontato'] = None
            self.count += 1
        else:
            DropItem(item)
        return item

