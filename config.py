import os

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    JWT_CODE = os.getenv("JWT_CODE")