import requests 
import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()
HIBP_API_KEY= os.environ.get("HIBP_API_KEY")
HIBP_BASE_URL= "https://haveibeenpwned.com/api/v3/breachedaccount"

HEADERS= {"hibp-api-key": HIBP_API_KEY, "user-agent": "Fairlex"}

def check_email_breaches(email: str)


if __name__ == "__main__":
    test_email = "account-exists@hibp-integration-test.com"
    try:
        breaches = check_email_breaches(test_email)