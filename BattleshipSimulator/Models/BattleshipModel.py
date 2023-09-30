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
        self.speed = 15
        
        self.attributes = {}
        self.observers = []
        self.systems = {}
        self.command_registry = {}
        self.path = []
        self.route = []
        self.setup()
    
    def setup(self):
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

        # Generate objects that are in the way - make this better in the future
        self.obstacles = [
            [(260, 320), (365,350), (270,440), (260, 320)]
        ]

    def update(self, timedelta):
        """
        Update the X and Y coordinates of the battleship at regular intervals.

        Parameters:
        -----------
        timedelta : float
            The time duration between coordinate updates (in seconds).
        """
        
        if len(self.path) > 0:
            self.last_x, self.last_y, self.last_angle = self.x, self.y, self.angle
            self.x, self.y, self.angle, self.path = SimulatorUtilities.update_path_coordinates_with_angle(self.path, self.speed, timedelta)

            dx, dy, da = self.x - self.last_x, self.y - self.last_y, self.angle - self.last_angle
            self.battleship_geometry = SimulatorUtilities.transform_coordinates(self.battleship_geometry, dx, dy, da)
            self.minimum_safe_area_geometry = SimulatorUtilities.transform_coordinates(self.minimum_safe_area_geometry, dx, dy, da)
        
            self.collision_warning = False
            self.collision_event = False
            for obstacle in self.obstacles:
                if SimulatorUtilities.polygons_intersect(self.minimum_safe_area_geometry, obstacle):
                    self.collision_warning = True
                if SimulatorUtilities.polygons_intersect(self.battleship_geometry, obstacle):
                    self.collision_event = True
    
    def set_path(self, coords):
        self.path = []
        self.path = (self.x, self.y)
        for coord in coords:
            self.path.append(coord)

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
        return self.attributes.get(system_name, {}).get(attr_name)

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