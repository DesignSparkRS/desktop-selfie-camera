#!/usr/bin/python
import os
import time
import pygame
from picamera import PiCamera
from sense_hat import SenseHat

# Setup Pygame (for display)

pygame.init()
screen = pygame.display.set_mode([800,480])

# Setup the Pi Camera

camera = PiCamera()
camera.resolution = (800, 480)
camera.hflip = True

# Setup the SenseHAT

sense = SenseHat()
sense.set_rotation(0)

# Function to display an image

def displayImage(file):
    image = pygame.image.load(file)
    imagerect = image.get_rect()

    screen.fill([0, 0, 0])
    screen.blit(image, imagerect)
    pygame.display.flip()

# Function to take a selfie

def getSelfie():
    # Start camera video preview 
    camera.start_preview()

    # Commence countdown
    sense.show_letter("3", text_colour=[255, 0, 0])
    time.sleep(1)
    sense.show_letter("2", text_colour=[255, 255, 0])
    time.sleep(1)
    sense.show_letter("1", text_colour=[0, 255, 0])
    time.sleep(1)
    sense.show_letter("0", text_colour=[0, 0, 255])

    # Capture image and stop preview
    filename = time.strftime("/selfies/%Y-%m-%d-%H-%M-%S.jpg")
    camera.capture(filename)
    camera.stop_preview()

    # Display image and clear SenseHAT display
    displayImage(filename)
    sense.clear()

# Display welcome image
displayImage("/usr/local/share/images/Welcome.png")

# Main loop

while True:
    # Wait for and process joystick events
    event = sense.stick.wait_for_event(emptybuffer=True)
    if event.direction == "middle" and event.action == "released":
        getSelfie()
    elif event.direction == "left" and event.action == "held":
        os.system("/sbin/shutdown -h now")
    else:
        pass
