#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

#change to the home directory of the executing user
cd ~

# clone the github repo to the home directory of the executing user
git clone https://github.com/Squeesyy/TooonieBox

# write current crontab to temporary file
crontab -l > tempcrontab

# add new crontask to the end of the file
echo "00 09 * * * bash ~/TooonieBox/update.sh" >> tempcrontab

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
ExecStart=/usr/bin/python3 /home/TooonieBox/program.py

[Install]
WantedBy=multi-user.target" > TooonieBox.service

sudo apt install python3-rpi.gpio 

python3 -m pip install -U pygame