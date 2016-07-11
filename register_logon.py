import pymongo
from selenium import webdriver
import time
from register_logon.captcha_methods import Captcha
from register_logon.register_methods import Register
from register_logon.login_methods import Login
from register_logon import registerDAO
from register_logon import loginDAO
from register_logon.captcha2upload.captcha2upload import CaptchaUpload

###These username exists for Rescator###
#zxwnmJgS, mickeymouse9130
#NFIbHzOo, HarDp@$s6

#################################Database Connector#################################
NAME_OF_SITE = "Dreammarket"
#NAME_OF_SITE = "Rescator"
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

registration_data = registerDAO.RegisterDAO(collection, NAME_OF_SITE)
login_data = loginDAO.LoginDAO(collection, NAME_OF_SITE)

def main():
    driver = webdriver.Chrome(executable_path="./chromedriver")
    print get_or_create_passwords()
    '''
    These methods overwrite the password in the database. If you dont
    specify a password or username, it will be generated. These
    methods would be usefull when you get banned.
    '''
    #overwrite_username_password()
    register(driver, registration_data)
    #login(driver, login_data)

def get_or_create_passwords():
    #This will return username and password pair from the DB or generate them and save to the DB
    username = registration_data.find_or_generate_username()
    password = registration_data.find_or_generate_password()
    return username, password
def overwrite_username_password(username = "", password = ""):
    username = registration_data.overwrite_username(username)
    password = registration_data.overwrite_password(password)
    return username, password
    
def register(driver, registration_data):
    x = 0
    limit = 40
    captcha_processor = registration_data.get_captcha_processor()
    print captcha_processor
    if captcha_processor == "decaptcha":
        limit = 3
    while x < limit:
        registration_url = registration_data.get_url()
        driver.get(registration_url)
        if captcha_processor == "decaptcha":
            mycaptcha = Register.input_captcha_decaptcha(driver, registration_data, capture_driver)
            print mycaptcha
        else:
            mycaptcha = Register.input_captcha_tesseract(driver, registration_data)
        if mycaptcha:
            Register.input_fields(driver, registration_data)
            Register.click_submit(driver, registration_data)
            verify = Register.verify_login_creation(driver, registration_data)
            if verify == True:
                break
        else:
            pass
            #print "Flag Incorrect Captcha (important for decaptcha)"
        x = x + 1
    print "{0} Login attempts".format(x + 1)
    
def login(driver, login_data):
    x = 0
    while x < 40:
        login_url = login_data.get_url()
        driver.get(login_url)
        Login.input_fields(driver, login_data)
        if login_data.get_captcha_processor == "WRITE decaptcha HERE":
            mycaptcha = Login.input_captcha_decaptcha(driver, login_data)
        else:
            mycaptcha = Login.input_captcha_tesseract(driver, login_data)
        if mycaptcha:
            Login.click_submit(driver, login_data)
            #Will get stuck in loop if Captcha is correct but Username doesnt exist
            verify = Login.verify_login(driver, login_data)
            if verify == True:
                break
        else:
            pass
            #print "Flag Incorrect Captcha (important for decaptcha)"
        x = x + 1
    print "{0} Login attempts".format(x + 1)

if __name__ == "__main__":
    main()
