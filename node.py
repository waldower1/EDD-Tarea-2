class node:

	def __init__(self, title, score):
		self.titles = [title]
		self.score = score
		self.left_son = None
		self.right_son = None
		self.parent = None
		self.height = 1