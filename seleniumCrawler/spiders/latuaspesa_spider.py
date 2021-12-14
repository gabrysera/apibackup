from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class LaTuaSpesaSpider():

    SHOP_NAME = 'LaTuaSpesa'
    CATEGORIES = ["Biologico", "senza glutine", "senza lattosio", "Bevande vegetali", "Yog0urt", "dessert vegetali", "Pane", "snack", 
    "Biscotti", "cereali", "Merendine", "snack dolci", "succo", "vini", "surgelati", "gelati", "vitamine","minerali", "tonici", "energetici",
    "integratori", "frutta", "verdura", "funghi", "legumi", "aromi", "carne" ,"pesce", "piatti pronti", "pasta fresca", "salse", "sughi", 
    "piadine", "basi dolci", "impasto", "basi salate", "patatine", "salumi", "formaggi", "uova", "pasta", "riso", "farina", "olio", "bevande",
    "caffe", "infusi", "dolcificanti", "birre", "torte", "minestroni", "pizza", "focaccia", "pasticceria", "omogeneizzati", "creme", "pappe",
    "pannolini", "salviettine", "infanzia", "cura corpo", "igiene", "condimenti", "sottaceti", "sottoli", "salse", "pate", "spezie", "dadi", 
    "in scatola", "Specialità etniche", "colazione", "caramelle", "cioccolato", "cialde", "capsule", "zucchero", "acqua", "aperitivi", "sciroppi",
    "liquori", "amari", "alcool", "capelli", "viso", "corpo", "uomo", "igiene orale", "Cura corpo", "casa", "animali", "cancelleria", "stampanti",
    "prese", "accessori telefonia", "pc", "pile", "lampadine", "giardinaggio", "pellet", "auto", "brico"]
    
    def crawl(category):
        
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

        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        
        driver.get("https://www.latuaspesa.com/shop/home")
        driver.implicitly_wait(10)
        driver.maximize_window()
        driver.find_element_by_css_selector(".icon-user").click()
        time.sleep(0.3)
        driver.find_element_by_id("username").send_keys("orlandofurioso1011@protonmail.com")
        driver.find_element_by_name("password").send_keys("Spider2021!")
        time.sleep(0.3)

        actions = ActionChains(driver)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        driver.find_element_by_class_name("icon-delete").click()
        driver.find_element_by_css_selector("input[type='search']").send_keys(category)
        actions.perform()
        
        Latuaspesa_products = []
        time.sleep(2)
        end_of_page = False
        while not end_of_page:
            driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
            time.sleep(1)
            try:
                driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menuContent"]/div[2]/div/div/div[2]/div[3]/div[2]/div[2]/button')))
                element.click()
                time.sleep(1)
            except:
                end_of_page = True
            
        soup = BeautifulSoup(driver.page_source)
        products = soup.find_all('div', class_ = 'col-xs-12 col-sm-6 col-md-4')
        for p in products:
            name = p.find('div', class_ = 'product-brand p-brand').text + ", " + p.find('div', class_ = 'product-name p-name').text
            code = p.find('div', class_ = 'product-id sr-only u-identifier').text
            price = p.find('span', class_ = 'price').text.replace('\xa0€','').replace(',','.')
            Latuaspesa_products.append((name, code, price, None))
        products_on_sale = soup.find_all('div', class_ = 'col-xs-12 col-sm-6 col-md-4 has-promo')
        for pos in products_on_sale:
            name = pos.find('div', class_ = 'product-brand p-brand').text + ", " + p.find('div', class_ = 'product-name p-name').text
            code = pos.find('div', class_ = 'product-id sr-only u-identifier').text
            prices = pos.find_all('span', class_ = 'price')
            #alcuni prodotti sono scontasti ma non si vede il prezzo originale
            try:
                price = prices[1].text.replace('\xa0€','').replace(',','.')
                original_price = prices[0].text.replace('\xa0€','').replace(',','.')
            except:
                price = prices[0].text.replace('\xa0€','').replace(',','.')
                original_price = None
            Latuaspesa_products.append((name, code, price, original_price))
        driver.close()
        return Latuaspesa_products