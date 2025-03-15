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
        #print(f"OSM output\n:{data}\n=====") ###Debugging
        # for location in data:
        #     if (location["addresstype"]) in ["city","town"]:
        #         return (location["lat"],location["lon"])
        return (data[0]["lat"], data[0]["lon"])
    else:
        print("Error:", response.status_code)


def get_earthquakes(location,rad_in_miles=100):
    print(f"Location lat/long: {location}")
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
    #print(f"Equake info from usgs:{equakes}")

    if not equakes:
        return None

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

        message=f"Hi, this is Geo-X! An earthquake has been detected {location}"
        message += f" of magnitude {mag} at {time_str}. It {tsunami_str} trigger a tsunami."

    elif n>1:
        ### Of the n quakes, find the one with the biggest magnitude
        max_mag=equakes[0]["properties"]["mag"]
        imax=0
        for i in range(1,n):
            if equakes[i]["properties"]["mag"] > max_mag:
                max_mag = equakes[i]["properties"]["mag"]
                imax=i

        tsunami=equakes[0]["properties"]["tsunami"]
        for i in range(1,n):
            tsunami = tsunami or equakes[i]["properties"]["tsunami"]

        if tsunami==1:
            tsunami_str="is likely to"
        else:
            tsunami_str="is unlikely to"

        location=equakes[imax]["properties"]["place"]
        time_str=format_quake_time(equakes[imax]["properties"]["time"])
        message=f"Hi this is Geo-X! {n} earthquakes have been detected near your designated area in the last 24 hours. "
        message += f"The strongest one, of magnitude {max_mag}, has been detected {location} at {time_str}. "
        message += f"It {tsunami_str} trigger a tsunami."

    return message

def text_to_speech(message):
    endpoint="https://translate.google.com/translate_tts"
    
    params={
        "ie":"UTF-8",
        "client":"tw-ob",
        #"q":"The strongest one, of magnitude 3.58, has been detected 56 km NNW of Charlotte Amalie, U.S. Virgin Islands  at 03:46 AM today. It is unlikely to trigger a tsunami.",
        "q":message,
        "tl":"en",
        "textlen":len(message)
    }

    response=requests.get(url=endpoint, params=params)

    if response.status_code==200:
        with open("tts.mp3", "wb") as f:
            f.write(response.content)
    else:
        print(f"Request to Google Translate failed with status code {response.status_code}")
        print(response.text)

    response.close()


center=get_region_center(region_name="New Dehli, India")
print(center)
equakes=get_earthquakes(center)
print(equakes)
e_message=create_notification(equakes)
print(e_message)
text_to_speech(e_message)