from state import state
from player import player
from map import adjacency, coord
from UI import UIControl
from game import PlayControl
import random
import cv2
import numpy as np
import math

playersNum = 3
statesNum = 42

#GENERATE PLAYERS
players = []
for i in range(playersNum):
	players.append(player(id=i, empire = []))

#GENERATE STATES
states = {}
for elem in adjacency:

	s = state(name = elem)
	s.armyNum = 1
	s.owner = None
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

#SELECT FIRST PLAYER
# just for now: player 0 starts

#DISTRIBUTE CARDs (territories)
states_name = []
for elem in adjacency:
	states_name.append(elem)

random.shuffle(states_name)

idx = 0
for i in range(statesNum):
	pid = idx%playersNum
	state = states[states_name[i]]
	players[pid].empire.append(state)
	state.owner = players[pid]
	idx+=1

deltaArmies = 35 - 5*(len(players)-3)

for player in players:
	player.deltaArmies =  1#deltaArmies - len(player.empire)


display, padding, ratio = UIControl(players)

PlayControl(players, display, padding, ratio)