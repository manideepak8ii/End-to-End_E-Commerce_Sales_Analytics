from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "delivery_orders.csv"

def main(n_orders=5000, seed=42):
    rng = np.random.default_rng(seed)
    hubs = np.array(["Central", "North", "South", "East", "West"])
    hub = rng.choice(hubs, size=n_orders)
    hour = rng.integers(8, 24, size=n_orders)
    peak = np.isin(hour, [12, 13, 19, 20, 21])
    effect = pd.Series(hub).map({"Central": 2, "North": 4, "South": 1, "East": 3, "West": 2}).to_numpy()
    prep = np.maximum(5, rng.normal(12, 4, n_orders))
    travel = np.maximum(5, rng.normal(18, 6, n_orders) + peak * 5 + effect)
    cancelled = rng.random(n_orders) < np.clip(0.035 + peak * 0.025 + effect * 0.004, 0, .25)
    minutes = np.round(prep + travel, 1)
    distance = np.round(np.clip(rng.gamma(2.2, 2.0, n_orders), .5, 15), 2)
    rating = np.where(~cancelled, np.clip(np.round(rng.normal(4.2 - (minutes > 35) * .45, .5), 1), 1, 5), np.nan)
    df = pd.DataFrame({
        "order_id": np.arange(1, n_orders + 1), "hub": hub, "order_hour": hour,
        "distance_km": distance, "prep_minutes": np.round(prep, 1),
        "delivery_minutes": minutes, "promised_minutes": 35,
        "status": np.where(cancelled, "Cancelled", "Completed"),
        "customer_rating": rating,
        "estimated_cost_inr": np.round(18 + distance * 4.2 + rng.normal(0, 2, n_orders), 2)
    })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"Generated {len(df)} synthetic orders: {OUT}")

if __name__ == "__main__":
    main()
