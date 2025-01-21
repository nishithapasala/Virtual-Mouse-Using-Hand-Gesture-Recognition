import numpy as np  # For mathematical calculations

# Function to calculate the angle between three points: a, b, and c
def get_angle(a, b, c):
    """
    Calculate the angle formed by three points (a, b, c) using vector mathematics.
    
    Args:
        a (tuple): Coordinates of the first point (x1, y1).
        b (tuple): Coordinates of the middle point (x2, y2).
        c (tuple): Coordinates of the third point (x3, y3).

    Returns:
        float: The absolute angle in degrees between the two vectors formed by the points.
    """
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])  # Calculate angle in radians
    angle = np.abs(np.degrees(radians))  # Convert radians to degrees
    return angle

# Function to calculate the distance between two points
def get_distance(landmark_list):
    """
    Calculate the Euclidean distance between two landmarks (points).
    
    Args:
        landmark_list (list): List of two points [(x1, y1), (x2, y2)].

    Returns:
        float: The interpolated distance between the two points.
    """
    if len(landmark_list) < 2:  # Ensure at least two points are provided
        return None
    (x1, y1), (x2, y2) = landmark_list[0], landmark_list[1]  # Extract coordinates of the two points
    L = np.hypot(x2 - x1, y2 - y1)  # Calculate Euclidean distance
    return np.interp(L, [0, 1], [0, 1000])  # Scale distance for consistent measurement
