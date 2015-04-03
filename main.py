#!/usr/bin python
from pyprocessing import *
from pong_src import *
import random
from multiprocessing import Process

ball = None
p1 = None
p2 = None
server = networking.OSCserver(7777, 'ff', "/player/position", "/ball/position")
cli = networking.OSCclient('localhost', 5555)

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

######SETUP######
def setup():
	global ball, p1
	size(500, 500)
	speedX = random.randint(-2,2)
	speedY = random.randint(-2,2)
	ball = pong_elements.Ball(width/2, height/2, 20, 20, speedX, speedY)
	players()

######LOOP######
def draw():
	global ball, p1, p2, server, cli
	background(0)
	stroke(255)
	for i in range(50):
		line(width/2, i*10, width/2, i*10-3)
	textSize(8)
	text("NETWORK PONG", 70, height-10)
	text("press 'q' to quit", 330, height-10)
	ball.display()
	ball.update()
	p1.display()
	p2.display()
	collision()
	oscData = server.receive()
	checkIncomeData(oscData)
	cli.sendMessage("/player/position", p1.x, p1.y)
	cli.sendMessage("/ball/position", ball.x, ball.y)

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
	if data[0] == '/player/position':
		p2.x = width - p2.scaleX - data[1][0]
		p2.y = data[1][1]
	if data[0] == '/ball/position':
		ball.x = data[1][0]
		ball.y = data[1][1]

###KEYPRESSED-EVENT###
def keyPressed():
	global p1, cli
	if key.char == "e": 
		p1.moveUp()
	elif key.char == "d":
		p1.moveDown()
	elif key.char == "q":
		exit(1)

##RUN-PYPROCESSING##
run()