import random
import cv2
import numpy as np
import math
from data import *

colors = [
	(255, 0, 0),
	(0, 255, 0),
	(0, 0, 255),
	(255, 255, 0),
	(255, 0, 255),
	(0, 255, 255),
	]

def UIupdate(game):

	image = cv2.imread("map.jpg")

	for player in game.players:
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


	game.padding = int(0.3*image.shape[1])

	game.display = np.zeros((image.shape[0], image.shape[1]+game.padding, 3), dtype=np.uint8)
	game.width = game.display.shape[0]
	game.height = game.display.shape[1]

	game.display[:, game.padding:] = image[:, :]

	text_x = 50
	text_y = 50

	for i in range(game.playersNum):
		text = "Player" + str(i) + ": " + str(game.players[i].deltaArmies)
		cv2.putText(game.display, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,  
	                   1, (255, 255, 255), 2, cv2.LINE_AA)
		text_y += 50

	if (game.moretext!=""):
		for i, line in enumerate(game.moretext.split('\n')):
			if (line!=""):
				cv2.putText(game.display, line, (50, text_y), cv2.FONT_HERSHEY_SIMPLEX,  
		                   1, (255, 255, 255), 2, cv2.LINE_AA)
				text_y+=50
		game.moretext=""


	if (game.state==WAR_PHASE):

		cv2.rectangle(game.display, tuple(game.att_box[0][0]), tuple(game.att_box[0][1]), (0, 0, 255), -1)
		cv2.rectangle(game.display, tuple(game.def_box[0][0]), tuple(game.def_box[0][1]), (255, 0, 0), -1)

		cv2.putText(game.display, "Attacker", (game.att_box[0][0][0]+15, game.att_box[0][0][1]+40), cv2.FONT_HERSHEY_SIMPLEX,  
		                   1, (0, 0, 0), 2, cv2.LINE_AA)
		cv2.putText(game.display, "Defender", (game.def_box[0][0][0]+15, game.def_box[0][0][1]+40), cv2.FONT_HERSHEY_SIMPLEX,  
		                   1, (0, 0, 0), 2, cv2.LINE_AA)

		for i, box in enumerate(game.att_box):
			if (i>0 and i<game.attacker.armyNum):
				cv2.rectangle(game.display, tuple(box[0]), tuple(box[1]), (0, 0, 0), 1)
				cv2.putText(game.display, str(i), (box[0][0]+70, box[0][1]+40), cv2.FONT_HERSHEY_SIMPLEX,  
		                   1, (0, 0, 0), 2, cv2.LINE_AA)
		for i, box in enumerate(game.def_box):
			if (i>0 and i<game.defender.armyNum+1):
				cv2.rectangle(game.display, tuple(box[0]), tuple(box[1]), (0, 0, 0), 1)
				cv2.putText(game.display, str(i), (box[0][0]+70, box[0][1]+40), cv2.FONT_HERSHEY_SIMPLEX,  
		                   1, (0, 0, 0), 2, cv2.LINE_AA)
	

	elif game.state==BATTLE_PHASE:
		cv2.rectangle(game.display, phase_button[0], phase_button[1], (255, 255, 255), 1)
		cv2.putText(game.display, "end battle", phase_text, cv2.FONT_HERSHEY_SIMPLEX,  
		                   1, (255, 255, 255), 2, cv2.LINE_AA)

	elif (game.state==MOVE_PHASE and game.toState!=None) or game.state==CONQUER_PHASE:
		if (game.state!=CONQUER_PHASE):
			cv2.rectangle(game.display, phase_button[0], phase_button[1], (255, 255, 255), 1)
			cv2.putText(game.display, "end turn", phase_text, cv2.FONT_HERSHEY_SIMPLEX,  
		                   1, (255, 255, 255), 2, cv2.LINE_AA)

		x_center = int((game.height+game.padding)/2)
		y_center = int(game.width/2)

		game.center=(x_center, y_center)
		game.radius = 300

		cv2.circle(game.display, game.center, game.radius, (0, 0, 255), -1)

		numpts = game.maxMove-game.minMove+1

		print("maxmove: ", game.maxMove, " minMove: ", game.minMove, " maxToMove: ", numpts)


		game.angle = 360/numpts
		cont_angle = 0
		delta = game.angle/2*3.141592/180
		text_radius = game.radius*2/3

		for i in range(numpts):
			ca = cont_angle*3.141592/180
			point = ( int(x_center+game.radius*math.cos(ca)), int(y_center+game.radius*math.sin(ca)))
			cv2.line(game.display, game.center, point, (0, 0, 0))
			cv2.putText(game.display, str(i+game.minMove), (int(x_center+text_radius*math.cos(ca+delta)), int(y_center+text_radius*math.sin(ca+delta))), cv2.FONT_HERSHEY_SIMPLEX,  
		                   1, (255, 255, 255), 2, cv2.LINE_AA)
			text_radius-=2

			cont_angle+=game.angle

	elif (game.state==MOVE_PHASE):
		cv2.rectangle(game.display, phase_button[0], phase_button[1], (255, 255, 255), 1)
		cv2.putText(game.display, "end turn", phase_text, cv2.FONT_HERSHEY_SIMPLEX,  
		                   1, (255, 255, 255), 2, cv2.LINE_AA)



	game.display = cv2.resize(game.display, (int(game.display.shape[1]*game.ratio), int(game.display.shape[0]*game.ratio)))
	cv2.imshow("image", game.display)

def UIControl(game):
	# RENDER img
	
	cv2.namedWindow("image")

	UIupdate(game)
	
	#cv2.waitKey(0)
