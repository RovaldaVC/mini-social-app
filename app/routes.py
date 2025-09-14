from flask_restful import Resource
from flask import request
from app.forms import signUpValidator, signInValidator, updateValidator
from app.models import signUpData, updateData
from flask_jwt_extended import jwt_required, create_access_token, get_jwt, get_jwt_identity
from bson.objectid import ObjectId

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
                "message":"error happened during validating",
                "error":validator.errors
            }, 400

class users(Resource):
    @jwt_required()
    def put(self, id=None):
        data = request.json
        validator = updateValidator(formdata=None, data=data)
        if id is None:
            if validator.validate():
                
                if userCollection.find_one({"username":data["username"]}):
                    return{
                        "status":"error",
                        "message":"this username already exist."
                        },409
            
                elif userCollection.find_one({"number":data["number"]}):
                    return{
                        "status":"error",
                        "message":"this number already exist."
                        },409
                else:
                    user = signUpData(formdata=None, data=data)
                    userupdate = userCollection.update_one({"username":data["username"]}, {"$set" :user.toDict()})
                    if  userupdate.modified_count > 0:
                        return{
                            "status":"successful",
                            "message":"user was updated successfully."
                        },200
                    else:
                        return{
                            "status":"error",
                            "message":"check if the username you inserted was correct."
                        },401
            else:
                return{
                "status": "error",
                "message": "Invalid input",
                "errors": validator.errors
            }, 400
        else:
            claims = get_jwt()
            role = claims["role"]
            number = get_jwt_identity()
            if role == "admin":
                if validator.validate():
                    # Fetch existing user
                    existing_user = userCollection.find_one({"username": data["username"]})
                    userData = updateData(data, existing_user)
                    targetedUser = userCollection.update_one(
                        {"username": data["username"]}, 
                        {"$set": userData.to_dict()})
                    
                return{
                    "status":"error",
                    "message":"Forbidden area, Access denied!"
                }, 403
    @jwt_required()
    def get(self, id=None):
        claims = get_jwt()
        role = claims["role"]
        if role == "admin":
            if id is None:
                usersList = userCollection.find({})
                return{
                    "status":"successfull",
                    "message":"you have access to the list of users",
                    "users": list(usersList)
                }, 200
            else:
                targetedUser = userCollection.find_one({"_id":ObjectId(id)})
                if targetedUser:
                    return{
                        "status":"successfull",
                        "message":"we found your user.",
                        "user":targetedUser
                    }
                else:
                    return{
                        "status":"error",
                        "message":"we couldn't find the user."
                    }, 404
        else:
            return{
                "status":"error",
                "message":"Forbidden area, Access denied!"
            }, 403
    @jwt_required()
    def delete(self, id=None):
        if id is None:
            number = get_jwt_identity()
            targetedUser = userCollection.delete_one({"number":number})
            if targetedUser.delete_count > 0:
                return{
                    "status":"successfull",
                    "message":"your account was deleted successfully."
                },200
            else:
                return{
                    "status":"error", 
                    "message":"we couldn't find your account"
                }, 404
        else:
            claims = get_jwt()
            role = claims["role"]
            if role == "admin":
                targetedUser = userCollection.delete_one({"_id":ObjectId})
                if targetedUser.deleted_count > 0:
                    return{
                        "status":"successfull",
                        "message":"your account was deleted successfully."
                    },200
                else:
                    return{
                        "status":"error",
                        "message":"we couldn't find your account, try again."
                    }, 404
            else:
                return{
                    "status":"error",
                    "message":"Forbidden area, Access denied!"
                },403

class texting(Resource):
    def post(self):
        pass
    def put(self):
        pass
    def get(self):
        pass
    def delete(self):
        pass

def init_routes(api):
    api.add_resource(signIn, "/sign_in")
    api.add_resource(signUp, "/sign_up")
    api.add_resource(users, "/users", "/users/<string:id>")

def setDatabase(app):
    global userCollection
    userCollection = app.db["users"]