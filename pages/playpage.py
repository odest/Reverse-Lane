import pygame,random,json

class PlayPage():
    def __init__(self,screen,size,list,npcList):
    	with open("docs/data.json","+r") as text:
    		self.data=json.load(text)
    	with open("docs/default.json","+r") as text:
    		self.default=json.load(text)
    		
    	if self.default["songAndSfx"]=="on":
	    	self.barrierSfx=pygame.mixer.Sound("sources/sounds/barrierSfx.wav")
	    	self.crashSfx=pygame.mixer.Sound("sources/sounds/crashSfx.wav")
	    	self.loopSfx=pygame.mixer.Sound("sources/sounds/vehicleLoopSfx.wav")
	    	self.loopSfx.set_volume(1)
	    	self.gasSfx=pygame.mixer.Sound("sources/sounds/gasSfx.wav")
	    	self.stopSfx=pygame.mixer.Sound("sources/sounds/stopSfx.wav")
	    	self.crashSfxStation=True
	    	self.loopSfx.play(-1)
    	else:self.crashSfxStation=False
    		
    	self.screen=screen
    	self.screenWidth, self.screenHeight =size[0],size[1]
    	self.run=True
    	self.fontOne="sources/fonts/edge.otf"
    	self.fontTwo="sources/fonts/glass.ttf"
    	self.smallFont=pygame.font.Font(self.fontTwo,round(self.screenWidth*24/720))
    	self.playerImageCount=self.default['playerImageCount']
    	self.playerColorCount=self.default['playerColorCount']
    	self.playerImageList=list
    	self.npcImageList=npcList
    	
    	self.darkBackgroundImageOne=pygame.transform.scale(pygame.image.load("sources/images/darkBackground.png"),(int(self.screenWidth),int(self.screenHeight)))
    	self.darkBackgroundImageTwo=pygame.transform.scale(self.darkBackgroundImageOne,(int(80*self.screenWidth/100),int(80*self.screenHeight/100)))
    	self.roadImage=pygame.transform.scale(pygame.image.load("sources/images/road{}.jpg".format(random.randint(1,4))), (self.screenWidth,self.screenHeight))
    	self.roadImageWidth,self.roadImageHeight=self.roadImage.get_size()
    	self.greenPanelRightImage=pygame.transform.scale(pygame.image.load("sources/images/panelGreen.png"),(round(70*(self.screenWidth/288)),round(40*(self.screenHeight/512))))
    	self.greenPanelLeftImage=pygame.transform.rotate(self.greenPanelRightImage,180)
    	self.redPanelImage=pygame.transform.rotate(pygame.transform.scale(pygame.image.load("sources/images/panelRed.png"),(round(70*(self.screenWidth/288)),round(40*(self.screenHeight/512)))),180)
    	self.playerImage=pygame.transform.scale(self.playerImageList[self.playerImageCount][self.playerColorCount],((round(40*(self.screenWidth/288)),round(82*(self.screenHeight/512)))))
    	self.playerImageWidth,self.playerImageHeight=self.playerImage.get_size()
    	self.playerX,self.playerY=self.screenWidth/2-self.playerImageWidth/2,120*self.screenHeight/100
    	self.playerRect = pygame.Rect(self.playerX,self.playerY, self.playerImageWidth,self.playerImageHeight)
    	self.fpsPanelImage=self.greenPanelLeftImage
    	self.roadXOne,self.roadYOne=0,0
    	self.roadXTwo,self.roadYTwo=0,-self.roadImageHeight
    	self.difficulty=self.default['difficulty']
    	self.numberOfEnemy=None
    	self.roadSpeed=self.data['playerDict']['features'][self.playerImageCount][0]/45
    	if self.difficulty=="easy":
    		self.numberOfEnemy=1
    		self.scoreDelay=self.roadSpeed/200
    	elif self.difficulty=="medium":
    		self.numberOfEnemy=3
    		self.scoreDelay=self.roadSpeed/100
    	elif self.difficulty=="hard":
    		self.numberOfEnemy=5
    		self.scoreDelay=self.roadSpeed/50
    	self.enemyList=[Enemy(self.screen,[self.screenWidth, self.screenHeight],self.npcImageList,i,self.difficulty) for i in range(self.numberOfEnemy)]
    	
    	self.playerAngle=0
    	self.playerDirection=None
    	self.score=0
    	self.handling=self.data['playerDict']['features'][self.playerImageCount][1]
    	self.braking=self.data['playerDict']['features'][self.playerImageCount][2]/18
    	self.yChange = 0
    	self.accelY = 0
    	self.maxSpeed = self.roadSpeed/2
    	self.minSpeed=-self.braking
    	self.time=0
    	
    	self.closeOvertakingStation=False
    	self.closeOvertakingCount=0
    	self.passNpcStation=False
    	self.touchStation=False
    	self.showNotesCount=0
    	self.showNotesStation=False
    	self.showNotes=self.default['showPlayPageNotes']
    	
    	self.statement=None
    	self.spaceKeyStation=True
    
    	
    	
    def draw(self,clock):
    	self.screen.blit(self.roadImage,(self.roadXOne,self.roadYOne))
    	self.screen.blit(self.roadImage,(self.roadXTwo,self.roadYTwo))
    	
    	self.playerRect.topleft = (int(self.playerX), int(self.playerY))
    	rotated = pygame.transform.rotate(self.playerImage, self.playerAngle)
    	surface_rect =self.playerImage.get_rect(topleft = self.playerRect.topleft)
    	new_rect = rotated.get_rect(center = surface_rect.center)
    	self.rect=self.screen.blit(rotated,new_rect.topleft)
    	
    	self.playerCrashRect=pygame.Rect(self.playerX,self.playerY,self.playerImageWidth,self.playerImageHeight)
    	
    	[i.draw() for i in self.enemyList]
    	
    	
    	#temp joistic and screen rects
    	self.left=pygame.draw.rect(self.screen,"red",(100,1100,100,100))
    	self.right=pygame.draw.rect(self.screen,"green",(520,1100,100,100))
    	self.up=pygame.draw.rect(self.screen,"blue",(310,1000,100,100))
    	self.down=pygame.draw.rect(self.screen,"white",(310,1150,100,100))
    	pygame.draw.rect(self.screen,"cyan",(0,0,self.screenWidth, self.screenHeight),1)
    	self.pauseButton=pygame.draw.rect(self.screen,"yellow",(610,600,100,100))
    	###
    	
    	self.screen.blit(self.fpsPanelImage,(0,0))
    	self.screen.blit(self.greenPanelRightImage,(self.screenWidth-self.redPanelImage.get_size()[0],0))
    	self.fps=clock.get_fps()
    	if self.fps<30:self.fpsPanelImage=self.redPanelImage
    	elif self.fps>=30:self.fpsPanelImage=self.greenPanelLeftImage
    	self.screen.blit(self.smallFont.render("FPS:{}".format(round(self.fps,1)), True,pygame.Color("goldenrod")),(5*self.screenWidth/100,2.9*self.screenHeight/100))
    	self.screen.blit(self.smallFont.render("SC:{}".format(round(self.score,1)), True,pygame.Color("goldenrod")),(81*self.screenWidth/100,2.9*self.screenHeight/100))
    	
    	if self.showNotes:
	    	self.showNotesCount+=1
	    	if self.showNotesCount==50:
	    		self.showNotesStation=True
	    	if self.showNotesStation:self.__showNotes()
	    		
    	
    def move(self):
    	self.yChange += self.accelY
    	if self.yChange >= self.maxSpeed:self.yChange = self.yChange/abs(self.yChange) * self.maxSpeed
    	elif self.yChange <= self.minSpeed:self.yChange = self.minSpeed
    	
    	if self.accelY == 0:
    	    if self.yChange > 0:
    	    	self.yChange -= 0.2
    	    	if self.yChange < 0.2:
    	    		self.yChange = 0
    	    elif self.yChange < 0:
    	    	self.yChange += 0.2
    	    	if self.yChange > -0.2:
    	    		self.yChange = 0

    	self.roadYOne+=self.roadSpeed+self.yChange
    	self.roadYTwo+=self.roadSpeed+self.yChange
    	self.score+=self.scoreDelay
    	self.time+=1
    	
    	[i.move(self.roadSpeed,self.yChange) for i in self.enemyList]
    	for i in self.enemyList:
    		if i.passNpc:
    			self.passNpcStation=True
    			self.__upgradeScoreText("+5","green")
    			
    		if self.playerCrashRect.colliderect(i.crashRect):
    			self.__crash()
    		elif self.playerCrashRect.colliderect(i.leftRect) or self.playerCrashRect.colliderect(i.rightRect):
    			self.__upgradeScoreText("+2x","cyan")
    		elif self.playerCrashRect.colliderect(i.safeRect):
    			self.touchStation=True
    			self.__upgradeScoreText("-5","red")
    			if self.playerDirection=="left":
    				i.npcOneX-=25
    				self.playerX+=5
    			elif self.playerDirection=="right":
    				i.npcOneX+=25
    				self.playerX-=5
    		
    	if self.playerY>80*self.screenHeight/100:self.playerY-=self.roadSpeed
    	
    	if self.roadYOne>self.screenHeight:
    		self.roadYOne=self.roadYTwo-self.roadImageHeight
    	elif self.roadYTwo>self.screenHeight:
    		self.roadYTwo=self.roadYOne-self.roadImageHeight
    	
    	if self.playerDirection=="left" and self.playerX>5*self.screenHeight/100:
    		self.playerX-=self.handling
    		if self.playerAngle<0:self.playerAngle=0
    		elif self.playerAngle<30:self.playerAngle += 2
    	elif self.playerDirection=="right" and self.playerX<43.5*self.screenHeight/100:
    		self.playerX+=self.handling
    		if self.playerAngle>0:self.playerAngle=0
    		elif self.playerAngle>-30:self.playerAngle -= 2
    		
    	elif self.playerX<5*self.screenHeight/100:
    		if self.default["songAndSfx"]=="on":
    			self.barrierSfx.play()
    		self.__upgradeScoreText("-5","red")
    		self.playerX=5*self.screenHeight/100
    	elif self.playerX>43.5*self.screenHeight/100:
    		if self.default["songAndSfx"]=="on":
    			self.barrierSfx.play()
    		self.__upgradeScoreText("-5","red")
    		self.playerX=43.5*self.screenHeight/100
    		
    	elif self.playerDirection=="up":
    		self.accelY = .2
    		self.playerAngle=0
    		if self.difficulty=="easy":
	    		self.scoreDelay=self.roadSpeed/100
	    	elif self.difficulty=="medium":
	    		self.scoreDelay=self.roadSpeed/50
	    	elif self.difficulty=="hard":
	    		self.scoreDelay=self.roadSpeed/25
    		if self.default["songAndSfx"]=="on":
	    		self.gasSfx.play()
    	elif self.playerDirection=="down":
    		self.accelY = -.2
    		self.playerAngle=0
    		if self.difficulty=="easy":
	    		self.scoreDelay=self.roadSpeed/400
	    	elif self.difficulty=="medium":
	    		self.scoreDelay=self.roadSpeed/200
	    	elif self.difficulty=="hard":
	    		self.scoreDelay=self.roadSpeed/100
    		if self.default["songAndSfx"]=="on":
	    		self.loopSfx.set_volume(0.25)
    	else:
    		self.roadSpeed=self.data['playerDict']['features'][self.playerImageCount][0]/45
    		if self.difficulty=="easy":
	    		self.scoreDelay=self.roadSpeed/200
	    	elif self.difficulty=="medium":
	    		self.scoreDelay=self.roadSpeed/100
	    	elif self.difficulty=="hard":
	    		self.scoreDelay=self.roadSpeed/50
    		if self.playerAngle<0:self.playerAngle+=2
    		elif self.playerAngle>0:self.playerAngle-=2
    		self.accelY=0
    		if self.default["songAndSfx"]=="on":
	    		self.loopSfx.set_volume(1.5)
	    		self.gasSfx.stop()
    		
    	
    def check(self,position,station,keyboard):
    	if self.showNotesStation==True:
    		self.position=position
    		if self.xLabel.collidepoint(self.position) or keyboard=="x":
    			self.run=True
    			self.showNotesStation=False
    			self.default['showPlayPageNotes']=False
    			with open("docs/default.json", "w") as f:f.write(json.dumps(self.default))
    		self.station=None
    		self.keyboard=None
    	elif self.showNotesStation==False:
	    	self.position=position
	    	self.station=station
	    	self.keyboard=keyboard
    	if self.station=="down":
	    	if self.keyboard=="left" or self.left.collidepoint(self.position):self.playerDirection="left"
	    	elif self.keyboard=="right" or self.right.collidepoint(self.position):self.playerDirection="right"
	    	elif self.keyboard=="up" or self.up.collidepoint(self.position):self.playerDirection="up"
	    	elif self.keyboard=="down" or self.down.collidepoint(self.position):self.playerDirection="down"
	    	elif self.keyboard=="space" and self.spaceKeyStation:self.__pause()
    	elif self.station=="up":
    		self.playerDirection=None
    		if self.keyboard=="space" and self.spaceKeyStation==False:self.spaceKeyStation=True
    		
    		
    def __pause(self):
    	self.spaceKeyStation=False
    	self.screen.blit(self.darkBackgroundImageOne,(0,0))
    	self.tempText=pygame.font.Font(self.fontTwo,round(self.screenWidth*32/720)).render(self.data['language']['space'][self.default['language']], True,"cyan")
    	self.screen.blit(self.tempText,(self.screenWidth/2-self.tempText.get_size()[0]/2,self.screenHeight/2-self.tempText.get_size()[1]/2))
    	self.run=not self.run
    	
    	
    def __crash(self):
    	self.run=False
    	self.statement="crash"
    	self.playerDirection=None
    	if self.default["songAndSfx"]=="on":
    		self.stopAllSfx=True
    		self.loopSfx.stop()
    		self.gasSfx.stop()
    		self.stopSfx.stop()
    		if self.crashSfxStation:
    			self.crashSfx.play()
    			self.crashSfxStation=False
    	if self.score>self.default['highScore']:self.default['highScore']=round(self.score)
    	with open("docs/default.json", "w") as f:
    		f.write(json.dumps(self.default))
    		
    		
    def __upgradeScoreText(self,text,color):
    	self.tempText=pygame.font.Font(self.fontTwo,round(self.screenWidth*40/720)).render(text, True,color)
    	self.screen.blit(self.tempText,(83*self.screenWidth/100,6*self.screenHeight/100))
    	self.closeOvertakingCount+=1
    	if self.closeOvertakingCount>5:
    		self.score+=1.5
    		self.closeOvertakingCount=0
    	if self.passNpcStation:
    		self.score+=5
    		self.passNpcStation=False
    	if self.touchStation:
    		self.score-=5
    		self.touchStation=False
    		
    		
    def __showNotes(self):
    	self.run=False
    	self.notesText=pygame.font.Font(self.fontOne,round(self.screenWidth*45/720)).render(self.data['language']['howToPlay'][self.default['language']], True,"cyan")
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
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*50/720)).render("A", True,"cyan"),(67.5*self.screenWidth/100,24.5*self.screenHeight/100))
    	self.tempTextOne=pygame.font.Font(self.fontTwo,round(self.screenWidth*25/720)).render(self.data['language']['playPageLeftAndAText'][self.default['language']], True,pygame.Color("goldenrod"))
    	self.screen.blit(self.tempTextOne,(self.screenWidth/2-self.tempTextOne.get_size()[0]/2,32*self.screenHeight/100))
    	
    	pygame.draw.rect(self.screen,(15,15,15),(20*self.screenWidth/100,36*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(0,138,138),(20*self.screenWidth/100,36*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100),1)
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*60/720)).render(">", True,"cyan"),(27.5*self.screenWidth/100,35.5*self.screenHeight/100))
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*32/720)).render("R I G H T", True,(0,138,138)),(21*self.screenWidth/100,39.5*self.screenHeight/100))
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*60/720)).render("/", True,(0,138,138)),(48*self.screenWidth/100,37*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(15,15,15),(60*self.screenWidth/100,36*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(0,138,138),(60*self.screenWidth/100,36*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100),1)
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*50/720)).render("D", True,"cyan"),(67.5*self.screenWidth/100,37.5*self.screenHeight/100))
    	self.tempTextTwo=pygame.font.Font(self.fontTwo,round(self.screenWidth*25/720)).render(self.data['language']['playPageRightAndDText'][self.default['language']], True,pygame.Color("goldenrod"))
    	self.screen.blit(self.tempTextTwo,(self.screenWidth/2-self.tempTextTwo.get_size()[0]/2,45*self.screenHeight/100))
    	
    	pygame.draw.rect(self.screen,(15,15,15),(20*self.screenWidth/100,49*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(0,138,138),(20*self.screenWidth/100,49*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100),1)
    	self.screen.blit(pygame.transform.rotate(pygame.font.Font(self.fontTwo,round(self.screenWidth*64/720)).render("<", True,"cyan"),270),(25*self.screenWidth/100,50*self.screenHeight/100))
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*32/720)).render("U P", True,(0,138,138)),(26.5*self.screenWidth/100,52.5*self.screenHeight/100))
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*60/720)).render("/", True,(0,138,138)),(48*self.screenWidth/100,50*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(15,15,15),(60*self.screenWidth/100,49*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(0,138,138),(60*self.screenWidth/100,49*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100),1)
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*50/720)).render("W", True,"cyan"),(67*self.screenWidth/100,50.5*self.screenHeight/100))
    	self.tempTextThree=pygame.font.Font(self.fontTwo,round(self.screenWidth*25/720)).render(self.data['language']['playPageUpAndWText'][self.default['language']], True,pygame.Color("goldenrod"))
    	self.screen.blit(self.tempTextThree,(self.screenWidth/2-self.tempTextThree.get_size()[0]/2,58*self.screenHeight/100))
    	
    	pygame.draw.rect(self.screen,(15,15,15),(20*self.screenWidth/100,62*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(0,138,138),(20*self.screenWidth/100,62*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100),1)
    	self.screen.blit(pygame.transform.rotate(pygame.font.Font(self.fontTwo,round(self.screenWidth*60/720)).render(">", True,"cyan"),-90),(25*self.screenWidth/100,63*self.screenHeight/100))
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*32/720)).render("D O W N", True,(0,138,138)),(21*self.screenWidth/100,65.5*self.screenHeight/100))
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*60/720)).render("/", True,(0,138,138)),(48*self.screenWidth/100,63*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(15,15,15),(60*self.screenWidth/100,62*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(0,138,138),(60*self.screenWidth/100,62*self.screenHeight/100,20*self.screenWidth/100,7*self.screenHeight/100),1)
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*50/720)).render("S", True,"cyan"),(67.5*self.screenWidth/100,63.5*self.screenHeight/100))
    	self.tempTextFour=pygame.font.Font(self.fontTwo,round(self.screenWidth*25/720)).render(self.data['language']['playPageDownAndSText'][self.default['language']], True,pygame.Color("goldenrod"))
    	self.screen.blit(self.tempTextFour,(self.screenWidth/2-self.tempTextFour.get_size()[0]/2,71*self.screenHeight/100))
    	
    	pygame.draw.rect(self.screen,(15,15,15),(30*self.screenWidth/100,75*self.screenHeight/100,40*self.screenWidth/100,7*self.screenHeight/100))
    	pygame.draw.rect(self.screen,(0,138,138),(30*self.screenWidth/100,75*self.screenHeight/100,40*self.screenWidth/100,7*self.screenHeight/100),1)
    	self.screen.blit(pygame.font.Font(self.fontTwo,round(self.screenWidth*40/720)).render("S P A C E", True,"cyan"),(38*self.screenWidth/100,77*self.screenHeight/100))
    	self.tempTextFive=pygame.font.Font(self.fontTwo,round(self.screenWidth*25/720)).render(self.data['language']['playPageSpaceText'][self.default['language']], True,pygame.Color("goldenrod"))
    	self.screen.blit(self.tempTextFive,(self.screenWidth/2-self.tempTextFive.get_size()[0]/2,84*self.screenHeight/100))
    		
    		
    		
class Enemy():
	def __init__(self,screen,size,npcList,numberOfEnemy,difficulty):
		self.screen=screen
		self.screenWidth,self.screenHeight=size[0],size[1]
		self.npcImageList=npcList
		self.numberOfEnemy=numberOfEnemy
		self.difficulty=difficulty
		self.passNpc=False
		self.npcXLaneList=[14,33,55,74]
		self.npcOneImage=random.choice(self.npcImageList)
		self.npcOneX=self.npcOneX=random.choice(self.npcXLaneList)*self.screenWidth/100
		if self.difficulty=="easy":
			self.npcOneY=-self.screenHeight
		elif self.difficulty=="medium":
			if self.numberOfEnemy==0:self.npcOneY=-self.screenHeight
			elif self.numberOfEnemy==1:self.npcOneY=-150*self.screenHeight/100
			elif self.numberOfEnemy==2:self.npcOneY=-2*self.screenHeight
		elif self.difficulty=="hard":
			if self.numberOfEnemy==0:self.npcOneY=-66*self.screenHeight/100
			elif self.numberOfEnemy==1:self.npcOneY=-self.screenHeight
			elif self.numberOfEnemy==2:self.npcOneY=-133*self.screenHeight/100
			elif self.numberOfEnemy==3:self.npcOneY=-166*self.screenHeight/100
			elif self.numberOfEnemy==4:self.npcOneY=-2*self.screenHeight
			
			
	def draw(self):
		self.screen.blit(self.npcOneImage,(self.npcOneX,self.npcOneY))
		self.bodyRect=pygame.Rect(self.npcOneX,self.npcOneY,self.npcOneImage.get_size()[0],self.npcOneImage.get_size()[1])
		self.crashRect=pygame.Rect(self.npcOneX,self.npcOneY+90*self.npcOneImage.get_size()[1]/100,self.npcOneImage.get_size()[0],10*self.npcOneImage.get_size()[1]/100)
		self.safeRect=pygame.Rect(self.npcOneX,self.npcOneY,self.npcOneImage.get_size()[0],90*self.npcOneImage.get_size()[1]/100)
		self.leftRect=pygame.Rect(self.npcOneX-50*self.npcOneImage.get_size()[0]/100,self.npcOneY,10*self.npcOneImage.get_size()[0]/100,self.npcOneImage.get_size()[1])
		self.rightRect=pygame.Rect(self.npcOneX+150*self.npcOneImage.get_size()[0]/100,self.npcOneY,10*self.npcOneImage.get_size()[0]/100,self.npcOneImage.get_size()[1])
		
		
	def move(self,roadSpeed,yChange):
	    self.npcOneY+=roadSpeed+yChange
	    if self.npcOneY>self.screenHeight:
	    	self.npcOneImage=random.choice(self.npcImageList)
	    	if self.difficulty=="easy":self.npcOneY=-self.npcOneImage.get_size()[1]
	    	elif self.difficulty=="medium":self.npcOneY=-self.screenHeight/2
	    	elif self.difficulty=="hard":self.npcOneY=-66*self.screenHeight/100
	    	self.npcOneX=random.choice(self.npcXLaneList)*self.screenWidth/100
	    	self.passNpc=True
	    else:self.passNpc=False