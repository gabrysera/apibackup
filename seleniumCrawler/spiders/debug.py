from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class CoopSpider:

    SHOP_NAME = 'coop'
    CATEGORIES = ["coop", "Biologico", "senza glutine", "senza lattosio", "Bevande vegetali", "Yogourt", "dessert vegetali", "Pane", "snack", 
    "Biscotti", "cereali", "Merendine", "succo", "vini", "surgelati", "gelati", "vitamine","minerali", "tonici", "energetici",
    "integratori", "frutta", "verdura", "funghi", "legumi", "aromi", "carne" ,"pesce", "piatti pronti", "pasta fresca", "salse", 
    "piadine", "patatine", "salumi", "formaggi", "uova", "pasta", "riso", "farina", "olio", "bevande",
    "caffe", "infusi", "dolcificanti", "birre", "torte", "minestroni", "pizza", "focaccia", "pasticceria", "omogeneizzati", "creme", "pappe",
    "pannolini", "salviettine", "igiene", "condimenti", "sottaceti", "sottoli", "salse", "pate", "spezie", "dadi", 
    "in scatola", "colazione", "caramelle", "cioccolato", "cialde", "capsule", "zucchero", "acqua", "aperitivi", "sciroppi",
    "liquori", "amari", "alcool", "capelli", "viso", "corpo", "uomo", "igiene orale", "casa", "animali", "cancelleria", "stampanti",
    "pile", "lampadine", "giardinaggio", "pellet", "auto"]

#    @classmethod
#    def crawl(cls, category):

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
#cambiare path eseguibile chromedriver.exe
browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
browser.get("https://www.coopshop.it/my/dashboard")
browser.implicitly_wait(20)
browser.maximize_window() 
#account liguria:liguriamarco2021 , liguriamarco@protonmail.com
#account lombardia:Spider2021! , orlandofurioso1011@protonmail.com
browser.find_element_by_name('username').send_keys('liguriamarco@protonmail.com') 
browser.find_element_by_name('password').send_keys('liguriamarco2021')

actions = ActionChains(browser)
actions.send_keys(Keys.ENTER)
actions.perform()
actions2 = ActionChains(browser)
time.sleep(2)
#element = browser.find_element_by_xpath('/html/body/div[1]/cookie-consent/section/section/div/div/div/div/div[2]/div[3]/div[1]')
#ActionChains(browser).move_to_element(element).click().perform()





coopProducts = []
browser.find_element_by_css_selector("input[type='search']").send_keys('pane')
browser.find_element_by_css_selector("input[type='search']").click()
time.sleep(5)
actions.send_keys(Keys.ENTER)
actions.perform()

end_of_page = False
browser.implicitly_wait(15)
last_height = browser.execute_script("return document.body.scrollHeight")
while not end_of_page:
    browser.implicitly_wait(15)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")     
    time.sleep(10)
    new_height = browser.execute_script("return document.body.scrollHeight")
    if last_height == new_height:
        end_of_page = True
    else:
        last_height = new_height
soup = BeautifulSoup(browser.page_source)
products = soup.find_all('div', class_ = 'col-xs-12 col-sm-6 col-md-4 ng-scope')
for p in products:
    try:
        nested = p.contents[0].contents[0].contents[0]
        name = nested.contents[10].text
        code = nested.contents[4].contents[0].contents[1].text
        price = nested.contents[5].contents[1].text.replace('\n',' ').replace(',','.').replace('\xa0','')
        try:
            old_price = nested.contents[5].contents[1].contents[0].contents[3].text.replace(',','.').replace('\xa0','')
            coopProducts.append((name, code, price, old_price)) 
        except:
            coopProducts.append((name, code, price, None))
    except Exception as e:
        print(e)
browser.close()
if len(coopProducts) < 2:
    print("found only" + str(len(coopProducts)) + "in category: " + 'pane')
#return coopProducts