import sys
import requests

TARGET_URL = "https://rvu-verse.onrender.com/"

def run_smoke_test():
    print(f"Starting smoke test against: {TARGET_URL}")
    try:
        response = requests.get(TARGET_URL, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        # 1. Verify standard HTTP success
        if response.status_code != 200:
            print(f"❌ FAILED: Expected status code 200, got {response.status_code}")
            sys.exit(1)
            
        # 2. Verify expected content is present (checking for login page basics)
        text = response.text.lower()
        if "rvuverse" not in text:
            print("❌ FAILED: Did not find 'rvuverse' in the response body.")
            sys.exit(1)
            
        if "login" not in text:
            print("❌ FAILED: Did not find 'login' in the response body.")
            sys.exit(1)
            
        print("✅ SUCCESS: Smoke test passed! The live site is up and reachable.")
        sys.exit(0)
        
    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED: Network error occurred during smoke test: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_smoke_test()
