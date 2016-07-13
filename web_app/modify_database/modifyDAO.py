class ModifyDAO:
    def __init__(self,collection, NAME_OF_SITE):
        self.collection = collection
        self.NAME_OF_SITE = NAME_OF_SITE
        self.site = collection.find_one({"name":self.NAME_OF_SITE})


    def set_login_username_xpath(self, xpath):
        self.site = collection.find_one({"name":self.NAME_OF_SITE})
        fields = self.site["login"]["fields"]
        new_fields_array = []
        for element in fields:
            if element["type"] == "username":
                new_element = {"xpath":xpath,"type":element['type'],"required":element['required']}
                new_fields_array.append(new_element)
            else:
                new_fields_array.append(element)
                
        self.collection.update({"name":self.NAME_OF_SITE},
                          {"$set":{"login.fields":new_fields_array}})

        
    def set_login_password_xpath(self, xpath):
        self.site = collection.find_one({"name":self.NAME_OF_SITE})
        fields = self.site["login"]["fields"]
        new_fields_array = []
        for element in fields:
            if element["type"] == "password":
                new_element = {"xpath":xpath,"type":element['type'],"required":element['required']}
                new_fields_array.append(new_element)
            else:
                new_fields_array.append(element)
                
        self.collection.update({"name":self.NAME_OF_SITE},
                          {"$set":{"login.fields":new_fields_array}})


    def set_registration_username_xpath(self, xpath):
        self.site = collection.find_one({"name":self.NAME_OF_SITE})
        fields = self.site["registration"]["fields"]
        new_fields_array = []
        for element in fields:
            if element["type"] == "username":
                print element
                new_element = {"xpath":xpath,"type":element['type'],"required":element['required']}
                new_fields_array.append(new_element)
            else:
                new_fields_array.append(element)
                
        self.collection.update({"name":self.NAME_OF_SITE},
                          {"$set":{"registration.fields":new_fields_array}})

        
    def set_registration_password_xpath(self, xpath):
        self.site = collection.find_one({"name":self.NAME_OF_SITE})
        fields = self.site["registration"]["fields"]
        new_fields_array = []
        for element in fields:
            if element["type"] == "password":
                new_element = {"xpath":xpath,"type":element['type'],"required":element['required']}
                new_fields_array.append(new_element)
            else:
                new_fields_array.append(element)
                
        self.collection.update({"name":self.NAME_OF_SITE},
                          {"$set":{"registration.fields":new_fields_array}})
            
def tes():
    print "test"
                
modify_data = ModifyDAO(collection, NAME_OF_SITE)
#modify_data.set_login_username_xpath("tosser")
#modify_data.set_login_password_xpath("cunt")
modify_data.set_registration_username_xpath("tosser")
modify_data.set_registration_password_xpath("cunt")
