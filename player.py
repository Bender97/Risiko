from state import state
from map import adjacency
import cv2

class player:
	def __init__(self, id, empire = [], target = [], bonusCards = []):
		self.id = id
		self.empire = empire
		self.target = target
		self.bonusCards = bonusCards
		self.deltaArmies = 0
		self.alive = True
		self.img = cv2.imread(imgs[self.id])

imgs = ["imgs/blue_army.png","imgs/green_army.png","imgs/red_army.png","imgs/purple_army.png","imgs/yellow_army.png","imgs/black_army.png"]