# Battleship Simulator

## Overview
Battleship Simulator is an interactive simulation game combining strategic gameplay with naval warfare educational elements. The game offers graphical (GUI) and command-line (CLI) interfaces, providing a versatile experience for various users. It's built using Python and leverages the `arcade` library for the graphical rendering.

## Features
- **Graphical and Command-Line Interfaces:** Choose between a fully interactive GUI and a straightforward CLI.
- **Customizable Scenarios:** Modify existing scenarios or create new ones to change game dynamics.
- **Realistic Naval Models:** Simulate real-world naval battleships with detailed configurations.
- **Dynamic Game Environment:** Navigate through different terrains and obstacles.

## Installation

To run Battleship Simulator, you must install Python (and the requirements.txt) on your computer. Follow these steps to install and run the game:

##### **Clone the Repository:**
```bash
   git clone https://github.com/yourusername/battleship-simulator.git
   cd battleship-simulator
```

##### Install Dependencies:

```
pip install -r requirements.txt
```

##### **Run the Battleship Simulator:**

```
python main.py
```

Follow on-screen instructions to navigate through the game.

### Docker Instructions (Linux Based Kernel)

Enable connections from your local Docker container server
```
xhost +local:docker
```

Build the Container (Linux OS)
```
docker build -t battleship_x11 .
```

Run the Container: 
```
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix battleship_x11
```

#### Customizing Scenarios
Scenarios are defined in YAML files. To create a new scenario or edit an existing one, modify the files in the scenarios directory. Refer to our scenario documentation for detailed guidelines on scenario creation.

## Contributing
Contributions to the Battleship Simulator are welcome! If you have suggestions or bug fixes, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
Thanks to the arcade library team for providing an excellent platform for game development.
This project was inspired by classic naval warfare strategies and simulations.
"NOTE---- NEED TO ADD MORE ACKS"



