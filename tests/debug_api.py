import requests
import json

BASE_API = "https://4c7d-47-247-173-78.ngrok-free.app"

def test_api():
    url = f"{BASE_API}/api/hospitals/?city=Indore"
    headers = {
        "ngrok-skip-browser-warning": "true",
        "Accept": "application/json"
    }
    
    print(f"Testing URL: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Status Code: {response.status_code}")
        print("Response Headers:")
        print(json.dumps(dict(response.headers), indent=2))
        print("\nResponse Body:")
        print(response.text)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nFound {len(data.get('hospitals', []))} hospitals.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
