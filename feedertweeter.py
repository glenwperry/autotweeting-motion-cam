#!/usr/bin/python
# coding=utf-8

#
# Feeder Tweeter (http://feedertweeter.net/)
# Copyright Manifold 2013+. All rights reserved.
# Author Chad Auld (cauld@wearemanifold.com)
# Licensed under the BSD License.
# https://bitbucket.org/cauld/feedertweeter/
#

'''
feedertweeter.py: 
This script watches for new bird pictures to be captured and 
then posts them to Twitter.
'''

import os
import time
from random import choice
from twython import Twython
from fsmonitor import FSMonitor

# Camera captures directory
CAMERA_CAPTURES_DIR = "/home/pi/picam/"

# A variety of possible post message so we don't always repeat the same thing
POST_MESSAGES = ["Me a TV star? I've got to be the luckiest guy in the world.",
                 "I want to be the poster boy to get your damn blood pressure checked",
                 "I knew when I grew up, I always wanted to be a liar.", 
                 "But Norman came out and you know what he did? He killed the guy with a hammer",
                 "Most people don't know that I am an accomplished dramatic actor.",
                 "Apparently you can see my scrotum for a split second on episode 161",
                 "Municipalities invariably take over resonsibility for their web sites once the web sites become larger",
                 "If you're in television, you're lying because you're just pretending to be yourself...",
                 "I've performed in several Shakespeare productions, including Hamlet.",
                 "Hamlet lives in an apartment with two women and has to pretend he's gay.",
                 "If I ever won the Nobel Prize they'd be playing the theme song from Three's Company.",
                 "The Harvey Lembeck Workshop was for me a support group. A place where I had the freedom to fall on my face.",
                 "Someone asked me if I did that on purpose. You bet I did.",
                 "In order for the township web site to work, people have to view it as a resource.",
                 "By getting the information available on the Township website, people will be able to participate.",
                 "You can't, in good conscience, ask volunteers to quickly do a major web site overhaul."]

# Get Twitter keys from the supervisord env(you've gone direct into the keys here, change for security reasons before public release)
APP_KEY = "YOUR APP KEY"
APP_SECRET = "YOUR APP SECRET"
OAUTH_TOKEN = 	"YOUR OAUTH TOKEN"
OAUTH_TOKEN_SECRET = "YOUR OAUTH TOKEN SECRET"

t = Twython("AYOUR PP KEY", "YOUR APP SECRET", "YOUR OAUTH TOKEN", "YOUR OAUTH TOKEN SECRET")

# Used to post status updates with bird images as new images are detected
def postNewMessage(fileName):
    print "Uploading new post with image..."
    fullFilePath = CAMERA_CAPTURES_DIR + fileName
    
    # Grab a random post message
    postmsg = choice(POST_MESSAGES)
    
    try:
        photo = photo = open(fullFilePath, 'rb')
        t.update_status_with_media(status=postmsg, media=photo)
    except Exception,msg:
        print msg

    # Once the image has been posted we can remove it (twitter is the archive)
    print "Post created, removing local image..."
    os.remove(fullFilePath)

######## MAIN #########

# Images are captured and placed in the "captures" directory as the 
# camera.py script detects movement.  We monitor the "captures" 
# directory for new files and process when detected.
m = FSMonitor()
watch = m.add_dir_watch(CAMERA_CAPTURES_DIR)

while True:
    for evt in m.read_events():
        # The FSMonitor evt.action_name we care about is "move to" (the file 
        # is created in another dir and moved as a whole)
        # Note: the evt.name will be the name of the new file
        if evt.action_name == 'move to':
            time.sleep(10) # Let the full file be written before continuing...
            postNewMessage(evt.name)
