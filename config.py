api = None

try:
    with open("api_key.txt") as f:
        api = f.readline()
except FileNotFoundError:
    print("API file not found")

USE_ROUNDED_COORDS = True
OPENWEATHER_API = api or "7549b3ff11a7b2f3cd25b56d21c83c6a"
OPENWEATHER_URL = (
        "http://api.openweathermap.org/data/2.5/weather?"
        "lat={latitude}&lon={longitude}&"
        "appid=" + OPENWEATHER_API + "&lang=ru&"
                                     "units=metric"
)
