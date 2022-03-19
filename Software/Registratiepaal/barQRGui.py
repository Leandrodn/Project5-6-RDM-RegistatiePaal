#Copyright 2022 - Project Group: 'Help de RDM werkplaatsen met een registratiesysteem'
#Working 04-02-2022 with Python 3.9.2 on Raspberry Pi 3b

from guizero import App, Text, Window, Picture, Box
from pynput.keyboard import Listener, Key
import threading
from gpiozero import Buzzer
from time import sleep
import requests as rq

# ===============================================

#    Workshops:
#    0 = Aqualab
#    1 = Elektrolab
#    2 = Energielab
#    3 = Houtwerkplaats
#    4 = Lijmlab
#    5 = Materialenlab
#    6 = Metaalwerkplaats
#    7 = Mobiliteitslab
#    8 = Protolab

#Change to a number from workshoplist above:
workshopNumber = 6

# ===============================================

workshopList = ["Aqualab", "Elektrolab", "Energielab", "Houtwerkplaats", "Lijmlab", "Materialenlab", "Metaalwerkplaats", "Mobiliteitslab", "Protolab"]
articleList = ["de", "het"]

workshop = workshopList [workshopNumber]

articleGUIText = ""
if (workshop == workshopList [3] or workshop == workshopList [6]):
    articleGUIText = articleList [0]
else: 
    articleGUIText = articleList [1] 

# ===============================================

app = App (title="RegistratiePaalGUI", width=800, height=480)
app.set_full_screen ()
text = Text (app, "\n")
pictureBox = Box (app)
hrlogo = Picture (pictureBox, image="LogoRDM.png", width=750, height=150)
Text (app, "\nWelkom bij {} {}\n\nLeg een van deze codes op het plankje:\n- QR-Code uit HR-app\n- Barcode op HR-pas  ".format (articleGUIText, workshop), size=30)

windowSuccess = Window (app, title="Success", visible=False, width=800, height=480)
windowSuccess.set_full_screen ()
Text (windowSuccess, "\n")
Picture (windowSuccess, image="vinkje.png", width=400, height=400)

windowFailed = Window (app, title="Failed", visible=False, width=800, height=480)
windowFailed.set_full_screen ()
Text (windowFailed, "\n")
Picture (windowFailed, image="kruis.png", width=400, height=400)

windowConnError = Window (app, title="Connection Error", visible=False, width=800, height=480)
windowConnError.set_full_screen ()
Text (windowConnError, "\n\nEr kan geen connectie worden gemaakt\nmet het internet of de API.\n\nControleer de internetaansluiting en\nraadpleeg anders een medewerker.\n\nProbeer het later opnieuw.", size=30)

windowAPI400 = Window (app, title="API 400 Status Code", visible=False, width=800, height=480)
windowAPI400.set_full_screen ()
Text (windowAPI400, "\n\nHTTP 400: Bad Request\n\nProbeer het later opnieuw.", size=30)

windowAPI401 = Window (app, title="API 401 Status Code", visible=False, width=800, height=480)
windowAPI401.set_full_screen ()
Text (windowAPI401, "\n\nHTTP 401: Student niet geregistreerd\n\nNeem contact op met de administratie.", size=30)

windowAPI404 = Window (app, title="API 404 Status Code", visible=False, width=800, height=480)
windowAPI404.set_full_screen ()
Text (windowAPI404, "\n\nHTTP 404\n\nDe opgevraagde pagina kan niet\nworden geladen.\n\nProbeer het later opnieuw.", size=30)

windowAPI500 = Window (app, title="API 500 Status Code", visible=False, width=800, height=480)
windowAPI500.set_full_screen ()
Text (windowAPI500, "\n\nHTTP 500: Internal Server Error\n\nProbeer het later opnieuw.", size=30)

listen = True
def open_window (currentWindow, windowType):
    global listen
    listen = False
    currentWindow.show (wait=True)
    
    if (windowType == "failed"):
        threadBuzzInvalid ()
    elif (windowType == "success"):
        threadBuzzValid ()
        
    currentWindow.after (2000, lambda: close_window (currentWindow))

def open_window_error (currentWindow):
    global listen
    listen = False
    currentWindow.show (wait=True)
    threadBuzzInvalid ()
    currentWindow.after (10000, lambda: close_window (currentWindow))
    
def close_window (currentWindow):
    global listen
    currentWindow.hide ()
    listen = True

# ===============================================

buzzer = Buzzer (12) #GPIO Pin 12 Raspberry Pi

def buzzValid ():
    buzzer.value = 1
    sleep (0.6)
    buzzer.value = 0

timeX = 0.2
def buzzInvalid ():
    buzzer.value = 1
    sleep (timeX)
    buzzer.value = 0
    sleep (timeX)
    buzzer.value = 1
    sleep (timeX)
    buzzer.value = 0
    sleep (timeX)
    buzzer.value = 1
    sleep (timeX)
    buzzer.value = 0

def threadBuzzValid ():
    buzzerThread = threading.Thread (target = buzzValid ())
    buzzerThread.start ()
    
def threadBuzzInvalid ():
    buzzerThread = threading.Thread (target = buzzInvalid ())
    buzzerThread.start ()

# ===============================================

studentNumList = list ()

def listToString (inputList): 
    returnString = "" 
    return (returnString.join (inputList))

# ===============================================

def on_press (key):
    if not listen:
        pass
    elif key == Key.enter:
        if not studentNumList:
            open_window (windowFailed, "failed")    
        else:   
            codeType = studentNumList.pop (0)

            if codeType == 'b' or codeType == 'B': 
                print ("CodeType: Barcode (Code 39)")
                codeType = "Barcode"
            elif codeType == 'Q' or codeType == 'q':
                print ("CodeType: QR-Code")
                codeType = "QR-code"

            studentNumString = listToString (studentNumList)
            print ("StudentNumString:", studentNumString)
            studentNumList.clear ()
            
            if studentNumString.isnumeric () and len (studentNumString) == 7: #studentNumString is correct format (studentnumber from HR)
                try:
                    url = 'http://81.169.254.222/register'
                    
                    jsonData = {
                                'stnum' : studentNumString,
                                'method' : codeType,
                                'workshop' : workshop
                                }
                    
                    postReq = rq.post (url, json = jsonData)
                    print ("Status Code:", postReq.status_code)
                    
                    if postReq.status_code == 201: #success
                        open_window (windowSuccess, "success")
                    elif postReq.status_code == 400:
                        open_window_error (windowAPI400)
                    elif postReq.status_code == 401:
                        open_window_error (windowAPI401) 
                    elif postReq.status_code == 404:
                        open_window_error (windowAPI404)
                    elif postReq.status_code == 500:
                        open_window_error (windowAPI500)
                    
                except:
                    open_window_error (windowConnError)
                
            else:
                #failed
                print ("Failed\n")
                open_window (windowFailed, "failed")
                
        print ()
        sleep (1) #delay between scans

    elif hasattr (key, 'char'):
        studentNumList.append (key.char)

# ===============================================

listener = Listener (on_press = on_press)
listener.start ()

# ===============================================

app.display()
