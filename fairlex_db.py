import os
from datetime import datetime, timezone, timedelta 
from typing import Optional, List, Dict, Any
from urllib import response


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
        self.breach_results: Collection = self.db["breach_results"]

    def _ensure_indexes(self):
        self.users.create_index([("email", ASCENDING)], unique=True)
        self.summarizer_logs.create_index([("email", ASCENDING), ("timestamp", ASCENDING)])
        self.breach_results.create_index([("email", ASCENDING), ("timestamp", ASCENDING)])

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
        
    def get_user_logs(self, email:str, limit:int=20)->List[Dict[str,Any]]:
        cursor=(self.summarizer_logs.find({"email":email.strip().lower()},{"_id":0}).sort("timestamp",-1).limit(limit))
        return list(cursor)
    """get the user log history in a form of python dictionary, will have to dispaly
    it for the user in the front end"""
    #------------ summarizer logs branch -----------
    def log_summary(
            self,
            email:str,
            category:str,
            original_text:str,
            summary: str,
            preview: int=200,
    ) -> str:
        """storing one summary log in the database and only a preview of the original text"""
        if category not in SUMMARIZER_CATEGORIES:
            raise ValueError(
                f"Unknow category '{category}'. Must be one of {SUMMARIZER_CATEGORIES}"
            )
        
        doc={
            "email": email.strip().lower(),
            "category": category,
            "original_text_preview":original_text[:preview],
            "summary": summary,
            "timestamp": datetime.now(timezone.utc),

        }
        results=self.summarizer_logs.insert_one(doc)
        return str(results.inserted_id)

    def save_breach_results (self, email:str, breaches:List[Dict[str, Any]])-> str:
        """SAVE the breach results in the database"""
        doc={
            "email": email.strip().lower(),
            "breaches": breaches,
            "checked_at": datetime.now(timezone.utc)
        }
        results = self.breach_results.insert_one(doc)
        return str(results.inserted_id)
    
    def get_breach_result(self, email:str, limit:int=20)->Optional[Dict[str,Any]]:
        cursor=self.breach_results.find_one({"email":email.strip().lower()},{"_id":0},sort=[("checked_at",-1)])
        return list(cursor)







def get_db() -> fairlexDB:
    try:
        return fairlexDB()
    except PyMongoError as e:
        raise RuntimeError(f"Could not connect to MongoDB: {e}")


    


   


