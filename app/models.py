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