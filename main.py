import RPi.GPIO as GPIO
import MFRC522
import signal
import pygame
import time
import json
# Here, we use a dictionary which allows us to do a one-direction lookup, where we use uidlist[<identifier>] to get the value assigned to <identifier>
# We open the JSON file that this is stored in, and parse it into a dictionary. Same goes for the timestamplist.
# Unfortunately, our function to store the json data converts all keys to Strings, and I don't want to write a custom JSON decoder.
# So I simply iterate through the list, convert everything and store it in a second list. It is not elegant, but it works reliably.

songlist = {}
timestamplist = {}

# This 'with open' handles opening and closing the file for us
with open('/root/TooonieBox/ToonieBox/songs.json') as song_json:
    songliststrings = json.load(song_json)

for key in songliststrings.keys():
    songlist[int(key)] = songliststrings[key]
del songliststrings


# This code will avoid problems when our timestamp JSON doesn't exist yet.
try:
    timestamp_json = open('/root/TooonieBox/ToonieBox/timestamps.json')
    timestampliststrings = json.load(timestamp_json)

    for key in timestampliststrings.keys():
        timestamplist[int(key)] = float(timestampliststrings[key])
    del timestampliststrings
except IOError:
    print('File not existent!')
finally:
    timestamp_json.close()



# This takes our songlist and adds a timestamp for UIDs which are in the songlist, but not in the timestampList (which must mean that they were newly added)
for key in list(songlist.keys()):
    if key not in timestamplist:
        timestamplist[key] = 0

paused = True
pygame.mixer.init()

continue_reading = True
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


# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Get the UID of the card
    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        pygame.mixer.music.pause()
        paused = True
        card_removed = False

        # Print UID
        # Because we are using a Dictionary, 
        # we can skip iterating through the list and instead just use the dictionary as a lookup table

        print(len(songlist))

        # Here, we "squish" the received bytes which are treated as ints here into one big long number.
        # This is done by using "binary shift". Essentially, we put the binary numbers in a long row and add them up.
        # Because converting them to a string and conatenating that string takes a lot of time and resources, we use binary shift.
        # There, we simply shift our binary number to the left (essentially adding zeros on the right), and add them up, which results in one large number.
        # All of this is then stored in the variable bsUID (BitShifted UID)

        bsUID = uid[0] << 24 + uid[1] << 16 + uid[2] << 8 + uid[3] << 0
        print("Card read UID: %s" % bsUID)

        # Es wird geguckt ob die gelesene ID dieselbe Zahlenfolge, wie ein Listeneintrag hat
        if bsUID in songlist:
            pygame.mixer.music.load('root/TooonieBox/TooonieBox/Musik/%s' % songlist[bsUID])
            pygame.mixer.music.set_volume(0.1)  # setzten der Lautstärke

            # abspielend es Liedes mit ZEitpunkt, welher in timestampliste eingetragen ins
            pygame.mixer.music.play(0, timestamplist[bsUID])
            paused = False
            print("unpausiert")
            while not card_removed:  # check ob RFID-Chip weg ist

                (status, TagType) = MIFAREReader.MFRC522_Request(
                    MIFAREReader.PICC_REQIDL)

                print(pygame.mixer.music.get_pos())

                if status != MIFAREReader.MI_OK:
                    card_removed_counter -= 1

                    if card_removed_counter == 0:
                        card_removed = True

                        if pygame.mixer.music.get_pos() != -1:
                            timestamplist[bsUID] += pygame.mixer.music.get_pos() / 1000
                            # timestamp wird gesetzt
                        else:
                            # wichtige Ausnahme!!! pos wird -1 wenn lied vorbei ist
                            timestamplist[bsUID] = 0
                        # print timestamp[0]
                        pygame.mixer.music.pause()
                        paused = True
                        with open('timestamps.json', 'w') as timestamp_json:
                            json.dump(timestamplist, timestamp_json)
                else:
                    card_removed_counter = 5
        else:
            #brug = timestamp[i+1]
            # kein passende ID in der Liste gefunden
            print("keine id gefunden")
