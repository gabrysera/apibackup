from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class IperalSpider:

    SHOP_NAME = 'iperal'
    CATEGORIES = ["Biologico", "senza glutine", "senza lattosio", "Bevande vegetali", "Yog0urt", "dessert vegetali", "Pane", "snack", 
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
        chrome_options.add_argument('--no-proxy-server')
        browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        browser.get("https://www.iperalspesaonline.it/")
        browser.implicitly_wait(30)
        element=browser.find_element(By.CSS_SELECTOR,".icon-profile")
        element.click()

        browser.maximize_window()    
        browser.find_element_by_xpath("//*[@id=\"cookie-bar-base\"]/div/div[2]/button[1]").click()   
        
        browser.find_element_by_xpath("//input[@type='email']").send_keys("orlandofurioso1011@protonmail.com")

        element3 = browser.find_element_by_xpath("//input[@type='password']")
        element3.send_keys("Spider2021")

        browser.find_element_by_css_selector("button[class='login-button v-btn v-btn--has-bg theme--light v-size--large']").click()
        time.sleep(2)
        try:
            browser.implicitly_wait(50)
            browser.find_element_by_css_selector("div[class='vuedl-layout__closeBtn']").click()

            browser.find_element_by_css_selector("i[class='v-icon notranslate icon icon-burgermenu theme--light']").click()
        except:
            time.sleep(1)
        try:
            browser.find_element_by_css_selector("div[class='vuedl-layout__closeBtn']").click()
            
            browser.find_element_by_css_selector("i[class='v-icon notranslate icon icon-burgermenu theme--light']").click()
        except:
            time.sleep(1)
        browser.find_element_by_css_selector("input[type='search']").send_keys(category)
        browser.find_element_by_css_selector("input[type='search']").send_keys(Keys.ENTER)
        
        iperalProducts = []
        
        next_page = True
        while next_page:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source)
            products = soup.find_all('div', class_ = 'd-flex body flex-column fill-width')
            for p in products:
                name = p.find('span', class_ = 'brand').text + ' ' + p.find('span', class_ = 'name').text + ' ' + p.find('span', class_ = 'descr').text.replace('\xa0€','')
                code = p.contents[0].attrs['title'].split('(')[1].split('-')[0]
                price = p.find('div', class_ = 'cur-price').text.replace('\xa0€','').replace(',','.')
                try:
                    old_price = p.find('div', class_ = 'old-price').text.replace('\xa0€','').replace(',','.')
                except:
                    old_price = None
                iperalProducts.append((name, code, price, old_price))
            browser.execute_script("document.body.scrollHeight")
            try:
                browser.implicitly_wait(10)
                browser.find_element_by_xpath('//*[@id="app"]/div[1]/main/div/div/div/div[2]/div[2]/nav/ul/li[8]/button').click()
            except:
                next_page = False
        browser.close()
        return iperalProducts

  