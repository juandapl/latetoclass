# Late to Class!
# Final Project
# by Chun Ting Liu and Juan Piñeros

# "What greater gift than the slow effect of a cat"
#                    -Charles Dickens

# "You talk about vengeance. Is vengeance going to make the final boss look less like the Professor? Or get rid of the obstacles?"
#                    -Don Vito Corleone

import os,random,time

add_library('minim')
player=Minim(this)
path=os.getcwd()

cat_sound=player.loadFile(path+"/sounds/meow.mp3")
background_sound=player.loadFile(path+"/sounds/background.mp3")
door_slam=player.loadFile(path+"/sounds/door_slam.mp3")
win_sound=player.loadFile(path+"/sounds/win_sound.mp3")
fail_sound=player.loadFile(path+"/sounds/fail_sound.mp3")
bomb_sound=player.loadFile(path+"/sounds/bomb.mp3")
electric_sound=player.loadFile(path+"/sounds/electricity.mp3")
jump_sound=player.loadFile(path+"/sounds/jump.mp3")

# Student 576*52
# RGAP gives the width of the buildings, to adjust all x-coordinates when displaying
RGAP = 206
UGAP = 100
WIDTH=520
HEIGHT=720

# return the distance of two points
def dis(x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5

class Wall:
    def __init__(self,y):
        self.yBottom = y
        self.yTop = y-52
        self.yAbsTop = y-62

        # generate the door
        self.doorX = random.randint(0,9)
        self.doorBroken = False

        
    def hitByProjectile(self,projectile):
        if projectile.y <= self.yBottom - 30:
            if projectile.x > 52*self.doorX and projectile.x < 52*(self.doorX+1):
                if not self.doorBroken:
                    door_slam.play()
                    door_slam.rewind()
                    self.doorBroken = True
                    game.student.books.remove(projectile)
    
    def update(self):
        for book in game.student.books:
            self.hitByProjectile(book)
    
    def display(self):
        # the wall is made of 10 tiles of 52x52, one of them being the door
        self.update()
        # this converts absolute y values to y values relative to the current yshift
        yTop = self.yTop-game.yshift+HEIGHT
        yAbsTop = self.yAbsTop-game.yshift+HEIGHT
        
        for i in range(10):
            if i == self.doorX and not self.doorBroken:
                image(game.doorTile, RGAP + (52*i), UGAP + yTop+11, 52, 41)
            elif i == self.doorX and self.doorBroken:
                pass
            else:
                noStroke()
                fill(0)
                rect(RGAP + (52*i), UGAP + yAbsTop, 52, 10) # draws the top of the wall
                image(game.wallTile, RGAP + (52*i), UGAP + yTop, 52, 52)
                
        # deletes the wall if it exits the screen on the bottom
        if self.yAbsTop > game.yshift:
            game.walls.remove(self)

class Creature:
    def __init__(self,x,y,r,g,w,h,num_frames):
        self.x=x
        self.y=y
        self.r=r
        self.g=y+r 
        self.vy=0
        self.vx=0
        self.img_w=w
        self.img_h=h
        self.num_frames=num_frames
        self.frame=0
        self.dir=RIGHT
        self.displaypos = 0
    #defines if the creature is on screen, regarding the y-shift
    def isOnScreen(self):
        return self.displaypos > 0 and self.displaypos < HEIGHT
    
# I made this new class "Projectile" in order to manage the final boss's projectiles
# in the same way you managed the Book - rotation, unit vector and so on.
class Projectile:
    def __init__(self,x,y,r,w,h,num_frames,objectiveX,objectiveY,speed):
        self.x=x
        self.y=y
        self.r=r
        # calculate the x, y regular component of the unit vector so that the speed the books fly can be the same
        objectiveY = objectiveY + game.yshift - HEIGHT
        self.vx= speed*((objectiveX-x)/dis(x,y,objectiveX,objectiveY))
        self.vy= speed*((objectiveY-y)/dis(x,y,objectiveX,objectiveY))
        self.img_w=w
        self.img_h=h
        self.num_frames=num_frames
        self.frame=0
        self.displaypos=0
        
    def isOnScreen(self):
        return self.displaypos + UGAP > 0 and self.displaypos < HEIGHT
        
    def display(self):
        self.update()
        if self.isOnScreen(): 
            # there is only one frame for the image of a projectile
            # but to create the effect of flying, it is rotated by 90 degrees every frame

            if self.frame==0:
                image(self.img, RGAP + self.x, UGAP + self.displaypos, self.img_w//2, self.img_h//2, 0,0, self.img_w,self.img_h)
            elif self.frame==1:
                image(self.img, RGAP + self.x, UGAP + self.displaypos, self.img_w//2, self.img_h//2, self.img_w, 0, 0, self.img_h)
            elif self.frame==2:
                image(self.img, RGAP + self.x, UGAP + self.displaypos, self.img_w//2, self.img_h//2, self.img_w,self.img_w, 0, 0)
            else:
                image(self.img, RGAP + self.x, UGAP + self.displaypos, self.img_w//2, self.img_h//2, 0,self.img_h, self.img_w,0)

# Professor's projectile
class F(Projectile):
    def __init__(self,x,y,r,w,h,num_frames,objectiveX,objectiveY,speed):
        Projectile.__init__(self,x,y,r,w,h,num_frames,objectiveX,objectiveY,speed)
        self.img=loadImage(path+"/images/F.png")
        self.vy=3

    def update(self):
        self.x+=self.vx
        self.y+=self.vy
        self.displaypos=self.y
        
        # if the player is hit by F
        if (self.x-game.student.x)**2 + (self.y-game.student.displaypos)**2 <= game.student.r**2+(self.r*0.85)**2:
            bomb_sound.play()
            bomb_sound.rewind()
            game.vyshift-=0.1
            game.professor.Fs.remove(self)
        if not self.isOnScreen():
            game.professor.Fs.remove(self)
        

    
# the notebook used for shooting
class Book(Projectile):
    def __init__(self,x,y,r,w,h,num_frames,objectiveX,objectiveY,speed):
        Projectile.__init__(self,x,y,r,w,h,num_frames,objectiveX,objectiveY,speed)
        self.img=loadImage(path+"/images/book.png")

        
    def collidesWith(self,other):
        return dis(self.x,self.y,other.x,other.y) <= self.r + other.r
    
    def update(self):
        if frameCount%7==0:
            self.frame=(self.frame+1)%self.num_frames
        self.x+=self.vx
        self.y+=self.vy
        self.displaypos = self.y-game.yshift+HEIGHT
        for cat in game.cats:
            if self.collidesWith(cat):
                cat_sound.play()
                cat_sound.rewind()
                game.cats.remove(cat)
                game.student.books.remove(self)
        
        # special collision detection with professor
        if game.ProfIsInstantiated:
            if self.displaypos < -30 and int(self.x) in game.professor.xRange:            
                game.ProfIsAlive = False
                game.student.books.remove(self)
        if not self.isOnScreen():
            game.student.books.remove(self)
                
                
# indicating how many books are left for the player to shoot            
class BooksBar:
    def __init__(self,x,y,w,h):
        self.x=x
        self.y=y
        self.img_w=w
        self.img_h=h
        self.num_frames=6
        self.left=5
        self.img=loadImage(path+"/images/HPbar.png")
        self.imgNone=loadImage(path+"/images/zeroLeft.png")
        
    def update(self):
        self.left=game.student.bookLeft
    def display(self):
        self.update()
        
        if self.left==0:
            image(self.imgNone, self.x, self.y, self.img_w//4, self.img_h//4)
        else:
            image(self.img, self.x, self.y, self.img_w//4, self.img_h//4, 0,(self.left-1)*self.img_h, self.img_w, self.left*self.img_h)

# to show how much progress is left to meet the professor
class ProgressBar:
    def __init__(self,x,y,w,h,t,shift):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.target = t
        self.progressLeft = t
        self.percent=1.0
        self.shift=shift
        
    def update(self):
        self.progressLeft=game.yshift-(self.shift-self.target)
        if not game.ProfIsInstantiated:
            self.percent=self.progressLeft/self.target
        else:
            self.percent=0.0

    def display(self):
        self.update()
        fill(255,0,0)
        rect(self.x, self.y, self.w*self.percent, self.h)
        
        fill(255,255,255)
        rect(self.x+self.w*self.percent, self.y, self.w*(1.0-self.percent), self.h)
        
        stroke(0,0,0)
        strokeWeight(8)
        noFill()
        rect(self.x, self.y, self.w, self.h)
        

class Cat(Creature):
    def __init__(self,x,y,r,g,w,h,num_frames):
        Creature.__init__(self,x,y,r,g,w,h,num_frames)
        self.vx=random.randint(1,4)
        self.dir=random.choice([LEFT,RIGHT])
        self.kind=random.choice([1,2,3]) #there are three kinds of cat
        if self.dir==LEFT:
            self.vx*=-1
        self.img=loadImage(path+"/images/Cat"+str(self.kind)+".png")
        
    def update(self):
        self.displaypos = self.y-game.yshift+HEIGHT
        
        # cats only move horizontally 
        self.x+=self.vx
        
        if frameCount%(8-self.vx)==0:
            self.frame=(self.frame+1)%self.num_frames
        
        # to avoid cats from moving out of the screen
        if self.x+self.r>WIDTH:
            self.vx*=-1
            self.dir=LEFT
        elif self.x-self.r<0:
            self.vx*=-1
            self.dir=RIGHT
            
        # deletes the cat if it exits the screen on the bottom
        if self.displaypos > HEIGHT:
            game.cats.remove(self)
        
        
    def display(self):
        self.update()
        
        if self.isOnScreen():
            # when the cat is moving left, the diplay of the image is inversed
            if self.dir==RIGHT:
                image(self.img, RGAP + (self.x-self.img_w//2), UGAP + self.displaypos-self.img_h//2, self.img_w,self.img_h, self.img_w*self.frame, 0, (self.frame+1)*self.img_w,self.img_h)
            elif self.dir==LEFT:
                image(self.img, RGAP + (self.x-self.img_w//2), UGAP + self.displaypos-self.img_h//2, self.img_w,self.img_h, (self.frame+1)*self.img_w, 0, self.img_w*self.frame, self.img_h)

        
class Professor(Creature):
    def __init__(self,x,y,r,g,w,h,num_frames):
        Creature.__init__(self,x,y,r,g,w,h,num_frames)
        self.vx=2
        self.dir=DOWN

        self.isMoving=False
        self.xRange = range(self.x-self.img_w//2,int(self.x-self.img_w//2+(self.img_w*1.5)))
        
        self.moveSpan=120
        self.lastMove=0
        self.lastStop=0
        self.stopSpan=180
        self.Fs=[] # the letter F the professor shoots
        
        self.images=[]
        self.images.append(loadImage(path+"/images/ProfessorWalking.png"))
        self.images.append(loadImage(path+"/images/ProfessorShooting.png"))
        
    def update(self):
        
        self.xRange = range(self.x-self.img_w//2,int(self.x-self.img_w//2+(self.img_w*1.5)))
        if self.isMoving and frameCount%8==0:
            self.frame=(self.frame+1)%self.num_frames
        
        # if the Professor is now stopped, check if he should move
        if not self.isMoving and frameCount>=self.lastStop+self.stopSpan:
            self.dir=random.choice([LEFT,RIGHT])
            self.isMoving=True
            self.lastMove=frameCount
            self.moveSpan=random.randint(120,300)
            
        # if the Professor is now moving, check if he should stop
        elif self.isMoving and frameCount>=self.moveSpan+self.lastMove:
            self.isMoving=False
            self.lastStop=frameCount
        
        # if the Professor stops, shoot the F every 4/6 seconds
        if not self.isMoving and frameCount%40==0:
            self.Fs.append(F(self.x,self.y-UGAP,50,100,100,4,0,0,3))

        if self.isMoving:
            self.x+=self.vx
            
        if self.x+self.r>WIDTH:
            self.vx*=-1
            self.dir=LEFT
        elif self.x-self.r<0:
            self.vx*=-1
            self.dir=RIGHT      
        
        # make sure the self.dir and the moving direction is coherent
        # becuase the direction of every move is decided randomly
        if self.dir==LEFT:
            self.vx=-abs(self.vx)
        elif self.dir==RIGHT:
            self.vx=abs(self.vx)
        
    def display(self):
        self.update()
        
        if len(self.Fs)>0:
            for f in self.Fs:
                f.display()
   
        if self.isMoving:
            # the condition for DOWN is to prevent bug because when the professor first appears he is facing down
            if self.dir==DOWN:
                self.dir=random.choice([RIGHT,LEFT])
                if self.dir==LEFT:
                    self.vx*=-1

            if self.dir==RIGHT:
                image(self.images[0], self.x-self.img_w//2+RGAP, self.y-self.img_h//2, self.img_w*1.5,self.img_h*1.5, self.img_w*self.frame, 0, (self.frame+1)*self.img_w,self.img_h)
            elif self.dir==LEFT:
                image(self.images[0], self.x-self.img_w//2+RGAP, self.y-self.img_h//2, self.img_w*1.5,self.img_h*1.5, (self.frame+1)*self.img_w, 0, self.img_w*self.frame, self.img_h)            
        
        else:
            image(self.images[1], self.x-self.img_w//2+RGAP,self.y-self.img_h//2, self.img_w*1.5, self.img_h*1.5, 0, 0, self.img_w, self.img_h)        



class Student(Creature):
    def __init__(self,x,y,r,g, w,h,num_frames):
        Creature.__init__(self,x,y,r,g,w,h,num_frames)
        # "a" for moving left
        # "d" for moving right
        # "w" for moving up (different from jump)
        # "s" for moving down
        # space for jumping
        
        self.key_handler={"a":False, "d":False, "w":False, "s":False, " ": False}
        self.bookLeft=6 #use to record how many books are left for shooting
        
        
        # There are three kinds of image to display the main character's movement
        # one is for moving left and right, and the other two are for moving upward (forward?) and downward (backward?)
        self.images=[]
        self.images.append(loadImage(path+"/images/StudentWalking.png"))
        self.images.append(loadImage(path+"/images/StudentWalkingForward.png"))
        self.images.append(loadImage(path+"/images/StudentWalkingBackward.png"))
        self.books=[]
        
        # there is one more argument for the main character class to distinguish the speed of moving up and jumping
        self.jump_y=0
        
        # this is changed once the student collides with an enemy
        self.slowed=False
        self.lastSlowed = 0
        
        # edit these speed values for easy debugging
        self.NormalSpeed = 4
        self.SlowSpeed = 2
        
        # keeps track of the wall above and below the player
        self.curWallUp = None
        self.curWallDown = None
        
    
    def shoot(self):
        # if the mouse is clicked
        # shoot the book in the direction of the unit vector created by the coordinates of the player and the mouse
        if self.bookLeft>0:
            self.bookLeft-=1
            self.books.append(Book(self.x,self.y,25,50,50,4,mouseX - RGAP,mouseY - UGAP,3))
   
    # the gravity method is applied only on the attribute jump_y instead of vy
    def gravity(self):
        if self.y+self.r>=self.g:
            self.jump_y=0
        else:
            self.jump_y+=0.4
            if self.y+self.r+self.jump_y>=self.g:
                self.jump_y=self.g-(self.y+self.r)
    
    def collidesWith(self,other):
        return dis(self.x,self.y,other.x,other.y) <= self.r + other.r and abs(self.g-other.y)<=62
    
    # I changed this part to make jumping between walls possible
    def collidesWithWall(self,wall):
        return self.g<=wall.yBottom and self.g>=wall.yAbsTop



    def update(self):
        self.displaypos = self.y-game.yshift+HEIGHT
        self.gravity()

        if self.key_handler["a"]==True and self.x-self.r>0:
            self.vx=0-self.NormalSpeed
            self.dir=LEFT
        elif self.key_handler["d"]==True and self.x+self.r<WIDTH:
            self.vx=self.NormalSpeed
            self.dir=RIGHT
        else:
            self.vx=0
        
        if self.key_handler["s"]==True and self.y+self.r<game.yshift:
            self.vy=self.NormalSpeed
            self.dir=DOWN    
        elif self.key_handler["w"]==True and self.y-self.r>game.yshift-HEIGHT:
            self.vy=0-self.NormalSpeed
            self.dir=UP
        else:
            self.vy=0
            
        
        
        # movement constraints
        if self.x-self.r < 0:
            self.x = 0 + self.r
        
        if self.x+self.r > WIDTH:
            self.x = WIDTH - self.r
        
        if self.y-self.r < game.yshift-HEIGHT:
            self.y = game.yshift-HEIGHT + self.r
            self.g=self.y+self.r
        
        moving = False
        for i in self.key_handler:
            moving = moving or self.key_handler[i]
        if not moving:
            self.vx=0
            self.vy=0
            
        # check for game over, when the player exits the screen on the bottom
        if self.displaypos > HEIGHT:
            game.StudentIsAlive = False
        
        # applies the slowed effect    
        if self.slowed:
            if self.vy > 0:
                self.vy = self.SlowSpeed
            if self.vy < 0:
                self.vy = 0-self.SlowSpeed
            if self.vx > 0:
                self.vx = self.SlowSpeed
            if self.vx < 0:
                self.vx = 0-self.SlowSpeed
                
        # takes out the slowed effect after six seconds
        if frameCount > self.lastSlowed + 360 or self.lastSlowed == 0:
            self.slowed = False
            
        # tests for collisions with cats
        for cat in game.cats:
            if self.collidesWith(cat):
                cat_sound.play()
                cat_sound.rewind()
                game.cats.remove(cat)
                self.slowed = True
                self.lastSlowed = frameCount
                
        # tests for collisions with walls
        # updates the current walls above and below
        for i in range(len(game.walls)):
            if game.walls[i].yAbsTop < self.y-self.r:
                self.curWallUp = game.walls[i]
                if i > 0:
                    self.curWallDown = game.walls[i-1] # naturally, the wall currently below the player would be the one before.
                break
        
        if self.curWallUp != None:
            if self.collidesWithWall(self.curWallUp):

                doorLeftLimit = self.curWallUp.doorX * 52
                doorRightLimit = (self.curWallUp.doorX+1) * 52
                
                if self.curWallUp.doorBroken and self.x > doorLeftLimit and self.x < doorRightLimit:
                    pass # it literally lets the character pass through
                else:
                    self.y = self.curWallUp.yBottom -self.r+1                      
                    self.g = self.y+self.r                        
        
        if self.curWallDown != None:
            if self.collidesWithWall(self.curWallDown):

                doorLeftLimit = self.curWallDown.doorX * 52
                doorRightLimit = (self.curWallDown.doorX+1) * 52
                
                if self.curWallDown.doorBroken and self.x > doorLeftLimit and self.x < doorRightLimit:
                    pass
                else:
                    self.g = self.curWallDown.yAbsTop
                    if self.jump_y==0:
                        self.y=self.g-self.r
        

        # jump movement control is independent
        if self.key_handler[" "]==True and self.y+self.r==self.g:
            jump_sound.play()
            jump_sound.rewind()
            self.jump_y=-6

        # move the ground according to the movement control by "w"
        # otherwise it would be considered as a jump
        if self.y==self.g-self.r: # this condition is to prevent the character keep moving up while jumping
            self.y+=self.vy    
            self.g+=self.vy 
        
        self.y+=self.jump_y
        self.x+=self.vx
        

        
        if frameCount%6 ==0 and (self.vx!=0 or self.vy!=0):
            self.frame=(self.frame+1)%self.num_frames
        
        # if a book flies out of the screen, delete it
        for book in self.books:
            if book.displaypos + UGAP < 0 or book.displaypos > HEIGHT or book.x < 0 or book.x > WIDTH:
                self.books.remove(book)
                
        # add a book to the student every three seconds
        if frameCount%180==0 and self.bookLeft+1<=6:
            self.bookLeft+=1

    def display(self):
        self.update()
        
        if self.isOnScreen():
            # display the image in four different ways according to student's moving direction
            if self.dir==RIGHT:
                image(self.images[0], RGAP + (self.x-self.img_w//2), UGAP + self.displaypos-self.img_h//2, self.img_w, self.img_h, self.frame*self.img_w,0, (self.frame+1)*self.img_w,self.img_h)
            elif self.dir==LEFT:
                image(self.images[0], RGAP + (self.x-self.img_w//2), UGAP + self.displaypos-self.img_h//2, self.img_w, self.img_h, (self.frame+1)*self.img_w,0, self.frame*self.img_w,self.img_h)
            elif self.dir==UP:
                image(self.images[2], RGAP + (self.x-self.img_w//2), UGAP + self.displaypos-self.img_h//2, self.img_w, self.img_h, self.frame*self.img_w,0, (self.frame+1)*self.img_w,self.img_h)
            elif self.dir==DOWN:
                image(self.images[1], RGAP + (self.x-self.img_w//2), UGAP + self.displaypos-self.img_h//2, self.img_w, self.img_h, self.frame*self.img_w,0, (self.frame+1)*self.img_w,self.img_h)
            
            # display the books that have been shot
            if len(self.books)>0:
                for book in self.books:
                    book.display()
                    
            
            
class Game:
    def __init__(self, w, h, g):
        self.w=w
        self.h=h
        self.g=g
        self.ProfIsAlive = True
        self.ProfIsInstantiated = False
        self.StudentIsAlive = True
        self.yshift = 100000
        self.vyshift = -0.35
        self.student=Student(100,99800,26,self.g, 64 ,52, 9) ###
        self.inPauseScreen = True
        self.starting = True
        self.titleScreen = loadImage(path+"/images/TitleScreen.png")
        
        self.booksBar=BooksBar(WIDTH+RGAP+20,300,626,185)
        self.wallTile = loadImage(path+"/images/WallPiece.png")
        self.doorTile = loadImage(path+"/images/door.png")
        
        self.nextGeneration = 100000 ####
        self.bg = loadImage(path+"/images/PalmsFloortiles.png")
        self.uframebg = loadImage(path+"/images/BridgeBackground.png")
        self.uframefg = loadImage(path+"/images/BridgeForeground.png")
        self.uframeside = loadImage(path+"/images/BridgeSide.png")
        self.bgypos = 0
        self.rframe = loadImage(path+"/images/PixelArtA4.png")
        
        # pixels the screen has to advance before starting the boss battle
        # change this to 500 to make the game way easier and faster
        self.targetValue = 1800
        
        #showing how many progress left to meet the professor
        self.progressBar=ProgressBar(WIDTH+RGAP+24, 350, 120, 20, self.targetValue, self.yshift)
        
        # initialises cat list, they are spawned with each wall in the wall list
        self.cats=[]
        self.walls=[]
        
        #self.background_sound=player.loadFile(path+"/sounds/background.mp3")
        background_sound.rewind()

    
    def update(self):
        
        # generates 1000 pixels of walls at a time, to save memory. The walls have randomly generated gaps.
        if self.yshift < self.nextGeneration:
            self.nextGeneration = self.nextGeneration - 1000
            yshift = int(self.yshift)
            for i in range(yshift-750, yshift-1750, -100):            
                self.walls.append(Wall(i))
                for j in range(random.randint(1,2)): # spawn 1 to 2 cats below the wall
                    self.cats.append(Cat(random.randint(40,WIDTH-40), random.randint(i,i+30), 13, 0, 32, 26, 3))
        
        # increments the yshift speed by 0.02 every 5 seconds
        if frameCount % 300 == 0:
            self.vyshift -= 0.02
            
        # when yshift has advanced 3500 pixels (ie. 25 walls), instantiate the professor
        # TODO remember to change the value when submitting!!!
        
        if self.yshift < 100000-self.targetValue and not self.ProfIsInstantiated:
            electric_sound.play()
            electric_sound.rewind()
            background_sound.pause()
            
            self.ProfIsInstantiated = True
            self.inPauseScreen = True
            # "BOSS BATTLE" screen, pause, restart loop when clicked

            noLoop()
            noStroke()
            fill(0,150)
            rect(0,200,WIDTH+(RGAP*2),(HEIGHT+UGAP)//2)
            textSize(40)
            fill(255)
            text("YOU FOUND THE EVIL PROFESSOR", 210, 300)
            textSize(30)
            text("He's the one that put all these obstacles!", 210, 360)
            text("It's payback time! To defeat him,", 210, 390)
            text("hit him with a notebook.", 210, 420)
            text("-click to start Boss Battle-", 210, 480)
            
            
            self.professor=Professor(WIDTH//2,30,26,100,64,52,9)
            
        if not self.ProfIsAlive:
            background_sound.pause()
            background_sound.rewind()
            win_sound.play()
            win_sound.rewind()
            noLoop()
            # here's what happens when prof dies
            noStroke()
            fill(0,150)
            rect(0,200,WIDTH+(RGAP*2),(HEIGHT+UGAP)//2)
            textSize(40)
            fill(255)
            text("YOU WIN", 210, 300)
            textSize(30)
            text("You hit the professor across the face", 210, 360)
            text("with a notebook.", 210, 390)
            text("In retrospective, that was probably not", 210, 450)
            text("the smartest idea ever. The VC is waiting", 210, 480)
            text("for you in her office.", 210, 510)
            text("-click to play again-", 210, 570)
            
        
        if not self.StudentIsAlive:
            background_sound.pause()
            background_sound.rewind()
            fail_sound.play()
            fail_sound.rewind()
            noLoop()
            # here's what happens when the student dies
            noStroke()
            fill(0,150)
            rect(0,200,WIDTH+(RGAP*2),(HEIGHT+UGAP)//2)
            textSize(40)
            fill(255)
            text("YOU LOSE", 210, 300)
            textSize(30)
            text("You didn't get to class in time.", 210, 360)
            text("Attendance was 15% of the grade.", 210, 390)
            text("-click to restart-", 210, 450)
            
        if self.starting:
            noLoop()
            image(game.titleScreen, 0, 0)
            
            
        
    def display(self):
        # background display
        # in case you didn't notice, we tried to reproduce the tiling pattern of the area around the palms c:
        
        if self.bgypos >= HEIGHT:
            self.bgypos = 0
            image(self.bg, RGAP + 0, UGAP + self.bgypos)
        else:
            image(self.bg, RGAP + 0, UGAP + self.bgypos, 520, HEIGHT-self.bgypos, 0, 0, 520, int(HEIGHT-self.bgypos))
            image(self.bg, RGAP + 0, UGAP + 0, 520, self.bgypos, 0, int(HEIGHT-self.bgypos), 520, HEIGHT)
        
        #display the image on the right and left
        image(self.rframe, 0, UGAP + 0, 206, 720, 206, 0, 0, 720)
        image(self.rframe, RGAP + 520, UGAP + 0)
        
        
        self.yshift += self.vyshift
        self.bgypos -= self.vyshift
        for wall in self.walls:
            wall.display()
        
        
        
        # upper frame display
        image(self.uframeside, 0, 0, 206, 100)
        image(self.uframeside, WIDTH+RGAP, 0, 206, 100)
        image(self.uframebg, RGAP, 0)
        if self.ProfIsInstantiated:
            self.professor.display()
        image(self.uframefg, RGAP, 0)
        image(self.uframefg, 0, 0, 206, 100, 0, 0, 206, 100)
        image(self.uframefg, WIDTH+RGAP, 0, 206, 100, 0, 0, 206, 100)
        for cat in self.cats:
            cat.display()
        self.student.display()
        self.booksBar.display()
        self.progressBar.display()
        

        
        self.update()
        
        
game=Game(WIDTH,HEIGHT,700)

def setup():
    size(WIDTH+(RGAP*2),HEIGHT+UGAP)


def draw():
    background(255,255,255)
    game.display()

    
    
def keyPressed():
    if key=='a':
        game.student.key_handler['a']=True
    elif key=='d':
        game.student.key_handler['d']=True
    elif key=='w':
        game.student.key_handler['w']=True
    elif key=='s':
        game.student.key_handler['s']=True
    elif key==' ':
        game.student.key_handler[' ']=True

def keyReleased():
    if key=='a':
        game.student.key_handler['a']=False
    elif key=='d':
        game.student.key_handler['d']=False
    elif key=='w':
        game.student.key_handler['w']=False
    elif key=='s':
        game.student.key_handler['s']=False
    elif key==' ':
        game.student.key_handler[' ']=False

def mouseClicked():
    global game
    # game over
    if not game.StudentIsAlive or not game.ProfIsAlive:
        background_sound.pause()
        fail_sound.pause()
        fail_sound.rewind()
        game = Game(WIDTH,HEIGHT,700)
        loop()
    # click for shooting
    elif not game.inPauseScreen and game.StudentIsAlive:
        game.student.shoot()
        
    # click to resume the game
    elif game.inPauseScreen:
        electric_sound.pause()
        electric_sound.rewind()
        background_sound.loop()
        loop()
        game.inPauseScreen = False
        game.starting = False
