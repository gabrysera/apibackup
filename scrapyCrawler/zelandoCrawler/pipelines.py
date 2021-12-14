import sqlite3
from scrapy.exceptions import DropItem
import os

class Pipeline:
    """dopo che lo spider analizza  un item, questo viene automaticamente processato attraverso il metodo process_item, che deve essere implementato
    dalla classe di pipeline specificata in settings.py (questa classe) e nel caso ce ne fosse piu di una deve essere specificata quale si usa 
    anche nella classe dello spider, attraverso l'attributo custom settings. Nel caso dello spider per carrefour infatti, questa classe CarrefourCrawlerPipeline 
    implementa il metodoprocess_item, nelle settyings abbiamo un dictionary contenente 'libraccioCrawler.pipelines.CarrefourCrawlerPipeline' 
    assieme ad altre pipelinee nella classe dello spider carrefourSpider abbiamo la custom settings  che specifica l'utilizzo di questa 
    pipeline.
    """
    
    def __init__(self):
        """in python __init__() method è chiamato automaticamente ogni volta che crei un instance di una classe, quindi in questo caso ogni
        volta che lo spider avra' analizzato un elemento poi quando in modo automatico va a chiamare il process_item method prima eseguira'
        questo init method che è utilizzato per connettersi al database e creare la tabella
        """        
        self.table_name = "ProdottiSpider"
        abs_pathname = os.path.abspath("tigota2.db")
        self.database_path = abs_pathname
        self.connect_to_db()
        self.create_table()

    def connect_to_db(self):
        self.conn = sqlite3.connect(self.database_path)
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS """ + self.table_name + """(
                        nome text,
                        codice text,
                        prezzo INTEGER, 
                        prezzo_originale INTEGER,
                        negozio text
        )""")

    def process_item(self, item, spider):
        """metodo chiamato automaticamente dallo spider (nel nostro caso CarrefourSpider) ogni volta che un item viene analizzato,
        cosi che poi qui possa essere appunto processato , che in questo caso significa in realta' metterlo in un database

        Args:
            item (Field)): item da inserire nel database
            spider (Spider): ogni spider come nome ha il nome del negozio su cui viene usato piu la parola 'Spider', quindi dallo spider
            name viene preso il nome del negozio cosi da inserirlo nel database con il prodotto

        Raises:
            Drop item 
        """        
        if item['nome'] != None:
            self.store_in_db(item, spider.name.replace('Spider',''))
            return item
        else:
            raise DropItem("item dropped")

    def store_in_db(self, item, shop_name):
        code = self.curr.execute("select codice from " + self.table_name + " where codice = "+"'"+ item['codice'] +"' AND negozio = " +"'"+ shop_name +"'").fetchone()
        if code == None:
            self.curr.execute("""insert into """ + self.table_name + """ values (?,?,?,?,?)""", (
                item['nome'],
                item['codice'],
                item['prezzo_non_scontato'],
                item['prezzo'],
                shop_name
                ))
        else:
            self.curr.execute("UPDATE " + self.table_name +" SET nome = ? ,prezzo = ? ,prezzo_originale = ? WHERE codice = ?", (
                        item['nome'],
                        item['prezzo'],
                        item['prezzo_non_scontato'],
                        item['codice'],
                    ))
        self.conn.commit()