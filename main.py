# Import modules from the Battleship package instead of individual classes
import BattleshipSimulator.BattleshipController as BattleCtrl
import BattleshipSimulator.Models.Environment as Environment
import BattleshipSimulator.Models.BattleshipModel as BattleModel
import BattleshipSimulator.Models.BattleshipSystem as BattleSystem
import BattleshipSimulator.Views.BattleshipView as BattleGUI
import arcade

# Constants for the screen width and height
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 768

def main():
    # Create the world
    world = Environment.World()
    # Create the model of the battleship
    model = BattleModel.BattleshipModel()
    world.attach_model(model, "Battleship")
    model.current_speed = 15
    # Attach various systems to the model
    rudder_system = BattleSystem.Rudder("Rudder", model)
    model.attach_system("Rudder", rudder_system)
    engine_system = BattleSystem.Engine("Engine", model)
    model.attach_system("Engine", engine_system)
    weapons_system = BattleSystem.Weapons("Weapons", model)
    model.attach_system("Weapons", weapons_system)
    navigation_system = BattleSystem.Navigation("Navigation", model)
    model.attach_system("Navigation", navigation_system)
    waypoints = [(100,100), (400,100), (400, 400), (100, 400), (150,150)]
    waypoints = [(200,200), (400, 400), (100, 400), (150,150)]
    model.x = waypoints[0][0]
    model.y = waypoints[0][1]
    for waypoint in waypoints:
        navigation_system.add_waypoint(*waypoint)
    
    # Create the controller and view, set up the window, and start the GUI loop
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Battleship Simulator")
    view = BattleGUI.BattleshipView(BattleCtrl.BattleshipController(world), SCREEN_WIDTH, SCREEN_HEIGHT)
    window.show_view(view)
    arcade.enable_timings()
    arcade.run()

if __name__ == "__main__":
    main()