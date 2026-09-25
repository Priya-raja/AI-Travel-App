from fastapi import FastAPI
from routes.planner import router as planner_router

app = FastAPI(
    title="Travel planner API",
    description="This is a travel planner API that allows users to plan their trips, find destinations, and manage their itineraries.",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "api": "Travel planner API",
        "version": "1.0.0",
        "endpoints":{
            "POST /plan_trip": "Create a personalized travel plan(Aggregated).",
            "GET /plan/stream": "Stream a travel plan (SSE)",
            "GET/plan/cache-stats": "View cache statistics for travel plans.",
            "DELETE /plan/cache": "Clear cached travel plans.",
        }
    }

app.include_router(planner_router)
