import pygame,json

class SplashScreen():
    def __init__(self,screen,size,list):
        with open("docs/default.json","+r") as text:
        	self.default=json.load(text)
        with open("docs/data.json","+r") as text:
        	self.data=json.load(text)
        	
        self.screen=screen
        self.screenWidth,self.screenHeight=size[0],size[1]
        self.playerImageList=list
        self.playerImageCount=self.default['playerImageCount']
        self.playerColorCount=self.default['playerColorCount']
        self.infoTextVisibility=True
        self.infoTextVisibilityCount=0
        
        self.tireRustImage=pygame.transform.scale(pygame.image.load("sources/images/tireRust.jpg"),(self.screenWidth,self.screenHeight))
        self.playerImage=pygame.transform.scale(self.playerImageList[self.playerImageCount][self.playerColorCount],(round(self.screenWidth*400/720),round(self.screenHeight*827/1280)))
        self.playerX,self.playerY=self.screenWidth/2-self.playerImage.get_size()[0]/2,self.screenHeight-self.playerImage.get_size()[1]/2
        
        self.font = pygame.font.Font("sources/fonts/edge.otf", round(self.screenWidth*120/720))
        self.reverseText=self.font.render("R E V E R S E", True,"cyan")
        self.laneText=self.font.render("L  A  N  E", True,"cyan")
        self.infoText=pygame.font.Font("sources/fonts/glass.ttf", round(self.screenWidth*20/720)).render(self.data['language']['splashScreenInfoText'][self.default['language']], True,"cyan")
        self.reverseTextX,self.reverseTextY=self.screenWidth/2-self.reverseText.get_size()[0]/2,self.playerImage.get_size()[1]-self.reverseText.get_size()[1]
        
        
    def draw(self,clicked):
        self.screen.blit(self.tireRustImage,(0,0))
        self.screen.blit(self.reverseText,(self.reverseTextX,self.reverseTextY))
        self.screen.blit(self.laneText,(self.screenWidth/2-self.laneText.get_size()[0]/2,14.5*self.screenHeight/100))
        self.screen.blit(self.playerImage,(self.playerX,self.playerY))
        
        if self.infoTextVisibility and clicked:self.screen.blit(self.infoText,(self.screenWidth/2-self.infoText.get_size()[0]/2,97.65*self.screenHeight/100))
        self.infoTextVisibilityCount+=1
        if self.infoTextVisibilityCount==10:self.infoTextVisibility=False
        elif self.infoTextVisibilityCount==15:self.infoTextVisibility=True
        elif self.infoTextVisibilityCount>15:self.infoTextVisibilityCount=0
        
        
    def move(self):
        if self.playerY>round(self.laneText.get_size()[1]*1.9):
            self.playerY-=5
            self.reverseTextY-=5
            self.screen.blit(self.playerImage,(self.playerX,self.playerY))
            self.screen.blit(self.reverseText,(self.reverseTextX,self.reverseTextY))
        else:return "start"