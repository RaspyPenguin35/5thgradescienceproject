import requests

def get_region_bbox(region_name):
    endpoint="https://nominatim.openstreetmap.org/search"
    
    params = {
        "q":region_name,
        "format":"json",
        "polygon_geojson":0 
    }
    headers={"User-Agent":"GeoX/1.0"}
    response = requests.get(endpoint, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()

        return(data[0]["boundingbox"])
    else:
        print("Error:", response.status_code)

bbox=get_region_bbox(region_name="New Jersey")
print(bbox)