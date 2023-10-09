class BattleshipSystem:
    """
    Base class for all ship subsystems. Provides a generic structure for individual systems.
    
    Attributes:
    -----------
    name : str
        The name of the system.
    model : BattleshipModel
        Reference to the main battleship model.
    """

    def __init__(self, name, model):
        self.name = name
        self.model = model
        self.logging_variables = []
        self.setup()
    
    def setup(self):
        pass

    def update(self, timedelta):
        pass

    def logging_package(self):
        return {f"{self.name}.{k}": getattr(self, k) for k in self.logging_variables}

    def commands(self):
        """
        List of commands this system can handle.

        Returns:
        --------
        list
            List of command strings.
        """
        return []

    def handle_command(self, command):
        """
        Handle a specific command.

        Parameters:
        -----------
        command : str
            The command to handle.
        """
        pass

    def update_attribute(self, attr_name, value):
        """
        A utility method to update attributes of this system in the model.

        Parameters:
        -----------
        attr_name : str
            The attribute's name.
        value : Any
            The value to set.
        """
        self.model.set_attribute(self.name, attr_name, value)

class Rudder(BattleshipSystem):
    """Represents the rudder system of the battleship."""
    
    def commands(self):
        return ["TURN_RIGHT", "TURN_LEFT"]

    def handle_command(self, command):
        match command:
            case "TURN_RIGHT":
                self.turn_right()
            case "TURN_LEFT":
                self.turn_left()
            case _:
                print(f"Unrecognized command: {command}")

    def turn_right(self):
        current_angle = self.model.get_attribute(self.name, "angle") or 0
        new_angle = current_angle + 5
        self.update_attribute("angle", new_angle)

    def turn_left(self):
        current_angle = self.model.get_attribute(self.name, "angle") or 0
        new_angle = current_angle - 5
        self.update_attribute("angle", new_angle)

class Engine(BattleshipSystem):
    """Represents the engine system of the battleship."""
    
    def setup(self):
        # TODO: pull constants from a config file
        self.min_speed = 0
        self.max_speed = 15
        self.acceleration = .5
        self.desired_speed = 15
        self.logging_variables = ["desired_speed"]
    
    def update(self, timedelta):
        if not self.model.collision_event:
            # Update the ship's current speed
            if self.model.current_speed != self.desired_speed:
                speed_difference = self.desired_speed - self.model.current_speed
                # The acceleration change is the acceleration divided by the timedelta
                acceleration_change = min(self.acceleration * timedelta, abs(speed_difference))
                if speed_difference > 0:
                    self.model.current_speed += acceleration_change
                else:
                    self.model.current_speed -= acceleration_change
        else:
            self.model.current_speed = 0

    def commands(self):
        return ["SET_SPEED"]

    def handle_command(self, command, *args):
        match command:
            case "SET_SPEED":
                self.set_speed(*args)
            case _:
                print(f"Unrecognized command: {command}")

    def set_speed(self, new_speed):
        if self.min_speed <= new_speed <= self.max_speed:
            self.desired_speed = new_speed

class Weapons(BattleshipSystem):
    """Represents the weapons system of the battleship."""
    
    def commands(self):
        return ["FIRE"]

    def handle_command(self, command):
        match command:
            case "FIRE":
                self.fire()
            case _:
                print(f"Unrecognized command: {command}")

    def fire(self):
        # Logic to fire weapons
        pass

class Navigation(BattleshipSystem):
    """Represents the navigation system of the battleship."""
    
    def setup(self):
        self.waypoints = []
        self.projected_path = []
    
    def update(self, timedelta):
        projected_path = [(self.model.x, self.model.y)]
        for waypoint in self.waypoints:
            projected_path.append((waypoint[0], waypoint[1]))
        self.projected_path = projected_path

    def commands(self):
        return ["ADD_WAYPOINT"]

    def handle_command(self, command, *args):
        match command:
            case "ADD_WAYPOINT":
                self.set_waypoint(*args)
            case _:
                print(f"Unrecognized command: {command}")

    def add_waypoint(self, x, y):
        self.waypoints.append((x, y))