from pydantic import BaseModel
from typing import List
import joblib 
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    no_of_adults: int
    no_of_children: int
    no_of_weekend_nights: int
    no_of_week_nights: int
    type_of_meal_plan: int
    required_car_parking_space: int
    room_type_reserved: int
    lead_time: int
    arrival_year: int
    arrival_month: int
    arrival_date: int
    market_segment_type: int
    repeated_guest: int
    no_of_previous_cancellations: int
    no_of_previous_bookings_not_canceled: int
    avg_price_per_room: float
    no_of_special_requests: int

# Load model and scaler once globally (optional for performance)
scaler = joblib.load("/Users/bhuwanneupane/Projects/hotel_reservation_prediction/artifacts/model/scalar.joblib")
model = joblib.load("/Users/bhuwanneupane/Projects/hotel_reservation_prediction/artifacts/model/model.joblib")

@app.post("/")
async def predict(request: InputData):
    input_data = [
        request.no_of_adults,
        request.no_of_children,
        request.no_of_weekend_nights,
        request.no_of_week_nights,
        request.type_of_meal_plan,
        request.required_car_parking_space,
        request.room_type_reserved,
        request.lead_time,
        request.arrival_year,
        request.arrival_month,
        request.arrival_date,
        request.market_segment_type,
        request.repeated_guest,
        request.no_of_previous_cancellations,
        request.no_of_previous_bookings_not_canceled,
        request.avg_price_per_room,
        request.no_of_special_requests
    ]

    input_array = np.array(input_data).reshape(1, -1)
    scaled_input = scaler.transform(input_array)
    prediction = model.predict(scaled_input)

    return {"prediction": prediction.tolist()}