import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


def scrape_nvidia_security():
    # Mongodb setup
    client = MongoClient("mongodb+srv://test:test123@cluster0.xqrer.mongodb.net/")
    db = client["vuln"]
    collection = db["nvidia"]

    url = "https://www.nvidia.com/content/dam/en-zz/Solutions/product-security/product-security.json"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch the page!")
        return
    
    bulletin_data = response.json()["data"]


