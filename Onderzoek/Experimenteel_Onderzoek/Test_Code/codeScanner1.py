# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
from time import sleep, time
import cv2
from gpiozero import Buzzer, LED, PWMOutputDevice
from threading import Thread

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser ()
ap.add_argument ("-o", "--output", type=str, default="barcodes.csv",
    help="path to output CSV file containing barcodes")
args = vars (ap.parse_args())

# initialize the video stream and allow the camera sensor to warm up
print ("[INFO] starting video stream...")
# vs = VideoStream(src=0).start()
vs = VideoStream (usePiCamera=True).start ()
sleep(2.0)

# open the output CSV file for writing and initialize the set of
# barcodes found thus far
csv = open (args["output"], "w")
found = set ()

#buzzer and LED shiz
buzzer = Buzzer (12)
led = LED (14)

timeOn = 0.5
timeOff = 1

def buzzAndLed():
    buzzer.toggle ()
    led.toggle ()
    sleep (timeOn)
    buzzer.toggle ()
    led.toggle ()

# loop over the frames from the video stream
scanCount = 0
startTime = time ()
deltaTime = 0
while True:
    # grab the frame from the threaded video stream and resize it to
    # have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    
    # find the barcodes in the frame and decode each of the barcodes
    code = pyzbar.decode(frame) #barcodes = list
    
    if code: #barcode is true if list has an item
        thread1 = Thread(target = buzzAndLed)
        thread1.start ()
        
        codeData = code[0].data.decode ("utf-8")
        codeType = code[0].type
        
        # print text in shell
        text = "{} ({})".format (codeData, codeType)
        print (text)
        scanCount += 1
        if (scanCount >= 101):
            deltaTime = time () - startTime
            break
        print ("Scan Count:", scanCount)
        
        # if the barcode text is currently not in our CSV file, write
        # the timestamp + barcode to disk and update the set
        if codeData or codeType not in found:
            csv.write("{}, {}, {}\n".format (datetime.datetime.now (),
                codeData,
                codeType))
            csv.flush ()
            found.add (codeData)
            
        #sleep (timeOff)    

    # show the output frame
    cv2.imshow ("Code Scanner", frame)
    key = cv2.waitKey (1) & 0xFF
 
    # if the `q` key was pressed, break from the loop
    if key == ord ("q"):
        break
    
# close the output CSV file do a bit of cleanup
print ("Delta Time:", deltaTime)
print ("[INFO] cleaning up...")
csv.close ()
cv2.destroyAllWindows ()
vs.stop ()
