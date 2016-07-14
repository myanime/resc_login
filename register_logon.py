import pymongo
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time

from classes.register_logon import RegisterLogon
from classes import registerDAO
from classes import loginDAO
from classes.captcha2upload.captcha2upload import CaptchaUpload


#################################Database Connector#################################
SITE_LIST = ["Hansa","Dreammarket","Rescator","Alphabay"]
NAME_OF_SITE = SITE_LIST[1]
PROXY = "schlupfi.de:3128"
DATABASE = "database"
COLLECTION = "sites"
CONNECTION_STRING = "mongodb://localhost:27017"
CAPTCHA_API_KEY = "72ac3cc4e1646f6c0c16da8addd81b07"

capture_driver = CaptchaUpload(CAPTCHA_API_KEY)
print "Captcha Balance: $", capture_driver.getbalance()
connection = pymongo.MongoClient(CONNECTION_STRING)
database = connection[DATABASE]
collection = database[COLLECTION]
####################################################################################

def main():
    driver = webdriver.Chrome(executable_path='./chromedriver')
    #IF you want to use your own proxy uncomment this and coment out above. Otherwise
    #It will use onion.to proxy. Only Alphabay at the moment supports cusotom proxy
    #(the xpaths have to be recollected - Not really a big job)
    #driver = setup_proxy()
    driver = load_page(driver)
    #register(driver)
    print login(driver)

    time.sleep(15)
    driver.close()

''' This method takes care of any DDOs captures that may arise'''
def load_page(driver):
    login_data = loginDAO.LoginDAO(collection, NAME_OF_SITE)
    login_object = RegisterLogon(login_data)

    page = login_data.get_url()
    ddos = login_data.get_ddos()
    x = 0
    if ddos:
        driver.set_page_load_timeout(30)
        driver.get(ddos)
        if ddos == driver.current_url:
            while x < 3:
                login_object.input_captcha_decaptcha(driver, capture_driver, ddos=True)
                submit = login_data.get_ddos_submit()
                driver.find_element_by_xpath(submit).click()
                time.sleep(5)
                verified = login_object.verify_login(driver, ddos=True)
                if verified:
                    time.sleep(3)
                    return driver
                else:
                    x = x + 1
                    time.sleep(3)
                    #driver.get(page)
    if x == 3:
        return False

    driver.set_page_load_timeout(30)
    driver.get(page)
    return driver

def setup_proxy():
    # The real onion links are through http:// not https://
    # The xpath will be slightly different when not using onion.to proxy - because of the banner add
    # Dreammarket: http://lchudifyeqm4ldjj.onion
    # Hansa: http://hansamkt2rr6nfg3.onion
    # https://rescator.cm/

    # Routes TOR through chrome, uses privoxy
    # apt-get install tor
    # apt-get install privoxy
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=http://127.0.0.1:8118')
    driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=chrome_options)
    # driver.get("http://www.whatismyip.com/")
    return driver


def get_or_create_passwords(data):
    # This will return username and password pair from the DB or generate them and save to the DB
    username = data.find_or_generate_username()
    password = data.find_or_generate_password()
    return username, password


'''
This method overwrites the password and username in the database. If you dont
specify a password or username, it will be generated. This would be useful when you get banned.
'''
def overwrite_username_password(data, username ="", password =""):
    username = data.overwrite_username(username)
    password = data.overwrite_password(password)
    return username, password


def register(driver):
    register_data = registerDAO.RegisterDAO(collection, NAME_OF_SITE)
    register_object = RegisterLogon(register_data)
    print get_or_create_passwords(register_data)
    x = 0
    limit, captcha_processor = get_limit_processor(register_data)
    while x < limit:
        driver.get(register_data.get_url())
        if captcha_processor == "decaptcha":
            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            mycaptcha = register_object.input_captcha_decaptcha(driver, capture_driver)
        else:
            mycaptcha = register_object.input_captcha_tesseract(driver)
        if mycaptcha:
            register_object.input_fields(driver)
            register_object.click_submit(driver)
            verify = register_object.verify_login(driver)
            if verify == True:
                break
        else:
            if captcha_processor == "decaptcha":
                print "Flag Incorrect Captcha (save a few cents when capthca is incorrect)"
        x = x + 1
    return "{0} Login attempts".format(x + 1)


def get_limit_processor(data):
    limit = 40
    captcha_processor = data.get_captcha_processor()
    print "Using:", captcha_processor
    if captcha_processor == "decaptcha":
        limit = 3
    return limit, captcha_processor


def login(driver):
    try:
        login_data = loginDAO.LoginDAO(collection, NAME_OF_SITE)
        login_object = RegisterLogon(login_data)
        print "Using username/login_register:", login_data.get_username(), login_data.get_password()
        x = 0
        limit, captcha_processor = get_limit_processor(login_data)
        while x < limit:
            driver.get(login_data.get_url())
            print login_object.input_fields(driver)
            if captcha_processor == "decaptcha":
                mycaptcha = login_object.input_captcha_decaptcha(driver, capture_driver)
            else:
                mycaptcha = login_object.input_captcha_tesseract(driver)
            if mycaptcha:
                login_object.click_submit(driver)
                verify = login_object.verify_login(driver)
                if verify == True:
                    break
            else:
                pass
                #print "Flag Incorrect Captcha (important for decaptcha)"
            x = x + 1
        return "{0} Login attempts".format(x + 1)
    except TimeoutException as timeout:
        driver.close()
        return "The page took too long to load", timeout


if __name__ == "__main__":
    main()
