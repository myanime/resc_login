from captcha_methods import Captcha

class Register:
    @staticmethod
    def verify_login_creation(driver, registration_data):
        validation_string = registration_data.get_validation_string()
        print validation_string
        html = driver.page_source
        if validation_string in html:
            print "Incorrect Captcha, trying again"
            return False
        else:
            print "Captcha Solved, login created sucessfully and saved to database for future login attempts"
            return True
    @staticmethod
    def click_submit(driver, registration_data):
        submit_button = registration_data.get_submit_button_xpath()
        driver.find_element_by_xpath(submit_button).click()
    @staticmethod
    def input_fields(driver, registration_data):
        username = registration_data.get_username()
        password = registration_data.get_password()
        fields_array = registration_data.get_fields_xpath()
        for field in fields_array:
            if field["type"] == "password":
                driver.find_element_by_xpath(field["xpath"]).send_keys(password)
            if field["type"] == "username":
                username_input = driver.find_element_by_xpath(field["xpath"])
                username_input.clear()
                username_input.send_keys(username)
            if field["type"] == "custom":
                driver.find_element_by_xpath(field["xpath"]).send_keys(field["value"])
            if field["type"] == "checkbox":
                checkbox = driver.find_element_by_xpath(field["xpath"])
                checkbox.click()
                
    @staticmethod
    def input_captcha_decaptcha(driver, registration_data, capture_driver):
        captcha_xpath = registration_data.get_captcha_xpath()
        originalImage = Captcha.get_captcha(driver, registration_data)
        thresholdImage = Captcha.threshold()
        #Makes it a bit eaiser to solve for the Captcha Monekys
        captcha =  capture_driver.solve("./captchas/threshold_captcha.png")
        driver.find_element_by_xpath(captcha_xpath).send_keys(captcha)
        return captcha
    @staticmethod
    def input_captcha_tesseract(driver, registration_data):
        captcha_xpath = registration_data.get_captcha_xpath()
        originalImage = Captcha.get_captcha(driver, registration_data)
        thresholdImage = Captcha.threshold()
        captcha = Captcha.decode_captcha(originalImage, thresholdImage)
        input_captcha = Captcha.length_check(captcha, registration_data)
        if input_captcha:
            try:
                driver.find_element_by_xpath(captcha_xpath).send_keys(input_captcha)
            except:
                #Sometimes tesseract gives back non ASCII letters
                return False
            return True #Still have to check for correct code
        else:
            return False
