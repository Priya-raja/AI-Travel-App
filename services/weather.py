from models.model import WeatherResponseModel
from services.cache import get_cache, set_cache
from datetime import datetime
import httpx
import os
from pathlib import Path


WEATHER_CACHE_TTL_SECONDS = 600

# Load WEATHER_API_KEY from environment or .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # fallback: try to load a .env file in project root
    env_path = Path(__file__).resolve().parents[2] / '.env'
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if not line or line.strip().startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

async def get_weather_data(
        destination: str,
        start_date: datetime,
        end_date: datetime) -> list[WeatherResponseModel]:
    """Fetch weather data for a destination between start and end dates."""
    start_date_text = start_date.strftime("%Y-%m-%d") if isinstance(start_date, datetime) else str(start_date)
    end_date_text = end_date.strftime("%Y-%m-%d") if isinstance(end_date, datetime) else str(end_date)
    cache_key = f"weather:{destination.strip().casefold()}:{start_date_text}:{end_date_text}"

    cached_weather = get_cache(cache_key)
    if cached_weather is not None:
        return cached_weather

    api_key = os.getenv('WEATHER_API_KEY', 'YOUR_WEATHERAPI_KEY')
    base_url = "https://api.weatherapi.com/v1/forecast.json"

    # Convert non-string params to str to satisfy httpx typing for `params`
    params = {
        "key": api_key,
        "q": str(destination),
        "sdt": start_date_text,
        "end_dt": end_date_text,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        weather_list = []
        for day in data.get("forecast", {}).get("forecastday", []):
            forecast = WeatherResponseModel(
                date=day["date"],
                condition=day["day"]["condition"]["text"],
                temperature_high=day["day"]["maxtemp_c"],
                temperature_low=day["day"]["mintemp_c"],
                humidity=day["day"]["avghumidity"],
                rain_chance=day["day"]["daily_chance_of_rain"],
            )
            weather_list.append(forecast)

        set_cache(cache_key, weather_list, WEATHER_CACHE_TTL_SECONDS)
        return weather_list
