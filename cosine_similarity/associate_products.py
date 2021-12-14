import sqlite3
from .cosine_distance import Cosine_distance

class Associate_products(object):  

    def __init__(self, spider_table_name, client_table_name, database_name):
        self.SPIDER_TABLE_NAME = spider_table_name
        self.CLIENT_TABLE_NAME = client_table_name
        self.DATABASE_NAME = database_name


    def cosine_similarity(self, negozio):
        vector = Cosine_distance
        conn = sqlite3.connect(self.DATABASE_NAME)
        cur = conn.cursor()
        offline_products = cur.execute("SELECT Descrizione, prezzo, 'Product Code' FROM " + self.CLIENT_TABLE_NAME).fetchall()  
        online_products = cur.execute("SELECT nome, prezzo, codice FROM " + self.SPIDER_TABLE_NAME).fetchall()
        dictionary = []
        for op in online_products:
            dictionary.append(op[0])
        for off_product in offline_products:
            result = vector.get_vectorized_word(vector, dictionary, off_product[0])
            if result['similarity'] > 0.85:
                print('associated')
            

    