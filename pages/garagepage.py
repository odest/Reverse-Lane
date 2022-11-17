import pygame,random,json

class GaragePage():
    def __init__(self,screen,size,list):
    	with open("docs/data.json","+r") as text:
    		self.data=json.load(text)
    	with open("docs/default.json","+r") as text:
    		self.default=json.load(text)
    		
    	if self.default['songAndSfx']=="on":
    		self.buttonSfx=pygame.mixer.Sound("sources/sounds/buttonSfx.wav")
    		self.panelSfx=pygame.mixer.Sound("sources/sounds/panelSfx.wav")
    		self.optionSfx=pygame.mixer.Sound("sources/sounds/optionSfx.wav")
    		self.buttonSfxStation=self.panelSfxStation=self.optionSfxStation=True
    	else:self.buttonSfxStation=self.panelSfxStation=self.optionSfxStation=False
    		
    	self.screen=screen
    	self.screenWidth,self.screenHeight =size[0],size[1]
    	self.fontOne="sources/fonts/edge.otf"
    	self.fontTwo="sources/fonts/glass.ttf"
    	self.bigFont = pygame.font.Font(self.fontOne, round(self.screenWidth*250/720))
    	self.middleFont = pygame.font.Font(self.fontOne, round(self.screenWidth*40/720))
    	self.smallFont = pygame.font.Font(self.fontOne, round(self.screenWidth*25/720))
    	self.minimalFont = pygame.font.Font(self.fontTwo, round(self.screenWidth*25/720))
    	self.playerImageCount=self.default['playerImageCount']
    	self.playerColorCount=self.default['playerColorCount']
    	self.playerImageList=list
    	self.playerImageWidth,self.playerImageHeight=self.screenWidth*300/720,self.screenHeight*620/1280
    	self.playerPriceTextList=[self.smallFont.render(self.data['playerDict']['prices'][i], True,"cyan") for  i in range(6)]
    	self.selectText=self.middleFont.render(self.data['language']['select'][self.default['language']], True,"cyan")
    	self.nextTextColor="dark green"
    	self.prevTextColor="dark green"
    	self.selectCircleCoords=[35,50,65]
    	
    	self.darkBackgroundImageOne=pygame.transform.scale(pygame.image.load("sources/images/darkBackground.png"),(int(self.screenWidth),int(self.screenHeight)))
    	self.darkBackgroundImageTwo=pygame.transform.scale(self.darkBackgroundImageOne,(int(80*self.screenWidth/100),int(80*self.screenHeight/100)))
    	self.normalPanelRightImage=pygame.transform.scale(pygame.image.load("sources/images/panelGreen.png"),(round(60*(self.screenWidth/288)),round(34*(self.screenHeight/512))))
    	self.normalPanelLeftImage=pygame.transform.rotate(self.normalPanelRightImage,180)
    	self.hoverPanelRightImage=pygame.transform.scale(pygame.image.load("sources/images/panelHover.png"),(round(60*(self.screenWidth/288)),round(34*(self.screenHeight/512))))
    	self.hoverPanelLeftImage=pygame.transform.rotate(self.hoverPanelRightImage,180)
    	self.normalButtonImage=pygame.transform.scale(pygame.image.load("sources/images/buttonNormal.png"),(round(self.screenWidth*350/720),round(self.screenHeight*117/1280)))
    	self.hoverButtonImage=pygame.transform.scale(pygame.image.load("sources/images/buttonHover.png"),(round(self.screenWidth*350/720),round(self.screenHeight*117/1280)))
    	
    	self.selectButtonImage=self.normalButtonImage
    	self.backToHomeButtonImage=self.normalPanelLeftImage
    	self.infoButtonImage=self.normalPanelRightImage
    	self.infoButtonVisibilityCount=0
    	self.infoButtonVisibilityStation=self.default['garagePageInfoButtonVisibilityStation']
    	self.showNotesStation=False
    	
    	self.speedText=self.smallFont.render(self.data['language']['speed'][self.default['language']], True,"cyan")
    	self.handlingText=self.smallFont.render(self.data['language']['handling'][self.default['language']], True,"cyan")
    	self.brakingText=self.smallFont.render(self.data['language']['braking'][self.default['language']], True,"cyan")
    	self.nameText=self.middleFont.render("R E V E R S E   L A N E", True,"cyan")
    	self.secondNameText=pygame.font.Font(self.fontTwo, round(self.screenWidth*18/720)).render("UNLIMITED SUPERCAR EDITION", True,(63,128,128))
    	

    def draw(self):
    	self.screen.blit(self.nameText,(self.screenWidth/2-self.nameText.get_size()[0]/2,1.8*self.screenHeight/100))
    	self.screen.blit(self.secondNameText,(self.screenWidth/2-self.secondNameText.get_size()[0]/2,5*self.screenHeight/100))
    	
    	self.screen.blit(pygame.transform.scale(self.playerImageList[self.playerImageCount][self.playerColorCount],(round(self.screenWidth*300/720),round(self.screenHeight*620/1280))),(self.screenWidth/2-self.playerImageWidth/2,self.screenHeight/5))
    	self.playerNameTextList=[self.middleFont.render(self.data['playerDict']['texts'][i], True,self.data['playerDict']['colors'][self.playerImageCount][self.playerColorCount]) for i in range(6)]
    	self.screen.blit(self.playerNameTextList[self.playerImageCount],(self.screenWidth/2-self.playerNameTextList[self.playerImageCount].get_size()[0]/2,13*self.screenHeight/100))
    	self.screen.blit(self.playerPriceTextList[self.playerImageCount],(self.screenWidth/2-self.playerPriceTextList[self.playerImageCount].get_size()[0]/2,17*self.screenHeight/100))
    	
    	self.selectButton=self.screen.blit(self.selectButtonImage,(self.screenWidth/2-self.normalButtonImage.get_size()[0]/2,89.5*self.screenHeight/100))
    	self.selectLabel=self.screen.blit(self.selectText,(self.screenWidth/2-self.selectText.get_size()[0]/2,92.5*self.screenHeight/100))
    	self.prevButton=self.screen.blit(self.bigFont.render("<", True,self.prevTextColor),(10*self.screenWidth/100,36*self.screenHeight/100))
    	self.nextButton=self.screen.blit(self.bigFont.render(">", True,self.nextTextColor),(80*self.screenWidth/100,36*self.screenHeight/100))
    	
    	self.screen.blit(self.speedText,(5*self.screenWidth/100,79*self.screenHeight/100))
    	self.screen.blit(self.handlingText,(5*self.screenWidth/100,82.5*self.screenHeight/100))
    	self.screen.blit(self.brakingText,(5*self.screenWidth/100,86*self.screenHeight/100))
    	
    	pygame.draw.rect(self.screen,self.data['playerDict']['colors'][self.playerImageCount][self.playerColorCount],(28*self.screenWidth/100,79*self.screenHeight/100,self.data['playerDict']['features'][self.playerImageCount][0]/45*5*self.screenWidth/100,2.1*self.screenHeight/100))
    	pygame.draw.rect(self.screen,self.data['playerDict']['colors'][self.playerImageCount][self.playerColorCount],(28*self.screenWidth/100,82.4*self.screenHeight/100,self.data['playerDict']['features'][self.playerImageCount][1]*4*self.screenWidth/100,2.1*self.screenHeight/100))
    	pygame.draw.rect(self.screen,self.data['playerDict']['colors'][self.playerImageCount][self.playerColorCount],(28*self.screenWidth/100,85.8*self.screenHeight/100,self.data['playerDict']['features'][self.playerImageCount][2]/2*self.screenWidth/100,2.1*self.screenHeight/100))
    	
    	pygame.draw.rect(self.screen,"cyan",(28*self.screenWidth/100,79*self.screenHeight/100,57*self.screenWidth/100,2.1*self.screenHeight/100),2)
    	pygame.draw.rect(self.screen,"cyan",(28*self.screenWidth/100,82.4*self.screenHeight/100,57*self.screenWidth/100,2.1*self.screenHeight/100),2)
    	pygame.draw.rect(self.screen,"cyan",(28*self.screenWidth/100,85.8*self.screenHeight/100,57*self.screenWidth/100,2.1*self.screenHeight/100),2)
    	
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*25/720)).render(str(self.data['playerDict']['features'][self.playerImageCount][0]), True,"cyan"),(86.5*self.screenWidth/100,79.2*self.screenHeight/100))
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*15/720)).render("km/h", True,"cyan"),(93*self.screenWidth/100,79.6*self.screenHeight/100))
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*25/720)).render("{}/10".format(self.data['playerDict']['features'][self.playerImageCount][1]), True,"cyan"),(86.5*self.screenWidth/100,82.6*self.screenHeight/100))
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*25/720)).render("{}/100".format(self.data['playerDict']['features'][self.playerImageCount][2]), True,"cyan"),(86.5*self.screenWidth/100,86*self.screenHeight/100))
    	
    	self.leftCircleButton=pygame.draw.circle(self.screen,self.data['playerDict']['colors'][self.playerImageCount][1],[self.selectCircleCoords[0]*self.screenWidth/100,73.5*self.screenHeight/100],self.screenWidth*30/720, 0)
    	self.middleCircleButton=pygame.draw.circle(self.screen,self.data['playerDict']['colors'][self.playerImageCount][0],[self.selectCircleCoords[1]*self.screenWidth/100,73.5*self.screenHeight/100],self.screenWidth*30/720, 0)
    	self.rightCircleButton=pygame.draw.circle(self.screen,self.data['playerDict']['colors'][self.playerImageCount][2],[self.selectCircleCoords[2]*self.screenWidth/100,73.5*self.screenHeight/100],self.screenWidth*30/720, 0)
    	self.circleButtonList=[self.middleCircleButton,self.leftCircleButton,self.rightCircleButton]
    	self.select_circle=pygame.draw.circle(self.screen,"cyan",self.circleButtonList[self.playerColorCount].center,self.screenWidth*35/720,3)
    	
    	if self.infoButtonVisibilityStation:
    		self.infoButtonVisibilityCount+=1
    		if self.infoButtonVisibilityCount==15:self.infoButtonImage=self.hoverPanelRightImage
    		elif self.infoButtonVisibilityCount==25:self.infoButtonImage=self.normalPanelRightImage
    		elif self.infoButtonVisibilityCount>25:self.infoButtonVisibilityCount=0
    	
    	self.backToHomeButton=self.screen.blit(self.backToHomeButtonImage,(0,0))
    	self.infoButton=self.screen.blit(self.infoButtonImage,(self.screenWidth-self.normalPanelRightImage.get_size()[0],0))
    	self.backToHomeLabel=self.screen.blit(self.smallFont.render(self.data['language']['back'][self.default['language']], True,"cyan"),(5*self.screenWidth/100,2.4*self.screenHeight/100))
    	self.infoLabel=self.screen.blit(self.smallFont.render(self.data['language']['info'][self.default['language']],True,"cyan"),(86*self.screenWidth/100,2.4*self.screenHeight/100))
    	if self.showNotesStation:self.__showNotes()
    
    	
    def check(self,position,station,keyboard):
    	if self.showNotesStation:
    		self.position=position
    		if self.xLabel.collidepoint(self.position) or keyboard=="x":
    			self.showNotesStation=False
    			self.default['garagePageInfoButtonVisibilityStation']=self.infoButtonVisibilityStation
    			with open("docs/default.json", "w") as f:f.write(json.dumps(self.default))
    		self.station=None
    		self.keyboard=None
    	elif self.showNotesStation==False:
	    	self.position=position
	    	self.station=station
	    	self.keyboard=keyboard
	    	
    	if self.station=="down":
    		if self.nextButton.collidepoint(self.position) or self.keyboard=="right":
    			self.__playSfx("option")
    			self.nextTextColor="green"
    		elif self.prevButton.collidepoint(self.position) or self.keyboard=="left":
    			self.__playSfx("option")
    			self.prevTextColor="green"
    		elif self.backToHomeButton.collidepoint(position) or self.backToHomeLabel.collidepoint(self.position) or self.keyboard=="backToHome":
    			self.__playSfx("panel")
    			self.backToHomeButtonImage=self.hoverPanelLeftImage
    		elif self.infoButton.collidepoint(self.position) or self.infoLabel.collidepoint(self.position) or self.keyboard=="info":
    			self.__playSfx("panel")
    			self.infoButtonImage=self.hoverPanelRightImage
    		elif self.selectButton.collidepoint(self.position) or self.selectLabel.collidepoint(self.position) or self.keyboard=="enter":
    			self.__playSfx("button")
    			self.selectButtonImage=self.hoverButtonImage
    		
    	elif self.station=="up":
    		if self.default['songAndSfx']=="on":self.buttonSfxStation=self.panelSfxStation=self.optionSfxStation=True
    		self.nextTextColor="dark green"
    		self.prevTextColor="dark green"
    		self.selectButtonImage=self.normalButtonImage
    		self.backToHomeButtonImage=self.normalPanelLeftImage
    		self.infoButtonImage=self.normalPanelRightImage
    		if self.nextButton.collidepoint(self.position) or self.keyboard=="right":
    			self.playerColorCount=0
    			self.playerImageCount+=1
    			if self.playerImageCount==6:self.playerImageCount=0
    		elif self.prevButton.collidepoint(self.position) or self.keyboard=="left":
    			self.playerColorCount=0
    			self.playerImageCount-=1
    			if self.playerImageCount==-6:self.playerImageCount=0
    		elif self.leftCircleButton.collidepoint(self.position) or self.keyboard=="one":
    			self.__playSfx("option")
    			self.playerColorCount=1
	    	elif self.middleCircleButton.collidepoint(self.position) or self.keyboard=="two":
	    		self.__playSfx("option")
	    		self.playerColorCount=0
	    	elif self.rightCircleButton.collidepoint(self.position) or self.keyboard=="three":
	    		self.__playSfx("option")
	    		self.playerColorCount=2
	    	elif self.backToHomeButton.collidepoint(self.position) or self.backToHomeLabel.collidepoint(self.position) or self.keyboard=="backToHome":return "home"
    		elif self.infoButton.collidepoint(self.position) or self.infoLabel.collidepoint(self.position) or self.keyboard=="info":self.showNotesStation=True
    		elif self.selectButton.collidepoint(self.position) or self.selectLabel.collidepoint(self.position) or self.keyboard=="enter":
    			self.default['playerImageCount']=self.playerImageCount
    			self.default['playerColorCount']=self.playerColorCount
    			with open("docs/default.json", "w") as f:
    				f.write(json.dumps(self.default))
    			return "home"
    			
    			
    def __playSfx(self,which):
    	if which=="button" and self.buttonSfxStation:
    		self.buttonSfx.play()
    		self.buttonSfxStation=False
    	elif which=="option" and self.optionSfxStation:
    		self.optionSfx.play()
    		self.optionSfxStation=False
    	elif which=="panel" and self.panelSfxStation:
    		self.panelSfx.play()
    		self.panelSfxStation=False
    			
    		
    def __showNotes(self):
    	self.infoButtonVisibilityStation=False
    	self.infoButtonImage=self.normalPanelRightImage
    	self.notesText=pygame.font.Font(self.fontOne,round(self.screenWidth*63/720)).render(self.data['language']['notes'][self.default['language']], True,"cyan")
    	self.screen.blit(self.darkBackgroundImageOne,(0,0))
    	self.screen.blit(self.darkBackgroundImageTwo,(10*self.screenWidth/100,10*self.screenHeight/100))
    	self.screen.blit(self.notesText,(self.screenWidth/2-self.notesText.get_size()[0]/2,15*self.screenHeight/100))
    	self.xLabel=self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*65/720)).render("X", True,"red"),(80.5*self.screenWidth/100,11*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(15,15,15),(20*self.screenWidth/100,23*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(0,138,138),(20*self.screenWidth/100,23*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100),1)
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*64/720)).render("<", True,"cyan"),(27.5*self.screenWidth/100,22.5*self.screenHeight/100))
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*32/720)).render("L E F T", True,(0,138,138)),(23*self.screenWidth/100,26.5*self.screenHeight/100))
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*60/720)).render("/", True,(0,138,138)),(48*self.screenWidth/100,24*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(15,15,15),(60*self.screenWidth/100,23*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(0,138,138),(60*self.screenWidth/100,23*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100),1)
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*60/720)).render(">", True,"cyan"),(68*self.screenWidth/100,22.5*self.screenHeight/100))
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*32/720)).render("R I G H T", True,(0,138,138)),(61*self.screenWidth/100,26.5*self.screenHeight/100))
    	self.tempTextOne=pygame.font.Font(self.fontTwo,round(self.screenWidth*21/720)).render(self.data['language']['garagePageUpDownText'][self.default['language']], True,"cyan")
    	self.screen.blit(self.tempTextOne,(self.screenWidth/2-self.tempTextOne.get_size()[0]/2,32*self.screenHeight/100))
    	
    	pygame.draw.rect(self.screen,(15,15,15),(20*self.screenWidth/100,38*self.screenHeight/100,14*self.screenWidth/100,7*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(0,138,138),(20*self.screenWidth/100,38*self.screenHeight/100,14*self.screenWidth/100,7*self.screenHeight/100),1)
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*50/720)).render("1", True,"cyan"),(25*self.screenWidth/100,39.5*self.screenHeight/100))
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*60/720)).render("/", True,(0,138,138)),(36*self.screenWidth/100,39*self.screenHeight/100))
    	
    	pygame.draw.rect(self.screen,(15,15,15),(43*self.screenWidth/100,38*self.screenHeight/100,14*self.screenWidth/100,7*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(0,138,138),(43*self.screenWidth/100,38*self.screenHeight/100,14*self.screenWidth/100,7*self.screenHeight/100),1)
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*50/720)).render("2", True,"cyan"),(48*self.screenWidth/100,39.5*self.screenHeight/100))
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*60/720)).render("/", True,(0,138,138)),(59*self.screenWidth/100,39*self.screenHeight/100))
    	
    	pygame.draw.rect(self.screen,(15,15,15),(66*self.screenWidth/100,38*self.screenHeight/100,14*self.screenWidth/100,7*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(0,138,138),(66*self.screenWidth/100,38*self.screenHeight/100,14*self.screenWidth/100,7*self.screenHeight/100),1)
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*50/720)).render("3", True,"cyan"),(71*self.screenWidth/100,39.5*self.screenHeight/100))
    	
    	self.tempTextTwo=pygame.font.Font(self.fontTwo,round(self.screenWidth*20/720)).render(self.data['language']['garagePageLeftRightText'][self.default['language']], True,"cyan")
    	self.screen.blit(self.tempTextTwo,(self.screenWidth/2-self.tempTextTwo.get_size()[0]/2,47*self.screenHeight/100))
    	
    	pygame.draw.rect(self.screen,(15,15,15),(20*self.screenWidth/100,53*self.screenHeight/100,14*self.screenWidth/100,7*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(0,138,138),(20*self.screenWidth/100,53*self.screenHeight/100,14*self.screenWidth/100,7*self.screenHeight/100),1)
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*50/720)).render("H", True,"cyan"),(25*self.screenWidth/100,54.5*self.screenHeight/100))
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*60/720)).render("/", True,(0,138,138)),(36*self.screenWidth/100,54*self.screenHeight/100))
    	
    	pygame.draw.rect(self.screen,(15,15,15),(43*self.screenWidth/100,53*self.screenHeight/100,14*self.screenWidth/100,7*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(0,138,138),(43*self.screenWidth/100,53*self.screenHeight/100,14*self.screenWidth/100,7*self.screenHeight/100),1)
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*50/720)).render("I", True,"cyan"),(48*self.screenWidth/100,54.5*self.screenHeight/100))
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*60/720)).render("/", True,(0,138,138)),(59*self.screenWidth/100,54*self.screenHeight/100))
    	
    	pygame.draw.rect(self.screen,(15,15,15),(66*self.screenWidth/100,53*self.screenHeight/100,14*self.screenWidth/100,7*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(0,138,138),(66*self.screenWidth/100,53*self.screenHeight/100,14*self.screenWidth/100,7*self.screenHeight/100),1)
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*50/720)).render("X", True,"cyan"),(71*self.screenWidth/100,54.5*self.screenHeight/100))
    	
    	self.keyHText=pygame.font.Font(self.fontTwo,round(self.screenWidth*20/720)).render(self.data['language']['garagePageKeyText'][self.default['language']]['h'], True,"cyan")
    	self.keyIText=pygame.font.Font(self.fontTwo,round(self.screenWidth*20/720)).render(self.data['language']['garagePageKeyText'][self.default['language']]['i'], True,"cyan")
    	self.keyXText=pygame.font.Font(self.fontTwo,round(self.screenWidth*20/720)).render(self.data['language']['garagePageKeyText'][self.default['language']]['x'], True,"cyan")
    	
    	self.screen.blit(self.keyHText,(self.screenWidth/2-self.keyHText.get_size()[0]/2,62*self.screenHeight/100))
    	self.screen.blit(self.keyIText,(self.screenWidth/2-self.keyIText.get_size()[0]/2,64*self.screenHeight/100))
    	self.screen.blit(self.keyXText,(self.screenWidth/2-self.keyXText.get_size()[0]/2,66*self.screenHeight/100))
    	
    	pygame.draw.rect(self.screen,(15,15,15),(30*self.screenWidth/100,72*self.screenHeight/100,40*self.screenWidth/100,7*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(0,138,138),(30*self.screenWidth/100,72*self.screenHeight/100,40*self.screenWidth/100,7*self.screenHeight/100),1)
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*40/720)).render("E N T E R", True,"cyan"),(38*self.screenWidth/100,74*self.screenHeight/100))
    	self.tempTextThree=pygame.font.Font(self.fontTwo,round(self.screenWidth*25/720)).render(self.data['language']['garagePageEnterText'][self.default['language']], True,"cyan")
    	self.screen.blit(self.tempTextThree,(self.screenWidth/2-self.tempTextThree.get_size()[0]/2,81*self.screenHeight/100))