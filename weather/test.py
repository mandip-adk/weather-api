# quick test script
import requests

for i in range(8):
    r = requests.get('http://localhost:8000/api/weather/?city=kathmandu')
    print(f"Request {i+1}: {r.status_code}")