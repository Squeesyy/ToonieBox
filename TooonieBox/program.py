import RPi.GPIO as GPIO
import MFRC522
import signal
import pygame
import time
import json
# Here, we use a dictionary which allows us to do a one-direction lookup, where we use uidlist[<identifier>] to get the value assigned to <identifier>
songlist = {168198678 : 'Freinds.mp3', 735411228 : 'Happier.mp3', 2282027179 : 'HereWithMe.mp3', 67311618 : 'HereWithMe.mp3'}    # UID der RIFD-Chips
#@TODO: Add a function to load the timestamps from a file!
timestamplist = {}

#This takes our songlist and adds a timestamp for UIDs which are in the songlist, but not in the timestampList (which must mean that they were newly added)
for key in list(songlist.keys()):
    if key not in timestamplist:
        timestamplist[key] = 0
timestamp = [0] *99     # Stopppositionen der Lieder 

brug = ""
paused = True
lastDetected = ""
pygame.mixer.init()
#pygame.mixer.music.load("/home/pi/Freinds.mp3")

#pygame.mixer.music.set_volume(0.1)
#pygame.mixer.music.play()1
#pygame.mixer.music.pause()
#paused = True
#pygame.mixer.music.pause()
#pygame.mixer.music.stop()


continue_reading = True
card_removed = False
card_removed_counter = 5


def end_read(signal,frame):          #end nachricht nachAbbruch
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()


signal.signal(signal.SIGINT, end_read)


MIFAREReader = MFRC522.MFRC522()



# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
        
        # Scan for cards   
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        
  
   
    
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        pygame.mixer.music.pause()
        paused = True
        card_removed = False
        # Print UID
        # Because we are using a Dictionary, we can skip iterating through the list.
        #for i in range(0,len(uidlist)):
        
        print(len(songlist))
        brug = songlist[i]

        # Here, we "squish" the received bytes which are treated as ints here into one big long number.
        # This is done by using "binary shift". Essentially, we put the binary numbers in a long row and add them up.
        # Because converting them to a string and conatenating that string takes a lot of time and resources, we use binary shift.
        # There, we simply shift our binary number to the left (essentially adding zeros on the right), and add them up, which results in one large number.
        # All of this is then stored in the variable bsUID (BitShifted UID)
        bsUID = uid[0] << 24 + uid[1] << 16 + uid[2] << 8 + uid[3] << 0
        print("Card read UID: %s" % bsUID)

        #Es wird geguckt ob die gelesene ID dieselbe Zahlenfolge, wie ein Listeneintrag hat
        if  bsUID in uid:
            pygame.mixer.music.load(songlist[bsUID]) # wenn gefunden dann wir aus dem listeneintrag die letzte Zahl genommen und nach der URl in dem Musikverzeichnis geguckt
            pygame.mixer.music.set_volume(0.1) # setzten der Lautstärke
            
            
            pygame.mixer.music.play(0,timestamplist[bsUID]) # abspielend es Liedes mit ZEitpunkt, welher in timestamplsite eingetragen ins
            paused = False
            print("unpausiert")
            while not card_removed: #check ob RFID-Chip weg ist

                (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

                print(pygame.mixer.music.get_pos())

                if status != MIFAREReader.MI_OK:
                    card_removed_counter -= 1

                    if card_removed_counter == 0:
                        card_removed = True

                        if pygame.mixer.music.get_pos() != -1:
                            timestamplist[bsUID] += (pygame.mixer.music.get_pos() / 1000)
                            #timestamp wird gesetzt
                        else:
                            timestamplist[bsUID] = 0 # wichtige Ausnahme!!! pos wird -1 wenn lied vorbei ist
                        #print timestamp[0]
                        pygame.mixer.music.pause()
                        paused = True
                else:
                    card_removed_counter = 5
        else:
            #brug = timestamp[i+1]
            print("keine id gefunden") # kein passende ID in der Liste gefunden
                
            
            
    
        # This is the default key for authentication
           # key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
            #MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
            #status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
           # if status == MIFAREReader.MI_OK:
            #    MIFAREReader.MFRC522_Read(8)
             #   MIFAREReader.MFRC522_StopCrypto1()
           # else:
           #     print "Authentication error"