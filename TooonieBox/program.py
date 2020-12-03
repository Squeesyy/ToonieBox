import RPi.GPIO as GPIO
import MFRC522
import signal
import pygame
import time
uidlist = []    # UID der RIFD-Chips
uidlist.append('10,6,130,22;0')   
uidlist.append('43,213,124,28;1')
uidlist.append('136,4,248,171;2')
uidlist.append('4,3,24,2;3')
timestamp = [0] *99     # Stopppositionen der Lieder 
urllist = []
urllist.append("/home/pi/TooonieBox/Musik/Freinds.mp3") #Verzeichnis Lieder
urllist.append("/home/pi/TooonieBox/Musik/Happier.mp3")
urllist.append("/home/pi/TooonieBox/Musik/HereWithMe.mp3")

    

brug = ""
brug = uidlist[0]
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
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()


signal.signal(signal.SIGINT, end_read)


MIFAREReader = MFRC522.MFRC522()



# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
        
        #print(brug)
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
        for i in range(0,len(uidlist)):     
            print len(uidlist)
            brug = uidlist[i]
            print "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])
            print("hall")  #Es wird geguckt ob die gelesene ID dieselbe Zahlenfolge, wie ein Listeneintrag hat
            if  uid[0] == int( brug[0:brug.find(',')]) and uid[1] == int( brug[brug.find(',') +1:brug.find(',',brug.find(',') +1)]) and uid[2] == int( brug[brug.find(',',brug.find(',')+1)+1:brug.find(',',brug.find(',',brug.find(',')+1) +1)]) and uid[3] == int( brug[brug.find(',',brug.find(',',brug.find(',')+1)+1)+1:brug.find(';')] ) and paused == True :
                pygame.mixer.music.load(urllist[int(brug[brug.find(';')+1:])]) # wenn gefunden dann wir aus dem listeneintrag die letzte Zahl genommen und nach der URl in dem Musikverzeichnis geguckt
                pygame.mixer.music.set_volume(0.1) # setzten der Lautstärke
                
               
                pygame.mixer.music.play(0,timestamp[int(brug[brug.find(';')+1:])]) # abspielend es Liedes mit ZEitpunkt, welher in timestamplsite eingetragen ins
                paused = False
                print "unpausert"
                while not card_removed: #check ob RFID-Chip weg ist
                   (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                   print pygame.mixer.music.get_pos()
                   if status != MIFAREReader.MI_OK:
                       card_removed_counter = card_removed_counter-1
                       if card_removed_counter==0:
                          card_removed = True
                          if pygame.mixer.music.get_pos() != -1:
                              timestamp.insert(int(brug[brug.find(';')+1:]), pygame.mixer.music.get_pos()/1000 + timestamp[int(brug[brug.find(';')+1:])]) #timestamp wird gesetzt
                          else:
                              timestamp.insert(int(brug[brug.find(';')+1:]), 0) # wichtige Ausnahme!!! pos wird -1 wenn lied vorbei ist
                          #print timestamp[0]
                          pygame.mixer.music.pause()
                          paused = True
                   else:
                       card_removed_counter = 5
            else:
                #brug = timestamp[i+1]
                print "hi" # kein passende ID in der Liste gefunden
                
            
            
    
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
    
  
        

#pygame.mixer.music.pause()
