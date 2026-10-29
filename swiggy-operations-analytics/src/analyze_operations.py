from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "delivery_orders.csv"
OUT = ROOT / "outputs"

def main():
    if not DATA.exists():
        raise FileNotFoundError("Run src/generate_data.py first.")
    df = pd.read_csv(DATA)
    df["completed"] = df["status"].eq("Completed")
    df["late"] = df["completed"] & (df["delivery_minutes"] > df["promised_minutes"])
    summary = df.groupby("hub", as_index=False).agg(
        total_orders=("order_id", "count"),
        completed_orders=("completed", "sum"),
        cancelled_orders=("status", lambda s: s.eq("Cancelled").sum()),
        avg_delivery_minutes=("delivery_minutes", "mean"),
        late_orders=("late", "sum"),
        avg_cost_inr=("estimated_cost_inr", "mean"),
        avg_rating=("customer_rating", "mean"))
    summary["cancellation_rate_pct"] = 100 * summary.cancelled_orders / summary.total_orders
    summary["on_time_rate_pct"] = 100 * (summary.completed_orders - summary.late_orders) / summary.completed_orders.replace(0, float("nan"))
    summary = summary.round(2).sort_values("cancellation_rate_pct", ascending=False)
    OUT.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUT / "hub_kpi_summary.csv", index=False)
    summary[(summary.cancellation_rate_pct >= 7) | (summary.on_time_rate_pct < 75)].to_csv(OUT / "hub_exceptions.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
