import subprocess

class ScrapyCrawler:

    def crawl_shop(shop_name):
        """con una lista di opzioni seleziona lo spider del negozio desiderato e lo fa partire tramite un subprocess

        Args:
            shop_name (String): nome del negozio per il quale si vuole eseguire il crawling
        """
        shops = ['pam', 'bennet', 'carrefour']
        if shop_name in shops:
            spider_name = shop_name + 'Spider'
            subprocess.check_output(['scrapy', 'crawl', spider_name], cwd=r'C:\Users\gabri\Desktop\pro\scrapyCrawler\zelandoCrawler')
        return None