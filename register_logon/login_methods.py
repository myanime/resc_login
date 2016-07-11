from selenium import webdriver
import time
import random
import string
from captcha_methods import Captcha
import loginDAO

class Login:
    @staticmethod
    def verify_login(driver, login_data):
        #This methods will need to be tweaked to account for all the problems that can arise when loging in.
        html = driver.page_source
        ###################RESCATOR/Site SPECIFIC#########################
        #Add field to DB, verification_string
        if "Buy @ Wholesale Prices!" in html:
            print "Captcha Solved, login created sucessfully and saved to database for future login attempts"
            return True
        else:
            print "Incorrect Captcha, trying again"
            return False
    @staticmethod    
    def click_checkboxes(driver, login_data):
        #Have to extend this, on alot of sites there will be a
        #lot of check boxes that need clicking, M/F etc etc
        checkbox_one = login_data.get_check_boxes_xpath()
        driver.find_element_by_xpath(checkbox_one).click() #... checkbox 2,3 etc
    @staticmethod
    def click_submit(driver, login_data):
        submit_button = login_data.get_submit_button_xpath()
        driver.find_element_by_xpath(submit_button).click()
    @staticmethod
    def input_fields(driver, login_data):
        username = login_data.get_username()
        password = login_data.get_password()
        fields_array = login_data.get_fields_xpath()
        for field in fields_array:
            if field["type"] == "password":
                driver.find_element_by_xpath(field["xpath"]).send_keys(password)
            if field["type"] == "username":
                driver.find_element_by_xpath(field["xpath"]).send_keys(username)
    @staticmethod
    def input_captcha_decaptcha(driver, login_data):
        #To be implemented
        return None
    @staticmethod
    def input_captcha_tesseract(driver, login_data):
        captch_xpath = login_data.get_captcha_xpath()
        originalImage = Captcha.get_captcha(driver)
        thresholdImage = Captcha.threshold()
        captcha = Captcha.decode_captcha(originalImage, thresholdImage)
        site_name = login_data.get_site_name()
        
        ###################RESCATOR/Site SPECIFIC#########################
        '''
        If the captcha is being solved using the OCR methods in the
        Captcha class, most probably an extra method needs to be added
        to the class, to deal with captcha length. OCR works on simple
        Captchas like those used on Rescator, but it takes a lot of tries
        between 5-40. An alternative is to add the length of the captcha to
        mongoDB: captcha_length
        '''
        if  site_name == "Rescator":
            input_captcha = Captcha.length_check(captcha)
        elif site_name == "Something Else":
            #input_captcha = Captcha.some_other_check(captcha)
            pass
        else:
            input_captcha = captcha
        ##################################################################
        if input_captcha:
            try:
                driver.find_element_by_xpath(captch_xpath).send_keys(input_captcha)
            except:
                #Sometimes tesseract gives back non ASCII letters
                return False
            return True #Still have to check for correct code
        else:
            return False
