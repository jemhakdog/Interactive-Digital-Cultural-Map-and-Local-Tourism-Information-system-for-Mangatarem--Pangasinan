"""Geospatial utility functions for distance calculations."""

import math


def haversine_distance(lat1, lng1, lat2, lng2):
    """
    Calculate the great-circle distance between two points on Earth.

    Args:
        lat1, lng1: Latitude and longitude of point 1 (degrees)
        lat2, lng2: Latitude and longitude of point 2 (degrees)

    Returns:
        Distance in kilometers
    """
    R = 6371  # Earth's radius in kilometers

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
