#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

#change to the home directory of the executing user
cd /home/pi

# clone the github repo to the home directory of the executing user
git clone https://github.com/Squeesyy/ToonieBox

# write current crontab to temporary file
crontab -l > tempcrontab

# add new crontask to the end of the file
echo "00 09 * * * bash /home/pi/TooonieBox/ToonieBox/update.sh" >> tempcrontab

# install new crontab
crontab tempcrontab

# remove temporary file
rm tempcrontab


# change to the services directory
cd /lib/systemd/system

# Add the service file

sudo echo "[Unit]
Description=The TooonieBox service
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/ToonieBox/main.py

[Install]
WantedBy=multi-user.target" > tooniebox.service

sudo apt-get install python3-rpi.gpio -y

python3 -m pip install -U pygame

sudo apt-get install git -y

sudo reboot
