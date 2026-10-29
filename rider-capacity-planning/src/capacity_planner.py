from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "capacity_plan.csv"
HUBS = ["Central", "North", "South", "East", "West"]

def build_history(seed=19, days=21):
    rng = np.random.default_rng(seed)
    rows = []
    for day in range(days):
        for hour in range(8, 24):
            peak = 1.8 if hour in (12, 13, 19, 20, 21) else 1.0
            weekend = 1.15 if day % 7 in (4, 5) else 1.0
            for hub, base in zip(HUBS, [26, 18, 23, 16, 20]):
                orders = max(0, int(rng.normal(base * peak * weekend, 5)))
                riders = max(1, int(rng.normal(base * .13, 2)))
                rows.append((day, hour, hub, orders, riders))
    return pd.DataFrame(rows, columns=["day", "hour", "hub", "orders", "available_riders"])

def main():
    df = build_history()
    latest = df.day.max()
    recent = df[df.day >= latest - 3]
    forecast = recent.groupby(["hub", "hour"], as_index=False).orders.mean().rename(columns={"orders": "forecast_orders"})
    supply = df[df.day == latest][["hub", "hour", "available_riders"]]
    plan = forecast.merge(supply, on=["hub", "hour"])
    plan["required_riders"] = np.ceil(plan.forecast_orders / 2.5).astype(int)
    plan["rider_gap"] = plan.required_riders - plan.available_riders
    plan["status"] = np.select([plan.rider_gap > 2, plan.rider_gap > 0],
                               ["Critical shortage", "Potential shortage"], default="Capacity adequate")
    plan["forecast_orders"] = plan.forecast_orders.round(1)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    plan.sort_values(["rider_gap", "hub", "hour"], ascending=[False, True, True]).to_csv(OUT, index=False)
    print(plan.sort_values("rider_gap", ascending=False).head(15).to_string(index=False))
    print(f"Saved: {OUT}")

if __name__ == "__main__":
    main()
