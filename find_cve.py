from dotenv import load_dotenv
import google.generativeai as genai
import re 
import json

load_dotenv()

GOOGLE_API_KEY = "AIzaSyCqDKadojoxqgQZm3fIj4x2A4BpByaFyIY"
genai.configure(api_key= GOOGLE_API_KEY)

def prompt_model(product_name):
        model = genai.GenerativeModel("gemini-pro")
        prompt = "Find only the cve_id,cwe_id,sevd_id or sesb_id for {product_name}"
        response = model.generate_content(prompt)
        if hasattr(response, 'candidates') and response.candidates:
            response_text = response.candidates[0].content.parts[0].text
        return response_text
                  
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

def finding_cve(json_data,outfile):
        try:
                with open(outfile, 'w') as file:
                        json.dump(json_data, file, indent=4)
                print(f"Report successfully saved to {outfile}")
        except IOError as e:
                print(f"Error saving the report to file: {e}")

        for item in json_data:
                CVE_ID = [item['cve_id'] for item in json_data]
        return CVE_ID

def save_cve_id(cve_id, output_file):
    try:
        with open(output_file, 'w') as file:
            json.dump(cve_id, file, indent=4)
        print(f"Report successfully saved to {output_file}")
    except IOError as e:
        print(f"Error saving the report to file: {e}")

def main():
        product_name = input("enter the product name: ")
       # url = input("enter the Url: ")  
        response_text = prompt_model(product_name)
        json_data = convert_json(response_text)
        output_file = r"C:\Users\susha\hackathon\product-extract\cve-details.json"
        cve_id = finding_cve(json_data,output_file)
        output_file1 = r"C:\Users\susha\hackathon\product-extract\cve-id.json"
        save_cve_id(cve_id,output_file1)


if __name__ == "__main__":
       main()