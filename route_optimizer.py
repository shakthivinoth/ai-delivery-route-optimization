"""Module 1: Route optimization using the Nearest Neighbor algorithm."""

# Sample coordinates (latitude, longitude) - used to draw the map.
LOCATIONS = {
    "Warehouse":  {"lat": 13.0827, "lng": 80.2707},
    "Customer A": {"lat": 13.1200, "lng": 80.2400},
    "Customer B": {"lat": 13.1100, "lng": 80.2650},
    "Customer C": {"lat": 13.0900, "lng": 80.2800},
    "Customer D": {"lat": 13.1000, "lng": 80.2900},
}

# Sample road distances in km between every pair of places.
_PAIRS = {
    ("Warehouse", "Customer A"): 12, ("Warehouse", "Customer B"): 9,
    ("Warehouse", "Customer C"): 4,  ("Warehouse", "Customer D"): 7,
    ("Customer A", "Customer B"): 5, ("Customer A", "Customer C"): 11,
    ("Customer A", "Customer D"): 8, ("Customer B", "Customer C"): 6,
    ("Customer B", "Customer D"): 3, ("Customer C", "Customer D"): 5,
}
DISTANCES = {}
for (a, b), km in _PAIRS.items():          # store both directions
    DISTANCES[(a, b)] = km
    DISTANCES[(b, a)] = km

DEFAULT_SPEED = 30  # km/h


def format_time(minutes):
    h, m = divmod(round(minutes), 60)
    return f"{h} h {m} min" if h else f"{m} min"


def nearest_neighbor(start, customers):
    """From the current stop, always go to the closest unvisited customer."""
    route, current, remaining = [start], start, list(customers)
    while remaining:
        nxt = min(remaining, key=lambda c: DISTANCES[(current, c)])
        route.append(nxt)
        remaining.remove(nxt)
        current = nxt
    return route


def optimize(customers, speed=DEFAULT_SPEED, start="Warehouse"):
    if start not in LOCATIONS:
        raise ValueError("Unknown warehouse.")
    if not customers:
        raise ValueError("Select at least one customer.")
    for c in customers:
        if c not in LOCATIONS or c == start:
            raise ValueError(f"Unknown customer: {c}")
    if speed <= 0:
        raise ValueError("Average speed must be greater than 0.")

    route = nearest_neighbor(start, customers)
    legs = [{"from": a, "to": b, "km": DISTANCES[(a, b)]}
            for a, b in zip(route, route[1:])]
    total_km = sum(leg["km"] for leg in legs)
    minutes = total_km / speed * 60          # Time = Distance / Speed
    return {
        "route": route,
        "legs": legs,
        "total_distance_km": total_km,
        "time_minutes": round(minutes, 1),
        "time_text": format_time(minutes),
        "average_speed": speed,
        "coordinates": [{"name": n, **LOCATIONS[n]} for n in route],
    }
