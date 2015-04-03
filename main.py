#!/usr/bin python
from pyprocessing import *
from pong_src import *
import random
import time

ball = None
p1 = None
p2 = None
win = False
speedX = None
speedY = None
winner = {'winner':''}
server = networking.OSCserver(7777, 'ff', "/player/position", "/ball/position")
cli = networking.OSCclient('localhost', 5555)
ellapsed = 0
startTime = 0

#####PLAYERS#####
def players():
	global p1, p2
	racketWidth = 10
	racketHeight = 100
	p1RacketX = 20
	p1RacketY = height/2 - racketHeight/2
	p2RacketX = (width-20) - racketWidth/2
	p2RacketY = height/2 - racketHeight/2
	p1 = pong_elements.Racket(p1RacketX, p1RacketY, racketWidth, racketHeight)
	p2 = pong_elements.Racket(p2RacketX, p2RacketY, racketWidth, racketHeight)

def randomSpeed():
	global speedX, speedY
	speedX = random.randint(-4,4)
	speedY = random.randint(-4,4)
	while speedX == 0 or speedY == 0:
		speedX = random.randint(-4,4)
		speedY = random.randint(-4,4)

######SETUP######
def setup():
	global ball, p1, winner, speedX, speedY
	size(500, 500)
	randomSpeed()
	ball = pong_elements.Ball(width/2, height/2, 20, 20, speedX, speedY)
	players()

######LOOP######
def draw():
	global win
	background(0)
	stroke(255)
	for i in range(50):
		line(width/2, i*10, width/2, i*10-3)
	textSize(8)
	text("NETWORK PONG", 70, height-10)
	text("press 'q' to quit", 330, height-10)
	if not win:
		global ball, p1, p2, server, cli
		checkGameOver()
		ball.display()
		ball.update()
		p1.display()
		p2.display()
		collision()
		oscData = server.receive()
		checkIncomeData(oscData)
		cli.sendMessage("/player/position", p1.x, p1.y)
		cli.sendMessage("/ball/position", ball.x, ball.y)
	
	if win:
		global win, winner, ellapsed, startTime
		textSize(28)
		maxTime = 3
		if ellapsed == 0:
			startTime = time.time()
			ellapsed = time.time() - startTime
		elif ellapsed > 0 and ellapsed < maxTime:
			ellapsed = time.time() - startTime
			print ellapsed
			if winner['winner'] == 'player1':
				background(0)
				text("YOU WIN!!", width/2 - 130, height/2)
				textSize(14)
				text("restarting game...", width/2 - 110, height/2 + 30)
			elif winner['winner'] == 'player2':
				background(0)
				text("YOU LOOSE!!", width/2 - 140, height/2)
				textSize(14)
				text("restarting game...", width/2 - 110, height/2 + 30)
		else:
			win = False
			ellapsed = 0
			print 'reseting'
			reset()

####P-B-COLLISION####
def collision():
	global ball, p1, p2
	if ball.x <= p1.x + p1.scaleX + ball.scaleX/2:
		if ball.y >= p1.y and ball.y <= p1.y + p1.scaleY:
			ball.speedX *= -1
	if ball.x >= p2.x - ball.scaleX/2:
		if ball.y >= p2.y and ball.y <= p2.y + p2.scaleY:
			ball.speedX *= -1

####COMPARE OSC DATA####
def checkIncomeData(data):
	global ball, p2
	try:
		start = True
		if data[0] == '/player/position':
			p2.x = width - p2.scaleX - data[1][0]
			p2.y = data[1][1]
		if data[0] == '/ball/position':
			ball.x = data[1][0]
			ball.y = data[1][1]
	except:
		data = None

##CHECK IF SOMEONE WINS##
def checkGameOver():
	global ball, p1, p2, win, winner
	if ball.x < 0:
		win = True
		winner['winner'] = 'player2'
	elif ball.x > width:
		win = True
		winner['winner'] = 'player1'

###KEYPRESSED-EVENT###
def keyPressed():
	global p1, cli
	if key.char == "e": 
		p1.moveUp()
	elif key.char == "d":
		p1.moveDown()
	elif key.char == "q":
		exit(1)

###RESET GAME###
def reset():
	global ball, p1, winner, win
	speedX = random.randint(-2,2)
	speedY = random.randint(-2,2)
	ball = pong_elements.Ball(width/2, height/2, 20, 20, speedX, speedY)
	players()

##RUN-PYPROCESSING##
run()