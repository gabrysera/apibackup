from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re
from webdriver_manager.chrome import ChromeDriverManager

"""Spider per esselunga, sottoforma di web driver utilizza metodi libreria selenium per navigare nel sito di esselunga
e utilizza poi libreria beautifulSoup per prendere l'html della pagina navigata da selenium sotto forma di un oggetto dal quale
poi vengono presi tutti i prodotti e ritornati sotto forma di lista di tuples.
Ogni tuple contiene quindi rispettivamente: nome, codice, prezzo e prezzo originale in caso di sconto (altrimenti valore nullo).
time: mentre selenium naviga la pagina spesso serve aspettare che una pagina carichi prima di eseguire altre operazioni
altrimenti selenium ferma la navigazione, a questo scopo viene utilizzato quando possibile il metodo implicitly_wait(tempo in secondi)
con il quale il driver prova per il periodo di tempo specificato a eseguire le istruzioni, e se non riesce dopo il tempo specificato allora
il driver da un errore. Quando non è possibile eseguire questo metod (ad esempio con lo scrolling di una pagina) allora si utilizza time.sleep
per cercare di assicurarsi che la pagina abbia abbastanza tempo di cariucare prima di eseguire un operazione
"""

class EsseSpider():
    """spider esselunga, per prima cosa indica nome del negozio sul quale viene eseguito il crawling. Utilizza
    una lista di categorie per ricercare prodotti da scaricare dal sito, il metodo crawl è appunto il metodo utilizzato per far
    partire lo spider, farlo navigare e fargli scaricare i prodotti di una determinata categoria

    Returns:
        lista di tuples: lista di tuples dove ogni tuple rappresenta un prodotto (nome, codice, prezzo, prezzo originale in caso di sconto)
    """

    SHOP_NAME = 'esselunga'
    CATEGORIES  = ["frutta e verdura", "pesce e sushi", "carne", "latticini, salumi e formaggi",
    "alimenti vegetali", "pane e pasticceria", "gastronomia e piatti pronti", "colazione, snack e integratori",
     "confezioni alimentari", "surgelati e gelati", "mondo bimbi", "acqua, birra e bibite", "Vini e liquori",
     "Igiene Persona","Cura persona", "Cura casa","Mondo animali", "Cancelleria e multimedia" , "Carte e ricariche"]

    def crawl(category):
        #viene utilizzato un user agent di google per diminuire possibilità di blocco dell'IP da parte del sito web target
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        #tutte queste chrome options listate servono a specificare utili impostazioni per aiutare la navigazione automatica in browser
        chrome_options = Options()
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--start-maximized")
        """la seguente opzione permette la navigazione in modalita headless, sconsigliata in quanto piu lenta e puo portare quindi ad 
        errori dovuti al non caricamento della pagina.
        """
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--ignore-certificate-errors')

        """crea oggetto driver, va specificato il path per prendere l'eseguibile chromedriver.exe
        vedi anche: https://chromedriver.chromium.org/getting-started
        """
        #'C:\Users\gabri\Desktop'
        #'../chromedriver'
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        """ da qui in poi il web driver nagiva il sito esselunga, dalla schermata dove va inserito il cap fino
        alla ricerca dei prodotti, per identificare elementi con cui interagire vengono usati id/css_selector/xpath
        """
        
        driver.get("https://www.esselungaacasa.it/")
        driver.implicitly_wait(10)
        driver.maximize_window()
        driver.find_element_by_id("postcode").send_keys(16145)
        time.sleep(1)
        driver.implicitly_wait(5)
        driver.find_element_by_css_selector("button").click()
       
        try:
            time.sleep(2)
            driver.implicitly_wait(5)
            driver.find_element_by_xpath("//*[@id=\"remodalDialog\"]/ng-include/power-guest-address-verified/div/p[2]/a").click()
        except:
            time.sleep(2)
            driver.implicitly_wait(5)
            driver.find_element_by_xpath("/html/body/div[1]/div[1]/esselunga-delivery-address-verifier/div/div/a").click()
            
        driver.implicitly_wait(5)
        driver.find_element_by_id("searchTextBox").send_keys(category)
        actions = ActionChains(driver)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id=\"cookie\"]/span[3]/a").click()
    
        """inizio  crawling:
            esselungaProducts sara' la lista finale con i prodotti estratti ,
            codes1 viene utilizzato per far si che non si prenda lo stesso prodotto piu' di una volta.
            Reached page è invece una bool che serve a fare scroll verso il basso fino a quando e' possibile poer visualizzare tutti i prodotti
            e per determinare il suo valore viene usato last_height.
            Nel loop quindi il bot continua ad andare in fondo alla pagina fino a che l'html non ha caricato tutti i prodotti, poi utilizzando
            BeatifulSoup si prende l'html della pagina a quel punto sotto forma di un oggetto 'Soup' dal quale possiamo prendere 
            i prodotti e le loro informazioni (i prodotti sono contenuti nella classe content-item).
        """
        reached_page_end = False
        last_height = driver.execute_script("return document.body.scrollHeight")
        while not reached_page_end:
            driver.implicitly_wait(15)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")     
            if last_height == new_height:
                reached_page_end = True
            else:
                last_height = new_height

        esselungaProducts = []   
        codes1 = ['000']
        soup = BeautifulSoup(driver.page_source)
        for item in soup.find_all(class_="content-item"):
            try:
                codice = item.text.split(')')[0].split('(')[1]
            except:
                codice = '000'
            if item.text != '' and codice not in codes1:
                try:
                    codes1.append(codice)
                    name = item.find('span', class_ = "product-brand").text
                    code = codice
                    prices = re.findall(r"[-+]?\d*\.\d+|\d+", item.find('span', class_ = "aria-hidden").text.replace(',', '.'))
                    price = prices[0]
                    try:
                        original_price = prices[1]
                    except:
                        original_price = None
                    esselungaProducts.append((name, code, price, original_price))  
                except Exception as e :print(e)      
        driver.close()
        return esselungaProducts