import requests

STRAPI_BASE_URL = "http://localhost:1337/api"

def fetch_products():
    
    response = requests.get(f"{STRAPI_BASE_URL}/products")
    if response.status_code == 200:
        
        return response.json()['data']
    
    return None

