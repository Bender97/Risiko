from state import state
from map import adjacency

class player:
	def __init__(self, id, empire = [], target = [], bonusCards = []):
		self.id = id
		self.empire = empire
		self.target = target
		self.bonusCards = bonusCards
		self.deltaArmies = 0