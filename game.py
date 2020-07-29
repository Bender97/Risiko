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

def getPos(game, x, y):
	if (x>=phase_button[0][0] and x<=phase_button[1][0] and y>=phase_button[0][1] and y<=phase_button[1][1]):
		return 1
	return -1

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

def getMoveControl(game, x, y):
	#print("last attack: ", game.attArmy)

	x_center = int((game.height+game.padding)/2)
	y_center = int(game.width/2)

	game.center=(x_center, y_center)
	game.radius = 300
	game.angle = 360/(game.maxMove-game.minMove+1)

	d_x = x - game.center[0]
	d_y = y - game.center[1]

	dist = math.sqrt(d_x**2+d_y**2)
	if (dist<=game.radius):

		angle = math.atan2(d_y, d_x) *180/3.141592

		if (angle>0):
			return math.floor(angle/game.angle)+game.minMove
		else:
			return math.floor((game.maxMove-game.minMove+1)+angle/game.angle)+game.minMove

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
						game.armiesCount = 0
						x = -1
						y = -1
						game.state = BATTLE_PHASE
			
				else:
					game.moretext += "+ " + str(game.players[game.pid].deltaArmies) + " tanks\n"	
		#endif PLACE_ARMIES_PHASE


		if game.state==BATTLE_PHASE:

			end_battle = getPos(game, x+game.padding, y)

			if (end_battle>=0):
				game.state = MOVE_PHASE
				x = -1
				y = -1
			
			else:
				#1 select my state
				stateOwner, state = getState(game, x, y)
				if (stateOwner==game.pid):
					if state.armyNum>=2:
						game.attacker = state
						print("Attacker is: " + game.attacker.name)
					else:
						print("ERROR: no sufficient armies")

				elif (stateOwner!=-1):
					if (game.attacker!=None and game.defender==None):			## FIRST CHOOSE ATTACKER, THEN DEFENDER
						if (state.name in game.attacker.adjacency):
							game.defender = state
							print("Defender is: " + game.defender.name)
							game.state = WAR_PHASE
							# I need these info to deal with move phase!
							game.attArmy = -1
							game.defArmy = -1
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
					#game.attacker.armyNum -= game.attArmy
					#game.defender.armyNum = game.attArmy
					game.defender.armyNum = 0
					x=-1
					y=-1

					game.minMove = game.attArmy
					game.maxMove = game.attacker.armyNum-1

					game.state = CONQUER_PHASE
			

				else:
					game.attacker = None
					game.defender = None
					game.state = BATTLE_PHASE

		if game.state == CONQUER_PHASE:
			print("CONQUER_PHASE")
			armiesToMove = getMoveControl(game, x+game.padding, y)
			
			if (armiesToMove!=-1):
				print("attacker moves  " + str(armiesToMove) + " armies from " + game.attacker.name + " to " + game.defender.name)
				game.attacker.armyNum -= armiesToMove
				game.defender.armyNum += armiesToMove
				game.state = BATTLE_PHASE

				game.attacker = None
				game.defender = None
				game.minMove = 0
				game.maxMove = 0
		
		if game.state == MOVE_PHASE:

			end_battle = getPos(game, x+game.padding, y)

			if (end_battle>=0):
				game.state = ASK_FOR_CARDS_PHASE
				print("Player"+str(game.pid) + " ends it's turn!")
				game.pid = (game.pid + 1) % len(game.players)
				
				game.armiesCount = 0										
				assign_std_armies(game)
				game.moretext += "Player" + str(game.pid) + " gains " + str(game.players[game.pid].deltaArmies) + " tanks!\n"
				print("Player", game.pid, " gains ", game.players[game.pid].deltaArmies)
			
			else:
				game.moretext += "++ MOVE PHASE\n"
				if (game.fromState==None or game.toState==None):
					#1 select fromState
					stateOwner, state = getState(game, x, y)
					if (stateOwner==game.pid):
						if (game.fromState==None):
							if state.armyNum>=2:
								game.fromState = state
								print("fromState is: " + game.fromState.name)
							else:
								print("ERROR: no sufficient armies")

						elif (game.toState==None):
							if (state.name in game.fromState.adjacency):
								game.toState = state
								print("toState is: " + game.toState.name)
								game.minMove = 0
								game.maxMove = game.fromState.armyNum-1
							else:
								print("ERROR! selected toState not adjacent")
					elif stateOwner>=0:
						print("not your state! keep off your hands")
				else:

					armiesToMove = getMoveControl(game, x+game.padding, y)
					
					if (armiesToMove!=-1):
						game.fromState.armyNum -= armiesToMove
						game.toState.armyNum   += armiesToMove
						game.state = ASK_FOR_CARDS_PHASE

						game.fromState = None
						game.toState = None

						print("Player"+str(game.pid) + " ends it's turn!")
						game.pid = (game.pid + 1) % len(game.players)
						
						game.armiesCount = 0
						assign_std_armies(game)
						game.moretext += "Player" + str(game.pid) + " gains " + str(game.players[game.pid].deltaArmies) + " tanks!\n"
						print("Player", game.pid, " gains ", game.players[game.pid].deltaArmies)


		game.moretext = "It's Player" + str(game.pid) + " turn!\n" + game.moretext
		UIupdate(game)


def PlayControl(game):

	cv2.setMouseCallback("image", click_handle, game)

		
	while(True):
		cv2.waitKey(0)
		break