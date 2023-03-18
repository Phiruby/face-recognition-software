import pygame
from pygame import mixer 
import os 
import pickle 
import time
import keyboard 

def trajectoryCheck(path):
    for root,dir,files in os.walk(path):
        return True
    return False 


mail=None


def findFile(name,path):
    for thrash,thrash2,files in os.walk(path):
        if name in files:
            return True 
    return False

class setupScreen():

    pygame.init()

    def __init__(self,pos,width,height,imgPath):

        self.pos=pos
        self.height=height 
        self.width=width 

        self.imgPath=imgPath 

        if self.imgPath!=None: 

            butImg=pygame.image.load(self.imgPath)
            buttonImage=pygame.transform.flip(butImg,False,False)
            buttonImage=pygame.transform.scale(buttonImage,(self.width,self.height))
            self.image=buttonImage        

    def drawImg(self,surface,text=None,textColor=[255,255,255]):
       
        surface.blit(self.image,self.pos)

        if text!=None:

            font=pygame.font.Font(None,int(self.height/2))
            message=font.render(text,True,textColor)
            surface.blit(message,[self.pos[0]+self.width/5,self.pos[1]+self.height/5])
        
    def drawRect(self,surface,color=[113,26,117]):

        pygame.draw.rect(surface,color,[self.pos[0],self.pos[1],self.width,self.height])
    

    def hoverDetect(self,mousePos):

        if (0<=mousePos[0]-self.pos[0]<=self.width) and (0<=mousePos[1]-self.pos[1]<=self.height):

            if self.imgPath!=None: 

                butImg=pygame.image.load('Images\\hoverButton.png')
                buttonImage=pygame.transform.flip(butImg,False,False)
                buttonImage=pygame.transform.scale(buttonImage,(self.width,self.height))
                self.image=buttonImage  

            return True 

        else: 

            if self.imgPath!=None:

                butImg=pygame.image.load('Images\\button.png')
                buttonImage=pygame.transform.flip(butImg,False,False)
                buttonImage=pygame.transform.scale(buttonImage,(self.width,self.height))
                self.image=buttonImage  

            return False 

    def buttonClick(self,mousePos):
        if self.hoverDetect(mousePos) and ev.type==1026:
            return True
        return False 

    def userInput(self,surface,event,baseString,font=pygame.font.Font(None,32)):

        if(event.type==pygame.KEYDOWN):

            if event.key==pygame.K_BACKSPACE:
                baseString=baseString[:-1]

            elif event.unicode!=' ' and event.key!=pygame.K_TAB:
                baseString=str(baseString)+str(event.unicode)

            elif event.unicode==' ' and event.key!=pygame.K_TAB:
                baseString+=' '

        text=font.render(baseString,True,(255,255,255))
        surface.blit(text,self.pos)
        return baseString

    def displayTextos(self,surface,msg,textColor=[255,255,255]):
        font=pygame.font.Font(None,self.height)
        message=font.render(msg,True,textColor)
        surface.blit(message,self.pos)


def main():
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
    # setButton=setupScreen([300,100],[113, 26, 117],100,200)
    # phoneBut=setupScreen([300,300],[113, 26, 117],100,200)
    # helpBut=setupScreen([300,500],[113,36,117],100,200)
    # msg2=setupScreen([115,700],[113,26,117],50,50)

    #mainObjectList=[setButton,phoneBut,helpBut]

    #-----------------------Set up/ Mail Screens-------------------#

    inputBut=setupScreen([0,500],800,100,None)
    text=setupScreen([200,300],50,50,None)
    inst=setupScreen([50,100],50,50,None)
    inst2=setupScreen([150,200],50,50,None)
    # errorMsg=setupScreen([115,650],[113,26,117],50,50)
    # errorMsg2=setupScreen([115,700],[113,26,117],50,50)
    # invalidPath=False

    setupObjList=[inst,inst2]
    fileObjRectList=[['Enter a path to a folder with your pictures'],
['Press TAB once you are done']]

    #----------------------Help Screen---------------------#
    guideMsg=setupScreen([50,100],50,45,None)
    guideMsg2=setupScreen([25,150],50,30,None)

    mailMsg=setupScreen([70,225],50,50,None)
    mailMsg2=setupScreen([40,275],50,30,None)

    genMsg=setupScreen([5,400],50,33,None)
    genMsg2=setupScreen([125,450],50,35,None)
    genMsg3=setupScreen([5,500],50,30,None)
    genMsg4=setupScreen([5,550],50,31,None)
    genMsg5=setupScreen([50,600],50,35,None)

    backBut=setupScreen([500,650],200,100,'Images\\button.png')
    extraHelpBut=setupScreen([100,650],200,100,'Images\\button.png')

    helpList=[backBut,extraHelpBut]
    textListHelp=['  Back','  More']
    helpStates=['main screen','folder help']

    helpObjectList=[guideMsg,guideMsg2,mailMsg,mailMsg2,genMsg,genMsg2,genMsg3,genMsg4,genMsg5]

    helpObjRectList=[['1: Click on "Set up" to enter a path to your folder.'],
    ['This folder must have pictures of yourself so the computer can recognize you'],
    ['2: Click on "Mail" to enter your email'],
    ['This is the email where you will be alerted when someone enters the room'],
    ['Once you have entered these information, the program will start running'],
    ['If you ever need to change settings, press "Ctrl+q"'],
    ['Note: the mail alerts may be sent to the spam section, so report it as "not spam"'],
    ['The folder path has to be in the format: "C:/Users/viloh/Documents/CSWork...."'],
     ['Make sure the path is to a FOLDER and NOT a single file!']]

    #------------------------Background setup---------------------#
    penguinBack=pygame.image.load('Images\image.jfif').convert()
    backgroundRect=penguinBack.get_rect()
    penguinBack=pygame.transform.scale(penguinBack,(surfaceSize,surfaceSize))
    
   
    butPos=[200,100]
    path='Images\\button.png'
    button=setupScreen(butPos,400,133,path)

    mailButton=setupScreen([200,300],400,133,'Images\\button.png')

    helpButton=setupScreen([200,500],400,133,'Images\\button.png')

    mainscreenObjects=[button,mailButton,helpButton]
    newStates=['enter file','enter mail','help screen']
    textList=['Enter file','Enter mail','Help center']
    
    
    negativeBeeps=pygame.mixer.Sound('Sounds\wrong-buzzer-6268.mp3')

    #---------------------------Help Screen-----------------------#
    helpScreen=pygame.image.load('Images\\helpScreen.png').convert()
    rect=helpScreen.get_rect()
    helpScreen=pygame.transform.scale(helpScreen,(surfaceSize,surfaceSize))

    folderHelp=pygame.image.load('Images\\folderHelp.png').convert()
    folderRect=folderHelp.get_rect()
    folderHelp=pygame.transform.scale(folderHelp,(surfaceSize,surfaceSize))
    

    mailEntered=False 
    folderEntered=False 

    progBrok=False
    firstRun=True

    #-----------------------------Main Program Loop---------------------------------------------#
    while True:       
        #-----------------------------Event Handling-----------------------------------------#
        global ev
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break                   #   ... leave game loop
        mousePos=pygame.mouse.get_pos()
        mainSurface.fill((0, 200, 255))
        mainSurface.blit(penguinBack,backgroundRect)

        #-----------------------------Program Logic---------------------------------------------#
        # Update your game objects and data structures here...
        
        if keyboard.is_pressed('q') and keyboard.is_pressed('ctrl'):
            print('hu')


        #-----------------------------Drawing Everything-------------------------------------#
        # We draw everything from scratch on each frame.
        # So first fill everything with the background color
        

               
        # Draw a circle on the surface

        threshold=1 
        mainSurface.fill((0,200,255))
        mainSurface.blit(penguinBack,backgroundRect)

        if(setupState=="main screen"):

            # mainObjRectList=[['Set up',50,[setButton.pos[0]+setButton.width/10,1.05*setButton.pos[1]],mousePos],
            # ['Phone #',50,[phoneBut.pos[0]+phoneBut.width/17,1.05*phoneBut.pos[1]],mousePos],
            # ['Help',50,[helpBut.pos[0]+helpBut.width/5,helpBut.pos[1]],mousePos] ]

            if(firstRun):

                mailEntered=findFile('userMail',os.getcwd())
                folderEntered=findFile('facialEncodings',os.getcwd())
                firstRun=False

            base=""

            for i in range(0,len(mainscreenObjects),1):

                if mainscreenObjects[i].buttonClick(mousePos):

                    setupState=newStates[i]
                    firstRun=True 
                    break 
                mainscreenObjects[i].drawImg(mainSurface,textList[i])
    
            # for i in range(0,len(mainscreenObjects)):
            #     mainscreenObjects[i].drawImg(mainSurface,textList[i])


        elif setupState=="help screen":

            mainSurface.blit(helpScreen,rect)

            # if backBut.buttonClick(mousePos):
            #     setupState="main screen"
            #     firstRun=True 

            # if extraHelpBut.buttonClick(mousePos):
            #     setupState='folder help'
            #     firstRun=True 

            for obj,mseg,newState in zip(helpList,textListHelp,helpStates):

                if obj.buttonClick(mousePos):
                    setupState=newState
                    firstRun=True 
                
                obj.drawImg(mainSurface,mseg)
            # for i in range(0,len(helpObjectList),1):
            #     helpObjectList[i].displayTextos(mainSurface,helpObjRectList[i][0])

            # backBut.drawImg(mainSurface,'  Back')
            # extraHelpBut.drawImg(mainSurface,'  More')

        elif setupState=="folder help":

            mainSurface.blit(folderHelp,folderRect) 

            if backBut.buttonClick(mousePos):
                setupState="help screen"
                firstRun=True 

            backBut.drawImg(mainSurface,'  Back')

        elif setupState=="enter file":

            mainSurface.fill((0,200,255))
            mainSurface.blit(penguinBack,backgroundRect)



            if(firstRun):

                if findFile('userMail',os.getcwd()):
                    mailEntered=True 

                firstRun=False
                invalidPath=False 

            inputBut.drawRect(mainSurface)

            base=inputBut.userInput(mainSurface,ev,base)
            inputBut.userInput(mainSurface,ev,base)

            if backBut.buttonClick(mousePos):
                setupState="main screen"
                firstRun=True 

            for i in range(0,len(setupObjList),1):
                setupObjList[i].displayTextos(mainSurface,fileObjRectList[i][0])
            
            backBut.drawImg(mainSurface,'  Back')
       
            if(ev.type==pygame.KEYDOWN):

                if ev.key==pygame.K_TAB:
                    direc=base

                    if trajectoryCheck(direc):
                        setupState="bootUp"
                        base=''
                        firstRun=True
                        
                    else:
                        pygame.mixer.Sound.play(negativeBeeps)
                        invalidPath=True

            if(invalidPath):
                text.displayTextos(mainSurface,'Please enter a valid path!')

        elif setupState=="enter mail":

            mainSurface.fill((0,200,255))
            mainSurface.blit(penguinBack,backgroundRect)

            mailObjList=[['Enter the email you want to be alerted'],
            ['Press TAB once you are done']]

            if(firstRun):
                progBrok=False 
                if findFile('facialEncodings',os.getcwd()):
                    folderEntered=True 

                firstRun=False 
            
            if backBut.buttonClick(mousePos):
                setupState="main screen"
                firstRun=True 

            inputBut.drawRect(mainSurface)

            base=inputBut.userInput(mainSurface,ev,base)
            inputBut.userInput(mainSurface,ev,base)

            for i in range(0,len(setupObjList),1):
                setupObjList[i].displayTextos(mainSurface,mailObjList[i][0])

            backBut.drawImg(mainSurface,"  Back")
       
            if(ev.type==pygame.KEYDOWN):

                if ev.key==pygame.K_TAB and not folderEntered:

                    mail=base
                    mailFile='userMail'
                    createFile=open(mailFile,'wb')
                    pickle.dump(mail,createFile)
                    createFile.close()
                    setupState="main screen"
                    firstRun=True 

                elif ev.key==pygame.K_TAB and folderEntered:

                    mail=base
                    mailFile='userMail'
                    createFile=open(mailFile,'wb')
                    pickle.dump(mail,createFile)
                    createFile.close()
                    setupState="closing"
                    print(setupState)
                    firstRun=True 





        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()
        
        clock.tick(60) #Force frame rate to be slower


    pygame.quit()     # Once we leave the loop, close the window.

main()