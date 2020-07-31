from state import state
from player import player
from map import *
from UI import UIControl
from game import PlayControl
from data import *

import random
import cv2
import numpy as np
import math

import pyautogui


class GameInfo:
	def __init__(self):
		self.playersNum = 6
		self.statesNum = 42
		self.players = []
		self.att_box = []
		self.def_box = []
		self.attacker = None
		self.defender = None

		self.attArmy = -1
		self.defArmy = -1

		self.fromState = None
		self.toState = None
		self.center = 0
		self.radius = 0
		self.angle = 0
		self.minMove = 0
		self.maxMove = 0


		#self.state = BATTLE_PHASE
		self.state = INIT_PHASE
		self.armiesCount = 0
		self.pid = 0
		self.display = None
		self.padding = 0
		self.ratio = 2/3
		self.moretext = ""

		self.cards = []

		## SCREEN size
		self.size = pyautogui.size()

game = GameInfo()

#GENERATE PLAYERS

for i in range(game.playersNum):
	game.players.append(player(id=i, empire = []))

#GENERATE STATES
states = {}
for elem in adjacency:

	s = state(name = elem)
	s.armyNum = 1
	s.owner = None

	s.adjacency = adjacency[elem]

	s.tl = coord[elem][0]
	s.br = coord[elem][1]

	width = s.br[0] - s.tl[0]
	height = s.br[1] - s.tl[1]

	w1 = int(0.04*width)
	w2 = int(0.07*width)
	s.width = w3 = int(0.26*width)

	h1 = int(0.04*height)
	h2 = int(0.07*height)
	s.height = h3 = int(0.26*height)

	for j in range(3):
		h = s.tl[1]+h1+j*h3+j*h2
		for i in range(3):
			s.pointsTL.append((s.tl[0]+w1+i*w2+i*w3, h))

	for p in s.pointsTL:
		s.pointsBR.append((p[0]+w3, p[1]+h3))

	w1 = int(0.01*width)
	w2 = int(0.02*width)
	s.width = w3 = int(0.23*width)

	h1 = int(0.01*height)
	h2 = int(0.02*height)
	s.height = h3 = int(0.23*height)

	for j in range(4):
		h = s.tl[1]+h1+j*h3+j*h2
		for i in range(4):
			s.pointsTL16.append((s.tl[0]+w1+i*w2+i*w3, h))


	for p in s.pointsTL16:
		s.pointsBR16.append((p[0]+w3, p[1]+h3))

	states[elem] = s

	## also build game.cards
	game.cards.append(elem)



#SELECT FIRST PLAYER
# just for now: player 0 starts

#DISTRIBUTE TERRITORIES

states_name = []
for elem in adjacency:
	states_name.append(elem)

random.shuffle(states_name)

idx = 0
for i in range(game.statesNum):
	pid = idx%game.playersNum
	state = states[states_name[i]]
	game.players[pid].empire.append(state)
	state.owner = game.players[pid]
	#if (state.owner.id==0):
	#	state.armyNum=10
	idx+=1

deltaArmies = 35 - 5*(game.playersNum-3)

for player in game.players:
	player.deltaArmies =  1#deltaArmies - len(player.empire)

### SHUFFLE CARDS
random.shuffle(game.cards)

UIControl(game)

###### ATTACKER AND DEFENDER CONTROL BOX

pad2 = 6
ht = 60

game.att_box.append([[332, 252], [504, 514]])

game.att_box.append([[332+pad2, 514-3*pad2-3*ht], [504-pad2, 514-3*pad2-2*ht]])
game.att_box.append([[332+pad2, 514-2*pad2-2*ht], [504-pad2, 514-2*pad2-ht]])
game.att_box.append([[332+pad2, 514-pad2-ht], [504-pad2, 514-pad2]])

for box in game.att_box:
	box[0][0]+=game.padding
	box[1][0]+=game.padding
	game.def_box.append([[box[0][0]+200, box[0][1]], [box[1][0]+200, box[1][1]]])

PlayControl(game)