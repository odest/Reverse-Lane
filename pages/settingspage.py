import pygame,random,json

class SettingsPage:
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
		self.screenWidth, self.screenHeight =size[0],size[1]
		self.fontOne="sources/fonts/edge.otf"
		self.fontTwo="sources/fonts/glass.ttf"
		self.bigFont = pygame.font.Font(self.fontOne, round(self.screenWidth*63/720))
		self.middleFont = pygame.font.Font(self.fontOne, round(self.screenWidth*40/720))
		self.smallFont = pygame.font.Font(self.fontOne, round(self.screenWidth*25/720))
		self.fontList=[self.smallFont,self.middleFont]
		
		self.playerImageList=list
		self.playerImageCount=self.default['playerImageCount']
		self.playerColorCount=self.default['playerColorCount']
		self.playerWidth,self.playerHeight=self.screenWidth*400/720,self.screenHeight*827/1280
		
		self.playerImage=pygame.transform.scale(self.playerImageList[self.playerImageCount][self.playerColorCount],(round(self.screenWidth*400/720),round(self.screenHeight*827/1280)))
		self.tireRustImage=pygame.transform.scale(pygame.image.load("sources/images/tireRust.jpg"),(self.screenWidth,self.screenHeight))
		self.backgroundImage=pygame.transform.scale(pygame.image.load("sources/images/settingBackground.png"),(self.screenWidth,self.screenHeight))
		self.darkBackgroundImageOne=pygame.transform.scale(pygame.image.load("sources/images/darkBackground.png"),(self.screenWidth,self.screenHeight))
		self.darkBackgroundImageTwo=pygame.transform.scale(self.darkBackgroundImageOne,(int(80*self.screenWidth/100),int(86*self.screenHeight/100)))
		self.normalButtonImage=pygame.transform.scale(pygame.image.load("sources/images/buttonNormal.png"),(round(self.screenWidth*350/720),round(self.screenHeight*117/1280)))
		self.hoverButtonImage=pygame.transform.scale(pygame.image.load("sources/images/buttonHover.png"),(round(self.screenWidth*350/720),round(self.screenHeight*117/1280)))
		self.offImage=pygame.transform.scale(pygame.image.load("sources/images/on.png"),(round(self.screenWidth*80/720),round(self.screenHeight*80/1280)))
		self.onImage=pygame.transform.scale(pygame.image.load("sources/images/off.png"),(round(self.screenWidth*80/720),round(self.screenHeight*80/1280)))
		self.normalPanelRightImage=pygame.transform.scale(pygame.image.load("sources/images/panelGreen.png"),(round(60*(self.screenWidth/288)),round(34*(self.screenHeight/512))))
		self.normalPanelLeftImage=pygame.transform.rotate(self.normalPanelRightImage,180)
		self.hoverPanelRightImage=pygame.transform.scale(pygame.image.load("sources/images/panelHover.png"),(round(60*(self.screenWidth/288)),round(34*(self.screenHeight/512))))
		self.hoverPanelLeftImage=pygame.transform.rotate(self.hoverPanelRightImage,180)
		
		self.languageData=self.data['language']
		self.saveText=self.middleFont.render(self.languageData['save'][self.default['language']], True,"cyan")
		self.songAndSfxText=self.bigFont.render(self.languageData['songAndSfx'][self.default['language']], True,"cyan")
		self.songAndSfxStation=self.default['songAndSfx']
		self.onOffImageList=[self.onImage,self.offImage]
		self.onOffDict=self.data['onOffDict']
		self.difficultyText=self.bigFont.render(self.languageData['difficulty'][self.default['language']], True,"cyan")
		self.difficultyStation=self.default['difficulty']
		self.difficultyDict=self.data['difficultyDict']
		self.languageText=self.bigFont.render(self.languageData['language'][self.default['language']], True,"cyan")
		self.languageStation=self.default['language']
		self.languageDict=self.data['languageDict']
		self.screenSizeText=self.bigFont.render(self.languageData['screenSize'][self.default['language']], True,"cyan")
		self.screenSize=self.default['screenSize']
		self.screenSizeStation=str(self.screenSize[0])
		self.screenSizeDict=self.data['screenSizeDict']
		self.notesStation="off"
		self.infoButtonVisibilityCount=0
		self.infoButtonImage=self.normalPanelRightImage
		self.settingPageInfoButtonVisibilityStation=self.default['settingPageInfoButtonVisibilityStation']

		if self.songAndSfxStation=="on":self.bottomCountOne=1
		elif self.songAndSfxStation=="off":self.bottomCountOne=2
		if self.difficultyStation=="easy":self.bottomCountTwo=3
		elif self.difficultyStation=="medium":self.bottomCountTwo=4
		elif self.difficultyStation=="hard":self.bottomCountTwo=5
		if self.languageStation=="tr":self.bottomCountThree=6
		elif self.languageStation=="en":self.bottomCountThree=7
		elif self.languageStation=="ge":self.bottomCountThree=8
		if self.screenSizeStation=="144":self.bottomCountFour=9
		elif self.screenSizeStation=="225":self.bottomCountFour=10
		elif self.screenSizeStation=="288":self.bottomCountFour=11
		elif self.screenSizeStation=="360":self.bottomCountFour=12
		elif self.screenSizeStation=="480":self.bottomCountFour=13
		elif self.screenSizeStation=="720":self.bottomCountFour=14
		
		self.arrowText=self.bigFont.render(">", True,(0,138,138))
		self.arrowY=-100
		self.arrowCoordsDict={0:-10,1:14,2:32,3:50,4:68}
		self.nameText=self.middleFont.render("R E V E R S E   L A N E", True,"cyan")
		self.secondNameText=pygame.font.Font(self.fontTwo, round(self.screenWidth*18/720)).render("UNLIMITED SUPERCAR EDITION", True,(63,128,128))
		self.ceoNameText=pygame.font.Font(self.fontTwo, round(self.screenWidth*18/720)).render("destrochloridium", True,(55,87,87))
		
	
	def draw(self):
		self.screen.blit(self.tireRustImage,(0,0))
		self.screen.blit(self.playerImage,(self.screenWidth/2-self.playerWidth/2,self.screenHeight/2-self.playerHeight/2))
		self.screen.blit(self.backgroundImage,(0,0))
		
		self.screen.blit(self.nameText,(self.screenWidth/2-self.nameText.get_size()[0]/2,1.8*self.screenHeight/100))
		self.screen.blit(self.secondNameText,(self.screenWidth/2-self.secondNameText.get_size()[0]/2,5*self.screenHeight/100))
		self.screen.blit(self.ceoNameText,(self.screenWidth/2-self.ceoNameText.get_size()[0]/2,97.65*self.screenHeight/100))
		
		self.saveButton=self.screen.blit(self.normalButtonImage,(self.screenWidth/2-self.normalButtonImage.get_size()[0]/2,84*self.screenHeight/100))
		self.saveLabel=self.screen.blit(self.saveText,(self.screenWidth/2-self.saveText.get_size()[0]/2,87*self.screenHeight/100))
		self.screen.blit(self.arrowText,(17*self.screenWidth/100,self.arrowY))
		
		self.screen.blit(self.songAndSfxText,(self.screenWidth/2-self.songAndSfxText.get_size()[0]/2,14*self.screenHeight/100))
		self.onButton=self.screen.blit(self.onOffImageList[self.onOffDict[self.songAndSfxStation]['onImage']],(25*self.screenWidth/100,21*self.screenHeight/100))
		self.onLabel=self.screen.blit(self.middleFont.render(self.languageData['on'][self.default['language']], True,self.onOffDict[self.songAndSfxStation]['onColor']),(37*self.screenWidth/100,22.6*self.screenHeight/100))
		self.offButton=self.screen.blit(self.onOffImageList[self.onOffDict[self.songAndSfxStation]['offImage']],(53*self.screenWidth/100,21*self.screenHeight/100))
		self.offLabel=self.screen.blit(self.middleFont.render(self.languageData['off'][self.default['language']], True,self.onOffDict[self.songAndSfxStation]['offColor']),(65*self.screenWidth/100,22.6*self.screenHeight/100))
		
		self.screen.blit(self.difficultyText,(self.screenWidth/2-self.difficultyText.get_size()[0]/2,32*self.screenHeight/100))
		self.easyLabel=self.screen.blit(self.fontList[self.difficultyDict[self.difficultyStation]['fontOne']].render(self.languageData['easy'][self.default['language']], True,self.difficultyDict[self.difficultyStation]['colorOne']),(self.difficultyDict[self.difficultyStation]['widthOne'][self.default['language']]*self.screenWidth/100,self.difficultyDict[self.difficultyStation]['heightOne']*self.screenHeight/100))
		self.mediumLabel=self.screen.blit(self.fontList[self.difficultyDict[self.difficultyStation]['fontTwo']].render(self.languageData['medium'][self.default['language']], True,self.difficultyDict[self.difficultyStation]['colorTwo']),(self.difficultyDict[self.difficultyStation]['widthTwo'][self.default['language']]*self.screenWidth/100,self.difficultyDict[self.difficultyStation]['heightTwo']*self.screenHeight/100))
		self.hardLabel=self.screen.blit(self.fontList[self.difficultyDict[self.difficultyStation]['fontThree']].render(self.languageData['hard'][self.default['language']], True,self.difficultyDict[self.difficultyStation]['colorThree']),(self.difficultyDict[self.difficultyStation]['widthThree'][self.default['language']]*self.screenWidth/100,self.difficultyDict[self.difficultyStation]['heightThree']*self.screenHeight/100))
		
		self.screen.blit(self.languageText,(self.screenWidth/2-self.languageText.get_size()[0]/2,50*self.screenHeight/100))
		self.trLabel=self.screen.blit(self.fontList[self.languageDict[self.languageStation]['fontOne']].render(self.languageData['turkish'][self.default['language']], True,self.languageDict[self.languageStation]['colorOne']),(self.languageDict[self.languageStation]['widthOne'][self.default['language']]*self.screenWidth/100,self.languageDict[self.languageStation]['heightOne']*self.screenHeight/100))
		self.enLabel=self.screen.blit(self.fontList[self.languageDict[self.languageStation]['fontTwo']].render(self.languageData['english'][self.default['language']], True,self.languageDict[self.languageStation]['colorTwo']),(self.languageDict[self.languageStation]['widthTwo'][self.default['language']]*self.screenWidth/100,self.languageDict[self.languageStation]['heightTwo']*self.screenHeight/100))
		self.geLabel=self.screen.blit(self.fontList[self.languageDict[self.languageStation]['fontThree']].render(self.languageData['german'][self.default['language']], True,self.languageDict[self.languageStation]['colorThree']),(self.languageDict[self.languageStation]['widthThree'][self.default['language']]*self.screenWidth/100,self.languageDict[self.languageStation]['heightThree']*self.screenHeight/100))
		
		self.screen.blit(self.screenSizeText,(self.screenWidth/2-self.screenSizeText.get_size()[0]/2,68*self.screenHeight/100))
		self.oneLabel=self.screen.blit(self.fontList[self.screenSizeDict[self.screenSizeStation]['fontOne']].render("144", True,self.screenSizeDict[self.screenSizeStation]['colorOne']),(self.screenSizeDict[self.screenSizeStation]['widthOne']*self.screenWidth/100,self.screenSizeDict[self.screenSizeStation]['heightOne']*self.screenHeight/100))
		self.twoLabel=self.screen.blit(self.fontList[self.screenSizeDict[self.screenSizeStation]['fontTwo']].render("225", True,self.screenSizeDict[self.screenSizeStation]['colorTwo']),(self.screenSizeDict[self.screenSizeStation]['widthTwo']*self.screenWidth/100,self.screenSizeDict[self.screenSizeStation]['heightTwo']*self.screenHeight/100))
		self.threeLabel=self.screen.blit(self.fontList[self.screenSizeDict[self.screenSizeStation]['fontThree']].render("288", True,self.screenSizeDict[self.screenSizeStation]['colorThree']),(self.screenSizeDict[self.screenSizeStation]['widthThree']*self.screenWidth/100,self.screenSizeDict[self.screenSizeStation]['heightThree']*self.screenHeight/100))
		self.fourLabel=self.screen.blit(self.fontList[self.screenSizeDict[self.screenSizeStation]['fontFour']].render("360", True,self.screenSizeDict[self.screenSizeStation]['colorFour']),(self.screenSizeDict[self.screenSizeStation]['widthFour']*self.screenWidth/100,self.screenSizeDict[self.screenSizeStation]['heightFour']*self.screenHeight/100))
		self.fiveLabel=self.screen.blit(self.fontList[self.screenSizeDict[self.screenSizeStation]['fontFive']].render("480", True,self.screenSizeDict[self.screenSizeStation]['colorFive']),(self.screenSizeDict[self.screenSizeStation]['widthFive']*self.screenWidth/100,self.screenSizeDict[self.screenSizeStation]['heightFive']*self.screenHeight/100))
		self.sixLabel=self.screen.blit(self.fontList[self.screenSizeDict[self.screenSizeStation]['fontSix']].render("720", True,self.screenSizeDict[self.screenSizeStation]['colorSix']),(self.screenSizeDict[self.screenSizeStation]['widthSix']*self.screenWidth/100,self.screenSizeDict[self.screenSizeStation]['heightSix']*self.screenHeight/100))
		
		if self.settingPageInfoButtonVisibilityStation:
			self.infoButtonVisibilityCount+=1
			if self.infoButtonVisibilityCount==15:self.infoButtonImage=self.hoverPanelRightImage
			elif self.infoButtonVisibilityCount==25:self.infoButtonImage=self.normalPanelRightImage
			elif self.infoButtonVisibilityCount>25:self.infoButtonVisibilityCount=0
		
		self.backToHomeButton=self.screen.blit(self.normalPanelLeftImage,(0,0))
		self.informationButton=self.screen.blit(self.infoButtonImage,(self.screenWidth-self.normalPanelRightImage.get_size()[0],0))
		self.backToHomeLabel=self.screen.blit(self.smallFont.render(self.data['language']['back'][self.default['language']], True,"cyan"),(5*self.screenWidth/100,2.4*self.screenHeight/100))
		self.informationLabel=self.screen.blit(self.smallFont.render(self.data['language']['info'][self.default['language']], True,"cyan"),(86*self.screenWidth/100,2.4*self.screenHeight/100))
		
		if self.notesStation=="on":self.__showNotes()
			
		
	def check(self,position,mouseStation,keyboardStation,keyboard,topCount):
		if self.notesStation=="on":
			self.position=position
			if self.xLabel.collidepoint(self.position) or keyboard=="x":
				self.notesStation="off"
				self.default['settingPageInfoButtonVisibilityStation']=self.settingPageInfoButtonVisibilityStation
				with open("docs/default.json", "w") as f:
					f.write(json.dumps(self.default))
			self.mouseStation=None
			self.keyboardStation=None
			self.keyboard=None
			self.topCount=0
		elif self.notesStation=="off":
			self.position=position
			self.mouseStation=mouseStation
			self.keyboardStation=keyboardStation
			self.keyboard=keyboard
			self.topCount=topCount
		
		self.arrowY=self.arrowCoordsDict[self.topCount]*self.screenHeight/100
		if self.keyboardStation=="down":
			if self.keyboard=="right":
				if self.topCount==1:self.bottomCountOne=2
				elif self.topCount==2:
					self.bottomCountTwo+=1
					if self.bottomCountTwo>5:self.bottomCountTwo=5
				elif self.topCount==3:
					self.bottomCountThree+=1
					if self.bottomCountThree>8:self.bottomCountThree=8
				elif self.topCount==4:
					self.bottomCountFour+=1
					if self.bottomCountFour>14:self.bottomCountFour=14
			elif self.keyboard=="left":
				if self.topCount==1:self.bottomCountOne=1
				elif self.topCount==2:
					self.bottomCountTwo-=1
					if self.bottomCountTwo<3:self.bottomCountTwo=3
				elif self.topCount==3:
					self.bottomCountThree-=1
					if self.bottomCountThree<6:self.bottomCountThree=6
				elif self.topCount==4:
					self.bottomCountFour-=1
					if self.bottomCountFour<9:self.bottomCountFour=9
					
			if self.bottomCountOne==1:self.songAndSfxStation="on"
			elif self.bottomCountOne==2:self.songAndSfxStation="off"
			if self.bottomCountTwo==3:self.difficultyStation="easy"
			elif self.bottomCountTwo==4:self.difficultyStation="medium"
			elif self.bottomCountTwo==5:self.difficultyStation="hard"
			if self.bottomCountThree==6:self.languageStation="tr"
			elif self.bottomCountThree==7:self.languageStation="en"
			elif self.bottomCountThree==8:self.languageStation="ge"
			if self.bottomCountFour==9:
				self.screenSizeStation="144"
				self.screenSize=[144,256]
			elif self.bottomCountFour==10:
				self.screenSizeStation="225"
				self.screenSize=[225,400]
			elif self.bottomCountFour==11:
				self.screenSizeStation="288"
				self.screenSize=[288,512]
			elif self.bottomCountFour==12:
				self.screenSizeStation="360"
				self.screenSize=[360,640]
			elif self.bottomCountFour==13:
				self.screenSizeStation="480"
				self.screenSize=[480,853]
			elif self.bottomCountFour==14:
				self.screenSizeStation="720"
				self.screenSize=[720,1280]
		elif self.keyboardStation=="up":self.keyboard=keyboard
			
		
		if self.mouseStation=="down":
			if self.onButton.collidepoint(self.position) or self.onLabel.collidepoint(self.position):
				self.__playSfx("option")
				self.songAndSfxStation="on"
				self.bottomCountOne=1
			elif self.offButton.collidepoint(self.position) or self.offLabel.collidepoint(self.position):
				self.__playSfx("option")
				self.songAndSfxStation="off"
				self.bottomCountOne=2
			elif self.easyLabel.collidepoint(self.position):
				self.__playSfx("option")
				self.difficultyStation="easy"
				self.bottomCountTwo=3
			elif self.mediumLabel.collidepoint(self.position):
				self.__playSfx("option")
				self.difficultyStation="medium"
				self.bottomCountTwo=4
			elif self.hardLabel.collidepoint(self.position):
				self.__playSfx("option")
				self.difficultyStation="hard"
				self.bottomCountTwo=5
			elif self.trLabel.collidepoint(self.position):
				self.__playSfx("option")
				self.languageStation="tr"
				self.bottomCountThree=6
			elif self.enLabel.collidepoint(self.position):
				self.__playSfx("option")
				self.languageStation="en"
				self.bottomCountThree=7
			elif self.geLabel.collidepoint(self.position):
				self.__playSfx("option")
				self.languageStation="ge"
				self.bottomCountThree=8
			elif self.oneLabel.collidepoint(self.position):
				self.__playSfx("option")
				self.screenSizeStation="144"
				self.screenSize=[144,256]
				self.bottomCountFour=9
			elif self.twoLabel.collidepoint(self.position):
				self.__playSfx("option")
				self.screenSizeStation="225"
				self.screenSize=[225,400]
				self.bottomCountFour=10
			elif self.threeLabel.collidepoint(self.position):
				self.__playSfx("option")
				self.screenSizeStation="288"
				self.screenSize=[288,512]
				self.bottomCountFour=11
			elif self.fourLabel.collidepoint(self.position):
				self.__playSfx("option")
				self.screenSizeStation="360"
				self.screenSize=[360,640]
				self.bottomCountFour=12
			elif self.fiveLabel.collidepoint(self.position):
				self.__playSfx("option")
				self.screenSizeStation="480"
				self.screenSize=[480,853]
				self.bottomCountFour=13
			elif self.sixLabel.collidepoint(self.position):
				self.__playSfx("option")
				self.screenSizeStation="720"
				self.screenSize=[720,1280]
				self.bottomCountFour=14
			elif self.backToHomeButton.collidepoint(self.position) or self.backToHomeLabel.collidepoint(self.position) or self.keyboard=="backToHome":
				self.__playSfx("panel")
				self.backToHomeButton=self.screen.blit(self.hoverPanelLeftImage,(0,0))
				self.backToHomeLabel=self.screen.blit(self.smallFont.render(self.data['language']['back'][self.default['language']], True,"cyan"),(5*self.screenWidth/100,2.4*self.screenHeight/100))
			elif self.informationButton.collidepoint(self.position) or self.informationLabel.collidepoint(self.position) or self.keyboard=="info":
				self.__playSfx("panel")
				self.informationButton=self.screen.blit(self.hoverPanelRightImage,(self.screenWidth-self.normalPanelRightImage.get_size()[0],0))
				self.informationLabel=self.screen.blit(self.smallFont.render(self.data['language']['info'][self.default['language']], True,"cyan"),(86*self.screenWidth/100,2.4*self.screenHeight/100))
			elif self.saveButton.collidepoint(self.position) or self.saveLabel.collidepoint(self.position) or self.keyboard=="enter":
				self.__playSfx("button")
				self.screen.blit(self.hoverButtonImage,(self.screenWidth/2-self.normalButtonImage.get_size()[0]/2,84*self.screenHeight/100))
				self.screen.blit(self.saveText,(self.screenWidth/2-self.saveText.get_size()[0]/2,87*self.screenHeight/100))
				
		elif self.mouseStation=="up":
			if self.default['songAndSfx']=="on":self.buttonSfxStation=self.panelSfxStation=self.optionSfxStation=True
			if self.saveButton.collidepoint(self.position) or self.saveLabel.collidepoint(self.position) or self.keyboard=="enter":
				self.default['songAndSfx']=self.songAndSfxStation
				self.default['difficulty']=self.difficultyStation
				self.default['language']=self.languageStation
				self.default['screenSize']=self.screenSize
				with open("docs/default.json", "w") as f:
					f.write(json.dumps(self.default))
				return "save"
			elif self.backToHomeButton.collidepoint(self.position) or self.backToHomeLabel.collidepoint(self.position) or self.keyboard=="backToHome":return "home"
			elif self.informationButton.collidepoint(self.position) or self.informationLabel.collidepoint(self.position) or self.keyboard=="info":self.notesStation="on"
			
			
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
		self.settingPageInfoButtonVisibilityStation=False
		self.infoButtonImage=self.normalPanelRightImage
		self.notesText=self.bigFont.render(self.languageData['notes'][self.default['language']], True,"cyan")
		self.screen.blit(self.darkBackgroundImageOne,(0,0))
		self.screen.blit(self.darkBackgroundImageTwo,(10*self.screenWidth/100,10*self.screenHeight/100))
		self.screen.blit(self.notesText,(self.screenWidth/2-self.notesText.get_size()[0]/2,15*self.screenHeight/100))
		self.xLabel=self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*65/720)).render("X", True,"red"),(80.5*self.screenWidth/100,11*self.screenHeight/100))
		pygame.draw.rect(self.screen,(15,15,15),(20*self.screenWidth/100,23*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100))
		pygame.draw.rect(self.screen,(0,138,138),(20*self.screenWidth/100,23*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100),1)
		self.screen.blit(pygame.transform.rotate(pygame.font.Font(self.fontTwo,round(self.screenWidth*64/720)).render("<", True,"cyan"),-90),(24.5*self.screenWidth/100,24*self.screenHeight/100))
		self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*32/720)).render("U P", True,(0,138,138)),(26*self.screenWidth/100,26.5*self.screenHeight/100))
		self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*60/720)).render("/", True,"cyan"),(48*self.screenWidth/100,24*self.screenHeight/100))
		pygame.draw.rect(self.screen,(15,15,15),(60*self.screenWidth/100,23*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100))
		pygame.draw.rect(self.screen,(0,138,138),(60*self.screenWidth/100,23*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100),1)
		self.screen.blit(pygame.transform.rotate(pygame.font.Font(self.fontTwo,round(self.screenWidth*60/720)).render("<", True,"cyan"),-270),(65*self.screenWidth/100,24*self.screenHeight/100))
		self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*32/720)).render("DOWN", True,(0,138,138)),(63*self.screenWidth/100,26.5*self.screenHeight/100))
		self.tempTextOne=pygame.font.Font(self.fontTwo,round(self.screenWidth*21/720)).render(self.languageData['upDownText'][self.default['language']], True,"cyan")
		self.screen.blit(self.tempTextOne,(self.screenWidth/2-self.tempTextOne.get_size()[0]/2,32*self.screenHeight/100))
		pygame.draw.rect(self.screen,(15,15,15),(20*self.screenWidth/100,38*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100))
		pygame.draw.rect(self.screen,(0,138,138),(20*self.screenWidth/100,38*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100),1)
		self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*64/720)).render("<", True,"cyan"),(28*self.screenWidth/100,37.5*self.screenHeight/100))
		self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*32/720)).render("LEFT", True,(0,138,138)),(25*self.screenWidth/100,41.5*self.screenHeight/100))
		self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*60/720)).render("/", True,"cyan"),(48*self.screenWidth/100,39*self.screenHeight/100))
		pygame.draw.rect(self.screen,(15,15,15),(60*self.screenWidth/100,38*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100))
		pygame.draw.rect(self.screen,(0,138,138),(60*self.screenWidth/100,38*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100),1)
		self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*60/720)).render(">", True,"cyan"),(68*self.screenWidth/100,37.5*self.screenHeight/100))
		self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*32/720)).render("RIGHT", True,(0,138,138)),(63*self.screenWidth/100,41.5*self.screenHeight/100))
		self.tempTextTwo=pygame.font.Font(self.fontTwo,round(self.screenWidth*20/720)).render(self.languageData['leftRightText'][self.default['language']], True,"cyan")
		self.screen.blit(self.tempTextTwo,(self.screenWidth/2-self.tempTextTwo.get_size()[0]/2,47*self.screenHeight/100))
		pygame.draw.rect(self.screen,(15,15,15),(30*self.screenWidth/100,53*self.screenHeight/100,40*self.screenWidth/100,7*self.screenHeight/100))
		pygame.draw.rect(self.screen,(0,138,138),(30*self.screenWidth/100,53*self.screenHeight/100,40*self.screenWidth/100,7*self.screenHeight/100),1)
		self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*40/720)).render("E N T E R", True,"cyan"),(38*self.screenWidth/100,55*self.screenHeight/100))
		self.tempTextThree=pygame.font.Font(self.fontTwo,round(self.screenWidth*25/720)).render(self.languageData['enterText'][self.default['language']], True,"cyan")
		self.screen.blit(self.tempTextThree,(self.screenWidth/2-self.tempTextThree.get_size()[0]/2,62*self.screenHeight/100))
		
		self.words = [word.split(" ") for word in self.languageData['noteText'][self.default['language']].splitlines()]
		self.space = pygame.font.Font(self.fontTwo,round(self.screenWidth*22/720)).size(" ")[0]
		self.max_width, self.max_height = self.screenWidth-15*self.screenWidth/100,self.screenHeight-25*self.screenHeight/100
		self.x, self.y = 15*self.screenWidth/100,70*self.screenHeight/100
		for line in self.words:
			for word in line:
				word_surface = pygame.font.Font(self.fontTwo,round(self.screenWidth*22/720)).render(word, 0, [0,180,180])
				word_width, word_height = word_surface.get_size()
				if self.x + word_width >= self.max_width:
					self.x = 15*self.screenWidth/100
					self.y += word_height
				self.screen.blit(word_surface, (self.x,self.y))
				self.x += word_width + self.space
			self.x = 15*self.screenWidth/100
			self.y += word_height