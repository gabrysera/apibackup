import sqlite3, random

class Parser():

    @classmethod
    def put_products_on_db(cls, database_name, spider):
        """dato un database e uno spider, fa partire lo spider, prende i prodotti e li carica nel database

        Args:
            database_name (String): nome del database dove verranno caricati i prodotti scaricati
            spider (Spider): selenium bot che fa da spider per un sito target

        Returns:
            [type]: [description]
        """
        random.shuffle(spider.CATEGORIES)
        for category in spider.CATEGORIES:
            products_tuple = spider.crawl(category)
            cls.write_to_db(products_tuple, database_name, spider.SHOP_NAME)
        return len(products_tuple)


    def write_to_db(products_tuples, database_name, negozio):
        """prende lista di tuples e nome database e inserisce dati della lista all'
            interno del database
    
        Args:
            products_tuples (list of tuples):lista con prodotti
            database_name ([type]): nome del database dove inserire i prodotti
        """        
        table_name = "ProdottiSpider"
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS """ + table_name + """(
                        nome text,
                        codice text,
                        prezzo INTEGER, 
                        prezzo_originale INTEGER,
                        negozio text
        )""")

        for i in range(0, len(products_tuples)):
            try:
                code = c.execute("select codice from " + table_name + " where codice = "+"'"+ products_tuples[i][1] +"' AND negozio = " +"'"+ negozio +"'").fetchone()
                if code == None:
                    c.execute("""insert into """ + table_name + """ values (?,?,?,?,?)""", (
                        products_tuples[i][0].replace('\"',' '),
                        products_tuples[i][1],
                        products_tuples[i][2],
                        products_tuples[i][3],
                        negozio
                        ))
                else:
                    c.execute("UPDATE " + table_name +" SET nome = ? ,prezzo = ? ,prezzo_originale = ? WHERE codice = ?", (
                        products_tuples[i][0].replace('\"',' '),
                        products_tuples[i][2],
                        products_tuples[i][3],
                        products_tuples[i][1]
                    ))
            except Exception as e:
                print("database insert error")
                print(e)
        conn.commit()
        conn.close()  
        print("commit")     