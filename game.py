from UI import UIupdate, mapRender
import cv2
import math

'''
	gameState:
		0 INIT -> players place their armies, in group of 3 and then the carry
			until: all players have finished their deltaArmies
		1 PLAYER0 obtains tanks
		2 PLAYER places its tanks then or set for PLAYER+1 or to BATTLE
		3 BATTLE PHASE
		4 POSITIONATE
		repeat
'''

gameState = 0
armiesCount =0
pid = 0 	# Player id

def click_handle(event, x, y, flags, param):
	global gameState
	global pid
	global armiesCount


	players = param[0]
	display = param[1]
	padding = param[2]
	ratio   = param[3]

	x = int(x/ratio-padding)
	y = int(y/ratio)
	
	if event == cv2.EVENT_LBUTTONUP:
		print(x, ": ", y)
		
		if (gameState==10):
			gameState = 2


		if gameState==0:
			for player in players:
				for state in player.empire:
					if (x>=state.tl[0] and x<=state.br[0] and y>=state.tl[1] and y<=state.br[1]):
						if (state.owner.id==pid):
							state.armyNum += 1
							players[pid].deltaArmies -= 1
							armiesCount += 1

							cont = 0
							for p in players:
								if (p.deltaArmies==0):
									cont += 1
								else:
									break
							if (cont == len(players)):
								gameState = 10
								pid = (pid + 1) % len(players)
								x=-1
								y=-1
							else:
								if (armiesCount==3 or players[pid].deltaArmies==0):
									print("Player"+str(pid) + " ends it's turn!")
									pid = (pid + 1) % len(players)
									armiesCount = 0

		if gameState==2:
			print("gamestate 2")

			for player in players:
				for state in player.empire:
					if (x>=state.tl[0] and x<=state.br[0] and y>=state.tl[1] and y<=state.br[1]):
						if (state.owner.id==pid):
							state.armyNum += 1
							players[pid].deltaArmies -= 1
							armiesCount += 1

							if (players[pid].deltaArmies==0):
									print("Player"+str(pid) + " ends it's turn!")
									pid = (pid + 1) % len(players)
									armiesCount = 0
									gameState+=1
									gameState=10

		if gameState==10:
			print("gamestate 10")

			players[pid].deltaArmies = math.floor(len(players[pid].empire)/3)

			print("Player", pid, " gains ", players[pid].deltaArmies)

		UIupdate(players, pid, gameState)


def PlayControl(players, display, padding, ratio):
	#Player0 starts
	global pid

	while(True):

		while(players[pid].deltaArmies!=0):
			UIupdate(players, pid, 0)
			
			# WAIT FOR CLICK HANDLED CORRECTLY
			param=  [players, display, padding, ratio]
			cv2.setMouseCallback("image", click_handle, param)

			break

		cv2.waitKey(0)
		break