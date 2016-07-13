import pymongo
from selenium import webdriver
from selenium.webdriver.common.proxy import *
import time

from classes.register_logon import RegisterLogon
from classes import registerDAO
from classes import loginDAO
from classes.captcha2upload.captcha2upload import CaptchaUpload

###These username exists for Rescator###
#zxwnmJgS, mickeymouse9130
#NFIbHzOo, HarDp@$s6

#################################Database Connector#################################
SITE_LIST = ["Hansa","Dreammarket","Rescator"]
NAME_OF_SITE = SITE_LIST[2]
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
    #driver = setup_proxy()
    driver = webdriver.Chrome(executable_path='./chromedriver')
    #register(driver)
    login(driver)


def setup_proxy():
    # Firefox Proxy
    myProxy = PROXY
    proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': myProxy,
    'ftpProxy': myProxy,
    'sslProxy': myProxy,
    'noProxy': '' # set this value as desired
    })
    # driver = webdriver.Firefox(proxy=proxy)

    # Chrome Proxy
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)
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
            mycaptcha = register_object.input_captcha_decaptcha(driver, capture_driver)
            print mycaptcha
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
    print "{0} Login attempts".format(x + 1)


def get_limit_processor(data):
    limit = 40
    captcha_processor = data.get_captcha_processor()
    print captcha_processor
    if captcha_processor == "decaptcha":
        limit = 3
    return limit, captcha_processor


def login(driver):
    login_data = loginDAO.LoginDAO(collection, NAME_OF_SITE)
    login_object = RegisterLogon(login_data)
    print login_data.get_username(), login_data.get_password()
    x = 0
    limit, captcha_processor = get_limit_processor(login_data)
    while x < limit:
        driver.get(login_data.get_url())
        login_object.input_fields(driver)
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
    print "{0} Login attempts".format(x + 1)


if __name__ == "__main__":
    main()
