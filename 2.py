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
#print(d2)
print(d2["current"]["temperature_2m"])
print(data["results"][0]["country"])
'''
url3=f"https://router.project-osrm.org/route/v1/driving/77.59,12.97;76.62,12.26"

res3=requests.get(url3)
d3=res3.json()
dur=(d3["routes"][0]["duration"])/3600
dist=(d3["routes"][0]["distance"])/1000
print(f"{round(dur,2)} hrs")
print(f"{round(dist,2)} km")