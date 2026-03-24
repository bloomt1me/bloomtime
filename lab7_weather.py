import requests
from datetime import datetime

API_KEY = "f433688eb2c7a2df13fb74f6bcaa6dff"
CITY = "Beijing"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather():
    """Fetch weather data for Beijing"""
    params = {
        "q": CITY,
        "appid": API_KEY,
        "units": "metric",
        "lang": "en"
    }
    
    try:
        print(f"🌐 Fetching weather for {CITY}...")
        response = requests.get(BASE_URL, params=params)
        print(f"📡 Server response status: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

def show_weather(data):
    """Display weather information for Beijing (7 fields)"""
    if not data:
        print("No weather data available")
        return
    
    print("\n" + "=" * 60)
    print(f"🌍 Beijing Weather - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    weather = data.get("weather", [{}])[0]
    print(f"☁️  Conditions: {weather.get('description', 'Unknown')}")
    
    main = data.get("main", {})
    print(f"🌡️  Temperature: {main.get('temp', 'Unknown')}°C")
    print(f"   Feels like: {main.get('feels_like', 'Unknown')}°C")
    print(f"   Min: {main.get('temp_min', 'Unknown')}°C")
    print(f"   Max: {main.get('temp_max', 'Unknown')}°C")
    
    print(f"💧 Humidity: {main.get('humidity', 'Unknown')}%")
    
    print(f"📊 Pressure: {main.get('pressure', 'Unknown')} hPa")
    
    wind = data.get("wind", {})
    wind_speed = wind.get('speed', 'Unknown')
    wind_deg = wind.get('deg', 'Unknown')
    
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    if wind_deg != 'Unknown':
        idx = round(wind_deg / 45) % 8
        wind_dir = directions[idx]
    else:
        wind_dir = 'Unknown'
    
    print(f"💨 Wind: {wind_speed} m/s ({wind_dir})")
    
    visibility = data.get('visibility')
    if visibility:
        print(f"👁️  Visibility: {visibility/1000} km")
    
    clouds = data.get("clouds", {})
    print(f"☁️  Cloudiness: {clouds.get('all', 'Unknown')}%")
    
    sys = data.get("sys", {})
    if sys.get("sunrise") and sys.get("sunset"):
        sunrise = datetime.fromtimestamp(sys.get("sunrise")).strftime("%H:%M")
        sunset = datetime.fromtimestamp(sys.get("sunset")).strftime("%H:%M")
        print(f"🌅 Sunrise: {sunrise}")
        print(f"🌇 Sunset: {sunset}")
    
    print("=" * 60)
    print(f"📝 Data source: OpenWeatherMap")

def main():
    print("=" * 60)
    print("  Lab Work №7 — Beijing Weather (OpenWeatherMap)")
    print("=" * 60)
    
    weather_data = get_weather()
    show_weather(weather_data)
    
    print("\n" + "=" * 60)
    print("✅ Program completed")

if __name__ == "__main__":
    main()