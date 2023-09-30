import BattleshipSimulator.Models.SimulatorUtilities as SimulatorUtilities
import BattleshipSimulator.Models.SimulatorViewUtilities as SimulatorViewUtilities
import arcade

class BattleshipView(arcade.View):
    """
    The GUI representation of the battleship using the arcade library.

    Attributes:
    -----------
    model : BattleshipModel
        The model representing the battleship's data and state.
    controller : BattleshipController
        The controller to handle user interactions and update the model.
    screen_width : int
        The width of the screen.
    screen_height : int
        The height of the screen.

    Methods:
    --------
    on_draw():
        Draws the battleship's representation and information on the screen.
    on_key_press(key, _):
        Handles key press events, triggering appropriate actions.
    on_key_release(key, _):
        Handles key release events.
    update(delta_time):
        Called to update the view's state.
    """

    PIXELS_PER_METER = 200 / 154

    def __init__(self, controller, screen_width=800, screen_height=600):
        """
        Initializes the BattleshipView with a model, controller, and window properties.

        Parameters:
        -----------
        controller : BattleshipController
            The controller to handle user interactions and update the model.
        screen_width : int, optional
            The width of the screen (default is 800).
        screen_height : int, optional
            The height of the screen (default is 600).
        """
        super().__init__()
        arcade.Window.background_color = arcade.color.BRIGHT_NAVY_BLUE
        self.controller = controller
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.mouse_x = 0
        self.mouse_y = 0
        self.elapsed_time = 0
        self.setup()
    
    def setup(self):
        self.status_bar = Status_Pane(self.screen_width - 150, self.screen_height / 2, 300, self.screen_height, self)
        self.battleship_safety_colors = [arcade.color.GREEN, arcade.color.ORANGE, arcade.color.RED]

        # Clear the ShapeList to update it
        self.obstacle_list = arcade.ShapeElementList()
        obstacle_color = arcade.color.BROWN
        for obstacle in self.controller.model_get("obstacles"):
            obstacle_shape = arcade.create_polygon(SimulatorViewUtilities.convert_coords_list_meters_to_pixels(
                obstacle, self.PIXELS_PER_METER),
            obstacle_color)
            self.obstacle_list.append(obstacle_shape)
    
    def on_update(self, timedelta):
        self.elapsed_time += timedelta
        self.controller.trigger_model_update(timedelta)
        self.status_bar.update(timedelta)
        
        collision_warning = self.controller.model_get("collision_warning")
        collision_event = self.controller.model_get("collision_event")
        if collision_warning:
            self.collision_index = 2 if collision_event else 1
        else:
            self.collision_index = 0
        # Clear the ShapeList to update it
        self.ship_shape_list = arcade.ShapeElementList()
        # Draw the battleship representation (a polygon)
        self.battleship_color = arcade.color.LIGHT_GRAY if self.collision_index != 2 else arcade.color.RED
        battleship_coordinates = SimulatorViewUtilities.convert_coords_list_meters_to_pixels(self.controller.model_get("battleship_geometry"), self.PIXELS_PER_METER)
        x, y, width, height = SimulatorViewUtilities.get_bounding_box(battleship_coordinates)
        self.battleship_coordinates = SimulatorUtilities.transform_coordinates(battleship_coordinates, -x, -y)
        self.battleship_shape = arcade.create_polygon(battleship_coordinates, self.battleship_color)
        self.ship_shape_list.append(self.battleship_shape)

        battleship_ring_coordinates = SimulatorViewUtilities.convert_coords_list_meters_to_pixels(self.controller.model_get("minimum_safe_area_geometry"), self.PIXELS_PER_METER)
        x, y, width, height = SimulatorViewUtilities.get_bounding_box(battleship_ring_coordinates)
        self.battleship_ring_coordinates = SimulatorUtilities.transform_coordinates(battleship_ring_coordinates, -x, -y)
        self.battleship_safety_shape = arcade.create_line_loop(battleship_ring_coordinates, self.battleship_safety_colors[self.collision_index], 2)
        self.ship_shape_list.append(self.battleship_safety_shape)

    def on_draw(self):
        """
        Draws the battleship's representation and information on the screen.
        """
        self.clear()
        arcade.start_render()
        arcade.draw_line_strip(SimulatorViewUtilities.convert_coords_list_meters_to_pixels(self.controller.model_get("path"), self.PIXELS_PER_METER), arcade.color.BLUE, 2)
        self.obstacle_list.draw()
        self.ship_shape_list.draw()
        self.status_bar.draw()
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_key_press(self, key, _):
        """
        Handles key press events, triggering appropriate actions.

        Parameters:
        -----------
        key : int
            The key code of the pressed key.
        _ : int
            Modifiers for the key press, not used here.
        """
        if key == arcade.key.RIGHT:
            self.controller.handle_action("TURN_RIGHT")

    def on_key_release(self, key, _):
        """
        Handles key release events.

        Parameters:
        -----------
        key : int
            The key code of the released key.
        _ : int
            Modifiers for the key release, not used here.
        """
        pass

class Status_Pane():

    STD_OFFSET = 5

    def __init__(self, x, y, width, height, parent_view):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_x = x + width // 2
        self.min_x = self.max_x - width
        self.max_y = y + height // 2
        self.min_y = self.max_y - height
        self.parent_view = parent_view
        self.setup()

    def setup(self):
        key_text = ""
        val_text = ""
        header_text = ""
        self.monitored_data = {
            "----- Model Data -----": {
                "Ship X (px)": round(self.parent_view.controller.model_get('x') / self.parent_view.PIXELS_PER_METER),
                "Ship Y (px)": round(self.parent_view.controller.model_get('y') / self.parent_view.PIXELS_PER_METER),
                "Ship X (m)": round(self.parent_view.controller.model_get('x'), 2),
                "Ship Y (m)": round(self.parent_view.controller.model_get('y'), 2),
                "Course Angle": f"{round(self.parent_view.controller.model_get('angle'))}°",
            },
            "----- View Data -----": {
                "Total Time": SimulatorViewUtilities.seconds_to_hms(self.parent_view.elapsed_time),
                "Time Delta": "0 ms",
                "Frame Rate": f"{int(arcade.get_fps())} FPS",
                "Mouse X (px)": self.parent_view.mouse_x,
                "Mouse Y (px)": self.parent_view.mouse_y,
                "Mouse X (m)": round(self.parent_view.mouse_x * self.parent_view.PIXELS_PER_METER, 2),
                "Mouse Y (m)": round(self.parent_view.mouse_y * self.parent_view.PIXELS_PER_METER, 2),
            }
        }
        for section in self.monitored_data:
            key_text += "\n"
            val_text += "\n"
            header_text += section + "\n"
            for key, value in self.monitored_data[section].items():
                header_text += "\n"
                key_text += key + "\n"
                val_text += str(value) + "\n"
            key_text += "\n"
            val_text += "\n"
            header_text += "\n"

        self.key_column = arcade.Text(key_text, self.min_x + 10, self.max_y - 10, arcade.color.WHITE, 12, self.width / 2, anchor_x="left", anchor_y = "top", multiline=True)
        self.val_column = arcade.Text(val_text, self.min_x + (self.width / 2), self.max_y - 10, arcade.color.WHITE, 12, self.width / 2, anchor_x="left", anchor_y = "top", multiline=True)
        self.header_column = arcade.Text(header_text, self.min_x + (self.width / 2), self.max_y - 10, arcade.color.YELLOW, 12, self.width, anchor_x = "center", anchor_y = "top", align = "center", multiline=True)

    def update(self, timedelta):
        key_text = ""
        val_text = ""
        header_text = ""
        self.monitored_data = {
            "----- Model Data -----": {
                "Ship X (px)": round(self.parent_view.controller.model_get('x') / self.parent_view.PIXELS_PER_METER),
                "Ship Y (px)": round(self.parent_view.controller.model_get('y') / self.parent_view.PIXELS_PER_METER),
                "Ship X (m)": round(self.parent_view.controller.model_get('x'), 2),
                "Ship Y (m)": round(self.parent_view.controller.model_get('y'), 2),
                "Course Angle": f"{round(self.parent_view.controller.model_get('angle'))}°",
            },
            "----- View Data -----": {
                "Total Time": SimulatorViewUtilities.seconds_to_hms(self.parent_view.elapsed_time),
                "Time Delta": f"{int(timedelta * 1000)} ms",
                "Frame Rate": f"{int(arcade.get_fps())} FPS",
                "Mouse X (px)": self.parent_view.mouse_x,
                "Mouse Y (px)": self.parent_view.mouse_y,
                "Mouse X (m)": round(self.parent_view.mouse_x * self.parent_view.PIXELS_PER_METER, 2),
                "Mouse Y (m)": round(self.parent_view.mouse_y * self.parent_view.PIXELS_PER_METER, 2),
            }
        }

        for section in self.monitored_data:
            key_text += "\n"
            val_text += "\n"
            header_text += section + "\n"
            for key, value in self.monitored_data[section].items():
                header_text += "\n"
                key_text += key + "\n"
                val_text += str(value) + "\n"
            key_text += "\n"
            val_text += "\n"
            header_text += "\n"
        
        self.key_column.text = key_text
        self.val_column.text = val_text
        self.header_column.text = header_text
    
    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, arcade.color.BLACK)
        self.key_column.draw()
        self.val_column.draw()
        self.header_column.draw()