import pygame,random,json
from pygame import mixer

class HomePage():
	def __init__(self,screen,size,list,where):
		with open("docs/data.json","+r") as text:
			self.data=json.load(text)
		with open("docs/default.json","+r") as text:
			self.default=json.load(text)
			
		if self.default['songAndSfx']=="on":
			self.buttonSfxStation=True
			self.buttonSfx=pygame.mixer.Sound("sources/sounds/buttonSfx.wav")
		else:self.buttonSfxStation=False
		
		self.playerImageCount=self.default['playerImageCount']
		self.player_color_count=self.default['playerColorCount']
		self.homePageAnimationStation=where
		self.playerImageList=list
		self.screen=screen
		self.screenWidth,self.screenHeight=size[0],size[1]
		self.onDraw=False
		self.drawAll=False
		self.clicked=True
		self.fontOne="sources/fonts/edge.otf"
		self.fontTwo="sources/fonts/glass.ttf"
		
		self.minimalFont = pygame.font.Font(self.fontTwo, round(self.screenWidth*18/720))
		self.middleFont = pygame.font.Font(self.fontOne, round(self.screenWidth*40/720))
		self.bigFont = pygame.font.Font(self.fontOne, round(self.screenWidth*100/720))
		
		self.backgroundImage=pygame.transform.scale(pygame.image.load("sources/images/darkBackground.png"),(self.screenWidth,self.screenHeight))
		self.tireRustImage=pygame.transform.scale(pygame.image.load("sources/images/tireRust.png"),(self.screenWidth,self.screenHeight))
		self.playerImage=pygame.transform.scale(self.playerImageList[self.playerImageCount][self.player_color_count],(round(self.screenWidth*400/720),round(self.screenHeight*827/1280)))
		self.playerWidth,self.playerHeight=self.playerImage.get_size()
		
		if self.homePageAnimationStation=="from bottom":self.playerY=self.screenHeight
		elif self.homePageAnimationStation=="from middle":
			self.drawAll=True
			self.playerY=self.screenHeight/2-self.playerHeight/2
		
		self.normalButtonImage=pygame.transform.scale(pygame.image.load("sources/images/buttonNormal.png"),(round(self.screenWidth*350/720),round(self.screenHeight*117/1280)))
		self.hoverButtonImage=pygame.transform.scale(pygame.image.load("sources/images/buttonHover.png"),(round(self.screenWidth*350/720),round(self.screenHeight*117/1280)))
		self.buttonWidth,self.buttonHeight=self.normalButtonImage.get_size()
		
		self.playText=self.middleFont.render(self.data['language']['play'][self.default['language']], True,"cyan")
		self.garageText=self.middleFont.render(self.data['language']['garage'][self.default['language']], True,"cyan")
		self.settingsText=self.middleFont.render(self.data['language']['settings'][self.default['language']], True,"cyan")
		self.ceoNameText=self.minimalFont.render("destrochloridium", True,(55,87,87))
		self.nameText=self.middleFont.render("R E V E R S E   L A N E", True,"cyan")
		self.secondNameText=self.minimalFont.render("UNLIMITED SUPERCAR EDITION", True,(63,128,128))
		
		self.showNotes=self.default['showHomePageNotes']
		if self.showNotes:
			self.pText=pygame.font.Font(self.fontTwo, round(self.screenWidth*25/720)).render(self.data['language']['pressP'][self.default['language']], True,(0,138,138))
			self.gText=pygame.font.Font(self.fontTwo, round(self.screenWidth*25/720)).render(self.data['language']['pressG'][self.default['language']], True,(0,138,138))
			self.sText=pygame.font.Font(self.fontTwo, round(self.screenWidth*25/720)).render(self.data['language']['pressS'][self.default['language']], True,(0,138,138))
			self.qText=pygame.font.Font(self.fontTwo, round(self.screenWidth*25/720)).render(self.data['language']['pressQ'][self.default['language']], True,(0,138,138))
			self.timeBarWidth=70*self.screenWidth/100
			
	
	def drawAllFunction(self):
		self.onDraw=True
		self.screen.blit(self.tireRustImage,(0,self.playerY+self.playerHeight-self.screenWidth*50/720))
		self.screen.blit(self.playerImage,(self.screenWidth/2-self.playerWidth/2,self.playerY))
		self.screen.blit(self.backgroundImage,(0,0))
		self.playButton=self.screen.blit(self.normalButtonImage,(self.screenWidth/2-self.buttonWidth/2,30*self.screenHeight/100))
		self.playLabel=self.screen.blit(self.playText,(self.screenWidth/2-self.playText.get_size()[0]/2,33*self.screenHeight/100))
		self.garageButton=self.screen.blit(self.normalButtonImage,(self.screenWidth/2-self.buttonWidth/2,45*self.screenHeight/100))
		self.garageLabel=self.screen.blit(self.garageText,(self.screenWidth/2-self.garageText.get_size()[0]/2,48*self.screenHeight/100))
		self.settingsButton=self.screen.blit(self.normalButtonImage,(self.screenWidth/2-self.buttonWidth/2,60*self.screenHeight/100))
		self.settingsLabel=self.screen.blit(self.settingsText,(self.screenWidth/2-self.settingsText.get_size()[0]/2,63*self.screenHeight/100))
		self.screen.blit(self.ceoNameText,(self.screenWidth/2-self.ceoNameText.get_size()[0]/2,97.65*self.screenHeight/100))
		self.screen.blit(self.nameText,(self.screenWidth/2-self.nameText.get_size()[0]/2,2.78*self.screenHeight/100))
		self.screen.blit(self.secondNameText,(self.screenWidth/2-self.secondNameText.get_size()[0]/2,6*self.screenHeight/100))
		
		if self.showNotes:
			self.screen.blit(self.pText,(self.screenWidth/2-self.pText.get_size()[0]/2,83*self.screenHeight/100))
			self.screen.blit(self.gText,(self.screenWidth/2-self.gText.get_size()[0]/2,86*self.screenHeight/100))
			self.screen.blit(self.sText,(self.screenWidth/2-self.sText.get_size()[0]/2,89*self.screenHeight/100))
			self.screen.blit(self.qText,(self.screenWidth/2-self.qText.get_size()[0]/2,92*self.screenHeight/100))
			
			pygame.draw.rect(self.screen,"cyan",(15*self.screenWidth/100,95*self.screenHeight/100,self.timeBarWidth,0.5*self.screenHeight/100))
			self.timeBarWidth-=2
			if self.timeBarWidth<0:
				self.showNotes=False
				self.default['showHomePageNotes']=self.showNotes
				with open("docs/default.json","w") as f:
					f.write(json.dumps(self.default))
		
		
	def draw(self):
		if self.homePageAnimationStation=="from bottom":
			if self.playerY>self.screenHeight/2-self.playerHeight/2 or self.drawAll==False:
				self.playerY-=15
				self.screen.blit(self.tireRustImage,(0,self.playerY+self.playerHeight-self.screenWidth*50/720))
				self.screen.blit(self.playerImage,(self.screenWidth/2-self.playerWidth/2,self.playerY))
				self.drawAll=True
			elif self.playerY<=self.screenHeight/2-self.playerHeight/2 and self.drawAll==True:
				self.drawAllFunction()
					
		elif self.homePageAnimationStation=="from middle":
			if self.drawAll==False:
				self.screen.blit(self.tireRustImage,(0,self.playerY+self.playerHeight-self.screenWidth*50/720))
				self.screen.blit(self.playerImage,(self.screenWidth/2-self.playerWidth/2,self.playerY))
			elif self.drawAll==True:
				self.drawAllFunction()
			
			
	def check(self,position,station,keyboard):
		self.keyboard=keyboard
		if station=="down":
			if self.playLabel.collidepoint(position) or self.playButton.collidepoint(position) or self.keyboard=="play":
				if self.buttonSfxStation:
					self.buttonSfx.play()
					self.buttonSfxStation=False
				self.screen.blit(self.hoverButtonImage,(self.screenWidth/2-self.buttonWidth/2,30*self.screenHeight/100))
				self.playLabel=self.screen.blit(self.playText,(self.screenWidth/2-self.playText.get_size()[0]/2,33*self.screenHeight/100))
			elif self.garageLabel.collidepoint(position) or self.garageButton.collidepoint(position) or self.keyboard=="garage":
				if self.buttonSfxStation:
					self.buttonSfx.play()
					self.buttonSfxStation=False
				self.screen.blit(self.hoverButtonImage,(self.screenWidth/2-self.buttonWidth/2,45*self.screenHeight/100))
				self.screen.blit(self.garageText,(self.screenWidth/2-self.garageText.get_size()[0]/2,48*self.screenHeight/100))
			elif self.settingsLabel.collidepoint(position) or self.settingsButton.collidepoint(position) or self.keyboard=="settings":
				if self.buttonSfxStation:
					self.buttonSfx.play()
					self.buttonSfxStation=False
				self.screen.blit(self.hoverButtonImage,(self.screenWidth/2-self.buttonWidth/2,60*self.screenHeight/100))
				self.screen.blit(self.settingsText,(self.screenWidth/2-self.settingsText.get_size()[0]/2,63*self.screenHeight/100))
				
		elif station=="up":
			if self.default['songAndSfx']=="on":self.buttonSfxStation=True
			if self.playLabel.collidepoint(position) or self.playButton.collidepoint(position) or self.keyboard=="play":
				self.clicked=False
				self.drawAll=False
				if self.playerY>-self.playerHeight:
					self.playerY-=15
				else:return "play"
			elif self.garageLabel.collidepoint(position) or self.garageButton.collidepoint(position) or self.keyboard=="garage":
				return "garage"
			elif self.settingsLabel.collidepoint(position) or self.settingsButton.collidepoint(position) or self.keyboard=="settings":
				return "settings"