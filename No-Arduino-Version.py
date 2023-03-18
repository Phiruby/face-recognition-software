#-----------------------------------------------------------------------------
# Name:        Safety First!
# Purpose:     If you are to leave your place unprotected, this program will keep an eye out and 
#              email you if a stranger enters the room
#
# Author:      Veebes
# Created:     04-May-2022
# Updated:     01-June-2022
#-----------------------------------------------------------------------------
#

import time
import cv2
import face_recognition as fr 
import pygame
import os 
import pickle 
import smtplib
import keyboard
import pyperclip

def readFile(fileName):
  '''
    Reads data from a file 
  
      Parameters
      ----------
      fileName: string
        The name of the file you want to read from

      Returns
      -------
      Any (data recieved from the file)
  '''
  reader=open(fileName,'rb')
  data=pickle.load(reader)
  reader.close()
  return data 

def writeFile(fileName,data):
  '''
    Writes data into a file 
  
      Parameters
      ----------
      fileName: string
        The name of the file you want to write to

      data: any
        The data you are writing to the file

      Returns
      -------
      None
  '''
  createFile=open(fileName,'wb')
  pickle.dump(data,createFile)
  createFile.close()


def sendMail(sender,passw,reciever,subject,msg):
    from email.mime.text import MIMEText
    '''
    sends mail to the reciprient 
  
      Parameters
      ----------
      sender: string 
        The email you want to send with

      passw: string
        The sender email password

      reciever: string
        The reciever's email id

       msg: string
        The mail text content
    

      Returns
      -------
      None
    '''

    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(sender,passw)
    server.sendmail(sender,reciever,msg)
    print('Mail sent')

def trajectoryCheck(path):
    '''
    Checks whether a path exists
  
      Parameters
      ----------

      path: string
        The path for a folder
      
      Returns
      -------
      Boolean 
    '''
    for root,dir,files in os.walk(path):

        return True

    return False 


def findFile(name,path):
    '''
    Finds whether a specific file exists
  
      Parameters
      ----------
      name: string
        The file name

      path: string
        The trajectory where you want to look for the file
      
      Returns
      -------
      Boolean 
    '''
    for root,dir,files in os.walk(path):
        if name in files:
            return True 
    return False

class setupScreen():

    pygame.init()

    def __init__(self,pos,width,height,imgPath):
        '''
    Initialize the class
  
      Parameters
      ----------
      pos: array
        The x and y coordinates

      width: int
        The width of the object

      height: int
        The height of the object

      imgPath: string
        The image path of the object, if it is an image
      
      Returns
      -------
      None
        '''

        self.pos=pos
        self.height=height 
        self.width=width 

        self.imgPath=imgPath 

        if self.imgPath!=None: 
            #Load and setup the image if there is an image path
            butImg=pygame.image.load(self.imgPath)
            buttonImage=pygame.transform.flip(butImg,False,False)
            buttonImage=pygame.transform.scale(buttonImage,(self.width,self.height))
            self.image=buttonImage        

    def drawImg(self,surface,text=None,textColor=[255,255,255]):
        '''
    Draws the image
  
      Parameters
      ----------
      surface: method
        The pygame surface to be drawn on

      text: string
        Any text on top of the object

      textColor: string
        The color of the string
      
      Returns
      -------
      None
    '''
       #Draw the text
        surface.blit(self.image,self.pos)
        #Draw text on the object, if it has text 
        if text!=None:

            font=pygame.font.Font(None,int(self.height/2))
            message=font.render(text,True,textColor)
            surface.blit(message,[self.pos[0]+self.width/5,self.pos[1]+self.height/5])
        
    def drawRect(self,surface,colorRect=[113,26,117]):
        '''
    Draws a rectangle
  
      Parameters
      ----------
      surface:method
        The surface to be drawn on

      colorRect: array
        The rgb color of the rectangle
      
      Returns
      -------
      None 
    '''

        pygame.draw.rect(surface,colorRect,[self.pos[0],self.pos[1],self.width,self.height])
    

    def hoverDetect(self,mousePos):
        '''
    Checks if the mouse is hovering over an object
  
      Parameters
      ----------
      mousePos: array
        The x and y coordinate of the mouse
      
      Returns
      -------
      Boolean 
    '''
        #If the mouse is hovering over the object
        if (0<=mousePos[0]-self.pos[0]<=self.width) and (0<=mousePos[1]-self.pos[1]<=self.height):

            if self.imgPath!=None: 
                #Change the image of the object to make it look like something is hovering over it
                butImg=pygame.image.load('Images\\hoverButton.png')
                buttonImage=pygame.transform.flip(butImg,False,False)
                buttonImage=pygame.transform.scale(buttonImage,(self.width,self.height))
                self.image=buttonImage  

            return True 

        else: 

            if self.imgPath!=None:
                #Once the person stops hovering over the button, return to regular image 
                butImg=pygame.image.load('Images\\button.png')
                buttonImage=pygame.transform.flip(butImg,False,False)
                buttonImage=pygame.transform.scale(buttonImage,(self.width,self.height))
                self.image=buttonImage  

            return False 

    def buttonClick(self,mousePos):
        '''
    Checks if the user clicked on an object
  
      Parameters
      ----------
      mousePos: array
        The x and y coordinate of the mouse 
      
      Returns
      -------
      Boolean
    '''
    #If the mouse is hovering over the object, and the button is clicked
        if self.hoverDetect(mousePos) and ev.type==1026:

            return True

        return False 

    def userInput(self,surface,event,baseString,font=pygame.font.Font(None,32)):
        '''
    Allows the user to type things that displays on the screen
  
      Parameters
      ----------
      surface: method
        The surface to draw the text on

      event: method
        The user events (i.e typing, click)
    
      baseString: string
        The string user has typed so far

      font: method
        Pygame font for displayed text
      
      Returns
      -------
      String 
        The new string once the user has completed an action (i.e if I have typed "ea" so far, and type on "e", then it returns "eae")
    '''

        
        if(event.type==pygame.KEYDOWN):

            vEntered= keyboard.is_pressed('v')
            ctrlEntered=keyboard.is_pressed('ctrl')
            bothENtered=False 

            if ctrlEntered: 

              bothENtered= (vEntered==ctrlEntered)

            #If the user clicked backspace, remove the last character of the entered string
            if event.key==pygame.K_BACKSPACE:
                baseString=baseString[:-1]

            #If the user entered a key (not ctrl+v or tab), add that to the string
            elif event.unicode!=' ' and event.key!=pygame.K_TAB and not bothENtered:
                baseString=str(baseString)+str(event.unicode)

            #If the user entered space, add a space in the string
            elif event.unicode==' ' and event.key!=pygame.K_TAB and not bothENtered:
                baseString+=' '

            #Had to use keyboard instead of pygame because pygame can only take in one event at a time
            #If the user pressed ctrl+v, paste whatever is on the clipboard 
            if keyboard.is_pressed('ctrl') and keyboard.is_pressed('v'):
              baseString+=pyperclip.paste()

        #Display the new text on the object location 
        text=font.render(baseString,True,(255,255,255))
        surface.blit(text,self.pos)
        return baseString

    def displayTextos(self,surface,msg,textColor=[255,255,255]):
        '''
    Displays a text object on the screen
  
      Parameters
      ----------
      surface: method
        the surface to draw the text on

      msg: string
        The msg to display on the screen

      textColor: array
        The rgb color of the text
      
      Returns
      -------
      None
    '''
    #Display text on the surface 
        font=pygame.font.Font(None,self.height)
        message=font.render(msg,True,textColor)

        surface.blit(message,self.pos)

#initialize the camera- might have to change the 0 to the camera position

frame=cv2.VideoCapture(0)

#If the user has already entered the settings, the program will not enter settings
if(findFile('facialEncodings',os.getcwd())) and findFile('userMail',os.getcwd()):
    programState="functioning"

else:
    programState="setup"

faceFinder=cv2.CascadeClassifier('haar\haarcascade_frontalface_default.xml')

firstRun=True
mailSent=False

#-----------------------------Setup------------------------------------------------------#
""" Set up the game and run the main game loop """
    # Prepare the pygame module for use
surfaceSize = 800   # Desired physical surface size, in pixels.

clock = pygame.time.Clock()  #Force frame rate to be slower

# Create surface of (width, height), and its window.
mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))

font=pygame.font.Font(None,32)
#-------------------------------Main Screen----------------------#
      
setupState="main screen"

msg2=setupScreen([115,700],50,50,None)
mailUser=setupScreen([115,430],30,50,None)
updateMsg=setupScreen([300,650],50,50,None)

#-----------------------Set up/ Mail Screens-------------------#

inputBut=setupScreen([0,500],800,100,None)
text=setupScreen([25,300],50,40,None)
text2=setupScreen([230,450],50,40,None)
inst=setupScreen([50,100],50,50,None)
inst2=setupScreen([150,200],50,50,None)
errorMsg=setupScreen([115,650],50,50,None)
errorMsg2=setupScreen([115,700],50,50,None)
# invalidPath=False

loadMsg=setupScreen([200,500],30,40,None)
setupObjList=[inst,inst2]
fileObjRectList=[['Enter a path to a folder with your pictures'],
['Press TAB once you are done']]

mailObjList=[['Enter the email you want to be alerted'],
            ['Press TAB once you are done']]

#----------------------Help Screen---------------------#
backBut=setupScreen([500,650],200,100,'Images\\button.png')
extraHelpBut=setupScreen([100,650],200,100,'Images\\button.png')

helpDict={backBut:'  Back', extraHelpBut:'  More'}
newHelpState={'  Back':'main screen', '  More':'folder help'}

helpScreen=pygame.image.load('Images\\helpScreen.png').convert()
rect=helpScreen.get_rect()
helpScreen=pygame.transform.scale(helpScreen,(surfaceSize,surfaceSize))

#------------------------Background setup & Images---------------------#
penguinBack=pygame.image.load('Images\image.jfif').convert()
backgroundRect=penguinBack.get_rect()
penguinBack=pygame.transform.scale(penguinBack,(surfaceSize,surfaceSize))


butPos=[200,100]
path='Images\\button.png'
button=setupScreen(butPos,400,133,path)

mailButton=setupScreen([200,300],400,133,path)

helpButton=setupScreen([200,500],400,133,path)

continueBut=setupScreen([600,20],200,67,path)

mainScreenDict={button:'Enter file',mailButton:'Enter mail',helpButton:'Help Screen'}

negativeBeeps=pygame.mixer.Sound('Sounds\wrong-buzzer-6268.mp3')

#--------Extra Folder Help----------#

folderHelp=pygame.image.load('Images\\folderHelp.png').convert()
folderRect=folderHelp.get_rect()
folderHelp=pygame.transform.scale(folderHelp,(surfaceSize,surfaceSize))

#-------------------------Variable initialization-------------#
mailEntered=False 
folderEntered=False 

progBrok=False
firstRun=True
settingsUpdate=False 

pygame.mixer.init()
pygame.mixer.music.load('Sounds\\heartbeat.wav')
pygame.mixer.music.play()
while True:

    ev = pygame.event.poll()    # Look for any event
    if ev.type == pygame.QUIT:  # Window close button clicked?
        break 

    if(programState=="setup"):
        mousePos=pygame.mouse.get_pos()
        #Fill in the surface 
        mainSurface.fill((0,200,255))
        mainSurface.blit(penguinBack,backgroundRect)

        #---------------------------------------------Main Screen-------------------------------------#

        if(setupState=="main screen"):

            #Initialize the variables during the first run of the setup state

            if(firstRun):
                mailEntered=findFile('userMail',os.getcwd())

                folderEntered=findFile('facialEncodings',os.getcwd())
                userSMail="Current mail: None"
                #If the user has entered a mail, make a string of that mail they entered  
                if mailEntered:
                  userSMail=readFile('userMail')
                  userSMail="Current mail: "+userSMail
                  
                firstRun=False

            base=""
            
            #Draw the buttons
            for object,messagee in mainScreenDict.items():
              #Check if the object is clicked
              if object.buttonClick(mousePos):
                #Change setup state if the object is clicked 
                setupState=messagee.lower()
                firstRun=True  
                settingsUpdate=False 
                
              object.drawImg(mainSurface,messagee)
            #Display user's current mail on the screen 
            mailUser.displayTextos(mainSurface,userSMail)
           
            #Give user the option to continue if they have entered both file 
            if mailEntered and folderEntered:
              continueBut.drawImg(mainSurface,'  Continue')

              #If the button is clicked, change set up state 
              if continueBut.buttonClick(mousePos):
                setupState="shift"
                firstRun=True  
                settingsUpdate=False
           
           #If there was no error loading the foder/file 
            if not progBrok:
                #Prompt the users for the next steps
                if mailEntered and not folderEntered:
                    msg2.displayTextos(mainSurface,'Mail entered! Proceed to enter folder')
                
                elif folderEntered and not mailEntered:
                    msg2.displayTextos(mainSurface,'Folder entered! Proceed to enter mail')
                #If the settings have been updated, display it on the screen 
                if settingsUpdate:
                    updateMsg.displayTextos(mainSurface,'Folder Updated!')

            #Display error message if the program did break
            else: 
                errorMsg.displayTextos(mainSurface,'There was an error loading your folder!')
                errorMsg2.displayTextos(mainSurface,'Enter clear picture & folder path')

        #--------------------------------------------Help Screen--------------------------------------------#
        elif setupState=="help screen": 
          #Display the image on the screen
            mainSurface.blit(helpScreen,rect)

            #Draw the objects and text on the screen
            for obj,txt in helpDict.items():
              #Check if the objects were clicked 
              if obj.buttonClick(mousePos):
                #Change to the respective set up state 
                setupState=newHelpState[txt]  
                
              obj.drawImg(mainSurface,txt)

        #-----------------------Folder Help---------------------#
        elif setupState=="folder help":
            #Display the image on the screen
            mainSurface.blit(folderHelp,folderRect) 

            #Check if the button is clicked
            if backBut.buttonClick(mousePos):
                setupState="help screen"

            #Draw the button

            backBut.drawImg(mainSurface,'  Back')

        #------------------------------------------Set up----------------------------------------------#

        elif setupState=="enter file":

            mainSurface.fill((0,200,255))
            mainSurface.blit(penguinBack,backgroundRect)


            #Set up variables during the first run of the program
            if(firstRun):

                mailEntered = findFile('userMail',os.getcwd())
                firstRun=False
                invalidPath=False 

            inputBut.drawRect(mainSurface)

            #Take in user input and display it
            base=inputBut.userInput(mainSurface,ev,base)
            inputBut.userInput(mainSurface,ev,base)

            #Check if the back button is clicked

            if backBut.buttonClick(mousePos):
                setupState="main screen" 
            
            #Draw the objects on the screen
            for i in range(0,len(setupObjList),1):
                setupObjList[i].displayTextos(mainSurface,fileObjRectList[i][0])
            
            backBut.drawImg(mainSurface,'  Back')

            #Check if the user pressed a key
       
            if(ev.type==pygame.KEYDOWN):
                #If the user pressed tab (meaning they have entered their folder)

                if ev.key==pygame.K_TAB:
                    direc=base
                    #Check if the trajectory they entered is valid
                    if trajectoryCheck(direc):
                        setupState="bootUp"
                        base=''
                        firstRun=True
                    #if not play error sound
                    else:
                        pygame.mixer.Sound.play(negativeBeeps)
                        invalidPath=True

            #Dispaly error message if the entered path is not valid
            if(invalidPath):
                text2.displayTextos(mainSurface,'Please enter a valid path!')

        #------------------------------------------------------Enter mail--------------------------------------------------#

        elif setupState=="enter mail":

            mainSurface.fill((0,200,255)) #Put the background on the screen 
            mainSurface.blit(penguinBack,backgroundRect)


            if(firstRun):
                #Initialize the main menu variables 
                progBrok=False 

                folderEntered = findFile('facialEncodings',os.getcwd())  
                mailEntered=findFile('userMail',os.getcwd())  
                invalidPath=False
                firstRun=False
 
            #If the button is clicked            
            if backBut.buttonClick(mousePos):
                setupState="main screen" 

            #Check for and display the string the user has typed so far 
            base=inputBut.userInput(mainSurface,ev,base)

            #Draw the texts on the screen
            for i in range(0,len(setupObjList),1):
                setupObjList[i].displayTextos(mainSurface,mailObjList[i][0])

            #Draw the buttons and the input rectangle 
            backBut.drawImg(mainSurface,"  Back")
            inputBut.drawRect(mainSurface)
            #If the person entered an invalid email, display the error message 
            if invalidPath:
              text2.displayTextos(mainSurface,'Please enter a valid mail!')
            #Check if the person pressed a key...
            if(ev.type==pygame.KEYDOWN):

                if ev.key==pygame.K_TAB:
                  #An if statement that just uses some restrictions to check if the email is valid
                  if "@" in base and "." in base:

                    #If the person pressed tab (meaning they entered their mail), enter new game state
                    if (not folderEntered) or (mailEntered and folderEntered):

                        mail=base
                        setupState="main screen"
                  #If folder is entered, go to closing state     
                    elif folderEntered:

                        mail=base
                        setupState="closing"
                    #Dump the user mail to a file so it can be opened anytime
                    mailFile='userMail'
                    writeFile(mailFile,mail)
                    firstRun=True 
                    
                  else:
                    #Display error message and play negative beeps
                    pygame.mixer.Sound.play(negativeBeeps)
                    invalidPath=True
            inputBut.userInput(mainSurface,ev,base)



        #--------------------------------------------Boot up-------------------------------------------#
        elif setupState=="bootUp":

            #If first time in this setup stage
            if(firstRun):
                #Check if the folder and mail is entered
                folderEntered=findFile('facialEncodings',os.getcwd())
                mailEntered=findFile('userMail',os.getcwd())

            #Draw loading screen objects
            mainSurface.fill((0, 200, 255))
            mainSurface.blit(penguinBack,backgroundRect)
            inputBut.drawRect(mainSurface)
            loadMsg.displayTextos(mainSurface,'Loading... This may take a while')
            #Have to put this here because the following for loop will take a while (and it only needs to run once)
            pygame.display.flip()
            faceEncodings=[]

            #Processes facial encodings in the images so it can be compared to other faces later
            for mainPath,folders,files in os.walk(direc):

                for file in files:

                    try:
                      #Join the main trajectory with the file so it makes a whole path
                        path=os.path.join(mainPath,file)
                        #Load the image of the path (prone to break if it isn't an image!)
                        picture=fr.load_image_file(path)
                        #Convert the picture to BGR because cv2 works on BGR
                        picture=cv2.cvtColor(picture,cv2.COLOR_RGB2BGR)
                        #Collect the face encodings of the FIRST face in the image (assuming there is only one image); if the image has no face it should return to main menu
                        encoding=fr.face_encodings(picture)[0]
                        #Add the face encodings in a list (which will later be added to a file)
                        faceEncodings.append(encoding)
                        progBrok=False 
                        

                    except:
                        #If there was an error loading a file in the folder, return to main menu
                        setupState="main screen"
                        progBrok=True
                        break 
                      
                if(progBrok):
                    break 
                    
            #If the program has not broken
            if not progBrok:            
                #Add the image encodings in a file 
                fileName='facialEncodings'
                writeFile(fileName,faceEncodings)
                
                #If the user has not entered mail or there already existed a folder file, return to main menu
                if (not mailEntered):
                    setupState="main screen" 
                
                elif (mailEntered and folderEntered):
                  setupState="main screen"
                  settingsUpdate=True 
                #If a folder file wasn't entered before and the mail is already entered, transition to functioning state 
                else:
                    setupState="closing"
                                       
  
        #----------------------------------------Closing----------------------------------------#
        elif(setupState=="closing"):

            mainSurface.fill((0, 200, 255))
            mainSurface.blit(penguinBack,backgroundRect)

            if (firstRun):
                #Catch the time when this code runs
                currTime=time.time()
                firstRun=False 
            #Display current time minus 'catch time' (basically a 10-sec countdown)
            timeLeft=round((10-(time.time()-currTime)),1)
            text.displayTextos(mainSurface,f'Initialized! The program will start running in {timeLeft} seconds')

            #Once the countdown reaches zero, go to setup state
            if timeLeft<=0:
                firstRun=True 
                setupState="shift"

        elif setupState=="shift":

          #Start running the camera and detection process. Also make the screen black
          programState="functioning"
          frame=cv2.VideoCapture(0)
          setupState="main screen"
          mainSurface.fill((0,0,0))

        
        pygame.display.flip() #Display new screen
        clock.tick(60) #Cap FPS @ 60
        
    elif(programState=="functioning"): 
        #Stop the music 
        pygame.mixer.music.stop()

        #If the person presses 'ctrl' and 'q', then return back to the settings page
        if keyboard.is_pressed('q') and keyboard.is_pressed('ctrl'):
         
            programState="setup"
            setupState="main screen"
            firstRun=True 
            mailSent=False 
            #Destroy all camera windows and stop camera
            frame.release()
            cv2.destroyAllWindows()
            #Begin the music again!
            pygame.mixer.music.play()
    

        #grab the camera frame 
        thrash,video=frame.read()

        faceList=faceFinder.detectMultiScale(video,1.3,5) #A list of all faces (unnamed) on the video (cascade = frontal face)
        
        faceEncodings=readFile('facialEncodings') #Read the face encodings of the home owner from their pictures which was imported in the file
       
        print(len(faceList)) #Prints amount of faces on the list
        #If the amount of faces (length of the list) is greater or equal 1
        if(len(faceList)>=1):
            #The face location of the person on the screen 
            faceLocations=fr.face_locations(video)
            #Grab the face encodings of the person caught on video
            camFaceEncodings=fr.face_encodings(video,faceLocations)

            #For each face on camera, step through their encodings
            for unknownEncoding in camFaceEncodings:
                #Check if the faces the owner inputed matches the ones on camera (in a list)
                strangeCheck=fr.compare_faces(faceEncodings,unknownEncoding)
                print(strangeCheck)
                
                #If the face encodings of the person on camera does NOT match ANY/SOME/MOST/ALL of the images of the owner's face:
                if False in strangeCheck and not mailSent:
                    #Read the file that has user's email
                    mailReciever=readFile('userMail')
                    #Send mail to the owner!
                    sendMail('dangmeco@gmail.com','bilohitha',mailReciever,'Alert','Someone has entered the room')
                    mailSent = True 
pygame.quit()
frame.release()
cv2.destroyAllWindows()
