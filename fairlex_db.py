import os
from datetime import datetime, timezone, timedelta 
from typing import Optional, List, Dict, Any


#==========================--MONGO DB CONNECTION--=========================
from pymongo import MongoClient,ASCENDING
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import PyMongoError
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.environ.get("MONGODB_DB_NAME", "fairlex")

#======================--CATEGORIES COLLECTION--=========================
SUMMARIZER_CATEGORIES = [
    "Educational",
    "Governmental",
    "Financial",
    "Healthcare",
    "Creating a new account",
    "Purchasing a product or service",
    "Employment",
    "Other"
]

#database configuration 
class fairlexDB:
    def __init__(self,uri:str=MONGO_URI, db_name:str=DB_NAME):
        self.client= MongoClient(uri)



   


