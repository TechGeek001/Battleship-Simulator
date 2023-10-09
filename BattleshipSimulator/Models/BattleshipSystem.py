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
    
    def commands(self):
        return ["ACCELERATE", "DECELERATE"]

    def handle_command(self, command):
        match command:
            case "ACCELERATE":
                self.accelerate()
            case "DECELERATE":
                self.decelerate()
            case _:
                print(f"Unrecognized command: {command}")

    def accelerate(self):
        # Logic for acceleration
        pass

    def decelerate(self):
        # Logic for deceleration
        pass


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
    
    def commands(self):
        return ["SET_DESTINATION"]

    def handle_command(self, command):
        match command:
            case "SET_DESTINATION":
                self.set_destination()
            case _:
                print(f"Unrecognized command: {command}")

    def set_destination(self):
        # Logic to set a new destination
        pass