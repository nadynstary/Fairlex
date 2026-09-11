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
        self.db=self.client[db_name]
        self.users: Collection = self.db["users"]
        self.summarizer_logs: Collection = self.db["summarizer_logs"]
        self._ensure_indexes()

    def _ensure_indexes(self):
        self.users.create_index([("email", ASCENDING)], unique=True)
        self.summarizer_logs.create_index([("email", ASCENDING), ("timestamp", ASCENDING)])

    # --------- Users Branch -----------
    #revisits and first visit (signup and signin)
    def upsert_user(self, email:str, name:Optional[str]=None) -> Dict[str, Any]:
        email=email.strip().lower()
        now=datetime.now(timezone.utc)
        update_doc = {
            "$set": {"email": email, "updated_at": now},
            "$setOnInsert": {"created_at": now}
        }
        if name:
            update_doc["$set"]["name"] = name.strip()

        self.users.update_one({"email": email}, update_doc, upsert=True)
        return self.users.find_one({"email": email},{"id":0})



   


