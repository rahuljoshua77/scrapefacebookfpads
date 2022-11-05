from hashlib import new
from attr import attributes
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os,json
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
cwd = os.getcwd()

opts = webdriver.ChromeOptions()

opts.headless = False
opts.add_argument('--disable-setuid-sandbox')
opts.add_argument('--log-level=3') 
opts.add_argument('--disable-infobars')
opts.add_argument('--no-sandbox')
opts.add_argument('--ignore-certifcate-errors')
opts.add_argument('--ignore-certifcate-errors-spki-list')
opts.add_argument("--incognito")
opts.add_argument('--no-first-run')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument("--disable-infobars")
opts.add_argument("--window-size=500,800")
opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_experimental_option("useAutomationExtension", False)
opts.add_experimental_option("excludeSwitches",["enable-automation"])
opts.add_experimental_option('excludeSwitches', ['enable-logging'])
opts.add_argument('--disable-notifications')
 
def xpath_type(el,mount):
    return wait(browser,10).until(EC.element_to_be_clickable((By.XPATH, el))).send_keys(mount)

def xpath_el(el):
    element_all = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, el)))
    return browser.execute_script("arguments[0].click();", element_all)

def open_browser(limit,url):
    global browser
    browser = webdriver.Chrome(options=opts)   
    browser.get(url)
    error = 1
    scroll = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, f'//div[text()="Pemberitahuan"]')))
    print(f"[{time.strftime('%d-%m-%y %X')}] Please wait, Trying to get data!")
    browser.execute_script("arguments[0].scrollIntoView();", scroll)
     
    for i in range(1,limit):
        try:
            link_fp = wait(browser,2).until(EC.presence_of_element_located((By.XPATH, f'(//span[text()="Bersponsor"]/parent::div/parent::div/parent::span/parent::div/parent::div/div/div/div/a)[{i}]'))).get_attribute('href')
            scroll = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, f'(//span[text()="Bersponsor"]/parent::div/parent::div/parent::span/parent::div/parent::div/div/div/div/a)[{i}]')))
            browser.execute_script("arguments[0].scrollIntoView();", scroll)
            print(f"[{time.strftime('%d-%m-%y %X')}] Get Link: {link_fp}")
            with open('success.txt','a') as f: f.write(f'{link_fp}\n')
                
            error = 1
        except Exception as e:
            if error == 10:
                print(f"[{time.strftime('%d-%m-%y %X')}] No Data, Program stop!")
                print(e)
                break
            else:
                error = error + 1
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print(f"[{time.strftime('%d-%m-%y %X')}] Delay 8s for getting new data")
                sleep(8)
                try:
                    link_fp = wait(browser,2).until(EC.presence_of_element_located((By.XPATH, f'(//span[text()="Bersponsor"]/parent::div/parent::div/parent::span/parent::div/parent::div/div/div/div/a)[{i}]'))).get_attribute('href')
                    scroll = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, f'(//span[text()="Bersponsor"]/parent::div/parent::div/parent::span/parent::div/parent::div/div/div/div/a)[{i}]')))
                    browser.execute_script("arguments[0].scrollIntoView();", scroll)
                
                    print(f"[{time.strftime('%d-%m-%y %X')}] Get Link: {link_fp}")
                    with open('success.txt','a') as f: f.write(f'{link_fp}\n')
                      
                except:
                    pass
        
if __name__ == '__main__':
    print(f"[{time.strftime('%d-%m-%y %X')}] Automation")
    url = input(f"[{time.strftime('%d-%m-%y %X')}] Link URL: ")
    limit = int(input(f"[{time.strftime('%d-%m-%y %X')}] Limit Data: "))
    open_browser(limit,url)
 
    
     
