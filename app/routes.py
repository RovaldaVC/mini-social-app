from flask_restful import Resource
from flask import request
from app.forms import signUpValidator, signInValidator
from app.models import signUpData
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt, get_jwt_identity
userCollection = None

class signUp(Resource):
    def post(self):
        
        data = request.json
        validator = signUpValidator(formdata=None, data=data)
        
        if validator.validate():
            if userCollection.find_one({"username":data["username"]}):
                return{
                    "status":"error",
                    "message":"this username already exist."
                },409
            
            if userCollection.find_one({"number":data["number"]}):
                    return{
                    "status":"error",
                    "message":"this number already exist."
                },409
                
            user = signUpData(formdata=None, data=data)
            userCollection.insert_one(user.toDict())
            return{
                    "status":"successful",
                    "message":"your account was created successfully"
                }, 201
        
        else:
            return{
                "status": "error",
                "message": "Invalid input",
                "errors": validator.errors
            }, 400

            
class signIn(Resource):
    def post(self):
        
        data = request.json
        validator = signInValidator(formdata=None, data=data)
        
        if validator.validate():
            user = userCollection.find_one({"username":data["username"]})
            if user:
                if signUpData.checkHashPassword(user["password"], data["password"]):
                    return{
                        "status":"successful",
                        "message":"you logged in",
                        "token": create_access_token(
                            identity=user["number"],
                            additional_claims={"role":"user"}   
                        )
                    }, 200
                else:
                    return{
                        "status":"error",
                        "message":"Invalid username or password"
                    }, 401
            else:
                return{
                    "status":"error",
                    "message":"Invalid username or password.",
                }, 401
        else:
            return{
                "status":"error",
                "message":"error happened during validaying",
                "error":validator.errors
            }, 400

class texting(Resource):
    def post(self):
        pass
    def put(self):
        pass
    def get(self):
        pass
    def delete(self):
        pass

class users(Resource):
    def put(self):
        pass
    def get(self):
        pass
    def delete(self):
        pass

def init_routes(api):
    api.add_resource(signIn, "/sign_in")
    api.add_resource(signUp, "/sign_up")

def setDatabase(app):
    global userCollection
    userCollection = app.db["users"]