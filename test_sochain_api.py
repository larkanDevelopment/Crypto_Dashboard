import requests

def fetch_transactions():
    try:
        address = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'  # Example BTC address
        url = f'https://sochain.com/api/v3/address/BTC/{address}'  # Correct endpoint format for V3
        response = requests.get(url)
        print(f"URL: {url}")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(data)  # Print the full response for debugging
    except Exception as e:
        print(f"Error fetching transactions: {e}")

fetch_transactions()
