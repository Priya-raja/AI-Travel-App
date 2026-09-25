from fastapi import APIRouter
from models.model import TravelRequestModel
from services.weather import get_weather_data


router = APIRouter(
    prefix="/plan",
    tags=["Travel Plan"],
)


@router.post("/")
async def create_travel_plan(
    travel_request: TravelRequestModel
):
    """
    aggregates weather, currency and places data into a comprehensive travel plan.
    """

    if travel_request.start_date > travel_request.end_date:
        raise ValueError("Start date cannot be after end date.")
    trip_duration = (travel_request.end_date - travel_request.start_date).days
    if trip_duration < 1:
        raise ValueError("Trip duration must be at least 1 day.")

    if trip_duration > 14:
        raise ValueError("Trip duration cannot exceed 14 days.")

    # Get me weather data
    weather_data = await get_weather_data(
        destination=travel_request.destination,
        start_date=travel_request.start_date,
        end_date=travel_request.end_date
    )
    return {
        "message": "Travel plan created successfully",
        "weather_data": weather_data
    }
