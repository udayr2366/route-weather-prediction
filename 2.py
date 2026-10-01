#checking whether i can leave or not using wheater api and geocoding apis
import requests
'''
loc=input("enter destination:")
url=f"https://geocoding-api.open-meteo.com/v1/search?name={loc.capitalize()}&count=1"
response=requests.get(url)
data=response.json()
print(response.status_code)
print(data['results'][0]["name"])
print(data["results"][0]["latitude"])
print(data["results"][0]["longitude"])


lat=data["results"][0]["latitude"]
long=data["results"][0]["longitude"]
url2=f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation"
res=requests.get(url2)
d2=res.json()
print(d2)
print(d2["current"]["temperature_2m"])
print(data["results"][0]["country"])
'''
url3=f"https://router.project-osrm.org/route/v1/driving/77.59,12.97;76.62,12.26?overview=full&geometries=geojson"

res3=requests.get(url3)
d3=res3.json()
cor=d3["routes"][0]["geometry"]["coordinates"]
points=cor[::50]
print(len(points))
j=1
headers = {
    "User-Agent": "UdayRouteWeather/1.0"
}

for i in points:
    rain=[]
    print(f"{j}.{i}")
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
    url4=f"https://api.open-meteo.com/v1/forecast?latitude={lat2}&longitude={long2}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation"
    res4=requests.get(url4)
    d4=res4.json()
    print(f"Temperature:{d4["current"]["temperature_2m"]}")
    print(f"Humidity:{d4["current"]["relative_humidity_2m"]}")
    print(f"Wind:{d4["current"]["wind_speed_10m"]}")
    per=d4["current"]["precipitation"]
    print(f"Percipitation:{per}")
    if per>0:
        print(f"!!CHANCES OF RAIN!! NEAR:{place}")
        rain.append(place)
    j=j+1

for male in rain:
    print(male)
dur=(d3["routes"][0]["duration"])/3600
dist=(d3["routes"][0]["distance"])/1000
print(f"{round(dur,2)} hrs")
print(f"{round(dist,2)} km")

