#!/bin/bash
# change into the Tooniebox directory. This should not be necessary and is just a failsafe
cd /home/Pi/ToonieBox

# use git to get the updates from the repo, if present.
git pull --no-commit

sudo apt update

sudo apt full-upgrade
