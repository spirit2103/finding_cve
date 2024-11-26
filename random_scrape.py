from dotenv import load_dotenv
import os
import requests
import re
from collections import defaultdict, UserDict, UserList
from bs4 import BeautifulSoup
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatMessagePromptTemplate
from pydantic import ValidationError, validate_call


"""
messages = [
    {"role": "user", "content": "You are tasked with extracting specific information from the following text content: {dom_content}. "
                                    "Please follow these instructions carefully: \n\n"
                                    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
                                    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
                                    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
                                    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."}
]

model = OllamaLLM(model="llama3")



# response = requests.get("https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=Microsoft Windows")
# if response.status_code != 200:
#     print(f"Request failed")
# print(response.json())




# def get_cve_id(file_name):
#     cve_id_list: list = []
#     cve_id_regex = r"CVE-\d{4}-\d{1,8}"
#     with open(file_name, 'r', encoding="utf-8") as file:
#         html_content = file.read()
#     matches = re.findall(cve_id_regex, html_content)
#     for cve in matches:
#         if cve not in cve_id_list:
#             cve_id_list.append(cve)
#     return cve_id_list

# x = get_cve_id("random.html")
# categorized_data = defaultdict(list)
# for cve in x:
#     year = cve.split("-")[1]
#     categorized_data[year].append(cve)




# print(len(categorized_data["2024"]))


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]


def parse_with_ollama(dom_chunks, parse_description):
    try:
        
        prompt = ChatMessagePromptTemplate.format_messages(messages)
        chain = prompt | model

        parsed_results = []
        for i, chunk in enumerate(dom_chunks, start=1):
            response = chain.invoke(
                {"dom_content": chunk, "parse_description": parse_description}
            )
            print(f"Parsed batch: {i} of {len(dom_chunks)}")
            parsed_results.append(response)
        return "\n".join(parsed_results)
    except ValidationError as exc:
        return (repr(exc.errors()[0]['type']))


# user_product = input("Enter the name of the productn: ")
# desc = f"Can you give me the cve id and description corresponding to the product {user_product} in a list form?"

# dom_data = split_dom_content(clean_body_content(extract_body_element(html_content)))
# # print(parse_with_ollama(dom_chunks=dom_data, parse_description=desc))
# print(dom_data)
#
"""

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


def main():
    # url: str = input("Enter the url to scrape: ")
    # Intel security page: trial
    # html_content = get_html(url="https://www.se.com/ww/en/work/support/cybersecurity/security-notifications.jsp")
    # print(html_content)
    with open("s_electric.html", 'r', encoding='utf-8') as file:
        html_content = file.read()
    print(clean_body_content(extract_body_element(html_content)))


if __name__ == "__main__":
    main()


