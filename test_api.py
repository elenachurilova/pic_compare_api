import requests

url = "http://localhost:5000/api/compare.json"

payload = "{\"image_one\" : \"https://www.memphisveterinaryspecialists.com/files/best-breeds-of-house-cats-memphis-vet-1-1.jpeg\",\"image_two\" : \"https://www.memphisveterinaryspecialists.com/files/best-breeds-of-house-cats-memphis-vet-1-1.jpeg\"}"
headers = {
    'user-agent': "vscode-restclient",
    'content-type': "application/json",
    'authorization': "Bearer 123"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)