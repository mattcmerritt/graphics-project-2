#==============================
# Christian Duncan
# CSC345/CSC645: Computer Graphics
#   Fall 2024
# Description:
#   Demonstrates use of a Camera class for easier navigation
#==============================

import sys
import pygame
from OpenGL.GLU import *
from OpenGL.GL import *
from utils import *
from camera import *

# These parameters define the camera's lens shape
CAM_NEAR = 0.01
CAM_FAR = 1000.0
CAM_ANGLE = 60.0

# These parameters define simple animation properties
FPS = 60.0
DELAY = int(1000.0 / FPS + 0.5)

# Global (Module) Variables (ARGH!)
window_dimensions = (1000, 800)
name = b'Look At Me, Mom!'
animate = False
viewAngle = 0
MAX_CYLINDER_HEIGHT = 10
cylinder_height = MAX_CYLINDER_HEIGHT/2
cylinder_step = 0.03
#eye = Point(0, 10, 70)
# look = Point(0, 0, 0)
#lookD = Vector(Point(0, 0, -1))
#up = Vector(Point(0, 1, 0))  # Usually what you want unless you want a tilted camera
#camera = Camera(CAM_ANGLE, window_dimensions[0]/window_dimensions[1], CAM_NEAR, CAM_FAR)

def main():
    init()
    global camera
    camera = Camera(CAM_ANGLE, window_dimensions[0]/window_dimensions[1], CAM_NEAR, CAM_FAR)
    camera.eye = Point(0, 5, 30)  # Position the camera
    camera.look = Point(0, 0, 0)  # Look at the center of the scene
    camera.up = Vector(Point(0, 1, 0))  # Set up vector

    # Enters the main loop.   
    # Displays the window and starts listening for events.
    main_loop()
    return

# Any initialization material to do...
def init():
    global tube, clock, running

    # pygame setup
    pygame.init()
    pygame.key.set_repeat(300, 50)
    pygame.display.set_mode(window_dimensions, pygame.DOUBLEBUF|pygame.OPENGL)
    clock = pygame.time.Clock()
    running = True

    tube = gluNewQuadric()
    gluQuadricDrawStyle(tube, GLU_LINE)

def main_loop():
    global running, clock, animate
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keyboard(event)

        if animate:
            # Advance to the next frame
            advance()

        # (Re)draw the scene (should only do this when necessary!)
        display()

        # Flipping causes the current image to be seen. (Double-Buffering)
        pygame.display.flip()

        clock.tick(FPS)  # delays to keep it at FPS frame rate

# Callback function used to display the scene
# Currently it just draws a simple polyline (LINE_STRIP)
def display():
    # Set the viewport to the full screen
    win_width = window_dimensions[0]
    win_height = window_dimensions[1]
    glViewport(0, 0, win_width, win_height)

    camera.setProjection()
    
    # Clear the Screen
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)


    # And draw the "Scene"
    glColor3f(1.0, 1.0, 1.0)
    draw_scene()

    # And show the scene
    glFlush()

# Advance the scene one frame
def advance():
    global cylinder_height, cylinder_step
    cylinder_height += cylinder_step
    if cylinder_height <= 0:
        # Reached the bottom - switch directions
        cylinder_height = 0
        cylinder_step = -cylinder_step
    elif cylinder_height >= MAX_CYLINDER_HEIGHT:
        # Reached the top - switch directions
        cylinder_height = MAX_CYLINDER_HEIGHT
        cylinder_step = -cylinder_step

# Function used to handle any key events
# event: The keyboard event that happened
def keyboard(event):
    global running, animate, viewAngle
    key = event.key # "ASCII" value of the key pressed
    if key == 27:  # ASCII code 27 = ESC-key
        running = False
    elif key == ord(' '):
        animate = not animate
    elif key == ord('a'):
        # Go left
        camera.turn(1)
    elif key == ord('d'):
        # Go right
        camera.turn(-1)
    elif key == ord('w'):
        # Go forward
        camera.slide(0,0,-1)
    elif key == ord('s'):
        # Go backward
        camera.slide(0,0,1)
    elif key == ord('q'):
        # Go up
        camera.slide(0,1,0)
    elif key == ord('e'):
        # Go down
        camera.slide(0,-1,0)
    elif key == pygame.K_LEFT:
        # turn world left
        viewAngle += 1
    elif key == pygame.K_RIGHT:
        # turn world right
        viewAngle -= 1

def draw_scene():
    """
    * draw_scene:
    *    Draws a simple scene with a few shapes
    """
    # Place the camera
    glMatrixMode(GL_MODELVIEW);
    camera.placeCamera()
    
    # Now transform the world
    glColor3f(1, 1, 1)
    glRotate(viewAngle, 0, 1, 0)
    draw() 

# Draw the entire scene - cylinders and spheres, oh my!
def draw():
    glPushMatrix()
    # TODO: determine necessary transformations
    drawGrid(20, 1)  # Draw a 40x40 grid with 1 unit steps
    glColor3f(0.0, 0.0, 0.0)  # Set color to black for contrast against white background
    drawCone(-10, 0, 0)
    drawCone(10, 0, 0)
    drawCar()

    # for i in range(-3,4):     # i goes from -3 to 3 (inclusive)
    #     for j in range(-3,4): # j does the same
    #         glPushMatrix()
    #         glTranslated(i*10, 0, j*10)  # Move to a "grid spot"
    #         glRotated(-90, 1, 0, 0)       # So it draws cylinder upwards
    #         if i == -3 and j == 3:
    #             # Draw a cone for this one
    #             gluCylinder(tube, 2, 0, cylinder_height, 40, 5)
    #         elif (i + j) % 2 == 0:
    #             gluCylinder(tube, 2, 2, cylinder_height, 40, 5)
    #         else:
    #             gluCylinder(tube, 2, 2, MAX_CYLINDER_HEIGHT - cylinder_height, 40, 5)
    #         glPopMatrix()
    glPopMatrix()

#=======================================
# Scene-drawing functions
#=======================================
def drawCone(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0) 
    gluCylinder(tube, 1, 0.2, 8, 20, 10)  # Base radius, top radius, height, 20 slices and stacks
    glPopMatrix()

def drawCar():
    # drawWheel should be called 4 times in here
    pass

def drawWheel():
    pass

def drawGrid(size, steps):
    glBegin(GL_LINES)
    glColor3f(0.5, 0.5, 0.5) 
    for i in range(-size, size+1, steps):
        glVertex3f(i, 0, -size)
        glVertex3f(i, 0, size)
        glVertex3f(-size, 0, i)
        glVertex3f(size, 0, i)
    glEnd() 
#=======================================
# Direct OpenGL Matrix Operation Examples
#=======================================
def printMatrix():
    """
    Prints out the Current ModelView Matrix
    The problem is in how it is stored in the system
    The matrix is in COL-major versus ROW-major so
    indexing is a bit odd.
    """
    m = glGetFloatv(GL_MODELVIEW_MATRIX)
   
    for row in range(4):
        for col in range(4):
            sys.stdout.write('{0:6.3f} '.format(m[col][row]))
        sys.stdout.write('\n')
    

if __name__ == '__main__': main()
