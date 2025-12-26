# producer/train_distributions.py
import pandas as pd
import json
from pathlib import Path

DATA_PATH = Path("../data/kaggle/olist")

# Load datasets
orders = pd.read_csv(DATA_PATH / "olist_orders_dataset.csv",
                     parse_dates=["order_purchase_timestamp"])
items = pd.read_csv(DATA_PATH / "olist_order_items_dataset.csv")
payments = pd.read_csv(DATA_PATH / "olist_order_payments_dataset.csv")
products = pd.read_csv(DATA_PATH / "olist_products_dataset.csv")
customers = pd.read_csv(DATA_PATH / "olist_customers_dataset.csv")

# ---- 1. Orders per minute (Poisson λ) ----
orders["minute"] = orders["order_purchase_timestamp"].dt.floor("min")
orders_per_minute = orders.groupby("minute").size()
lambda_orders = orders_per_minute.mean()

# ---- 2. Items per order (discrete distribution) ----
items_per_order = items.groupby("order_id").size()
item_dist = items_per_order.value_counts(normalize=True).to_dict()

# ---- 3. Payment values (mean, std) ----
payment_mean = payments["payment_value"].mean()
payment_std = payments["payment_value"].std()

# ---- 4. Product category probabilities ----
product_dist = (
    products["product_category_name"]
    .value_counts(normalize=True)
    .to_dict()
)

# ---- 5. Customer state probabilities ----
customer_state_dist = (
    customers["customer_state"]
    .value_counts(normalize=True)
    .to_dict()
)

# Save learned stats
stats = {
    "lambda_orders_per_minute": lambda_orders,
    "items_per_order_dist": item_dist,
    "payment_mean": payment_mean,
    "payment_std": payment_std,
    "product_category_dist": product_dist,
    "customer_state_dist": customer_state_dist
}

Path("models").mkdir(exist_ok=True)
with open("models/stats.json", "w") as f:
    json.dump(stats, f, indent=4)

print("Statistical model trained and saved.")

