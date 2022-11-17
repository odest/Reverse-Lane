import pygame,os,sys,random,json
from pygame.locals import *
from pygame import mixer
from pages.splashscreen import SplashScreen
from pages.homepage import HomePage
from pages.settingspage import SettingsPage
from pages.garagepage import GaragePage
from pages.playpage import PlayPage
from pages.crashpage import CrashPage

class MainPage():
	def __init__(self):
		with open("docs/data.json","+r") as text:
			self.data=json.load(text)
		with open("docs/default.json","+r") as text:
			self.default=json.load(text)
			
		self.SCREENWIDTH = self.default['screenSize'][0]
		self.SCREENHEIGHT = self.default['screenSize'][1]
		pygame.init()
		os.environ['SDL_VIDEO_CENTERED'] = "1"
		pygame.display.set_caption("REVERSE LANE")
		pygame.mixer.music.load("sources/sounds/themaMusic.mp3")
		if self.default['songAndSfx']=="on":pygame.mixer.music.play(-1)
		self.SCREEN = pygame.display.set_mode((self.SCREENWIDTH,self.SCREENHEIGHT))
		self.icon = pygame.transform.scale(pygame.image.load('sources/images/icon.png'),(50,50))
		pygame.display.set_icon(self.icon)
		self.MAINCLOCK = pygame.time.Clock()
		
		self.playerDict=self.data['playerDict']
		self.playerImageList=[]
		for names in range(6):
			tempList=[]
			for colors in range(3):
			 	image=pygame.image.load("sources/images/player/{}/{}{}.png".format(self.playerDict['names'][names],self.playerDict['names'][names],self.playerDict['colors'][names][colors].title()))
			 	tempList.append(image)
			self.playerImageList.append(tempList)
			
		self.tempNpcImageList=[pygame.image.load("sources/images/npc/npc{}.png".format(i)) for i in range(1,33)]
		self.tempNpcSizeList=[i.get_size() for i in self.tempNpcImageList]
		self.npcImageList=[pygame.transform.rotate(pygame.transform.scale(self.tempNpcImageList[i],(round(35*(self.SCREENWIDTH/288)),round(self.tempNpcSizeList[i][1]/self.tempNpcSizeList[i][0]*35*(self.SCREENHEIGHT/512)))),180) for i in range(32)]
		
		
		
	def start(self):
		self.splashScreenFunction()
		
	def __quit(self):
		pygame.quit()
		sys.exit()
    
		
	def splashScreenFunction(self):
		self.splashScreenObject=SplashScreen(self.SCREEN,(self.SCREENWIDTH,self.SCREENHEIGHT),self.playerImageList)
		self.run=None
		self.clicked=True
		while True:
		    self.SCREEN.fill((0,138,138))
		    for event in pygame.event.get():
		    	if event.type == QUIT:self.__quit()
    			elif event.type==MOUSEBUTTONDOWN:
    				self.run=True
    				self.clicked=False
    			elif event.type==MOUSEBUTTONUP:
    				self.run=False
    				self.clicked=True
    			elif event.type == KEYDOWN:
    				self.run=True
    				self.clicked=False
    			elif event.type == KEYUP:
    				self.run=False
    				self.clicked=True
    				
		    self.splashScreenObject.draw(self.clicked)
		    if self.run:
		    	self.splashScreenStation=self.splashScreenObject.move()
		    	if self.splashScreenStation=="start":self.homePageFunction("from bottom")
		    self.MAINCLOCK.tick(60)
		    pygame.display.update()
		    
		    
		    
	def homePageFunction(self,fromWhere):
		with open("docs/default.json","+r") as text:
			self.default=json.load(text)
		if self.default['songAndSfx']=="off":pygame.mixer.music.pause()
		elif self.default['songAndSfx']=="on":
			if pygame.mixer.music.get_busy()==0:pygame.mixer.music.play(-1)
			elif pygame.mixer.music.get_busy()==1:pygame.mixer.music.unpause()
		self.homePageObject=HomePage(self.SCREEN,(self.SCREENWIDTH,self.SCREENHEIGHT),self.playerImageList,fromWhere)
		self.station=None
		self.keyboard=None
		self.position=(-1,-1)
		while True:
			self.SCREEN.fill((0,138,138))
			for event in pygame.event.get():
				if event.type == QUIT:self.__quit()
				elif event.type==MOUSEBUTTONDOWN:
					if self.homePageObject.clicked:
						self.station="down"
						self.position=pygame.mouse.get_pos()
				elif event.type==MOUSEBUTTONUP:
					if self.homePageObject.clicked:
						self.station="up"
						self.position=pygame.mouse.get_pos()
				elif event.type == KEYDOWN:
					if self.homePageObject.clicked:
						self.station="down"
						self.keyboard=""
						if event.key == K_ESCAPE:self.__quit()
						elif event.key == K_p:self.keyboard="play"
						elif event.key == K_g:self.keyboard="garage"
						elif event.key == K_s:self.keyboard="settings"
						elif event.key == K_q or event.key == K_x:self.__quit()
				elif event.type==KEYUP:
					if self.homePageObject.clicked:self.station="up"
					
			self.homePageObject.draw()
			if self.homePageObject.onDraw:
				self.homePageStation=self.homePageObject.check(self.position,self.station,self.keyboard)
				if self.homePageStation=="play":self.playPageFunction()
				elif self.homePageStation=="settings":self.settingsPageFunction()
				elif self.homePageStation=="garage":self.garagePageFunction()
			self.MAINCLOCK.tick(60)
			pygame.display.update()			
			
			
			
	def settingsPageFunction(self):
		self.settingsPageObject=SettingsPage(self.SCREEN,(self.SCREENWIDTH,self.SCREENHEIGHT),self.playerImageList)
		self.position,self.mouseStation,self.keyboardStation,self.keyboard,self.topCount=(-1,-1),None,None,None,0
		while True:
			self.SCREEN.fill((0,138,138))
			for event in pygame.event.get():
				if event.type == QUIT:self.__quit()
				elif event.type==MOUSEBUTTONDOWN:
					self.position=pygame.mouse.get_pos()
					self.mouseStation="down"
				elif event.type==MOUSEBUTTONUP:
					self.position=pygame.mouse.get_pos()
					self.mouseStation="up"
				elif event.type == KEYDOWN:
					self.keyboardStation="down"
					self.keyboard=None
					if event.key == K_ESCAPE:self.__quit()
					elif event.key == K_DOWN:
						self.topCount+=1
						if self.topCount==5:self.topCount=1
					elif event.key == K_UP:
						self.topCount-=1
						if self.topCount<1:self.topCount=4
					elif event.key == K_LEFT:self.keyboard="left"
					elif event.key == K_RIGHT:self.keyboard="right"
					elif event.key == K_h:
						self.mouseStation="down"
						self.keyboard="backToHome"
					elif event.key == K_i:
						self.mouseStation="down"
						self.keyboard="info"
					elif event.key == K_x:
						self.mouseStation="down"
						self.keyboard="x"
					elif event.key == K_RETURN:
						self.mouseStation="down"
						self.keyboard="enter"
					else:self.topCount=0
				elif event.type == KEYUP:
					self.keyboardStation="up"
					if event.key == K_i or  event.key == K_h or event.key == K_x:self.mouseStation="up"
					elif event.key == K_RETURN:
						self.mouseStation="up"
						self.keyboard="enter"
				
			self.settingsPageObject.draw()
			self.settingsPageStation=self.settingsPageObject.check(self.position,self.mouseStation,self.keyboardStation,self.keyboard,self.topCount)
			if self.settingsPageStation=="home" or self.settingsPageStation=="save":self.homePageFunction("from middle")
			self.MAINCLOCK.tick(60)
			pygame.display.update()
			
			
			
	def garagePageFunction(self):
		self.garagePageObject=GaragePage(self.SCREEN,(self.SCREENWIDTH,self.SCREENHEIGHT),self.playerImageList)
		self.run=False
		self.keyboard=""
		self.station=None
		self.position=(-1,-1)
		while True:
			self.SCREEN.fill((2,44,43))
			for event in pygame.event.get():
				if event.type == QUIT:self.__quit()
				elif event.type==MOUSEBUTTONDOWN:
					self.run=True
					self.position=pygame.mouse.get_pos()
					self.station="down"
					self.keyboard=""
				elif event.type==MOUSEBUTTONUP:
					self.position=pygame.mouse.get_pos()
					self.station="up"
				elif event.type == KEYDOWN:
					self.run=True
					self.station="down"
					self.keyboard=""
					self.position=(-1,-1)
					if event.key == K_ESCAPE:self.__quit()
					elif event.key == K_RIGHT:self.keyboard="right"
					elif event.key == K_LEFT:self.keyboard="left"
					elif event.key == K_1:self.keyboard="one"
					elif event.key == K_2:self.keyboard="two"
					elif event.key == K_3:self.keyboard="three"
					elif event.key == K_RETURN:self.keyboard="enter"
					elif event.key == K_h:self.keyboard="backToHome"
					elif event.key == K_i:self.keyboard="info"
					elif event.key == K_x:self.keyboard="x"
				elif event.type==KEYUP:self.station="up"
        			
			self.garagePageObject.draw()
			if self.run:
				self.garagePageStation=self.garagePageObject.check(self.position,self.station,self.keyboard)
				if self.station=="up":self.run=False
				if self.garagePageStation=="home":self.homePageFunction("from middle")
			self.MAINCLOCK.tick(60)
			pygame.display.update()
			
			
			
			
	def playPageFunction(self):
		pygame.mixer.music.set_volume(0.25)
		self.playPageObject=PlayPage(self.SCREEN,(self.SCREENWIDTH,self.SCREENHEIGHT),self.playerImageList,self.npcImageList)
		self.position=(-1,-1)
		self.station=None
		self.keyboard=None
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:self.__quit()
				elif event.type==MOUSEBUTTONDOWN:
					self.keyboard=None
					self.position=pygame.mouse.get_pos()
					self.station="down"
				elif event.type==MOUSEBUTTONUP:
					self.position=pygame.mouse.get_pos()
					self.station="up"
					
				elif event.type == KEYDOWN:
					self.station="down"
					self.keyboard=None
					if event.key == K_ESCAPE:self.__quit()
					elif event.key == K_DOWN or event.key == K_s:self.keyboard="down"
					elif event.key == K_UP or event.key == K_w:self.keyboard="up"
					elif event.key == K_LEFT or event.key == K_a:self.keyboard="left"
					elif event.key == K_RIGHT or event.key == K_d:self.keyboard="right"
					elif event.key == K_SPACE:self.keyboard="space"
					elif event.key == K_x:self.keyboard="x"
				elif event.type == KEYUP:
					self.station="up"
			
			
			if self.playPageObject.run:
				self.playPageObject.draw(self.MAINCLOCK)
				self.playPageObject.move()
			elif self.playPageObject.run==False and self.playPageObject.showNotesStation==False and self.playPageObject.statement=="crash":
				self.crashPageFunction()
			self.playPageObject.check(self.position,self.station,self.keyboard)
			
			self.MAINCLOCK.tick(60)
			pygame.display.update()
			
			
			
			
	def crashPageFunction(self):
		pygame.mixer.music.set_volume(1)
		self.crashPageObject=CrashPage(self.SCREEN,(self.SCREENWIDTH,self.SCREENHEIGHT))
		self.position=(-1,-1)
		self.station=None
		self.keyboard=None
		self.crashPageObject.draw(self.playPageObject.score)
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:self.__quit()
				elif event.type==MOUSEBUTTONDOWN:
					self.position=pygame.mouse.get_pos()
					self.station="down"
				elif event.type==MOUSEBUTTONUP:
					self.position=pygame.mouse.get_pos()
					self.station="up"
				elif event.type == KEYDOWN:
					self.station="down"
					self.keyboard=None
					if event.key == K_ESCAPE:self.__quit()
					elif event.key == K_r or  event.key == K_SPACE:self.keyboard="restart"
					elif event.key == K_h:self.keyboard="home"
					elif event.key == K_g:self.keyboard="garage"
					elif event.key == K_s:self.keyboard="settings"
					elif event.key == K_q or event.key == K_e:self.keyboard="exit"
				elif event.type == KEYUP:
					self.station="up"
			
			
			if self.crashPageObject.showNotesStation:self.crashPageObject.showNotes()
			self.crashPageStation=self.crashPageObject.check(self.position,self.station,self.keyboard)
			if self.crashPageStation=="restart":self.playPageFunction()
			elif self.crashPageStation=="home":self.homePageFunction("from middle")
			elif self.crashPageStation=="garage":self.garagePageFunction()
			elif self.crashPageStation=="settings":self.settingsPageFunction()
			elif self.crashPageStation=="exit":self.__quit()
			self.MAINCLOCK.tick(60)
			pygame.display.update()