from captcha_methods import Captcha
from selenium.common.exceptions import NoSuchElementException

class RegisterLogon:
    def __init__(self, data):
        self.data = data

    def verify_login(self, driver, ddos=False):
        validation_string = self.data.get_validation_string(ddos)
        print "Checking for text:", validation_string
        html = driver.page_source
        if validation_string in html:
            print "Incorrect Captcha, trying again"
            return False
        else:
            print "Captcha Solved"
            return True

    def click_submit(self, driver):
        submit_button = self.data.get_submit_button_xpath()
        driver.find_element_by_xpath(submit_button).click()

    def input_fields(self, driver):
        username = self.data.get_username()
        password = self.data.get_password()
        fields_array = self.data.get_fields_xpath()
        for field in fields_array:
            if field["type"] == "password":
                try:
                    driver.find_element_by_xpath(field["xpath"]).send_keys(password)
                except NoSuchElementException as not_found:
                    driver.close()
                    return field["xpath"], "xpath not found", not_found
            if field["type"] == "username":
                try:
                    username_input = driver.find_element_by_xpath(field["xpath"])
                    username_input.clear()
                    username_input.send_keys(username)
                except NoSuchElementException as not_found:
                    driver.close()
                    return field["xpath"], "xpath not found", not_found
            if field["type"] == "custom":
                try:
                    driver.find_element_by_xpath(field["xpath"]).send_keys(field["value"])
                except NoSuchElementException as not_found:
                    driver.close()
                    return field["xpath"], "xpath not found", not_found
            if field["type"] == "checkbox":
                try:
                    checkbox = driver.find_element_by_xpath(field["xpath"])
                    checkbox.click()
                except NoSuchElementException as not_found:
                    driver.close()
                    return field["xpath"], "xpath not found", not_found
        return "Fields entered sucessfully..."

    def input_captcha_decaptcha(self, driver, capture_driver, ddos=False):
        if ddos:
            captcha_xpath = self.data.get_captcha_xpath_ddos()
            originalImage = Captcha.get_captcha(driver, self.data, ddos=True)
        else:
            #If the site is Rescator, use the DownLoadMethod to get the captcha
            if self.data.NAME_OF_SITE == "Rescator":
                captcha_xpath = self.data.get_captcha_xpath()
                originalImage = Captcha.get_captcha_dlm(driver, self.data)
            else:
                captcha_xpath = self.data.get_captcha_xpath()
                originalImage = Captcha.get_captcha(driver, self.data)
                thresholdImage = Captcha.threshold()

        # This will solve the threshold captcha, the next one the real captcha
        # captcha =  capture_driver.solve("./captchas/threshold_captcha.png")
        captcha = capture_driver.solve("./captchas/captcha.png")
        print "Solve attempt by 2Captcha: ", captcha
        driver.find_element_by_xpath(captcha_xpath).send_keys(captcha)
        return captcha

    def input_captcha_tesseract(self, driver):
        captcha_xpath = self.data.get_captcha_xpath()
        originalImage = Captcha.get_captcha_dlm(driver, self.data)
        thresholdImage = Captcha.threshold()
        captcha = Captcha.decode_captcha(originalImage, thresholdImage)
        input_captcha = Captcha.length_check(captcha, self.data)
        if input_captcha:
            try:
                driver.find_element_by_xpath(captcha_xpath).send_keys(input_captcha)
            except:
                #Sometimes tesseract gives back non ASCII letters
                return False
            return True #Still have to check for correct code
        else:
            return False
