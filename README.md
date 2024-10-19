# graphics-project-2

This code is the full scene for Project 2: Wireframe Scene, done by Matthew Merritt, Michael Merritt, and Harsh Gandhi. 

The code is divided into three files, with the following breakdown:

- `car_scene_pygame.py` - Contains the animated 3D scene with cones and moving car. This is the file that should be run.
- `utils.py` - Supporting module borrowed from class examples. Includes classes for points and vectors.
- `camera.py` - Supporting module borrowed from class examples. Includes camera movement and rotation.

In terms of controls, the following features are included:
- `Escape` - Closes the pygame scene window and ends the program.
- `Space` - Starts/pauses/resumes the car animation.
- `A` - Rotates the camera left about the y-axis (effectively like turning your head).
- `D` - Rotates the camera right about the y-axis (effectively like turning your head).
- `W` - Moves the camera forward relative to the direction it is looking.
- `S` - Moves the camera backward relative to the direction it is looking.
- `Q` - Moves the camera up along the y-axis.
- `E` - Moves the camera down along the y-axis.
- `G` - Toggle the grid shown on the ground.
- `Left Arrow` - Rotates the world clockwise.
- `Right Arrow` - Rotates the world counterclockwise.
- `Up Arrow` - Increases the car movement speed.
- `Down Arrow` - Decreases the car movement speed.

Note about bonus features:

The grid is included to help with visualizing the rotations and current position of the camera. The speed of the car can also be adjusted, with the distance travelled corresponding to the arc length travelled by the wheels. Additionally, the speed of the car is capped, only being able to increase or decrease between 8 different speeds. 
