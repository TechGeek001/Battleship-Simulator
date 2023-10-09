from BattleshipSimulator.Models.Logger import CSVLogger

class BattleshipController:
    """
    The controller in the MVC architecture. Handles user interactions and updates the model.

    Attributes:
    -----------
    model : BattleshipModel
        The model representing the battleship's data and state.
    """
    
    def __init__(self, world):
        """
        Initializes the BattleshipController with a model.

        Parameters:
        -----------
        model : BattleshipModel
            The model representing the battleship's data and state.
        """
        self.world = world
        self.logger = CSVLogger("results.csv")
        self.logger.log(self.world.logging_package())
        self.simulation_running = True
    
    def update(self, timedelta):
        self.world.update(timedelta)
        self.logger.log(self.world.logging_package())
        if self.model_get("collision_event"):
            self.terminate_simulation(False)
            self.logger.close()

    def handle_action(self, action):
        """
        Handle user actions and update the model.

        Parameters:
        -----------
        action : str
            The user action to handle.
        """
        self.model.handle_command(action)
    
    def world_get(self, variable_name):
        if ":" not in variable_name:
            return getattr(self.world, variable_name)
        else:
            system_name, variable_name = variable_name.split(":", maxsplit = 1)
            return self.world.get_attribute(system_name, variable_name)
    
    def model_get(self, variable_name):
        if ":" not in variable_name:
            return getattr(self.world.models["Battleship"], variable_name)
        else:
            system_name, variable_name = variable_name.split(":", maxsplit = 1)
            return self.world.models["Battleship"].get_attribute(system_name, variable_name)

    def model_set(self, variable_name, value):
        if ":" not in variable_name:
            setattr(self.world.models["Battleship"], variable_name, value)
        else:
            system_name, variable_name = variable_name.split(":", maxsplit = 1)
            self.world.models["Battleship"].set_attribute(system_name, variable_name, value)
    
    def terminate_simulation(self, status):
        self.simulation_running = False