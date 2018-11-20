from ..utils import FilterBuilder
from .ConnectionService import ConnectionService

class TransactionList:
    def __init__(self, service, data):
        self.data = data
        self.service = service

    def next(self): 
        if "links" in self.data and "next" in self.data["links"]:
            next_link = self.data["links"]["next"]
            print("Next:", next_link)
            next_path = next_link[next_link.rfind(".io/")+4:]
            nt = self.service.session.api.get(next_path)
            self.data = nt
            return self

        return None

class User:
    def __init__(self, service):
        self.service = service

    def forUser(self, id):
        self.id = id
        return self

    def get(self):
        r = self.service.get(self.id)
        self.email = r["email"]
        self.mobile = r["mobile"]
        return self

    def update(self, email = None, mobile = None):
        return self.service.update(self.id, email=email, mobile=mobile)

    def delete(self):
        return self.service.delete(self.id)

    def createConnection(self, data):
        return ConnectionService(self.service.session, self).create(data)

    def refreshAllConnections(self):
        return self.service.refreshAllConnections(self.id)

    def listAllConnections(self, filter=None):
        return self.service.listAllConnections(self.id, filter)

    def getTransaction(self, id):
        return self.service.getTransaction(self.id, id)

    def getTransactions(self, filter = None):
        return self.service.getTransactions(self.id, filter)

    def getAccount(self, id):
        return self.service.getAccount(self.id, id)

    def getAccounts(self, filter = None):
        return self.service.getAccounts(self.id, filter)


class UserService:
    def __init__(self, session):
        self.session = session
    
    def forUser(self, id):
        return User(self).forUser(id)

    def get(self, id):
        r = self.session.api.get("users/" + id)

        u = User(self)
        u.id = r["id"]
        u.email = r["email"]
        u.mobile = r["mobile"]

        return u

    def create(self, email = None, mobile = None):
        json = {}
        if email == None and mobile == None:
            raise Exception("Neither email or mobile were provided")
        if email != None:
            json["email"] = email
        if mobile != None:
            json["mobile"] = mobile
            
        r = self.session.api.post("users/", json=json)

        u = User(self)
        u.id = r["id"]
        u.email = r["email"]
        u.mobile = r["mobile"]

        return u

    def update(self, id, email = None, mobile = None):
        json = {}
        if email == None and mobile == None:
            raise Exception("Neither email or mobile were provided")
        if email != None:
            json["email"] = email
        if mobile != None:
            json["mobile"] = mobile
            
        r = self.session.api.post("users/" + id, json=json)

        u = User(self)
        u.id = r["id"]
        u.email = r["email"]
        u.mobile = r["mobile"]

        return u

    def delete(self, id):            
        self.session.api.delete("users/" + id)

        return None

    def refreshAllConnections(self, id):
        r = self.session.api.post("users/" + id + "/connections/refresh")

        return r

    def listAllConnections(self, id, filter=None):
        url = "users/" + id + "/connections"
        if filter != None:
            if type(filter).__name__ != "FilterBuilder":
                raise Exception("Provided filter must be an instance of FilterBuilder class")
            url = url + "?" + filter.getFilter()
        return self.session.api.get(url)

    def getTransaction(self, user_id, id):
        return self.session.api.get("users/" + user_id + "/transactions/" + id)

    def getTransactions(self, user_id, filter = None):
        url = "users/" + user_id + "/transactions"
        if filter != None:
            if type(filter).__name__ != "FilterBuilder":
                raise Exception("Provided filter must be an instance of FilterBuilder class")
            url = url + "?" + filter.getFilter()

        t = self.session.api.get(url)

        return TransactionList(self, t)
        
    def getAccount(self, user_id, id):
        return self.session.api.get("users/" + user_id + "/accounts/" + id)

    def getAccounts(self, user_id, filter = None):
        url = "users/" + user_id + "/accounts"
        if filter != None:
            if type(filter).__name__ != "FilterBuilder":
                raise Exception("Provided filter must be an instance of FilterBuilder class")
            url = url + "?" + filter.getFilter()

        return self.session.api.get(url)
