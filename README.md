# Route Weather Checker 

A Python-based route planning tool that checks weather conditions at multiple points along a driving route.

The project combines **geocoding, route calculation, weather forecasting, reverse geocoding, and concurrent API requests** to determine whether rain is expected along a planned journey.

 Features

- Accepts starting point and destination from the user
- Accepts a planned departure date and time
- Converts locations into geographical coordinates using the Open-Meteo Geocoding API
- Calculates the driving route using OSRM
- Divides the route into multiple checkpoints
- Calculates the expected arrival time at each checkpoint
- Retrieves hourly weather information from Open-Meteo
- Detects precipitation along the route
- Classifies precipitation as:
  - Light rain
  - Moderate rain
  - Heavy rain
- Uses reverse geocoding to identify locations where rain is detected
- Uses `ThreadPoolExecutor` to perform independent weather API requests concurrently
- Measures program execution time

# Technologies Used

- Python
- Requests
- Open-Meteo API
- Open-Meteo Geocoding API
- OSRM Routing API
- Nominatim / OpenStreetMap
- `concurrent.futures`
- `datetime`
- `time`

##  How It Works

The application follows this workflow:

```text
Start
  │
  ▼
Enter starting point & destination
  │
  ▼
Geocode locations
  │
  ▼
Calculate driving route
  │
  ▼
Select route checkpoints
  │
  ▼
Calculate expected arrival time
  │
  ▼
Request weather data concurrently
  │
  ▼
Check precipitation
  │
  ├── No rain → Continue
  │
  └── Rain detected
          │
          ▼
     Reverse geocode location
          │
          ▼
     Classify rainfall
  │
  ▼
Display route & weather information
  │
  ▼
Display execution time
