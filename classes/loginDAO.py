class LoginDAO:

    def __init__(self, collection, NAME_OF_SITE):
        self.collection = collection
        self.NAME_OF_SITE = NAME_OF_SITE
        self.site = self.collection.find_one({"name":self.NAME_OF_SITE})

    def get_url(self):
        return self.site["login_register"]["url"]

    def get_captcha_processor(self):
        return self.site["login_register"]["captcha"]["processor"]

    def get_check_boxes_xpath(self):
        return self.site['login_register']['check_boxes']

    def get_submit_button_xpath(self):
        return self.site['login_register']['submit_button']

    def get_username(self):
        self.site = self.collection.find_one({"name":self.NAME_OF_SITE})
        return self.site["login_register"]["username"]

    def get_password(self):
        self.site = self.collection.find_one({"name":self.NAME_OF_SITE})
        return self.site["login_register"]["password"]

    def get_fields_xpath(self):
        return self.site["login_register"]["fields"]

    def get_captcha_xpath(self):
        return self.site["login_register"]["captcha"]["form"]

    def get_captcha_image_xpath(self):
        return self.site["login_register"]["captcha"]["image"]

    def get_site_name(self):
        return self.site["name"]

    def get_captcha_length(self):
        return self.site["login_register"]["captcha"]["length"]

    def get_validation_string(self, ddos=False):
        if ddos:
            return self.site["ddos"]["validation_string"]
        else:
            return self.site["validation_string"]

    def get_ddos(self):
        try:
            return self.site['ddos']["url"]
        except KeyError:
            return False

    def get_captcha_xpath_ddos(self):
        return self.site['ddos']["form"]

    def get_captcha_image_xpath_ddos(self):
        return self.site['ddos']["image"]

    def get_ddos_submit(self):
        return self.site['ddos']["submit"]
