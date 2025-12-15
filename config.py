# config.py

# 1. Location Settings
# The city you want to load. Start small to keep it fast!
PLACE_NAME = "Central Park, New York, USA"

# 2. Noise Multipliers (The "Stick")
# High number = Avoid this street
NOISE_WEIGHTS = {
    'motorway': 10.0,
    'trunk': 9.0,
    'primary': 8.0,
    'secondary': 6.0,
    'tertiary': 4.0,
    'residential': 1.2,
    'living_street': 1.0,
    'service': 1.5,
    'footway': 0.5,
    'cycleway': 0.5,
    'pedestrian': 0.3,
    'track': 0.8,
    'path': 0.4,
    'steps': 3.0,        # Quiet, but physically annoying
}

# 3. Greenery Multipliers (The "Carrot")
# If a street is inside a park, we multiply the cost by this.
# 0.5 means the street is treated as "half as long" by the algorithm,
# so the algorithm will detour to find it.
PARK_MULTIPLIER = 0.4

# Default weight if we can't identify the road
DEFAULT_NOISE_WEIGHT = 2.0