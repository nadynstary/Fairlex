import requests 
import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()



HIBP_API_KEY= os.environ.get("HIBP_API_KEY")

print(f"Loaded key: '{HIBP_API_KEY}'")

HIBP_BASE_URL= "https://haveibeenpwned.com/api/v3/breachedaccount"

HEADERS= {"hibp-api-key": HIBP_API_KEY, "user-agent": "Fairlex"}

def check_email_breaches(email: str) -> List[Dict[str,Any]]:
    if not HIBP_API_KEY:
        raise RuntimeError("HIBP_API_KEY is not set. ")
    email = email.strip().lower()
    url = f"{HIBP_BASE_URL}/{email}"
    params = {"truncateResponse": "false"}

    response = requests.get(url, headers=HEADERS, params=params)

    #response cases
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return []
    elif response.status_code == 401:
        raise RuntimeError("HIBP rejected the API key. Please check if the key is valid.")
    elif response.status_code == 429:
        raise RuntimeError("Rate limited by HIBP, too many requests. Please try again later.")
    else:
        raise RuntimeError(f"Unexpected HIBP response: {response.status_code} - {response.text}")
    
if __name__ == "__main__":
    test_email ="account-exists@hibp-integration-tests.com"
    try:
        breaches = check_email_breaches(test_email)
        if breaches:
            print(f"Breaches found for {test_email}:")
            for breach in breaches:
                print(f" - {breach['Name']}")
        else:
            print(f"No breaches found for {test_email}.")
    except RuntimeError as e:
        print(f"Error: {e}")
