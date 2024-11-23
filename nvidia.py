import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from nvidia_data import x
import re 


def scrape_nvidia_security(product_name:str):
    # Mongodb setup
    # client = MongoClient("mongodb+srv://test:test123@cluster0.xqrer.mongodb.net/")
    # db = client["vuln"]
    # collection = db["nvidia"]

    # url = "https://www.nvidia.com/content/dam/en-zz/Solutions/product-security/product-security.json"
    # response = requests.get(url)

    # if response.status_code != 200:
        # print("Failed to fetch the page!")
        # return
    
    # bulletin_data: list = response.json()["data"]
    
    matching_entries: list = []
    for entry in x:
        if product_name.lower() in entry["title"].lower():
            matching_entries.append(entry)

    # iterate through the entries and getting description tag text
    return matching_entries


def fetch_description_from_link(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return "Failed to fetch description"
        soup = BeautifulSoup(response.text, "html.parser")
        print(soup.prettify())
        table = soup.find("figure", class_="table")
        print(table)
        tbody_tag = table.find("tbody")
        print(tbody_tag)
        d_tag = tbody_tag.find_all("td")
        if d_tag:
            return d_tag[1].get_text()
        else:
            return "Description not found on the page"

    except requests.RequestException as e:
        return f"Error fetching description: {e}"


def extract_product_details(entries: list):
    product_regex = r">(.+?)</a>"
    url_regex = r"https://nvidia.custhelp.com/app/answers/detail/a_id/\d{1,8}"
    
    structured_data = []

    for entry in entries:
        product_name = re.search(product_regex, entry["title"]).group(1)
        cve_id = entry["cve identifier(s)"]
        severity = entry["severity"]
        publish_date = entry["publish date"]
        last_updated = entry["last updated"]
        url = re.search(url_regex, entry["title"]).group(0)
        description = fetch_description_from_link(url)
        
        # store the structured data
        product_details = {
            "product_name": product_name,
            "cve_id": cve_id,
            "severity": severity,
            "publish date": publish_date,
            "last updated": last_updated,
            "description": description,
            "link": url,
        }

        structured_data.append(product_details)
    return structured_data

scrape_data = scrape_nvidia_security("GPU")
extract_product_details(scrape_data)
