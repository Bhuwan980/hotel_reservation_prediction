import React, { useState } from "react";
import "./App.css";
import axios from "axios";

function App() {
  const [formData, setFormData] = useState({
    no_of_adults: "",
    no_of_children: "",
    no_of_weekend_nights: "",
    no_of_week_nights: "",
    type_of_meal_plan: "",
    required_car_parking_space: "",
    room_type_reserved: "",
    lead_time: "",
    arrival_year: "",
    arrival_month: "",
    arrival_date: "",
    market_segment_type: "",
    repeated_guest: "",
    no_of_previous_cancellations: "",
    no_of_previous_bookings_not_canceled: "",
    avg_price_per_room: "",
    no_of_special_requests: "",
  });

  const [prediction, setPrediction] = useState(null);

  const formatLabel = (key) =>
    key.replaceAll("_", " ").replace(/\b\w/g, (char) => char.toUpperCase());

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    try {
      const cleanedData = {};
      for (const key in formData) {
        cleanedData[key] = isNaN(formData[key])
          ? formData[key]
          : Number(formData[key]);
      }
  
      const res = await axios.post("http://127.0.0.1:5000/", cleanedData);
      setPrediction(res.data.prediction);
    } catch (err) {
      console.error(err);
      alert("Something went wrong with the prediction.");
    }
  };

  const mealOptions = {
    "Meal Plan 1": 1,
    "Meal Plan 2": 2,
    "Meal Plan 3": 3,
    "Not Selected": 0,
  };

  const roomOptions = {
    "Room Type 1": 1,
    "Room Type 2": 2,
    "Room Type 3": 3,
    "Room Type 4": 4,
    "Room Type 5": 5,
  };

  const marketOptions = {
    Online: 1,
    Offline: 2,
    Corporate: 3,
    Complementary: 4,
  };

  return (
    <div className="app">
      <h2>Hotel Booking Cancellation Prediction</h2>
      <form onSubmit={handleSubmit} className="grid-form">
        {Object.keys(formData).map((key) => (
          <div className="form-group" key={key}>
            <label>{formatLabel(key)}</label>

            {key === "type_of_meal_plan" ? (
              <select name={key} onChange={handleChange} required>
                <option value="">Select...</option>
                {Object.entries(mealOptions).map(([label, val]) => (
                  <option key={val} value={val}>
                    {label}
                  </option>
                ))}
              </select>
            ) : key === "room_type_reserved" ? (
              <select name={key} onChange={handleChange} required>
                <option value="">Select...</option>
                {Object.entries(roomOptions).map(([label, val]) => (
                  <option key={val} value={val}>
                    {label}
                  </option>
                ))}
              </select>
            ) : key === "market_segment_type" ? (
              <select name={key} onChange={handleChange} required>
                <option value="">Select...</option>
                {Object.entries(marketOptions).map(([label, val]) => (
                  <option key={val} value={val}>
                    {label}
                  </option>
                ))}
              </select>
            ) : key === "arrival_year" ? (
              <select name={key} onChange={handleChange} required>
                <option value="">Select...</option>
                {[2017, 2018, 2019].map((year) => (
                  <option key={year} value={year}>
                    {year}
                  </option>
                ))}
              </select>
            ) : key === "arrival_month" ? (
              <select name={key} onChange={handleChange} required>
                <option value="">Select...</option>
                {Array.from({ length: 12 }, (_, i) => i + 1).map((month) => (
                  <option key={month} value={month}>
                    {month}
                  </option>
                ))}
              </select>
            ) : (
              <input
                type="number"
                name={key}
                value={formData[key]}
                onChange={handleChange}
                required
              />
            )}
          </div>
        ))}
      </form>

      <button onClick={handleSubmit}>Predict</button>

      {prediction && (
        <div className="result">
          <h3>Prediction: {prediction}</h3>
        </div>
      )}
    </div>
  );
}

export default App;