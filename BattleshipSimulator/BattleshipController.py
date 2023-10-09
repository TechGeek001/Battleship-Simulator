class BattleshipController:
    """
    The controller in the MVC architecture. Handles user interactions and updates the model.

    Attributes:
    -----------
    model : BattleshipModel
        The model representing the battleship's data and state.
    """
    
    def __init__(self, model):
        """
        Initializes the BattleshipController with a model.

        Parameters:
        -----------
        model : BattleshipModel
            The model representing the battleship's data and state.
        """
        self.model = model

    def handle_action(self, action):
        """
        Handle user actions and update the model.

        Parameters:
        -----------
        action : str
            The user action to handle.
        """
        self.model.handle_command(action)
    
    def model_get(self, variable_name):
        if ":" not in variable_name:
            return getattr(self.model, variable_name)
        else:
            system_name, variable_name = variable_name.split(":", maxsplit = 1)
            return self.model.get_attribute(system_name, variable_name)

    def model_set(self, variable_name, value):
        if ":" not in variable_name:
            setattr(self.model, variable_name, value)
        else:
            system_name, variable_name = variable_name.split(":", maxsplit = 1)
            self.model.set_attribute(system_name, variable_name, value)
    
    def trigger_model_update(self, timedelta):
        self.model.update(timedelta)
