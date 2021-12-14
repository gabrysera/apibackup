from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class TigrosSpider:

    SHOP_NAME = 'tigros'
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
        #'C:\Users\gabri\Desktop\chromedriver'
        #'../chromedriver'
        browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

        browser.get("https://www.tigros.it/shop/home")

        browser.implicitly_wait(10)
        browser.maximize_window() 
        browser.find_element(By.CSS_SELECTOR,".dropdown-toggle").click()
        
        browser.find_element_by_name('username').send_keys('orlandofurioso1011@protonmail.com') 
        browser.find_element_by_name('password').send_keys('Spider2021!')
        actions = ActionChains(browser)
        actions.send_keys(Keys.ENTER)
        actions.perform()

        element = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-close-button")))
        element.click()
        browser.find_element_by_css_selector("input[type='search']").send_keys(category)
        actions.perform()

        end_of_page = False
        tigrosProducts = []
        while not end_of_page:
            time.sleep(1)
            browser.execute_script("window.scrollBy(0,document.body.scrollHeight)")
            time.sleep(1)
            browser.execute_script("window.scrollBy(0,-650)")
            time.sleep(0.5)
            try:
                time.sleep(0.5)
                element = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-load-more")))
                element.click()
            except:
                end_of_page = True
        soup = BeautifulSoup(browser.page_source)
        products = soup.find_all('div', class_ = 'col-xs-12 col-sm-6 col-md-6 col-lg-4')
        for p in products:
            name = p.find('a', class_ = 'sr-only u-url product-url-detail').text + " " + p.find('div', class_ = 'product-qty').text
            code = p.find('div', class_ = 'product-brand p-brand').previous.replace('cod.','')
            try:
                price = p.find('div', class_ = "promo_body price-font").text
                try:
                    original_price = p.find('span', class_ = "price_old category-inpage").text
                except:
                    original_price = None
            except:
                try:
                    price = p.find('span', class_ = 'cur-price price-font').text
                except:
                    price = None
                original_price = None     
            tigrosProducts.append((name, code, price, original_price))
        browser.close()
        print('\n' + str(len(tigrosProducts)) + " : " + category + '\n')
        return tigrosProducts