"""Utility Functions for Parking app."""

from math import radians, sin, cos, acos


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance in kilometers between two points using the Law of Cosines formula.
    """
    R = 6371000  # Radius of Earth in meters (6,371 kilometers)
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    cos_angle = sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1)
    distance = R * acos(cos_angle)

    return round(distance)
