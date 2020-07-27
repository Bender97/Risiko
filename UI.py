import random
import cv2
import numpy as np
import math

display = []

ratio = 2/3
padding = 0

moretext = ""

colors = [
	(255, 0, 0),
	(0, 255, 0),
	(0, 0, 255),
	(255, 255, 0),
	(255, 0, 255),
	(0, 255, 255),
	]

def mapRender(players):
	global display
	global moretext
	global padding

	image = cv2.imread("map.jpg")

	for player in players:
		for s in player.empire:
			cv2.rectangle(image, s.tl, s.br, colors[s.owner.id], 2)

			if (s.armyNum<=9):
				for j in range(s.armyNum):
					cv2.rectangle(image, s.pointsTL[j], s.pointsBR[j], colors[s.owner.id], 2)
			else:				
				qty = s.armyNum

				for j in range(math.floor(qty/10)):
					cv2.rectangle(image, s.pointsTL16[j], s.pointsBR16[j], colors[s.owner.id], -1)

				for j in range(qty - math.floor(qty/10)*10):
					c = math.floor(qty/10) + j
					cv2.rectangle(image, s.pointsTL16[c], s.pointsBR16[c], colors[s.owner.id], 2)


	padding = int(0.3*image.shape[1])

	display = np.zeros((image.shape[0], image.shape[1]+padding, 3), dtype=np.uint8)

	display[:, padding:] = image[:, :]

	text_x = 50
	text_y = 50

	for i in range(len(players)):
		text = "Player" + str(i) + ": " + str(players[i].deltaArmies)
		cv2.putText(display, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,  
	                   1, (255, 255, 255), 2, cv2.LINE_AA)
		text_y += 50

	if (moretext!=""):
		for i, line in enumerate(moretext.split('\n')):
			if (line!=""):
				cv2.putText(display, line, (50, text_y), cv2.FONT_HERSHEY_SIMPLEX,  
		                   1, (255, 255, 255), 2, cv2.LINE_AA)
				text_y+=50
		moretext=""


	display = cv2.resize(display, (int(display.shape[1]*ratio), int(display.shape[0]*ratio)))
	cv2.imshow("image", display)

def UIControl(players):
	# RENDER img
	
	cv2.namedWindow("image")

	mapRender(players)

	return display, padding, ratio
	
	#cv2.waitKey(0)



def UIupdate(players, pid, gameState):
	global display
	global moretext
	moretext = "It's Player" + str(pid) + " turn!\n"
	
	if (gameState==0):
		moretext += "+ " + str(players[pid].deltaArmies) + " tanks\n"
	elif (gameState==10):
		moretext += "Player" + str(pid) + " gains " + str(players[pid].deltaArmies) + " tanks!\n"
		moretext += "+ " + str(players[pid].deltaArmies) + " tanks\n"
	elif (gameState==2):
		moretext += "+ " + str(players[pid].deltaArmies) + " tanks\n"
	elif (gameState==3):
		moretext += "Player" + str(pid) + " BATTLE PHASE\n"

	mapRender(players)