import pygame,json

class CrashPage:
	def __init__(self,screen,size):
		with open("docs/data.json","+r") as text:
		  	self.data=json.load(text)
		with open("docs/default.json","+r") as text:
			self.default=json.load(text)
			
		if self.default['songAndSfx']=="on":
			self.buttonSfx=pygame.mixer.Sound("sources/sounds/buttonSfx.wav")
			self.buttonSfxStation=True
		else:self.buttonSfxStation=False
		
		self.screen=screen
		self.screenWidth,self.screenHeight=size[0],size[1]
		
		self.font="sources/fonts/edge.otf"
		self.minimalFont = pygame.font.Font("sources/fonts/glass.ttf", round(self.screenWidth*19/720))
		self.smallFont=pygame.font.Font("sources/fonts/glass.ttf", round(self.screenWidth*32/720))
		self.middleFont = pygame.font.Font(self.font, round(self.screenWidth*40/720))
		self.bigFont = pygame.font.Font(self.font, round(self.screenWidth*80/720))
		
		self.backgroundImage=pygame.transform.scale(pygame.image.load("sources/images/darkBackground.png"),(self.screenWidth,self.screenHeight))
		self.cardBackgroundImage=pygame.transform.scale(pygame.transform.rotate(pygame.image.load("sources/images/Card.png"),90),(round(self.screenWidth*600/720),round(self.screenHeight*1000/1280)))
		self.normalButtonImage=pygame.transform.scale(pygame.image.load("sources/images/buttonNormal.png"),(round(self.screenWidth*350/720),round(self.screenHeight*117/1280)))
		self.hoverButtonImage=pygame.transform.scale(pygame.image.load("sources/images/buttonHover.png"),(round(self.screenWidth*350/720),round(self.screenHeight*117/1280)))
		
		self.crashedText=self.bigFont.render(self.data['language']['crashed'][self.default['language']], True, "cyan")
		self.restartText = self.middleFont.render(self.data['language']['restart'][self.default['language']], True, "cyan")
		self.homeText = self.middleFont.render(self.data['language']['home'][self.default['language']], True, "cyan")
		self.exitText = self.middleFont.render(self.data['language']['exit'][self.default['language']], True, "cyan")
		self.garageText = self.middleFont.render(self.data['language']['garage'][self.default['language']], True, "cyan")
		self.settingsText = self.middleFont.render(self.data['language']['settings'][self.default['language']], True, "cyan")
		
		self.highScoreText = self.smallFont.render("{} : {}".format(self.data['language']['highScore'][self.default['language']],self.default['highScore']), True, pygame.Color("goldenrod"))
		
		self.ceoNameText=self.minimalFont.render("DESTROCHLORIDIUM", True,(55,87,87))
		
		self.showNotesStation=self.default['showCrashPageNotes']
		self.showNotesCount=0
		self.count=0
		self.color=pygame.Color("goldenrod")
		self.textList=[self.data['language']['pressR'][self.default['language']],self.data['language']['pressH'][self.default['language']],self.data['language']['pressG'][self.default['language']],self.data['language']['pressS'][self.default['language']],self.data['language']['pressQ'][self.default['language']]]
		self.textCount=0
		
	
	def draw(self,score):
		self.screen.blit(self.backgroundImage,(0,0)) 
		self.screen.blit(self.cardBackgroundImage,(self.screenWidth/2-self.cardBackgroundImage.get_size()[0]/2,self.screenHeight/2-self.cardBackgroundImage.get_size()[1]/2))
		self.screen.blit(self.crashedText,(self.screenWidth/2-self.crashedText.get_size()[0]/2,16*self.screenHeight/100))
		self.yourScoreText = self.smallFont.render("{} : {}".format(self.data['language']['yourScore'][self.default['language']],round(score)), True, pygame.Color("goldenrod"))
		self.screen.blit(self.yourScoreText,(self.screenWidth/2-self.yourScoreText.get_size()[0]/2,25*self.screenHeight/100))
		self.screen.blit(self.highScoreText,(self.screenWidth/2-self.highScoreText.get_size()[0]/2,30*self.screenHeight/100))
		
		self.restartButton=self.screen.blit(self.normalButtonImage,(self.screenWidth/2-self.normalButtonImage.get_size()[0]/2,36*self.screenHeight/100))
		self.restartLabel=self.screen.blit(self.restartText,(self.screenWidth/2-self.restartText.get_size()[0]/2,39*self.screenHeight/100))
		self.homeButton=self.screen.blit(self.normalButtonImage,(self.screenWidth/2-self.normalButtonImage.get_size()[0]/2,46*self.screenHeight/100))
		self.homeLabel=self.screen.blit(self.homeText,(self.screenWidth/2-self.homeText.get_size()[0]/2,49*self.screenHeight/100))
		self.garageButton=self.screen.blit(self.normalButtonImage,(self.screenWidth/2-self.normalButtonImage.get_size()[0]/2,56*self.screenHeight/100))
		self.garageLabel=self.screen.blit(self.garageText,(self.screenWidth/2-self.garageText.get_size()[0]/2,59*self.screenHeight/100))
		self.settingsButton=self.screen.blit(self.normalButtonImage,(self.screenWidth/2-self.normalButtonImage.get_size()[0]/2,66*self.screenHeight/100))
		self.settingsLabel=self.screen.blit(self.settingsText,(self.screenWidth/2-self.settingsText.get_size()[0]/2,69*self.screenHeight/100))
		self.exitButton=self.screen.blit(self.normalButtonImage,(self.screenWidth/2-self.normalButtonImage.get_size()[0]/2,76*self.screenHeight/100))
		self.exitLabel=self.screen.blit(self.exitText,(self.screenWidth/2-self.exitText.get_size()[0]/2,79*self.screenHeight/100))
		
		self.screen.blit(self.ceoNameText,(self.screenWidth/2-self.ceoNameText.get_size()[0]/2,97.65*self.screenHeight/100))
		
		
		
	def check(self,position,station,keyboard):
		self.position=position
		self.station=station
		self.keyboard=keyboard
		if self.station=="down":
			if self.restartLabel.collidepoint(self.position) or self.restartButton.collidepoint(self.position) or self.keyboard=="restart":
				self.__playSfx()
				self.screen.blit(self.hoverButtonImage,(self.screenWidth/2-self.normalButtonImage.get_size()[0]/2,36*self.screenHeight/100))
				self.screen.blit(self.restartText,(self.screenWidth/2-self.restartText.get_size()[0]/2,39*self.screenHeight/100))
			elif self.garageLabel.collidepoint(self.position) or self.garageButton.collidepoint(self.position) or self.keyboard=="garage":
				self.__playSfx()
				self.screen.blit(self.hoverButtonImage,(self.screenWidth/2-self.normalButtonImage.get_size()[0]/2,56*self.screenHeight/100))
				self.screen.blit(self.garageText,(self.screenWidth/2-self.garageText.get_size()[0]/2,59*self.screenHeight/100))
			elif self.homeLabel.collidepoint(self.position) or self.homeButton.collidepoint(self.position) or self.keyboard=="home":
				self.__playSfx()
				self.screen.blit(self.hoverButtonImage,(self.screenWidth/2-self.normalButtonImage.get_size()[0]/2,46*self.screenHeight/100))
				self.screen.blit(self.homeText,(self.screenWidth/2-self.homeText.get_size()[0]/2,49*self.screenHeight/100))
			elif self.exitLabel.collidepoint(self.position) or self.exitButton.collidepoint(self.position) or self.keyboard=="exit":
				self.__playSfx()
				self.screen.blit(self.hoverButtonImage,(self.screenWidth/2-self.normalButtonImage.get_size()[0]/2,76*self.screenHeight/100))
				self.screen.blit(self.exitText,(self.screenWidth/2-self.exitText.get_size()[0]/2,79*self.screenHeight/100))
			elif self.settingsLabel.collidepoint(self.position) or self.settingsButton.collidepoint(self.position) or self.keyboard=="settings":
				self.__playSfx()
				self.screen.blit(self.hoverButtonImage,(self.screenWidth/2-self.normalButtonImage.get_size()[0]/2,66*self.screenHeight/100))
				self.screen.blit(self.settingsText,(self.screenWidth/2-self.settingsText.get_size()[0]/2,69*self.screenHeight/100))
		elif self.station=="up":
			if self.default['songAndSfx']=="on":self.buttonSfxStation=True
			if self.restartLabel.collidepoint(self.position) or self.restartButton.collidepoint(self.position) or self.keyboard=="restart":return 'restart'
			elif self.garageLabel.collidepoint(self.position) or self.garageButton.collidepoint(self.position) or self.keyboard=="garage":return 'garage'
			elif self.homeLabel.collidepoint(self.position) or self.homeButton.collidepoint(self.position) or self.keyboard=="home":return 'home'
			elif self.settingsLabel.collidepoint(self.position) or self.settingsButton.collidepoint(self.position) or self.keyboard=="settings":return 'settings'
			elif self.exitLabel.collidepoint(self.position) or self.exitButton.collidepoint(self.position) or self.keyboard=="exit":return 'exit'
			else:
				self.screen.blit(self.normalButtonImage,(self.screenWidth/2-self.normalButtonImage.get_size()[0]/2,36*self.screenHeight/100))
				self.screen.blit(self.restartText,(self.screenWidth/2-self.restartText.get_size()[0]/2,39*self.screenHeight/100))
				self.screen.blit(self.normalButtonImage,(self.screenWidth/2-self.normalButtonImage.get_size()[0]/2,46*self.screenHeight/100))
				self.screen.blit(self.homeText,(self.screenWidth/2-self.homeText.get_size()[0]/2,49*self.screenHeight/100))
				self.screen.blit(self.normalButtonImage,(self.screenWidth/2-self.normalButtonImage.get_size()[0]/2,56*self.screenHeight/100))
				self.screen.blit(self.garageText,(self.screenWidth/2-self.garageText.get_size()[0]/2,59*self.screenHeight/100))
				self.screen.blit(self.normalButtonImage,(self.screenWidth/2-self.normalButtonImage.get_size()[0]/2,66*self.screenHeight/100))
				self.screen.blit(self.settingsText,(self.screenWidth/2-self.settingsText.get_size()[0]/2,69*self.screenHeight/100))
				self.screen.blit(self.normalButtonImage,(self.screenWidth/2-self.normalButtonImage.get_size()[0]/2,76*self.screenHeight/100))
				self.screen.blit(self.exitText,(self.screenWidth/2-self.exitText.get_size()[0]/2,79*self.screenHeight/100))
					
			
	def __playSfx(self):
		if self.buttonSfxStation:
			self.buttonSfx.play()
			self.buttonSfxStation=False
			
			
	def showNotes(self):
		self.count+=1
		if self.count==30:self.color="cyan"
		elif self.count==60:self.color=pygame.Color("goldenrod")
		elif self.count>60:
			self.count=0
			self.textCount+=1
			self.showNotesCount+=1
			if self.showNotesCount>10:
				self.showNotesStation=False
				self.default['showCrashPageNotes']=False
				with open("docs/default.json", "w") as f:f.write(json.dumps(self.default))
			if self.textCount>4:self.textCount=0
		pygame.draw.rect(self.screen,(2,44,43),(5*self.screenWidth/100,90*self.screenHeight/100,90*self.screenWidth/100,5*self.screenHeight/100))
		self.tempText=pygame.font.Font("sources/fonts/glass.ttf",round(self.screenWidth*22/720)).render(self.textList[self.textCount], True,self.color)
		self.screen.blit(self.tempText,(self.screenWidth/2-self.tempText.get_size()[0]/2,91.5*self.screenHeight/100))