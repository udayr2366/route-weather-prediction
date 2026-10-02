#checking whether i can leave or not using wheater api and geocoding apis
import requests
from datetime import datetime,timedelta


loc1=input("Enter Starting point:")
loc2=input("Enter Destination point:")

time_input = input("Enter departure date and time (YYYY-MM-DD HH:MM): ")
start_time = datetime.strptime(time_input, "%Y-%m-%d %H:%M")
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

checks=int(input("Number of check points on the way(recommended 30-45):"))

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
for j, i in enumerate(points):
    #calcuating distance for each checkpoint i.e it will check distance from 1-70 then 70-140
    arrival_time = start_time + timedelta(seconds=sum(durations[:j * sets]))

    #making time floor and ceil eg. 5:12->5:00 and 5:42->6:00
    if arrival_time.minute < 30:
        weather_time = arrival_time.replace(minute=0, second=0, microsecond=0)
    else:
        weather_time = (arrival_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

    weather_time = weather_time.strftime("%Y-%m-%dT%H:%M")


    print(f"{j + 1}. {i}")
    print("Expected arrival:", arrival_time.strftime("%H:%M"))
    url5=f"https://nominatim.openstreetmap.org/reverse?lat={i[1]}&lon={i[0]}&format=json"
    res5=requests.get(url5, headers=headers)
    d5=res5.json()
    address = d5["address"]

    place = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("suburb")
        or "Unknown"
    )

    print(place)
    long2=i[0]
    lat2=i[1]
    url4=f"https://api.open-meteo.com/v1/forecast?latitude={lat2}&longitude={long2}&hourly=temperature_2m,precipitation&timezone=auto"
    res4=requests.get(url4)
    d4=res4.json()
    times = d4["hourly"]["time"]
    index = times.index(weather_time)
    temps = d4["hourly"]["temperature_2m"]
    per = d4["hourly"]["precipitation"]
    temperature = temps[index]
    pres = per[index]
    print(f"Temperature:{temperature}")
    print(f"Percipitation:{pres}\n")
    match pres:
        case x if 0.0<x<=2.5:
            rain[place]=[pres,"light rain"]
        case x if 2.5<x<=7.5:
            rain[place]=[pres,"moderate rain"]
        case x if 7.5<x:
            rain[place]=[pres,"heavy rain"]
        

    

for mallee in rain.items():
    print(mallee)
if not rain:
    print("No rain on the way have a good day!")
dur=(d3["routes"][0]["duration"])/3600
dist=(d3["routes"][0]["distance"])/1000
print(f"{round(dur,2)} hrs")
print(f"{round(dist,2)} km")