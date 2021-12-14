import sqlite3

class Read_products_from_db():

    def read(shop_name):
        """prende dal database prodotti che sono stati associati tramite codice ean tramite sqlite query

        Args:
            shop_name (String): Nome negozio dal quale si vogliono vedere i prodotti matchati

        Returns:
            [list]: lista di oggetti che poi verranno convertiti in json per restituirli al front end tramite API
        """
        database_name = 'prodotti.db'
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        total = cursor.execute("SELECT COUNT(*) FROM prodotti_cliente WHERE negozio ='"+shop_name+"\'").fetchone()[0]
        db_products = cursor.execute("""SELECT Descrizione, SpiderProdotti.prezzo , prodotti_cliente.Prezzo, codice FROM SpiderProdotti 
                                        INNER JOIN prodotti_cliente ON SpiderProdotti.negozio=prodotti_cliente.negozio 
                                        WHERE SpiderProdotti.codice = prodotti_cliente.'Product Code' AND SpiderProdotti.negozio = '"""
                                        +shop_name+"\'").fetchall()
        products_data = []
        for p in db_products:
            product = {'name' : p[0], 'priceOnline':p[1], 'priceOffline':p[2], 'code':p[3]}
            products_data.append(product)
        print(total)
        return {'productsData': products_data,
                'numberOfProducts':str(round((len(db_products))/total*100))}
