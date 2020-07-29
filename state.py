from map import adjacency
import random

class state:
	def __init__(self, name = "**", armyNum=0, owner=None):
		### STATE
		self.name = name
		self.armyNum = armyNum
		self.owner = owner

		### COORDINATES
		self.tl = (-1, -1)
		self.br = (-1, -1)
		self.width = -1
		self.height = -1
		self.pointsTL = []
		self.pointsBR = []
		self.pointsTL16 = []
		self.pointsBR16 = []
		
		### ADJACENCY
		self.adjacency = []

		self.selected = False


	def attack(self, opponent, myArmyNum, oppArmyNum):
		myArmy = []
		oppArmy = []

		for i in range(1, myArmyNum):
			myArmy.append(random.randint(1, 6))
		for i in range(1, oppArmyNum):
			oppArmy.append(random.randint(1, 6))
		

		myArmy.sort()
		oppArmy.sort()

		myLost = 0
		oppLost = 0

		for i in range(min(len(myArmy), len(oppArmy))):
			if(myArmy[i]>oppArmy):
				oppLost += 1
			else:
				myLost +=1

		print("attacker loses " + str(myLost) + " and defender loses " + str(oppLost))

		#### ATTENZIONE! BISOGNA AGGIORNARE IL NUMERO DI ARMATE!!