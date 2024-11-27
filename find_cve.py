from dotenv import load_dotenv
import google.generativeai as genai
import re 
import json

load_dotenv()

GOOGLE_API_KEY = "AIzaSyCqDKadojoxqgQZm3fIj4x2A4BpByaFyIY"
genai.configure(api_key= GOOGLE_API_KEY)

product_name = input("enter the product name: ")
model = genai.GenerativeModel("gemini-pro")
prompt = "For {product_name} Find only the cve_id,cwe_id,sevd_id or sesb_id"
response = model.generate_content(prompt)

if hasattr(response, 'candidates') and response.candidates:
    if hasattr(response.candidates[0], 'content') and response.candidates[0].content.parts:
        response_text = response.candidates[0].content.parts[0].text           # print(f"Extracted Content: {response_text}")
            
def convert_json(content):
        lines = content.strip().split("\n")
        headers = [header.strip() for header in lines[0].split("|") if header.strip()]
        data_lines = lines[2:]
        data = []

        for line in data_lines:
                values = [value.strip() for value in line.split("|") if value.strip()]
                if len(values) == len(headers):
                        data.append(dict(zip(headers,values)))

        return data

json_data = convert_json(response_text)

with open("cve_data.json","w") as f:
        json.dump(json_data, f, indent=4)

for item in json_data:
        CVE_ID = item['cve_id']
        print(f"CVE ID: {CVE_ID}")

