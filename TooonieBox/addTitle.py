import os
import RPi.GPIO as GPIO
import MFRC522
import signal
import time

os.system('sudo service tooniebox stop')
print('In case you did not already do that, please move the new audio file to the \'Musik\' directory, otherwise you will have to manually upload it to the GitHub repo.')
input('Press Enter to continue...')
filename = input('Please enter the filename in the correct case and with its file extension: ')
print('You must now bring the chip near the RFID reader. You have one miute to do so.')

songlist = {}

# This 'with open' handles opening and closing the file for us
with open('songs.json') as song_json:
    songliststrings = json.load(song_json)

for key in songliststrings.keys():
    songlist[int(key)] = songliststrings[key]
del songliststrings

card_removed = False

# Add error tolerance to the code and avoid stuttering playback
card_removed_counter = 5


def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()


signal.signal(signal.SIGINT, end_read)


MIFAREReader = MFRC522.MFRC522()


# This loop keeps checking for chips for one minute. If one is near it will get the UID and authenticate
# 1 minute from now
timeout = time.time() + 60




while True:
    if(time.time() > timeout):
        print('You did not bring a working chip near the reader. This either means that your chip is broken, or it is not supported by the reader.')
        break
    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Get the UID of the card
    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        bsUID = uid[0] << 24 + uid[1] << 16 + uid[2] << 8 + uid[3] << 0
        print("Card read UID: %s" % bsUID)

        # Es wird geguckt ob die gelesene ID dieselbe Zahlenfolge wie ein Listeneintrag hat.
        # Wenn nicht, fahre fort.
        if bsUID not in songlist:
            songlist[bsUID] = filename
            with open('songs.json', 'w') as song_json:
                json.dump(songlist, song_json)
            message = 'Added file %s and associated it with the Chip UID %s' % (filename, bsUID)
            os.system('git add Musik/%s' % filename)
            os.system('git commit -m \'%s\'' message)

        else:
            print("This tag is already used in the songs file!")