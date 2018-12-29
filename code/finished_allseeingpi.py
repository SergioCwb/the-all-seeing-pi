from picamera import PiCamera
from gpiozero import Button
from overlay_functions import *
from time import gmtime, strftime
from guizero import App, PushButton, Text, Picture
from twython import Twython
import time
import sys
"""
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
"""

def btn_left():
    global preview_active
    if (preview_active):
        next_overlay()
    else:
        new_picture()
    
def btn_right():
    global preview_active
    if (preview_active):
        take_picture()
    else:
        new_picture()
        preview_active = True    

# Tell the next overlay button what to do
def next_overlay():
    global overlay
    global preview_active
    overlay = next(all_overlays)
    preview_overlay(camera, overlay)

# Tell the take picture button what to do
def take_picture():
    global output
    global preview_active
    output = strftime("/home/pi/allseeingpi/image-%d-%m_%H:%M:%s.png", gmtime())
    time.sleep(3)
    camera.capture(output)
    camera.stop_preview()
    remove_overlays(camera)
    output_overlay(output, overlay)

    # Save a smaller gif
    size = 800, 600
    gif_img = Image.open(output)
    gif_img.thumbnail(size, Image.ANTIALIAS)
    gif_img.save(latest_photo, 'gif')

    # Set the gui picture to this picture
    your_pic.set(latest_photo)
    
    # Reset the buttons
    preview_active = False


def new_picture():
    global preview_active
    remove_overlays(camera)
    camera.start_preview()
    preview_overlay(camera, overlay)
    preview_active = True

def send_tweet():
    twitter = Twython(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )

    # Send the tweet
    message = "The All Seeing Pi saw you!"
    with open(output, 'rb') as photo:
        twitter.update_status_with_media(status=message, media=photo)

def getOut():
    sys.exit()

# Set up buttons
next_overlay_btn = Button(23)
next_overlay_btn.when_pressed = btn_left #next_overlay
take_pic_btn = Button(25)
take_pic_btn.when_pressed = btn_right #take_picture

# Set up camera (with resolution of the touchscreen)
camera = PiCamera()
camera.resolution = (800, 600) # 800, 480
camera.hflip = True

# Start camera preview
camera.start_preview()

# Enable external buttons functions
preview_active = True

# Set up filename
output = ""

latest_photo = '/home/pi/allseeingpi/latest.gif'

app = App("@CabineDeFotos on Twitter!", 1024, 800)
# app.tk.attributes("-fullscreen", True)
message = Text(app, "The All Seeing Pi saw you!")
your_pic = Picture(app, latest_photo)
new_pic = PushButton(app, new_picture, text="New Picture")
# tweet_pic = PushButton(app, send_tweet, text="Tweet picture")
getOut = PushButton(app, getOut, text="Quit")
app.display()
