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