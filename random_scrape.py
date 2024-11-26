from dotenv import load_dotenv
import os
import re
import requests
from collections import defaultdict, UserDict, UserList
from bs4 import BeautifulSoup


"""
    Main part 
"""

# load the environment varaibles
load_dotenv()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_html(url: str) -> any:
    """
    Get the html content provided the given url
    Args:
        url to screpe
    Returns: 
        Returns the html content
    """

    # Scraper api payload
    payload = {
        'api_key': os.getenv("SCRAPER_API"), # fetch the api_key
        'url': url, # the site to scrape 
        'render': 'true' # to allow the js rendering
    }

    try:
        response = requests.get('https://api.scraperapi.com/', params=payload, headers=headers)
        if response.status_code != 200:
            return f"Failed to fetch the page!\n Status code: {response.status_code}"
        return response.text

    except requests.RequestException as e:
        return f"Error fetching docs: {e}"


def extract_body_element(html_content) -> str:
    """
    Takes html content and extract the body part
    Args:
        html content
    Returns:
        String or the body of html content
    """
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    """
    Preprocess the body of html Content
    Args:
        Takes noisy body of html
    Returns:
        Returns str or cleaned_content
    """
    soup = BeautifulSoup(body_content, "html.parser")

    # Removes the script and style tags
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")

    stripped_lines = []
    lines = cleaned_content.splitlines()
    for line in lines:
        if line.strip():
            stripped_lines.append(line)
    cleaned_content = "\n".join(stripped_lines)
    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    """Split content in chunks of 6000 length"""

    result = []
    for i in range(0, len(dom_content), max_length):
        chunk = dom_content[i:i+max_length]
        result.append(chunk)
    return result


def main():
    # url: str = input("Enter the url to scrape: ")
    # Schenider Electric 
    html_content = get_html(url="https://www.se.com/ww/en/work/support/cybersecurity/security-notifications.jsp")
    # with open("s_electric.html", 'r', encoding='utf-8') as file:
    #     html_content = file.read()
    print(split_dom_content(clean_body_content(extract_body_element(html_content))))


if __name__ == "__main__":
    main()


