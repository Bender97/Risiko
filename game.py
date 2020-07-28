from UI import UIupdate
import cv2
import math
import random
from data import *

'''
	game.state:
		0 INIT -> players place their armies, in group of 3 and then the carry
			until: all players have finished their deltaArmies
		1 PLAYER0 obtains tanks
		2 PLAYER places its tanks then or set for PLAYER+1 or to BATTLE
		3 BATTLE PHASE
		4 POSITIONATE
		repeat
'''

def getState(game, x, y):
	for player in game.players:
		for state in player.empire:
			if (x>=state.tl[0] and x<=state.br[0] and y>=state.tl[1] and y<=state.br[1]):
				return state.owner.id, state
	return -1, None

def getAttackerControl(game, x, y):

	if (x>=game.att_box[1][0][0] and x<=game.att_box[1][1][0]):
		for i in range(1, 4):
			if (y>=game.att_box[i][0][1] and y<=game.att_box[i][1][1]):
				return i

	return -1
def getDefenderControl(game, x, y):

	if (x>=game.def_box[1][0][0] and x<=game.def_box[1][1][0]):
		for i in range(1, 4):
			if (y>=game.def_box[i][0][1] and y<=game.def_box[i][1][1]):
				return i

	return -1

def assign_std_armies(game):
	game.players[game.pid].deltaArmies = math.floor(len(game.players[game.pid].empire)/3)

def click_handle(event, x, y, flags, param):
	game = param
	if event == cv2.EVENT_LBUTTONUP:

		game.moretext = ""

		x = int(x/game.ratio-game.padding)
		y = int(y/game.ratio)

		if game.state==INIT_PHASE:
			stateOwner, state = getState(game, x, y)
			if (stateOwner==game.pid):				
				state.armyNum += 1
				game.players[game.pid].deltaArmies -= 1
				game.armiesCount += 1

				cont = 0
				for p in game.players:
					if (p.deltaArmies==0):
						cont += 1
					else:
						game.moretext += "+ " + str(game.players[game.pid].deltaArmies) + " tanks\n"
						break
				if (cont == len(game.players)):
					game.pid = (game.pid + 1) % len(game.players)
					assign_std_armies(game)
					game.moretext += "Player" + str(game.pid) + " gains " + str(game.players[game.pid].deltaArmies) + " tanks!\n"
					print("Player", game.pid, " gains ", game.players[game.pid].deltaArmies)
					game.state = ASK_FOR_CARDS_PHASE
					x=-1
					y=-1
				else:
					if (game.armiesCount==3 or game.players[game.pid].deltaArmies==0):
						print("Player"+str(game.pid) + " ends it's turn!")
						game.pid = (game.pid + 1) % len(game.players)
						game.armiesCount = 0

		#endif INIT_PHASE


		if game.state==ASK_FOR_CARDS_PHASE:
			print("ASK_FOR_CARDS_PHASE")			
			# TO IMPLEMENT!!!
			game.state = PLACE_ARMIES_PHASE
		#endif ASK_FOR_CARDS_PHASE


		if game.state==PLACE_ARMIES_PHASE:
			print("PLACE_ARMIES_PHASE")

			stateOwner, state = getState(game, x, y)
			if (stateOwner==game.pid):			
				state.armyNum += 1
				game.players[game.pid].deltaArmies -= 1
				game.armiesCount += 1

				if (game.players[game.pid].deltaArmies==0):
						#print("Player"+str(pid) + " ends it's turn!")
						#pid = (pid + 1) % len(players)
						game.armiesCount = 0										
						#assign_std_armies(players, pid)
						#moretext += "Player" + str(pid) + " gains " + str(players[pid].deltaArmies) + " tanks!\n"
						#print("Player", pid, " gains ", players[pid].deltaArmies)
						x = -1
						y = -1
						game.state = BATTLE_PHASE
			
				else:
					game.moretext += "+ " + str(game.players[game.pid].deltaArmies) + " tanks\n"	
		#endif PLACE_ARMIES_PHASE


		if game.state==BATTLE_PHASE:

			#1 select my state
			stateOwner, state = getState(game, x, y)
			if (stateOwner==game.pid):			
				if (game.attacker==None):
					if state.armyNum>=2:
						game.attacker = state
						print("Attacker is: " + game.attacker.name)
					else:
						print("ERROR: no sufficient armies")

			elif (stateOwner!=-1):
				if (game.attacker!=None and game.defender==None):
					if (state.name in game.attacker.adjacency):
						game.defender = state
						print("Defender is: " + game.defender.name)
						game.state = WAR_PHASE
						x = -1
						y = -1
					else:
						print("ERROR! selected defender not adjacent")

			game.moretext += "++ BATTLE PHASE"


		if game.state == WAR_PHASE and x!=-1:
			# attacker selects it's army
			if (game.attArmy<0):
				game.attArmy = getAttackerControl(game, x+game.padding, y)
				print("attacker chooses: ", game.attArmy)
			elif game.defArmy<0:
				game.defArmy = getDefenderControl(game, x+game.padding, y)
				print("defender chooses: ", game.defArmy)

			if (game.defArmy>0):
				#WAR!

				attack = []
				defense = []
				for i in range(game.attArmy):
					attack.append(random.randint(1, 6))
				for i in range(game.defArmy):
					defense.append(random.randint(1, 6))

				attack.sort(reverse=True)
				defense.sort(reverse=True)
				print("attack:  " + str(attack))
				print("defense: " + str(defense))
				attackLost = 0
				defenseLost = 0

				for i in range(min(game.attArmy, game.defArmy)):
					if attack[i]<=defense[i]:
						attackLost+=1
					else:
						defenseLost+=1

				print("attack  (", game.attacker.name, ") loses: ", attackLost)
				print("defense (", game.defender.name, ") loses: ", defenseLost)

				game.attacker.armyNum-=attackLost
				game.defender.armyNum-=defenseLost

				if (game.defender.armyNum==0):
					print("attack  (", game.attacker.name, ") conquers: ", game.defender.name)
					
					game.players[game.defender.owner.id].empire.remove(game.defender)
					game.players[game.pid].empire.append(game.defender)

					game.defender.owner = game.players[game.pid]
					game.attacker.armyNum -= (game.attArmy-attackLost)
					game.defender.armyNum = (game.attArmy-attackLost)

					


				game.attacker = None
				game.defender = None
				game.attArmy = -1
				game.defArmy = -1
				game.state = BATTLE_PHASE
		

		game.moretext = "It's Player" + str(game.pid) + " turn!\n" + game.moretext
		UIupdate(game)


def PlayControl(game):

	cv2.setMouseCallback("image", click_handle, game)

		
	while(True):
		cv2.waitKey(0)
		break