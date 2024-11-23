import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from nvidia_data import x
import re 


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

URL = "https://www.nvidia.com/content/dam/en-zz/Solutions/product-security/product-security.json"


def scrape_nvidia_security(product_name:str)-> list | str:
    """
    Fetch and filter NVIDIA security bulletin entries matching the given product name 

    Args:
        product_name (str): The name of the product to search for.
    Returns:
        A list of matching security bulletin entries
    """

    matching_entries: list = []
    try:
        # Send a get request to the URL with a dummy header 
        response = requests.get(url=URL, headers=headers)

        if response.status_code != 200:
            return "Failed to fetch the page!"

        # bulletin data from NVIDIA security
        bulletin_data: list = response.json()["data"]

        # Searching for matching product entries
        for entry in bulletin_data:
            if product_name.lower() in entry["title"].lower():
                matching_entries.append(entry)
        return matching_entries

    except requests.RequestException as e:
        return f"Error while fetching data: {e}"
    except KeyError:
        return f"Unexpected json structure"


def fetch_description_from_link(url):
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            return "Failed to fetch description"
        soup = BeautifulSoup(response.text, "html.parser")
        table_tag = soup.select_one("figure.table")
        tbody_tag = table_tag.find("tbody")
        d_tag = tbody_tag.find_all("td")
        if d_tag:
            return d_tag[1].get_text()
        else:
            return "Description not found on the page"

    except requests.RequestException as e:
        return f"Error fetching description: {e}"

def extract_product_details(entries: list)-> list | str:
    """
    Extract the details of a particular product
    Args:
        Takes a list of matched title that matches in the nvidia bulletin list
    Returns:
        A list of the product detail(s)
    """

    product_regex = r">(.+?)</a>"
    url_regex = r"https://nvidia.custhelp.com/app/answers/detail/a_id/\d{1,8}"

    structured_data: list = []

    # Iterate through each entries to get details
    for entry in entries:
        try:
            product_name = re.search(product_regex, entry["title"]).group(1)
            cve_id = entry["cve identifier(s)"]
            severity = entry["severity"]
            publish_date = entry["publish date"]
            last_updated = entry["last updated"]
            url = re.search(url_regex, entry["title"]).group(0)
            description = fetch_description_from_link(url)

            # store the structured data
            product_details: dict = {
                "product_name": product_name,
                "cve_id": cve_id,
                "severity": severity,
                "publish date": publish_date,
                "last updated": last_updated,
                "description": description,
                "link": url,
            }

            structured_data.append(product_details)
        except Exception as e:
            return f"Error processing entry: {entry}\nError: {e}"
    return structured_data

data = extract_product_details(scrape_nvidia_security("NeMo"))
print(data)

