import requests

STRAPI_BASE_URL = "http://localhost:1337/api"

def fetch_products():
    response = requests.get(f"{STRAPI_BASE_URL}/products")
    if response.status_code == 200:
        return response.json()['data']
    return None

BASE_URL = "https://cms.okolabor.com/api/okolabors/"

def fetch_data(page=1, page_size=10, sort_by="page_title", locale="en"):
    
    params = {
        'page': page,
        'pageSize': page_size,
        'sort': f"{sort_by}:ASC",
        'plugins[i18n][locale]': locale
    }
    headers = {
        'Authorization': 'Bearer cca7b6195b1d6765ad623a4974d777085dafb02593aed6f49ad419dc258cf1fc05dff06ed8dabc11fed265a3dd29475036c931ae579b113f378ddc2e0d7a0b5e6081403e9ba54bdb169d07a771be5c60061b533d141375dd0625d164a466c3e61e532c0afcf5a8143d21ec54d099dd4aad92367bd93c8d9b8f5a97c30b42442d'
    }
    response = requests.get(BASE_URL, params=params, headers=headers)
    
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError as e:
            print("JSON Decode Error:", e)
            return None
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None