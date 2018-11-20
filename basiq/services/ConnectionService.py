import time

class Connection:
    def __init__(self, service):
        self.service = service

    def forConnection(self, id):
        self.id = id
        return self

    def refresh(self):
        return self.service.refresh(self.id)

    def update(self, password):
        return self.service.update(self.id, password)

    def delete(self):
        return self.service.delete(self.id)

class Job:
    def __init__(self, service):
        self.service = service

    def forJob(self, id):
        self.id = id
        return self

    def getConnectionId(self):
        if hasattr(self, "links") and "source" not in self.links:
            return ""
        
        if hasattr(self, "links") == False:
            return ""

        return self.links["source"][self.links["source"].rfind("/")+1:]

    def getConnection(self):
        if self.getConnectionId() == "":
            j = self.service.getJob(self.id)
        else:
            j = self

        return self.service.get(j.getConnectionId())

    def waitForCredentials(self, interval, timeout, i = 0):
        j = self.service.getJob(self.id)

        time.sleep(interval / 1000)

        if i * (interval / 1000) > timeout:
            return False

        i += 1

        step = j.steps[0]
        if step["status"] == "success":
            return self.service.get(j.getConnectionId())
        if step["status"] == "failed":
            return False
            
        return self.waitForCredentials(interval, timeout, i)

    def waitForAccounts(self, interval, timeout, i = 0):
        j = self.service.getJob(self.id)

        time.sleep(interval / 1000)

        if i * (interval / 1000) > timeout:
            return False

        i += 1

        step = j.steps[1]
        if step["status"] == "success":
            return self.service.get(j.getConnectionId())
        if step["status"] == "failed":
            return False

        return self.waitForAccounts(interval, timeout, i)

    def waitForTransactions(self, interval, timeout, i = 0):
        j = self.service.getJob(self.id)

        time.sleep(interval / 1000)

        if i * (interval / 1000) > timeout:
            return False

        i += 1

        step = j.steps[2]
        if step["status"] == "success":
            return self.service.get(j.getConnectionId())
        if step["status"] == "failed":
            return False
            
        return self.waitForTransactions(interval, timeout, i)

class ConnectionService:
    def __init__(self, session, user):
        self.session = session
        self.user = user

    def forConnection(self, id):
        return Connection(self).forConnection(id)

    def get(self, id):
        r = self.session.api.get("users/" + self.user.id + "/connections/" + id)

        c = Connection(self)
        c.id = r["id"]
        c.status = r["status"]
        c.last_used = r["lastUsed"]
        c.institution = r["institution"]
        c.accounts = r["accounts"]
        c.links = r["links"]

        return c

    def getJob(self, id):
        r = self.session.api.get("jobs/" + id)

        j = Job(self)
        j.id = r["id"]
        j.created = r["created"]
        j.updated = r["updated"]
        j.links = r["links"]
        if "steps" in r:
            j.steps = r["steps"]

        return j

    def create(self, connection_data):
        if "loginId" not in connection_data:
            raise Exception("Login id needs to be suplied")
        if "password" not in connection_data:
            raise Exception("Password id needs to be suplied")
        if "institution" not in connection_data:
            raise Exception("Institution data needs to be suplied")
        if "id" not in connection_data["institution"]:
            raise Exception("Institution id needs to be suplied")

        r = self.session.api.post("users/" + self.user.id + "/connections", json=connection_data)

        j = Job(self)
        j.id = r["id"]

        return j

    def update(self, id, password, security_code=None, secondary_login_id=None):
        data = {'password': password}
        if security_code is not None:
            data['securityCode'] = security_code
        if secondary_login_id is not None:
            data['secondaryLoginId'] = secondary_login_id
        r = self.session.api.post("users/" + self.user.id + "/connections/" + id, json=data)

        j = Job(self)
        j.id = r["id"]

        return j

    def delete(self, id):
        self.session.api.delete("users/" + self.user.id + "/connections/" + id)

        return None

    def refresh(self, id):
        r = self.session.api.post("users/" + self.user.id + "/connections/" + id + "/refresh")

        j = Job(self)
        j.id = r["id"]

        return j
