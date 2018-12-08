class Data:

	def __init__(self, titles, score):
		self.titles = titles
		self.score = score

class Node:
	def __init__(self, title, score, par = None):
		self.data = [Data(title, score)]
		self.parent = par
		self.child = []
	
	def __lt__(self, node):
		return self.data[0].score < node.data[0].score
		
	def add(self, new_node):
		for child in new_node.child:
			child.parent = self
		for data in new_node.data:
			added = False
			for anime in self.data:
				if anime.score == data.score:
					anime.titles.extend(data.titles)
					added = True
					break
			if not added:
				self.data.append(data)

		self.data.sort(key=lambda x: x.score)
		self.child.extend(new_node.child)
		if len(self.child) > 1:
			self.child.sort()
		if len(self.data) > 2:
			self.split()
	
	def insert(self, new_node):
		if len(self.child) == 0:
			self.add(new_node)			
		elif new_node.data[0].score > self.data[-1].score:
			self.child[-1].insert(new_node)
		else:
			for i in range(0, len(self.data)):
				if new_node.data[0].score < self.data[i].score:
					self.child[i].insert(new_node)
					break
	
	def split(self):
		left_child = Node(self.data[0].titles, self.data[0].score, self)
		right_child = Node(self.data[2].titles, self.data[2].score, self)
		if self.child:
			self.child[0].parent = left_child
			self.child[1].parent = left_child
			self.child[2].parent = right_child
			self.child[3].parent = right_child
			left_child.child = [self.child[0], self.child[1]]
			right_child.child = [self.child[2], self.child[3]]
					
		self.child = [left_child]
		self.child.append(right_child)
		self.data = [self.data[1]]
		
		if self.parent:
			if self in self.parent.child:
				self.parent.child.remove(self)
			self.parent.add(self)
		else:
			left_child.parent = self
			right_child.parent = self
			
	def find(self, score):
		for data in self.data:
			if score == data.score and data.titles:
				return data
		if len(self.child) == 0:
			return False
		elif score > self.data[-1].score:
			return self.child[-1].find(score)
		else:
			for i in range(len(self.data)):
				if score < self.data[i].score:
					return self.child[i].find(score)

	def find_destroy(self, score):
		for data in self.data:
			if score == data.score:
				return self
		if len(self.child) == 0:
			return False
		elif score > self.data[-1].score:
			return self.child[-1].find_destroy(score)
		else:
			for i in range(len(self.data)):
				if score < self.data[i].score:
					return self.child[i].find_destroy(score)
		
	def remove(self, data, item):
		for d in self.data:
			if d == data:
				del d.titles[item]

	def print(self):
		try:
			self.child[0].print()
		except Exception as e:
			pass
		try:
			for title in self.data[0].titles:
				print("Title: {}, Score: {}".format(title, self.data[0].score))
		except Exception as e:
			pass
		try:
			self.child[1].print()
		except Exception as e:
			pass
		try:
			for title in self.data[1].titles:
				print("Title: {}, Score: {}".format(title, self.data[1].score))
		except Exception as e:
			pass
		try:
			self.child[2].print()
		except Exception as e:
			pass
	
class TwoThree:
	def __init__(self, name, data):
		self.root = None
		self.name = name
		for anime in data:
			if self.root == None:
				self.root = Node([anime["title"]], anime["score"])
			else:
				self.insert(self.root, anime["title"], anime["score"])
		
	def insert(self, node, title, score):
		self.root.insert(Node([title], score))
		while self.root.parent:
			self.root = self.root.parent
	
	def find(self, node, score):
		return self.root.find(score)
		
	def delete_title(self, data, index):
		node = self.root.find_destroy(data.score)
		node.remove(data, index)

	def min(self, cur_node):
		cur = cur_node
		while cur.child and cur.child[0].data[0].score < cur.data[0].score:
			cur = cur.child[0]
		return cur.data[0]

	def max(self, cur_node):
		cur = cur_node
		while cur.child and cur.child[-1].data[-1].score > cur.data[-1].score:
			cur = cur.child[-1]
		return cur.data[-1]

	def print_tree(self, cur_node):
		cur_node.print()
