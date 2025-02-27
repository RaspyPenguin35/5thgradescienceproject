import requests

def get_region_bbox(region_name):
    endpoint="https://nominatim.openstreetmap.org/search"
    
    params = {
        "q":region_name,
        "format":"json",
        "polygon_geojson":0 
    }
   
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        # Print the data
        print(response)
    else:
        print("Error:", response.status_code)




    