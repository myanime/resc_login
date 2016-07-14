import random
import string
class RegisterDAO:

    def __init__(self, collection, NAME_OF_SITE):
        self.collection = collection
        self.NAME_OF_SITE = NAME_OF_SITE
        self.site = self.collection.find_one({"name":self.NAME_OF_SITE})

    def overwrite_username(self, username = ""):
        if username == "":
            for i in range(8):
                username = username + random.choice(string.ascii_letters)
        self.collection.update(
                           {"name":self.NAME_OF_SITE},
                           {"$set":{"login_register.username":username}},
                           True
                        )
        return username
    def overwrite_password(self, password = ""):
        if password == "":
            for i in range(8):
                password = password + random.choice(string.ascii_letters)
        self.collection.update(
                           {"name":self.NAME_OF_SITE},
                           {"$set":{"login_register.password":password}},
                           True
                        )
        return password
    def find_or_generate_username(self):
        self.site = self.collection.find_one({"name":self.NAME_OF_SITE})
        try:
            username = self.site["login_register"]["username"]
            return username
        except:
            username = ""
            for i in range(8):
                username = username + random.choice(string.ascii_letters)
            self.collection.update(
                               {"name":self.NAME_OF_SITE},
                               {"$set":{"login_register.username":username}},
                               True
                            )
            return username
  
    def find_or_generate_password(self):
        self.site = self.collection.find_one({"name":self.NAME_OF_SITE})
        try:
            password = self.site["login_register"]["password"]
            return password
        except:
            password = ""
            for i in range(8):
                password = password + random.choice(string.ascii_letters)
            self.collection.update(
                               {"name":self.NAME_OF_SITE},
                               {"$set":{"login_register.password":password}},
                               True
                            )
            return password
    def get_url(self):
        return self.site["registration"]["url"]
    def get_captcha_processor(self):
        return self.site["registration"]["captcha"]["processor"]
    def get_check_boxes_xpath(self):
        return self.site['registration']['check_boxes']
    def get_submit_button_xpath(self):
        return self.site['registration']['submit_button']
    #Note - these methods get the Password and Username from the Login section
    def get_username(self):
        self.site = self.collection.find_one({"name":self.NAME_OF_SITE})
        return self.site["login_register"]["username"]
    def get_password(self):
        self.site = self.collection.find_one({"name":self.NAME_OF_SITE})
        return self.site["login_register"]["password"]
    def get_fields_xpath(self):
        return self.site["registration"]["fields"]
    def get_captcha_xpath(self):
        return self.site["registration"]["captcha"]["form"]
    def get_captcha_image_xpath(self):
        return self.site["registration"]["captcha"]["image"]
    def get_site_name(self):
        return self.site["name"]
    def get_captcha_length(self):
        return self.site["registration"]["captcha"]["length"]
    def get_validation_string(self, ddos=False):
        return self.site["validation_string"]


        
