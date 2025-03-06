import requests
from datetime import datetime,timedelta

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


def get_earthquakes(bbox):
    now=datetime.now()
    prev=now-timedelta(hours=24)
    
    endpoint="https://earthquake.usgs.gov/fdsnws/event/1/query"

    params = {
        "format": "geojson",
        "starttime":prev.isoformat(),
        "endtime":now.isoformat(),
        "minlatitude":float(bbox[0]),
        "maxlatitude":float(bbox[1]),
        "minlongitude":float(bbox[2]),
        "maxlongitude":float(bbox[3]),
        "minmagnitude":3.0
    }
    response = requests.get(url=endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data['features'])} earthquakes in the specified region.")
        #print(data.keys())
        #print(data["features"])
        #print((data["features"]))
        print(data["features"][0]["properties"])
        print(data["features"][0]["geometry"])
        #want the following: mag,place,time,felt,alert,tsunami
        #maybe will add the following: cdi,mmi,sig
    else:
        print(f"Error: {response.status_code}")
        print("Error details:", response.text)

bbox=get_region_bbox(region_name="California")
print(bbox)
equake=get_earthquakes(bbox)
print(equake)