from captcha_methods import Captcha

class RegisterLogon:
    def __init__(self, data):
        self.data = data

    def verify_login(self, driver):
        validation_string = self.data.get_validation_string()
        print validation_string
        html = driver.page_source
        if validation_string in html:
            print "Incorrect Captcha, trying again"
            return False
        else:
            print "Captcha Solved, login created sucessfully and saved to database for future login attempts"
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

    def input_captcha_decaptcha(self, driver, capture_driver):
        captcha_xpath = self.data.get_captcha_xpath()
        originalImage = Captcha.get_captcha(driver, self.data)
        thresholdImage = Captcha.threshold()
        #Makes it a bit eaiser to solve for the Captcha Monekys, but sometimes doesnt work
        #captcha =  capture_driver.solve("./captchas/threshold_captcha.png")
        captcha = capture_driver.solve("./captchas/captcha.png")
        driver.find_element_by_xpath(captcha_xpath).send_keys(captcha)
        return captcha

    def input_captcha_tesseract(self, driver):
        captcha_xpath = self.data.get_captcha_xpath()
        originalImage = Captcha.get_captcha(driver, self.data)
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
