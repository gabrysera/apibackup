from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from scrapyCrawler.zelandoCrawler.start_crawling import ScrapyCrawler
from seleniumCrawler.start_crawling import SeleniumSpiders
from flask_cors import CORS, cross_origin
from read_products_from_db import Read_products_from_db as rpd
app = Flask(__name__)
api = Api(app)
CORS(app, support_credentials=True)
"""per avviare parte server: nel terminal nella cartella del progetto scrivere: python myapp.py oppure run da vs code.
per avviare front end andare dal terminal nella folder crawlerwebapp e nel terminal scrivere: npm run serve
"""

#Post method per far partire gli spider
@app.route('/SpidersView', methods=['POST']) 
@cross_origin(supports_credentials=True)
def post():
    """post method per fare partire gli spider
    """
    data = request.json
    SeleniumSpiders.crawl_shop(data['name'], 'prova.db')
    ScrapyCrawler.crawl_shop(data['name'])
    return jsonify(data)

#get method per prendere dal database i prodotti associati 
@app.route('/MatchesView', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_products():
    """API GET che prende prodotti di un determinato negozio che sono stati associati con i corrispondenti del sito online

    Returns:
        [Object in JSON format]: json contenente prodotti e le loro informazioni (nome, prezzo online, prezzo offline, codice)
    """
    data = request.args
    result = rpd.read(data['shopName'])
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
