class LoginDAO:

    def __init__(self, collection, NAME_OF_SITE):
        self.collection = collection
        self.NAME_OF_SITE = NAME_OF_SITE
        self.site = self.collection.find_one({"name":self.NAME_OF_SITE})
    def get_url(self):
        return self.site["login"]["url"]
    def get_captcha_processor(self):
        return self.site["login"]["captcha"]["processor"]
    def get_check_boxes_xpath(self):
        return self.site['login']['check_boxes']
    def get_submit_button_xpath(self):
        return self.site['login']['submit_button']
    def get_username(self):
        self.site = self.collection.find_one({"name":self.NAME_OF_SITE})
        return self.site["login"]["username"]
    def get_password(self):
        self.site = self.collection.find_one({"name":self.NAME_OF_SITE})
        return self.site["login"]["password"]
    def get_fields_xpath(self):
        return self.site["login"]["fields"]
    def get_captcha_xpath(self):
        return self.site["login"]["captcha"]["form"]
    def get_site_name(self):
        return self.site["name"]



        
