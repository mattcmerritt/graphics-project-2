#==============================
# Matthew Merritt, Michael Merritt, Harsh Gandhi
# CSC345/CSC645: Computer Graphics
#   Fall 2024
# Description:
#   Displays a scene with an animated car and moving camera,
#   Boilerplate code is reused from examples in class.
#==============================

import sys
import pygame
import math
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

# Global (Module) Variables

# Window data
window_dimensions = (1000, 800)
name = b'Project 2'
animate = False
viewAngle = 0
# Car position / state information
spinAngle = 0
movingForward = True
distance = 0
# Constants
WHEEL_RADIUS = 0.75
MAX_ROTATIONS = 3

# Camera information
# eye = Point(0, 10, 70)
# look = Point(0, 0, 0)
# lookD = Vector(Point(0, 0, -1))
# up = Vector(Point(0, 1, 0))  # Usually what you want unless you want a tilted camera
# camera = Camera(CAM_ANGLE, window_dimensions[0]/window_dimensions[1], CAM_NEAR, CAM_FAR)

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
    global spinAngle, movingForward, distance
    # update the wheel spin angle
    if movingForward:
        spinAngle -= 1
    else:
        spinAngle += 1

    # switch movement direction if the car moves far enough
    if spinAngle >= 360 * MAX_ROTATIONS:
        movingForward = True
    elif spinAngle <= -360 * MAX_ROTATIONS:
        movingForward = False

    # determine how far the car has moved using the spinAngle
    # uses the arc length traveled by wheel as it spins, with the
    #   assumption that the wheel is perfectly circular
    distance = spinAngle * (math.pi / 180) * WHEEL_RADIUS

# Function used to handle any key events
# event: The keyboard event that happened
def keyboard(event):
    global running, animate, viewAngle, spinAngle
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

# Draw the entire scene - cones and car
def draw():
    glPushMatrix()

    drawGrid(20, 1)  # Draw a 40x40 grid with 1 unit steps
    glColor3f(0.0, 0.0, 0.0)  # Set color to black for contrast against white background
    drawCone(-10, 0, 0)
    drawCone(10, 0, 0)
    drawCar(0, WHEEL_RADIUS, 2 + distance)

    glPopMatrix()

#=======================================
# Scene-drawing functions
#=======================================

# function to draw a singular cone
def drawCone(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0) 
    gluCylinder(tube, 1, 0.2, 8, 20, 10)  # Base radius, top radius, height, 20 slices and stacks
    glPopMatrix()

# function to draw the car, including the body and wheels
def drawCar(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)

    # car body dimensions
    #   needed to properly offset other components
    width = 6
    height = 1
    length = 8

    # body
    drawRect(width, height, length) 
    
    # spoiler
    glPushMatrix()
    glTranslatef(0, height, -2.5)
    drawRect(width, height, 1) 
    glPopMatrix()

    # adding the wheels
    # left wheels
    drawWheel(-width/2, 0, -(length/2 - WHEEL_RADIUS), -90)
    drawWheel(-width/2, 0, (length/2 - WHEEL_RADIUS), -90)

    # right wheels
    drawWheel(width/2, 0, -(length/2 - WHEEL_RADIUS), 90)
    drawWheel(width/2, 0, (length/2 - WHEEL_RADIUS), 90)

    glPopMatrix()

# function to draw a rotating wheel of the car
def drawWheel(x, y, z, rotation):
    glPushMatrix()

    # Move the wheel to the desired location
    glTranslatef(x, y, z)
    # Rotate the wheel about the Y-axis so it is facing the proper way
    glRotatef(rotation, 0, 1, 0)

    # Rotate the wheel about the Z-axis to mimic the wheel spinning
    # Note: since the wheels on the left are rotated with a negative angle,
    #   they will spin the opposite way normally (for example, moving 
    #   clockwise instead of counterclockwise). To correct this, the spin 
    #   angle is changed to its opposite value.
    if rotation < 0:
        glRotatef(-spinAngle, 0, 0, 1)
    else:
        glRotatef(spinAngle, 0, 0, 1)
    
    # The inputs for gluCylinder are:
    #   Quadric shape, radius of cylinder at base, radius of cylinder at top, 
    #   height, number of sides along circumference, number of slices with lines
    gluCylinder(tube, WHEEL_RADIUS, WHEEL_RADIUS, 0.5, 10, 4)

    glPopMatrix()
    pass

# utility function to draw a grid / plane
def drawGrid(size, steps):
    glBegin(GL_LINES)
    glColor3f(0.5, 0.5, 0.5) 
    for i in range(-size, size+1, steps):
        glVertex3f(i, 0, -size)
        glVertex3f(i, 0, size)
        glVertex3f(-size, 0, i)
        glVertex3f(size, 0, i)
    glEnd() 

# utility method to draw a rectangular prism
def drawRect(w, h, l):
    glPushMatrix()
    # note: "front" = side toward initial camera
    # top
    glBegin(GL_LINE_LOOP)
    glVertex3f(-w/2, h/2, -l/2) # front left
    glVertex3f(w/2, h/2, -l/2) # front right
    glVertex3f(w/2, h/2, l/2) # back right
    glVertex3f(-w/2, h/2, l/2) # back left
    glEnd()
    # bottom
    glBegin(GL_LINE_LOOP)
    glVertex3f(-w/2, -h/2, -l/2) # front left
    glVertex3f(w/2, -h/2, -l/2) # front right
    glVertex3f(w/2, -h/2, l/2) # back right
    glVertex3f(-w/2, -h/2, l/2) # back left
    glEnd()
    # connectors
    glBegin(GL_LINES)
    # front left
    glVertex3f(-w/2, h/2, -l/2)
    glVertex3f(-w/2, -h/2, -l/2)
    # front right
    glVertex3f(w/2, h/2, -l/2)
    glVertex3f(w/2, -h/2, -l/2)
    # back right
    glVertex3f(w/2, h/2, l/2)
    glVertex3f(w/2, -h/2, l/2)
    # back left
    glVertex3f(-w/2, h/2, l/2)
    glVertex3f(-w/2, -h/2, l/2)
    glEnd()

    glPopMatrix()

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
