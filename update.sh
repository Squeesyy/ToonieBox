#!/bin/bash
# change into the Tooniebox directory. This should not be necessary and is just a failsafe
cd /home/pi/ToonieBox

# use git to get the updates from the repo, if present.
git pull --no-commit
