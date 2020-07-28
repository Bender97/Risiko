from UI import UIupdate
import cv2
import math
from data import *

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

def assign_std_armies(players, pid):
	players[pid].deltaArmies = math.floor(len(players[pid].empire)/3)

def click_handle(event, x, y, flags, param):

	if event == cv2.EVENT_LBUTTONUP:
		global gameState
		global pid
		global armiesCount

		moretext = ""

		players = param[0]
		display = param[1]
		padding = param[2]
		ratio   = param[3]

		x = int(x/ratio-padding)
		y = int(y/ratio)

		if gameState==INIT_PHASE:
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
									moretext += "+ " + str(players[pid].deltaArmies) + " tanks\n"
									break
							if (cont == len(players)):
								pid = (pid + 1) % len(players)
								assign_std_armies(players, pid)
								moretext += "Player" + str(pid) + " gains " + str(players[pid].deltaArmies) + " tanks!\n"
								print("Player", pid, " gains ", players[pid].deltaArmies)
								gameState = ASK_FOR_CARDS_PHASE
								x=-1
								y=-1
							else:
								if (armiesCount==3 or players[pid].deltaArmies==0):
									print("Player"+str(pid) + " ends it's turn!")
									pid = (pid + 1) % len(players)
									armiesCount = 0

		#endif INIT_PHASE


		if gameState==ASK_FOR_CARDS_PHASE:
			print("ASK_FOR_CARDS_PHASE")			
			# TO IMPLEMENT!!!
			gameState = PLACE_ARMIES_PHASE
		#endif ASK_FOR_CARDS_PHASE


		if gameState==PLACE_ARMIES_PHASE:
			print("PLACE_ARMIES_PHASE")

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
									gameState = BATTLE_PHASE
									assign_std_armies(players, pid)
									moretext += "Player" + str(pid) + " gains " + str(players[pid].deltaArmies) + " tanks!\n"
									print("Player", pid, " gains ", players[pid].deltaArmies)
									gameState = ASK_FOR_CARDS_PHASE
			
			moretext += "+ " + str(players[pid].deltaArmies) + " tanks\n"	
			#endif PLACE_ARMIES_PHASE

		moretext = "It's Player" + str(pid) + " turn!\n" + moretext
		UIupdate(players, moretext)


def PlayControl(players, display, padding, ratio):
	#Player0 starts
	global pid

	while(True):

		while(players[pid].deltaArmies!=0):
			UIupdate(players, "")
			
			# WAIT FOR CLICK HANDLED CORRECTLY
			param=  [players, display, padding, ratio]
			cv2.setMouseCallback("image", click_handle, param)

			break

		cv2.waitKey(0)
		break