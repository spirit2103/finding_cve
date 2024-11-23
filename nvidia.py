import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from nvidia_data import x
import re 


# TODO: Not getting description for multiple entry of a given product [BUG]

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
        if not table_tag:
            return "No table found on the page"
        
        tbody_tag = table_tag.find("tbody")
        if not tbody_tag:
            return "No table body found on the page"
        rows = tbody_tag.find_all("tr")
        descriptions: list = []

        for row in rows:
            cells = row.find_all("td")
            if len(cells) > 1:
                cve_id = cells[0].get_text(strip=True)
                description = cells[1].get_text(strip=True)  # Description in the second cell
                descriptions.append({"cve_id": cve_id, "description": description})
        return descriptions if descriptions else "No descriptions found in the table"
        # if rows:
        #     return rows[1].get_text()
        # else:
        #     return "Description not found on the page"

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

        product_name = re.search(product_regex, entry["title"]).group(1)
        cve_id = entry["cve identifier(s)"]
        severity = entry["severity"]
        publish_date = entry["publish date"]
        last_updated = entry["last updated"]
        url = re.search(url_regex, entry["title"]).group(0)
        descriptions = fetch_description_from_link(url)

        # Handle multiple descriptions
        if isinstance(descriptions, list):
            for desc in descriptions:
                product_details = {
                    "product_name": product_name,
                    "cve_id": desc["cve_id"],
                    "severity": severity,
                    "publish date": publish_date,
                    "last updated": last_updated,
                    "description": desc["description"],
                    "link": url,
                }
                structured_data.append(product_details)
        else:
            # If no descriptions found, still log the entry
            product_details = {
                "product_name": product_name,
                "cve_id": cve_id,
                "severity": severity,
                "publish date": publish_date,
                "last updated": last_updated,
                "description": descriptions,  # Error message or fallback
                "link": url,
            }
            structured_data.append(product_details)
    return structured_data

data = extract_product_details(scrape_nvidia_security("NeMo"))
print(data)
# print(scrape_nvidia_security("GPU Display Driver"))

