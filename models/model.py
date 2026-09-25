from pydantic import BaseModel, Field
from datetime import datetime


class TravelRequestModel(BaseModel):
    id: int = Field(..., description="Unique identifier for the travel request")
    destination: str = Field(..., description="Destination of the travel request")
    start_date: datetime = Field(..., description="Start date of the travel")
    end_date: datetime = Field(..., description="End date of the travel")
    base_currency: str = "INR"

class WeatherResponseModel(BaseModel):
    date: datetime = Field(..., description="Date for which weather data is fetched")
    temperature_high: float = Field(..., description="Temperature in Celsius")
    temperature_low: float = Field(..., description="Low temperature in Celsius")
    condition: str = Field(..., description="Weather condition (e.g., Sunny, Rainy)")
    humidity: float = Field(..., description="Humidity percentage")
    rain_chance: float = Field(..., description="Chance of rain percentage")
