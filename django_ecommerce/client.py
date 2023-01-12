import requests
import json

response = requests.get('http://httpbin.org/get')

print(response.json())
print(response.status_code)