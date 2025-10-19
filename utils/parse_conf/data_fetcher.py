import requests
import json

# Fetch API data
def fetch_data_from_url(full_url):
   
    if not full_url:
        print("\nError: No URL provided.")
        return None

    print(f"\nAttempting to fetch data from: {full_url}")

    try:
        headers = {
            "User-Agent": "User-Agent"
        }
        response = requests.get(full_url, headers=headers)
        response.raise_for_status() # Raises an exception if HTTP error encountered
        
        if not response.text.strip():
            return []
        
        return response.json()
    
    except requests.exceptions.RequestException as exc:   # Define the exception as exc
        print(f"\nError fetching data from {full_url} endpoint: {exc}") # Return the occurring exception
        return None
    except json.JSONDecodeError:
        print(f"\nError: Failed to decode JSON from response at {full_url}")
        return None