import BattleshipSimulator.Models.SimulatorUtilities as SimulatorUtilities

from shapely.geometry import Polygon
import time

class BattleshipModel:
    """
    The main model of the battleship, maintaining the attributes of the ship and its systems.
    
    Attributes:
    -----------
    attributes : dict
        Dictionary to store attributes of each system.
    observers : list
        List of observers (e.g., the view) that get notified when the model changes.
    systems : dict
        Dictionary to store attached systems.
    command_registry : dict
        Dictionary to map commands to systems that handle them.
    """

    MINIMUM_SAFE_DISTANCE = 100 # In meters

    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 90
        self.last_x = 0
        self.last_y = 0
        self.last_angle = 90
        self.current_speed = 0
        self.logging_variables = ["x", "y", "angle", "current_speed", "collision_warning", "collision_event"]
        
        self.systems = {}
        self.command_registry = {}
        self.setup()
    
    def setup(self):
        self.world = None
        self.collision_warning = False
        self.collision_event = False

        # Calculate the polygon that represents the ship (units are in meters)
        width = 20
        length = 154

        self.battleship_geometry = [
            (width / 2 ,  length),
            (width * .8,  length * .87),
            (width     ,  length * .375),
            (width * .9,  length * .15),
            (width * .8,  0),
            (width * .2,  0),
            (width * .1,  length * .15),
            (0         ,  length * .375),
            (width * .2,  length * .87)
        ]
        # Center the geometry on 0,0 meters
        self.battleship_geometry = SimulatorUtilities.transform_coordinates(self.battleship_geometry, -width / 2, -length / 2)
        self.minimum_safe_area_geometry = self.calculate_min_safe_distance_area()

    def update(self, timedelta):
        """
        Update the X and Y coordinates of the battleship at regular intervals.

        Parameters:
        -----------
        timedelta : float
            The time duration between coordinate updates (in seconds).
        """
        
        self.collision_warning = False
        self.collision_event = False
        current_msa_geometry = SimulatorUtilities.transform_coordinates(self.minimum_safe_area_geometry, self.x, self.y, self.angle)
        current_bs_geometry = SimulatorUtilities.transform_coordinates(self.battleship_geometry, self.x, self.y, self.angle)
        for obstacle in self.world.obstacles:
            if SimulatorUtilities.polygons_intersect(current_msa_geometry, obstacle):
                self.collision_warning = True
            if SimulatorUtilities.polygons_intersect(current_bs_geometry, obstacle):
                self.collision_event = True
        
        for system in self.systems.values():
            system.update(timedelta)
        
        if len(self.systems["Navigation"].waypoints) > 0:
            self.last_x, self.last_y, self.last_angle = self.x, self.y, self.angle
            self.x, self.y, self.angle, self.systems["Navigation"].waypoints = SimulatorUtilities.update_path_coordinates_with_angle(self.systems["Navigation"].waypoints, self.current_speed, timedelta)

    def logging_package(self):
        logging_package = {k: getattr(self, k) for k in self.logging_variables}
        for system in self.systems.values():
            system_log_package = system.logging_package()
            for k, v in system_log_package.items():
                logging_package[k] = v
        return logging_package
    
    def set_attribute(self, system_name, attr_name, value):
        """
        Sets an attribute for a specific system and notifies observers.
        
        Parameters:
        -----------
        system_name : str
            The name of the system.
        attr_name : str
            The name of the attribute.
        value : Any
            The value of the attribute.
        """
        if system_name not in self.attributes:
            self.attributes[system_name] = {}
        self.attributes[system_name][attr_name] = value

    def get_attribute(self, system_name, attr_name):
        """
        Gets an attribute for a specific system.
        
        Parameters:
        -----------
        system_name : str
            The name of the system.
        attr_name : str
            The name of the attribute.
            
        Returns:
        --------
        value : Any
            The value of the attribute.
        """
        return getattr(self.systems[system_name], attr_name)

    def attach_system(self, system_name, system):
        """
        Attach a system to the battleship and register its commands.
        
        Parameters:
        -----------
        system_name : str
            The name of the system.
        system : BattleshipSystem
            The system object.
        """
        self.systems[system_name] = system
        for command in system.commands():
            if command in self.command_registry:
                raise KeyError(f"Could not attach '{system.__class__.__name__}'; command '{command}' already handled by '{self.command_registry[command].__class__.__name__}'")
            self.command_registry[command] = system

    def handle_command(self, command):
        """
        Route the command to the appropriate system.
        
        Parameters:
        -----------
        command : str
            The command to be executed.
        """
        system = self.command_registry.get(command)
        if system:
            system.handle_command(command)
        else:
            print(f"Warning: No system can handle the command '{command}'!")
    
    def calculate_min_safe_distance_area(self):
        """
        Expand a convex polygon in all directions using the Minkowski sum concept.
        
        The function leverages the `buffer` method from the Shapely library, which computes 
        the Minkowski sum of the input polygon and a disk of a given radius. This results in 
        expanding the polygon uniformly in every direction by the specified distance.

        Parameters
        ----------
        vertices : list of tuple
            A list of (x, y) tuples defining the convex polygon.
        distance : float, optional
            The distance to expand the polygon in all directions. Default is 100.

        Returns
        -------
        list of tuple
            A list of (x, y) vertices of the expanded polygon. The last point is not repeated.
        """
        
        # Create a shapely polygon from the vertices
        polygon = Polygon(self.battleship_geometry)
        # Use buffer to expand the polygon
        expanded_polygon = polygon.buffer(self.MINIMUM_SAFE_DISTANCE)
        return list(expanded_polygon.exterior.coords)