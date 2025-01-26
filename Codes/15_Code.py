import requests
import dotenv
import os
import json

dotenv.load_dotenv()

api_key = os.getenv("UPSTAGE_API_KEY")
filename = "Images/11_Image2.png"
 
url = "https://api.upstage.ai/v1/document-ai/document-parse"
headers = {"Authorization": f"Bearer {api_key}"}
files = {"document": open(filename, "rb")}
response = requests.post(url, headers=headers, files=files)
# Pretty-print the JSON response
response_json = response.json()
print(json.dumps(response_json, indent=4))