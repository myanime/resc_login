import pymongo

class ModifyDAO:
    def __init__(self, NAME_OF_SITE="Rescator"):
        self.NAME_OF_SITE = NAME_OF_SITE
        DATABASE = "database"
        COLLECTION = "sites"
        CONNECTION_STRING = "mongodb://localhost:27017"
        connection = pymongo.MongoClient(CONNECTION_STRING)
        database = connection[DATABASE]
        collection = database[COLLECTION]

        self.collection = collection
        self.NAME_OF_SITE = NAME_OF_SITE
        self.site = collection.find_one({"name":self.NAME_OF_SITE})

    def get_sites(self):
        cursor = self.collection.find()
        site_array = []
        for name in cursor:
            site_array.append(name["name"])
        return site_array

    def set_login_username_xpath(self, xpath):
        self.site = self.collection.find_one({"name":self.NAME_OF_SITE})
        fields = self.site["login_register"]["fields"]
        new_fields_array = []
        for element in fields:
            if element["type"] == "username":
                new_element = {"xpath":xpath,"type":element['type'],"required":element['required']}
                new_fields_array.append(new_element)
            else:
                new_fields_array.append(element)
                
        self.collection.update({"name":self.NAME_OF_SITE},
                          {"$set":{"login_register.fields":new_fields_array}})

        
    def set_login_password_xpath(self, xpath):
        self.site = self.collection.find_one({"name":self.NAME_OF_SITE})
        fields = self.site["login_register"]["fields"]
        new_fields_array = []
        for element in fields:
            if element["type"] == "password":
                new_element = {"xpath":xpath,"type":element['type'],"required":element['required']}
                new_fields_array.append(new_element)
            else:
                new_fields_array.append(element)
                
        self.collection.update({"name":self.NAME_OF_SITE},
                          {"$set":{"login_register.fields":new_fields_array}})


    def set_registration_username_xpath(self, xpath):
        self.site = self.collection.find_one({"name":self.NAME_OF_SITE})
        fields = self.site["registration"]["fields"]
        new_fields_array = []
        for element in fields:
            if element["type"] == "username":
                #print element
                new_element = {"xpath":xpath,"type":element['type'],"required":element['required']}
                new_fields_array.append(new_element)
            else:
                new_fields_array.append(element)
                
        self.collection.update({"name":self.NAME_OF_SITE},
                          {"$set":{"registration.fields":new_fields_array}})

        
    def set_registration_password_xpath(self, xpath):
        self.site = self.collection.find_one({"name":self.NAME_OF_SITE})
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

