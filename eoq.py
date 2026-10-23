from math import radians, sin, cos, sqrt, asin


# =========================
# Inventory Functions
# =========================

def calculate_atp(on_hand, reserved):
    """
    Calculate Available-to-Promise (ATP) inventory.
    """

    if not isinstance(on_hand, int) or not isinstance(reserved, int):
        raise ValueError("Stock quantities must be whole numbers.")

    if on_hand < 0 or reserved < 0:
        raise ValueError("Stock quantities cannot be negative.")

    if reserved > on_hand:
        raise ValueError("Reserved stock cannot exceed on-hand stock.")

    return on_hand - reserved


def inventory_discrepancy(system_stock, physical_stock):
    """
    Calculate inventory discrepancy.
    Positive = system shows more stock than physically available.
    Negative = physical stock exceeds system stock.
    """
    return system_stock - physical_stock


def sufficient_stock(atp, requested_quantity):
    """
    Determine whether ATP can fulfil the customer's order.
    """
    return atp >= requested_quantity


# =========================
# Distance Functions
# =========================

def calc_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two locations using
    the Haversine formula.
    """

    earth_radius = 6371  # km

    lat1, lon1, lat2, lon2 = map(
        radians,
        [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * asin(sqrt(a))

    return earth_radius * c


# =========================
# Cost Function
# =========================

def fulfilment_cost(fixed_cost, cost_per_km, distance):
    """
    Calculate total fulfilment cost.
    """
    return fixed_cost + (cost_per_km * distance)


# =========================
# Store Selection Function
# =========================

def select_best_store(stores):
    """
    Select the cheapest eligible store.
    """

    eligible_stores = [

        store for store in stores

        if store["sufficient_stock"]
        and store["within_service_area"]
        and store["data_is_current"]

    ]

    if not eligible_stores:
        return None

    return min(
        eligible_stores,
        key=lambda store: store["fulfilment_cost"]
    )


# =========================
# Main Fulfilment Workflow
# =========================

def fulfil_order(
        stores,
        customer_lat,
        customer_lon,
        order_quantity,
        service_radius=25,
        fixed_cost=20,
        cost_per_km=2):

    evaluated_stores = []

    for store in stores:

        try:

            # ATP
            atp = calculate_atp(
                store["on_hand"],
                store["reserved"]
            )

            # Stock check
            stock_available = sufficient_stock(
                atp,
                order_quantity
            )

            # Distance calculation
            distance = calc_distance(
                store["lat"],
                store["lon"],
                customer_lat,
                customer_lon
            )

            # Service area check
            serviceable = distance <= service_radius

            # Delivery cost
            cost = fulfilment_cost(
                fixed_cost,
                cost_per_km,
                distance
            )

            evaluated_stores.append({
                "name": store["name"],
                "atp": atp,
                "distance": round(distance, 2),
                "sufficient_stock": stock_available,
                "within_service_area": serviceable,
                "fulfilment_cost": round(cost, 2),
                "data_is_current": store["data_is_current"]
            })

        except ValueError as e:
            print(f"Store {store['name']} error: {e}")

    return select_best_store(evaluated_stores)


# =========================
# Example Data
# =========================

stores = [

    {
        "name": "Store A",
        "on_hand": 50,
        "reserved": 10,
        "lat": -25.7479,
        "lon": 28.2293,
        "data_is_current": True
    },

    {
        "name": "Store B",
        "on_hand": 100,
        "reserved": 20,
        "lat": -25.7600,
        "lon": 28.2500,
        "data_is_current": True
    },

    {
        "name": "Store C",
        "on_hand": 15,
        "reserved": 10,
        "lat": -26.0000,
        "lon": 28.4000,
        "data_is_current": True
    }

]


# =========================
# Run Example
# =========================

customer_lat = -25.7500
customer_lon = 28.2300
order_quantity = 30

best_store = fulfil_order(
    stores,
    customer_lat,
    customer_lon,
    order_quantity
)

if best_store:
    print("\nRecommended Fulfilment Store")
    print("----------------------------")
    print(f"Store: {best_store['name']}")
    print(f"ATP: {best_store['atp']}")
    print(f"Distance: {best_store['distance']} km")
    print(f"Cost: R{best_store['fulfilment_cost']}")
else:
    print("No suitable store found.")
