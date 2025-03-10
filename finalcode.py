import requests
from datetime import datetime,timedelta

def get_region_center(region_name):
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
        for location in data:
            if (location["addresstype"]) in ["city","town"]:
                return (location["lat"],location["lon"])
    else:
        print("Error:", response.status_code)


def get_earthquakes(location,rad_in_miles=100):
    now=datetime.now()
    prev=now-timedelta(hours=24)
    
    endpoint="https://earthquake.usgs.gov/fdsnws/event/1/query"

    params = {
        "format": "geojson",
        "starttime":prev.isoformat(),
        "endtime":now.isoformat(),
        "latitude":float(location[0]),
        "longitude":float(location[1]),
        "maxradiuskm":rad_in_miles*1.60934,
        "minmagnitude":3.0
    }
    response = requests.get(url=endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        #print(f"Found {len(data['features'])} earthquakes in the specified region.")
        #print(data.keys())
        #print(data["features"])
        #print((data["features"]))
        #print(data["features"][0]["properties"])
        #print(data["features"][0]["geometry"])
        #want the following: mag,place,time,tsunami
        return(data["features"])
    else:
        print(f"Error: {response.status_code}")
        print("Error details:", response.text)


def format_quake_time(usgs_time):
    # USGS timestamp is in milliseconds since the Unix epoch (January 1st, 1970)
    # Convert to a datetime object
    dt = datetime.fromtimestamp(usgs_time / 1000)

    # Get current time and calculate "yesterday"
    now = datetime.now()
    yesterday = now - timedelta(days=1)

    # Determine the output format
    if dt.date() == dt.date():
        time_str = f"{dt.strftime('%I:%M %p')} today"
    else:
        time_str = f"{dt.strftime('%I:%M %p')} yesterday"

    return (time_str)


def create_notification(equakes):
    n=len(equakes)
    if n==1:
        mag=equakes[0]["properties"]["mag"]
        location=equakes[0]["properties"]["place"]
        time_str=format_quake_time(equakes[0]["properties"]["time"])
        tsunami=equakes[0]["properties"]["tsunami"]
        if tsunami==1:
            tsunami_str="is likely to"
        else:
            tsunami_str="is unlikely to"

        message=f"Hi, this is GeoX! An earthquake has been detected {location}"
        message += f" of magnitude {mag} at {time_str}. It {tsunami_str} trigger a tsunami."
    elif n>1:
        message="More"
    else:
        message=None

    return message

center=get_region_center(region_name="Los Angeles, CA")
print(center)
equakes=get_earthquakes(center)
print(equakes)
e_message=create_notification(equakes)
print(e_message)