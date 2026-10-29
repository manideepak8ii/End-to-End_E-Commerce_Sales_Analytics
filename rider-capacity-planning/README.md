# Rider Capacity Planning

A transparent baseline model for hourly order-demand planning by hub. It estimates the riders required for forecast demand and flags potential staffing gaps.

## Run
```bash
python -m pip install pandas numpy
python src/capacity_planner.py
```

The script generates synthetic history, forecasts demand using a trailing average, estimates rider needs using an explicit productivity assumption (2.5 orders/rider/hour), and exports a capacity plan. Calibrate assumptions against real operational data before practical deployment. No actual Swiggy data is used.

Inspired by public logistics analytics ideas: https://github.com/PetersonVital/delivery-route-optimization
