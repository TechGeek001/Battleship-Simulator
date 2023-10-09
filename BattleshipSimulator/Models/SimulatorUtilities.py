import math
from shapely.geometry import Polygon
from shapely.affinity import translate, rotate, scale

def calculate_angle_degrees(x1, y1, x2, y2):
    """
    Calculate the angle (in degrees) between two coordinates.

    Parameters:
    -----------
    x1 : float
        X-coordinate of the first point.
    y1 : float
        Y-coordinate of the first point.
    x2 : float
        X-coordinate of the second point.
    y2 : float
        Y-coordinate of the second point.
    
    Returns:
    --------
    angle_degrees : float
        The angle (in degrees) between the two coordinates.
    """
    # Calculate the difference in X and Y coordinates
    delta_x = x2 - x1
    delta_y = y2 - y1

    # Use atan2 to calculate the angle in radians
    angle_radians = math.atan2(delta_y, delta_x)

    # Convert radians to degrees
    angle_degrees = (math.degrees(angle_radians) - 90) % 360

    return angle_degrees

def update_circle_coordinates(current_x, current_y, center_x, center_y, radius, speed, timedelta):
    """
    Update the current x, y coordinates around a circle and return the angle in degrees.

    Parameters:
    -----------
    current_x : float
        Current X-coordinate.
    current_y : float
        Current Y-coordinate.
    center_x : float
        X-coordinate of the center of the circle.
    center_y : float
        Y-coordinate of the center of the circle.
    radius : float
        Radius of the circle.
    speed : float
        Speed of movement in pixels per second.
    timedelta : float
        Time duration since the last update (in seconds).

    Returns:
    --------
    new_x : float
        New X-coordinate after the update.
    new_y : float
        New Y-coordinate after the update.
    facing_angle_degrees : float
        Angle (in degrees) that the battleship is facing.
    """
    # Calculate the angular speed in radians per second
    angular_speed = speed / radius

    # Calculate the change in angle based on elapsed time
    delta_angle = angular_speed * timedelta

    # Calculate the new angle
    current_angle = math.atan2(current_y - center_y, current_x - center_x)
    new_angle = current_angle + delta_angle

    # Calculate the new coordinates
    new_x = center_x + radius * math.cos(new_angle)
    new_y = center_y + radius * math.sin(new_angle)

    # Convert the facing angle to degrees
    facing_angle_degrees = math.degrees(new_angle)

    return new_x, new_y, facing_angle_degrees % 360

import math

def update_path_coordinates_with_angle(path, speed, timedelta):
    """
    Update the current x, y coordinates along a defined path based on a given speed and time delta.
    
    Parameters:
    -----------
    path : list of tuple
        A list of (x, y) coordinates defining the path.
    speed : float
        Speed of movement in units per second.
    timedelta : float
        Time duration since the last update (in seconds).
        
    Returns:
    --------
    new_x : float
        New X-coordinate after the update.
    new_y : float
        New Y-coordinate after the update.
    facing_angle_degrees : float
        Angle (in degrees) that the object is facing.
    updated_path : list of tuple or empty list
        Updated path starting from the new position or an empty list if the object reaches the end of the path.
    """
    
    # Calculate the distance to be covered in this timestep
    distance_to_cover = speed * timedelta
    
    # Extract the current position and the next waypoint
    current_pos = path[0]
    next_waypoint = path[1]
    
    # Calculate the distance to the next waypoint
    distance_to_next_waypoint = math.sqrt((next_waypoint[0] - current_pos[0])**2 + 
                                        (next_waypoint[1] - current_pos[1])**2)
    
    # Determine the direction vector (normalized) to the next waypoint
    dx = (next_waypoint[0] - current_pos[0]) / distance_to_next_waypoint
    dy = (next_waypoint[1] - current_pos[1]) / distance_to_next_waypoint
    
    # Calculate the facing angle
    facing_angle_rad = math.atan2(dy, dx)
    facing_angle_degrees = math.degrees(facing_angle_rad) % 360
    
    while distance_to_cover > distance_to_next_waypoint and len(path) > 2:
        # Subtract the distance to the next waypoint from the total distance to cover
        distance_to_cover -= distance_to_next_waypoint
        
        # Move to the next segment of the path
        path.pop(0)
        current_pos = path[0]
        next_waypoint = path[1]
        
        # Calculate the distance to the next waypoint
        distance_to_next_waypoint = math.sqrt((next_waypoint[0] - current_pos[0])**2 + 
                                            (next_waypoint[1] - current_pos[1])**2)
        
        # Determine the direction vector (normalized) to the next waypoint
        dx = (next_waypoint[0] - current_pos[0]) / distance_to_next_waypoint
        dy = (next_waypoint[1] - current_pos[1]) / distance_to_next_waypoint
    
    if len(path) <= 2 and distance_to_cover >= distance_to_next_waypoint:
        # If the object reaches the end of the path or exceeds the path length
        return current_pos[0], current_pos[1], facing_angle_degrees, []
    
    # Update the current position based on the remaining distance to cover
    new_x = current_pos[0] + dx * distance_to_cover
    new_y = current_pos[1] + dy * distance_to_cover
    
    # Update the path to start from the new position
    updated_path = [(new_x, new_y)] + path[1:]
    
    return new_x, new_y, facing_angle_degrees, updated_path

def polygons_intersect(polygon1_coords, polygon2_coords):
    """
    Determine if one polygon touches or overlaps another polygon with optional transformations.

    Parameters:
    -----------
    polygon1_coords : list of tuple
        A list of (x, y) tuples defining the first polygon.
    polygon2_coords : list of tuple
        A list of (x, y) tuples defining the second polygon.
    offset1 : tuple, optional
        An (x, y) tuple defining the offset for the first polygon.
    offset2 : tuple, optional
        An (x, y) tuple defining the offset for the second polygon.
    angle1 : float, optional
        Rotation angle in degrees for the first polygon.
    angle2 : float, optional
        Rotation angle in degrees for the second polygon.

    Returns:
    --------
    bool
        True if the polygons touch or overlap after transformations, otherwise False.
    """

    # Convert coordinates to Shapely Polygons
    polygon1 = Polygon(polygon1_coords)
    polygon2 = Polygon(polygon2_coords)

    # Check if the polygons intersect (touch or overlap)
    return polygon1.intersects(polygon2)

def transform_coordinates(coords, dx=0, dy=0, rotation_deg=0, scaling_factor=1.0, origin='center'):
    """
    Apply transformations to a set of coordinates.

    Parameters:
    - coords (list of tuple): List of (x, y) coordinates.
    - dx (float): Translation in x-direction.
    - dy (float): Translation in y-direction.
    - rotation_deg (float): Rotation angle in degrees.
    - scaling_factor (float): Factor by which to scale the shape. Default is 1.0 (no scaling).
    - origin (str or tuple): The point around which rotation and scaling will be performed.

    Returns:
    - list of tuple: Transformed coordinates.
    """
    polygon = Polygon(coords)
    
    # Translate
    polygon = translate(polygon, xoff=dx, yoff=dy)
    
    # Rotate
    polygon = rotate(polygon, angle=rotation_deg, origin=origin)
    
    # Scale
    polygon = scale(polygon, xfact=scaling_factor, yfact=scaling_factor, origin=origin)
    
    return list(polygon.exterior.coords)