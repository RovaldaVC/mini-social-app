from werkzeug.security import generate_password_hash, check_password_hash

class signUpData():
    
    def __init__(self, data):
        self.username = data["username"]
        self.password = data["password"]
        self.name = data["name"]
        self.family = data.get("family")
        self.number = data.get("number")

    
    def toHashPassword(self):
        return generate_password_hash(self.password)
    
    def checkHashPassword(hashed_password, plain_password):
        return check_password_hash(hashed_password, plain_password)
        
    def toDict(self):
        return{
            "name":self.name,
            "username":self.username,
            "password":self.toHashPassword()
        }

class updateData:
    def __init__(self, data, existing_user):
        self.username = data.get("username", existing_user["username"])
        self.name = data.get("name", existing_user["name"])
        self.family = data.get("family", existing_user.get("family"))
        self.password = self.hash_password(data, existing_user)

    def hash_password(self, data, existing_user):
        if "password" in data and data["password"]:
            return generate_password_hash(data["password"])
        else:
            return existing_user["password"]

    def to_dict(self):
        return {
            "username": self.username,
            "name": self.name,
            "password": self.password,
            "family": self.family
        }