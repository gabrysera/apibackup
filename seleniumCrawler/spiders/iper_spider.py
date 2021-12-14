from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class IperSpider:

    SHOP_NAME = 'iper'
    CATEGORIES = ["Biologico", "senza glutine", "senza lattosio", "Bevande vegetali", "Yogurt", "dessert vegetali", "Pane", "snack", 
    "Biscotti", "cereali", "Merendine", "snack dolci", "succo", "vini", "surgelati", "gelati", "vitamine","minerali", "tonici", "energetici",
    "integratori", "frutta", "verdura", "funghi", "legumi", "aromi", "carne" ,"pesce", "piatti pronti", "pasta fresca", "salse", "sughi", 
    "piadine", "basi dolci", "impasto", "basi salate", "patatine", "salumi", "formaggi", "uova", "pasta", "riso", "farina", "olio", "bevande",
    "caffe", "infusi", "dolcificanti", "birre", "torte", "minestroni", "pizza", "focaccia", "pasticceria", "omogeneizzati", "creme", "pappe",
    "pannolini", "salviettine", "infanzia", "cura corpo", "igiene", "condimenti", "sottaceti", "sottoli", "salse", "pate", "spezie", "dadi", 
    "in scatola", "Specialità etniche", "colazione", "caramelle", "cioccolato", "cialde", "capsule", "zucchero", "acqua", "aperitivi", "sciroppi",
    "liquori", "amari", "alcool", "capelli", "viso", "corpo", "uomo", "igiene orale", "Cura corpo", "casa", "animali", "cancelleria", "stampanti",
    "prese", "accessori telefonia", "pc", "pile", "lampadine", "giardinaggio", "pellet", "auto", "brico"]

    @classmethod
    def crawl(cls, category):
        
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options = Options()
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--start-maximized")
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--ignore-certificate-errors')
        browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

        browser.get("https://iperdrive.iper.it/spesa-online/it/varese")
        browser.maximize_window() 
        browser.implicitly_wait(10)
        browser.find_element(By.CSS_SELECTOR,".ada-tooltip-close").click()
        browser.find_element_by_xpath('//*[@id="iubenda-cs-banner"]/div/div/div/div[2]/div[2]/button[2]').click()
        browser.find_element_by_id("searchButton").click()
        browser.find_element_by_id("SimpleSearchForm_SearchTerm").send_keys(category)
        actions = ActionChains(browser)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        next_page = True
        iperProducts = []
        c = 1
        while next_page:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source)
            products = soup.find_all('div', class_ = 'ada-product-wrapper')
            c += 1
            for p in products:
                products_info = p.find('div', class_ = 'product-description-wrapper')
                p_name = products_info.contents[1].text.replace('\n','').replace('\t','').lower()
                p_brand = products_info.contents[3].text.replace('\n','').replace('\t','')
                p_id = p.contents[15].text.replace('\n','').replace('\t','').lower()
                p_price = p.find('div', class_ = 'final-price').text.replace('\n','').replace('\t','').replace(',','.')
                p_old_price = p.find('div', class_ = 'old-price').text.replace('\n','').replace('\t','').replace(',','.')
                if '€' not in p_old_price:
                    p_old_price = None
                iperProducts.append((p_brand + ", " + p_name, p_id, p_price, p_old_price))
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            try:
                browser.implicitly_wait(10)
                browser.find_element_by_xpath("//a[@title='Passa a pagina "+ str(c) +"']").click()
            except:
                next_page = False
        browser.close()
        return iperProducts