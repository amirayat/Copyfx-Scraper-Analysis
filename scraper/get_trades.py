
import time
import pandas as pd

from random import randint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager


extension='/home/amir/code/copyfx/scraper/extension_8_2_3_0.crx'


class Scraper():
    """ calss to scrape copyfx """

    def __init__(self, headless=True):
        """ initial confs"""

        chrome_options = webdriver.ChromeOptions()

        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_extension(extension)

        if headless:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(
                                    ChromeDriverManager().install()),
                                    options=chrome_options)
        time.sleep(1)  # Wait for some time to load

    def gotopage(self):
        """
        go to trader page
        """

        time.sleep(60)

        TRADER_URL = str()
                                                                                                                #NAME                                       Com     Investors   Balance     Fund          
        # TRADER_URL = 'https://www.copyfx.com/ratings/rating-all/show/143640/tab/profit/period/all/'           #WALLSTREETINVEST - DAX ONLY                30%     1636        8046        4664943
        # TRADER_URL = 'https://www.copyfx.com/ratings/rating-all/show/94638/tab/profit/period/all/'            #EASY124                                    30%     1396        10546       1888311
        # TRADER_URL = 'https://www.copyfx.com/ratings/rating-all/show/115440/tab/profit/period/all/'           #KINGSCROSS - I ONLY GOLD                   30%     441         2107        1274386      
        # TRADER_URL = 'https://www.copyfx.com/ratings/rating-all/show/155126/tab/profit/period/all/'           #THREESIXNINEVIPS - KARMA GOLD VIPS         30%     34          2273        1117124
        # TRADER_URL = 'https://www.copyfx.com/ratings/rating-all/show/76541/tab/profit/period/all/'            #TITOVIGOR - TIO BILLIONS                   15%     165         3000        809456
        # TRADER_URL = 'https://www.copyfx.com/ratings/rating-all/show/185017/tab/profit/period/all/'           #HAMCAPITAL - HIGH ALCHEMY                  10%     178         1015        578773
        # TRADER_URL = 'https://www.copyfx.com/ratings/rating-all/show/171747/tab/profit/period/all/'           #SCALPINGDAYTRADING - SCALPING DAY TRADING  25%     411         605         692356
        # TRADER_URL = 'https://www.copyfx.com/ratings/rating-all/show/121676/tab/profit/period/all/'           #ULTRONFX - ULTRON EURUSD                   30%     265         250         458758
        # TRADER_URL = 'https://www.copyfx.com/ratings/rating-all/show/89198/tab/trading-history/period/all/'   #SIMPLETRADEEA                              30%     604         727         2999702
        # TRADER_URL = 'https://www.copyfx.com/ratings/rating-all/show/87240/tab/trading-history/period/all/'   #NORTHEASTWAYINBTC                          30%     105         0           
        # TRADER_URL = 'https://www.copyfx.com/ratings/rating-all/show/87242/tab/trading-history/period/all/'   #FASTWAYINETH                               30%     292         32999       361585
        # TRADER_URL = 'https://www.copyfx.com/ratings/rating-all/show/85119/tab/trading-history/period/all/'   #FASTWAY                                    30%     259         28531       309015
        
        self.driver.get(TRADER_URL)

        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="account-info-tabs-ul"]/li[3]/a'))) 
        time.sleep(randint(1, 2))

    def tadehistorytab(self):
        """
        select tradehistory tab
        """
        self.driver.find_element(By.XPATH, '//*[@id="account-info-tabs-ul"]/li[3]/a').click()
        time.sleep(randint(1, 2))

    def crawltrades(self):
        """
        navigate on trade pages
        """ 
        for i in range(10):
            time.sleep(1)
            trade_list = self.driver.find_element(By.XPATH, '//*[@id="card-right"]/div[2]/div[2]').text.replace("\n",",").split("#")[1:]
            if trade_list:
                print(trade_list)
                break
        tradef_df  = pd.DataFrame(trade_list)[0].str.split(',',expand=True)
        to = int(self.driver.find_element(By.XPATH, '//*[@id="tab_trading-history"]/div/div/div[2]/ul/li[7]/a').text)
        for page in range(2,to):
            # self.driver.find_element(By.XPATH, f'//a[@data-page = "{page}"]').click()
            for i in range(3):
                try:
                    self.driver.find_element(By.LINK_TEXT, str(page)).click()
                    break
                except:
                    time.sleep(2)
            time.sleep(3)
            trade_list = self.driver.find_element(By.XPATH, '//*[@id="card-right"]/div[2]/div[2]').text.replace("\n",",").split("#")[1:]
            tradef_df  = pd.concat([tradef_df,pd.DataFrame(trade_list)[0].str.split(',',expand=True)])
            tradef_df.to_csv("trades.csv", sep=",")


    


if __name__ == '__main__':
    """Enter your login credentials here"""
    from pprint import pprint

    fb = Scraper(headless=False)
    fb.gotopage()
    fb.tadehistorytab()
    fb.crawltrades()
