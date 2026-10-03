#checking whether i can leave or not using wheater api and geocoding apis
import requests
from datetime import datetime,timedelta
import time
from concurrent.futures import ThreadPoolExecutor



loc1=input("Enter Starting point:")
loc2=input("Enter Destination point:")

time_input = input("Enter departure date and time (YYYY-MM-DD HH:MM): ")
start_time = datetime.strptime(time_input, "%Y-%m-%d %H:%M")
checks=int(input("Number of check points on the way(recommended 30-45):"))

start_time_for_program = time.perf_counter()

print(start_time)

data1 = requests.get(
    f"https://geocoding-api.open-meteo.com/v1/search?name={loc1}&count=1"
).json()

data2 = requests.get(
    f"https://geocoding-api.open-meteo.com/v1/search?name={loc2}&count=1"
).json()

lat1 = data1["results"][0]["latitude"]
long1 = data1["results"][0]["longitude"]

lat2 = data2["results"][0]["latitude"]
long2 = data2["results"][0]["longitude"]
url3=f"https://router.project-osrm.org/route/v1/driving/{long1},{lat1};{long2},{lat2}?overview=full&geometries=geojson&annotations=true"

res3=requests.get(url3)
d3=res3.json()


total_duration = d3["routes"][0]["duration"]
cor=d3["routes"][0]["geometry"]["coordinates"]



sets=len(cor)//checks
points=cor[::sets]
if points[-1]!=cor[-1]:
    points.append(cor[-1])

print(len(points))
annotation = d3["routes"][0]["legs"][0]["annotation"]

distances = annotation["distance"]
durations = annotation["duration"]



#nominatim need user and purpose inside request.get , so header file is created
headers = {
    "User-Agent": "UdayRouteWeather/1.0"
}
#to store the places where there is precipitation
rain={}
def check_weather(point, weather_time):

    lon = point[0]
    lat = point[1]

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,precipitation"
        f"&timezone=auto"
    )

    response = requests.get(url)
    data = response.json()

    times = data["hourly"]["time"]
    index = times.index(weather_time)

    temperature = data["hourly"]["temperature_2m"][index]
    precipitation = data["hourly"]["precipitation"][index]

    return point, temperature, precipitation

elapsed_seconds = 0
weather_times = []

elapsed_seconds = 0
weather_times = []

for j, i in enumerate(points):

    arrival_time = start_time + timedelta(
        seconds=elapsed_seconds
    )

    if arrival_time.minute < 30:
        weather_time = arrival_time.replace(
            minute=0,
            second=0,
            microsecond=0
        )
    else:
        weather_time = (
            arrival_time + timedelta(hours=1)
        ).replace(
            minute=0,
            second=0,
            microsecond=0
        )

    weather_times.append(
        weather_time.strftime("%Y-%m-%dT%H:%M")
    )

    # move forward by the duration of this checkpoint section
    elapsed_seconds += sum(
        durations[j * sets:(j + 1) * sets]
    )
with ThreadPoolExecutor(max_workers=5) as executor:

    results = executor.map(
        check_weather,
        points,
        weather_times
    )   

for mallee in rain.items():
    print(mallee)
if not rain:
    print("No rain on the way have a good day!")
dur=(d3["routes"][0]["duration"])/3600
dist=(d3["routes"][0]["distance"])/1000
print(f"{round(dur,2)} hrs")
print(f"{round(dist,2)} km")

end_time_for_program = time.perf_counter()

print(f"Computation time: {end_time_for_program - start_time_for_program:.2f} seconds")