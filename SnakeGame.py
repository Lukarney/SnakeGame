from cmu_112_graphics import *
from tkinter import*
from PIL import Image #


import random
#defines player
class Player(object):
    def __init__(self,mode):
        #instantiates everything for the player
        self.mode=mode
        self.x=self.mode.playerX
        self.y=self.mode.playerY
        self.dx=10
        self.dy=5
        self.lives=3
        #for snake images
        self.snakeIdle='https://i.imgur.com/2zhLYzE.png'
        self.snakeMoving='https://i.imgur.com/2zhLYzE.png'
        spritestrip=self.mode.loadImage(self.snakeMoving)
        spritestrip1=self.mode.scaleImage(spritestrip,3)
        #makes snake image move
        heartURL=('https://cdn.pixabay.com/photo/2017/09/23/16/33/'+
        'pixel-heart-2779422_1280.png')
        heart=self.mode.loadImage(heartURL)
        self.heart=self.mode.scaleImage(heart,1/30)
        #uses sprite strip to create moving image
        self.sprites=[]
        for i in range(10):
                sprite = spritestrip1.crop(((0+31.8*i)*3, 3*10, 
                                            3*(31+31.8*i), 3*48))
                self.sprites.append(sprite)
        self.spriteCounter=0
    #checks to see if player collided with cacti
    def checkCollisions(self):
        cactiToKeep={}
        for cactus in self.mode.cacti:
            if cactus.containsPoint(self.mode.playerX+self.mode.scrollX,
            self.y) and isinstance(cactus,EnemyCactus):
                self.mode.lives-=1
            elif cactus.containsPoint(self.mode.playerX+self.mode.scrollX,
            self.y) and isinstance(cactus,FriendlyCactus):
                pass
            else:
                cactiToKeep[cactus]=self.mode.cacti[cactus]
        self.mode.cacti=cactiToKeep
    #checks to see if player collides with hole
    def holeCollide(self):
        if self.mode.hole.containsPoint(self.mode.playerX+self.mode.scrollX,
                                        self.y):
            self.mode.isGameOver=True
            
    #checks to see if the player collides with a heart 
    # and gets removes heart from the board
    def heartCollide(self):
        heartsToKeep=[]
        for heart in self.mode.hearts:
            if heart.containsPoint(self.mode.playerX+self.mode.scrollX,
                                    self.y):
                self.mode.lives+=1
            else:
                heartsToKeep.append(heart)
        self.mode.hearts=heartsToKeep
    #moves player based on the cordinates given from the GameMode class     
    def move(self,cordinate):
        if cordinate=="Up":
            self.y=self.y-self.dy
        if cordinate=="Down":
            self.y=self.y+self.dy
        if(self.y>self.mode.height):
            self.y-=self.dy
        if(self.y<self.mode.height*.75):
            self.y+=self.dy
 
    #checks to see if the player is alive 
    #changes gmeover and died if it's true
    def checkIfAlive(self):
        if self.mode.lives<=0:
            self.mode.isGameOver=True
            self.mode.died=True
        if self.mode.playerX>620:
            self.mode.died=True
        

    #changes sprite animation and checks collisions every time
    def timerFired(self):
        self.spriteCounter = ((1 + self.spriteCounter) % len(self.sprites))
        self.checkCollisions()
        self.holeCollide()
        self.checkIfAlive()
        self.heartCollide()
        
    #draws the snake
    def draw(self, canvas):
        if(self.mode.isGameOver==False):
            #draw sprite
            sprite = self.sprites[self.spriteCounter]
            #cannot move above a y of 450, (25,450)
            canvas.create_image(self.mode.playerX, self.y,
            image=ImageTk.PhotoImage(sprite))
        #draw lives in the top right
        for i in range(self.mode.lives):
            canvas.create_image(self.mode.canvasWidth-(1+i)*50, 40,
        image=ImageTk.PhotoImage(self.heart))
#defines items that help the player
class Friend(object):
    def __init__(self,mode,y):
        self.mode=mode
        self.y=y
    #distance function which is used for collision
    def distance(self,x1,y1,x2,y2):
        return ((x1-x2)**2+(y1-y2)**2)**.5
    #cecks if the item contains the point
    def containsPoint(self,x,y):
        return self.distance(self.x,self.y,x,y)<25
#defines the heart
class Heart(Friend):
    def __init__(self,mode,x,y):
        super().__init__(mode,y)
        self.x=x
        self.lives=self.mode.lives
        heartURL=('https://cdn.pixabay.com/photo/2017/09/23/16/33/'+
        'pixel-heart-2779422_1280.png')
        heart=self.mode.loadImage(heartURL)
        self.heart=self.mode.scaleImage(heart,1/30)
    #draws the heart that player can get 
    def draw(self,canvas):
        drawX=self.x
        drawY=self.y
        canvas.create_image(drawX-self.mode.scrollX,drawY,
        image=ImageTk.PhotoImage(self.heart))
#defines class hole
class Hole(Friend):
    def __init__(self,mode,y):
        super().__init__(mode,y)
        self.x=.65*self.mode.boundx1
        url='http://pixelartmaker.com/art/24d7d2439776568.png'
        self.holeImage=self.mode.loadImage(url)
        self.holeImage1=self.mode.scaleImage(self.holeImage,1/9)
    #draws the hole
    def draw(self,canvas):
        drawX=self.x
        drawY=self.y
        canvas.create_image(drawX-self.mode.scrollX,drawY,
        image=ImageTk.PhotoImage(self.holeImage1))
#defines all the cactus objects
class Cactus(object):
    def __init__(self,mode,x,y):
        self.mode=mode
        self.x=x
        self.y=y
    
    def __eq__(self,other):
        return (isinstance(other,Cactus))
    #defines distance functions for cactus
    def distance(self,x1,y1,x2,y2):
        return ((x1-x2)**2+(y1-y2)**2)**.5
    #defines contains point for cactus
    def containsPoint(self,x,y):
        return self.distance(self.x,self.y,x,y)<25

class EnemyCactus(Cactus):
    def __init__(self,mode,x,y):
        super().__init__(mode,x,y)
        cactusImage=('https://i.imgur.com/lHsZL9J.png')
        self.cactus1=self.mode.loadImage(cactusImage)
        self.cactusImage=self.mode.scaleImage(self.cactus1,1/10)
    #checks to see if the other object if is an enemycactus  
    def __eq__(self,other):
        return (isinstance(other,EnemyCactus)) 
    
    def __hash__(self):
        return hash((self.x,self.y))
    #draws the enemy cactus on the scrolling page
    def draw(self,canvas):
        drawX=self.x-self.mode.scrollX
        drawY=self.y
        canvas.create_image(drawX,
        drawY,image=ImageTk.PhotoImage(self.cactusImage))

class FriendlyCactus(Cactus):
    def __init__(self,mode,x,y):
        super().__init__(mode,x,y)
        cactusImage=('https://www.sccpre.cat/mypng/full/52-521042'+
         '_cute-soft-kawaii-tumblr-pastel-pixelart-pixel-cactus.png')
        self.cuteCactus=self.mode.loadImage(cactusImage)
        self.cactusImage=self.mode.scaleImage(self.cuteCactus,1/10)
    #checks to see if other item is a FriendlyCactus
    def __eq__(self,other):
        return (isinstance(other,FriendlyCactus)) 
    
    def __hash__(self):
        return hash((self.x,self.y))
    #draw the friednly cactus on the scrolling page
    def draw(self,canvas):
        drawX=self.x-self.mode.scrollX
        drawY=self.y
        canvas.create_image(drawX,
        drawY,image=ImageTk.PhotoImage(self.cactusImage))


class GameMode(Mode):
    def appStarted(mode):
        #mode.object=Object()
        #for background images
        mode.bkground1=mode.loadImage('https://i.imgur.com/DcFU1Kw.png')
        mode.bkground2=mode.scaleImage(mode.bkground1,2/3)
        #for cursor images
        cursorURL='http://pixelartmaker.com/art/73bfcdeff52f39c.png'
        cursorScale=mode.loadImage(cursorURL)
        mode.cursorImage=mode.scaleImage(cursorScale,1/5)
        #instantiates important features of the game
        mode.backgrounds=[mode.bkground2]*20
        #instantiates snake, object and scroll
        mode.scrollX=0
        mode.scrollMargin=7
        mode.playerX=mode.scrollMargin*18
        mode.playerY=mode.height*.85
        mode.playerWidth=11*3-28*3
        mode.playerHeight=3*10-3*48
        mode.sandHeight=450
        mode.canvasWidth=600
        mode.canvasHeight=600
        (mode.boundy0,mode.boundy1)=(mode.height*.7,mode.height)
        (mode.boundx0,mode.boundx1)=(mode.scrollMargin*27,mode.width*3.5)
        mode.draggingHeart=None
        mode.cursor=[-1,-1]
        mode.cacti={}
        mode.hearts=[]
        mode.snake=Player(mode)
        mode.lives=3
        mode.hole=Hole(mode,random.randint(mode.boundy0+40,
        mode.boundy1-30))
        #creates enemy cactus in cacti dictionary
        for i in range(15):
            randomX=random.randint(mode.boundx0,mode.boundx1)
            #randomX=900
            randomY=random.randint(mode.boundy0,mode.boundy1)
            mode.cacti[(EnemyCactus(mode,randomX,randomY))]=(randomX,randomY)
        #adds friendly cactus to cacti dictionary
        for i in range(1):
            randomX=random.randint(mode.boundx0,mode.boundx1)
            #randomX=900
            randomY=random.randint(mode.boundy0,mode.boundy1)
            mode.cacti[(FriendlyCactus(mode,randomX,randomY))]=(randomX,randomY)
        #adds heart to hearts list
        for i in range(1):
            randomX=random.randint(mode.boundx0,mode.boundx1*.6)
            #randomX=900
            randomY=random.randint(mode.boundy0+mode.boundy0*.1,mode.boundy1)
            mode.hearts.append(Heart(mode,randomX,randomY))
        #sets up functions for the end game
        mode.died=False
        mode.isGameOver=False
    #checks to see if a key is pressed
    def keyPressed(mode,event):
        mode.snake.move(event.key)
        if (event.key=='h'):
            mode.app.setActiveMode(mode.app.helpMode)
        if (event.key=='S'):
            print("""
            1.you can only move up and down
            2.The goal is to go into the hole at the end of the track
            -when the snake sees his hole, he speeds up
            -if you miss the hole, you loose
            3.Going into the cacti causes that cactus to disappear
            -If you go into an enemy cactus, the snake to loose a life
                (the enemy cactus looks like a regular cacti)
            -If you go into a friendly cactus, you don't loose a life
                (the friendly cactus is the bunny-looking one)
            4.Going into the heart makes you gain an extra life
            -You can move the heart by drag and dropping it anywhere
            """)
        #checks to see if game is over and sets up for end game screen
        if(mode.isGameOver==True):
            if event.key=="r":
                mode.appStarted()
    #moves cursor with mouse
    def mouseMoved(mode,event):
        mode.app._root.configure(cursor='none')
        mode.cursor=[event.x,event.y]
    #collects hear when mouse is pressed
    def mousePressed(mode,event):
        for heart in mode.hearts:
            if heart.containsPoint(event.x+mode.scrollX,event.y):
                mode.draggingHeart=heart
    #doesn't hold heart on cursor anymore
    def mouseReleased(mode,event):
        mode.draggingHeart=None
    #moves heart when the mouse is dragge
    def mouseDragged(mode,event):
        mode.cursor=[event.x,event.y]
        if not mode.draggingHeart is None:
            mode.draggingHeart.x=event.x+mode.scrollX
            mode.draggingHeart.y=event.y

    def timerFired(mode):
        if(mode.isGameOver==False):
            mode.snake.timerFired()
            mode.scrollX+=mode.scrollMargin
        #changes isGameOver if player died
        if(mode.died==True):
            mode.isGameOver=True
         
    def redrawAll(mode,canvas):
        cx=mode.playerX# this scrolls the player
        bckgroundEnd=730
        backgroundStart=640
        #drawsbackground and snake
        if mode.scrollX<bckgroundEnd:
            cx-=mode.scrollX#this scrolls the player
            canvas.create_image(backgroundStart-mode.scrollX, 300,
            image=ImageTk.PhotoImage(mode.bkground2))
            #cannot move above a y of 450, (25,450)
            mode.snake.draw(canvas)
        #if player reaches end of image it stops scrolling byt the items
        #keep moving
        else:
            mode.playerX+=mode.scrollMargin//2#this keeps the player moving
            canvas.create_image(backgroundStart%100/10*-1, 300,
            image=ImageTk.PhotoImage(mode.bkground2))
            #cannot move above a y of 450, (25,450)
            mode.snake.draw(canvas)
        #draws hole
        mode.hole.draw(canvas)
        #draws cacti(enemy and friendly cacti)
        for cactus in mode.cacti:
              cactus.draw(canvas)
        #draws hearts
        for heart in mode.hearts:
              heart.draw(canvas)
        #draws cursor while moving
        canvas.create_image(mode.cursor[0], mode.cursor[1],
            image=ImageTk.PhotoImage(mode.cursorImage))
        #draws end game mode text
        if(mode.isGameOver==True):
            if(mode.died==True):
                font = 'Arial 26 bold'
                canvas.create_text(mode.width/2, 150, 
                text="You did not make it :(\n press r to restart", font=font)   
            else:
                font = 'Arial 26 bold'
                text=('You complete the Yee to my Haw,\nWINNER!\n'+
                'press r to restart')
                canvas.create_text(mode.width/2, 150,text=text, font=font)

class SplashScreenMode(Mode):
    def appStarted(mode):
        urlStartScreen='https://i.imgur.com/psVcn8I.png'
        mode.bkground1=mode.loadImage(urlStartScreen)
        mode.snakeIdle='https://i.imgur.com/y6rR0MG.png'
        spritestrip=mode.loadImage(mode.snakeIdle)
        spritestrip1=mode.scaleImage(spritestrip,3)
        mode.sprites=[]
        #Creates moving sprite images
        for i in range(10):
                sprite = spritestrip1.crop(((0+31.8*i)*3, 3*10, 
                                            3*(31+31.8*i), 3*48))
                mode.sprites.append(sprite)
        mode.spriteCounter=0
    def timerFired(mode):
        mode.spriteCounter = ((1 + mode.spriteCounter) % len(mode.sprites))
    #draws snake and background
    def redrawAll(mode, canvas):
        canvas.create_image(300, 300,image=ImageTk.PhotoImage(mode.bkground1))
        #draw sprite
        sprite = mode.sprites[mode.spriteCounter]
        #cannot move above a y of 450, (25,450)
        canvas.create_image(300, 500,
        image=ImageTk.PhotoImage(sprite))
    #if any key is pressed the game starts
    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)
#help mode gives user help on the game
class HelpMode(Mode):
    def appStarted(mode):
        url='https://i.imgur.com/wDuVMcy.png'
        mode.bkground1=mode.loadImage(url)
        bkground2=mode.scaleImage(mode.bkground1,2/3)
    #draws background
    def redrawAll(mode, canvas):
        canvas.create_image(300, 300,
            image=ImageTk.PhotoImage(mode.bkground1))
    #if any key is pressed the game starts
    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)
#holds all the game functions
class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 50
 
def runCreativeSideScroller():
    MyModalApp(width=600,height=600)
runCreativeSideScroller()