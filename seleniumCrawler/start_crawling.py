#import parser and spiders
from .parser import Parser
from .spiders.esse_spider import EsseSpider 
from .spiders.iperal_spider import IperalSpider
from .spiders.tigros_spider import TigrosSpider
from .spiders.coop_spider import CoopSpider
from .spiders.iper_spider import IperSpider
from .spiders.latuaspesa_spider import LaTuaSpesaSpider

#spider get products and put them on Online database
"""chiama principale metodo spider che prende prodotti e li carica su un database.
parametri: categoria per c6rawler, nome database dove inserire i dati
"""
class SeleniumSpiders:

    def crawl_shop(shop_name, database_name):
        """con una lista di opzioni seleziona lo spider del negozio desiderato e lo fa partire

        Args:
            shop_name (String): nome del negozio per il quale si vuole eseguire il crawling
            database_name (String): nome del database sul quale vogliono essere salvati i prodotti
        """
        options = {'esselunga' : EsseSpider,
                    'iperal' : IperalSpider,
                    'tigros' : TigrosSpider,
                    'coop' : CoopSpider,
                    'iper' : IperSpider,
                    'latuaspesa' : LaTuaSpesaSpider
        }
        if shop_name in options.keys():
            return Parser.put_products_on_db(database_name, options[shop_name])
        else:
            return None




