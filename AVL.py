from node import node


class AVL:

	def __init__(self, name, data):
		self.name = name
		self.root = None
		for anime in data:
			if self.root == None:
				self.root = node(anime["title"], anime["score"])
			else:
				self.insert(self.root, anime["title"], anime["score"])

	def insert(self, cur_node, title, score):
		if score < cur_node.score:
			if cur_node.left_son == None:
				cur_node.left_son = node(title, score)
				cur_node.left_son.parent = cur_node
				self.inspect_insertion(cur_node.left_son)
			else:
				self.insert(cur_node.left_son, title, score)
		elif score > cur_node.score:
			if cur_node.right_son == None:
				cur_node.right_son = node(title, score)
				cur_node.right_son.parent = cur_node
				self.inspect_insertion(cur_node.right_son)
			else:
				self.insert(cur_node.right_son, title, score)
		else:
			cur_node.titles.append(title)

	def print_tree(self, cur_node):
		if cur_node:
			self.print_tree(cur_node.left_son)
			for title in cur_node.titles:
				print("Title: {}, Score: {}".format(title, cur_node.score))
			self.print_tree(cur_node.right_son)


	def find(self, cur_node, score):
		if score == cur_node.score and cur_node.titles != []:
			return cur_node
		elif score < cur_node.score and cur_node.left_son:
			return self.find(cur_node.left_son, score)
		elif score > cur_node.score and cur_node.right_son:
			return self.find(cur_node.right_son, score)
		else:
			return None

	def delete_title(self, cur_node, title):
		del cur_node.titles[title]
		if cur_node.titles == []:
			self.delete_node(cur_node)

	def delete_node(self, node_to_del):

		node_parent = node_to_del.parent

		if not node_to_del.left_son and not node_to_del.right_son:
			if node_parent:
				if node_parent.left_son == node_to_del:
					node_parent.left_son = None
				else:
					node_parent.right_son = None
			else:
				self.root = None

		elif not node_to_del.left_son or not node_to_del.right_son:
			if node_to_del.left_son:
				son = node_to_del.left_son
			else:
				son = node_to_del.right_son
			if node_parent:
				if node_parent.left_son == node_to_del:
					node_parent.left_son = son
				else:
					node_parent.right_son = son
			else:
				self.root = son
			son.parent = node_parent

		else:
			successor = self.min(node_to_del.right_son)
			node_to_del.score = successor.score
			node_to_del.titles = successor.titles
			self.delete_node(successor)

		if node_parent:
			node_parent.height = 1 + max(self.get_height(node_parent.left_son),
			                             self.get_height(node_parent.right_son))

			self.inspect_deletion(node_parent)

	def inspect_insertion(self, cur_node, path=[]):
		if cur_node.parent:
			path.append(cur_node)
			left_height = self.get_height(cur_node.parent.left_son)
			right_height = self.get_height(cur_node.parent.right_son)

			if abs(left_height - right_height) > 1:
				path.append(cur_node.parent)
				self.rebalance_node(path[-1],path[-2],path[-3])
			else:
				new_height = 1 + cur_node.height 
				if new_height > cur_node.parent.height:
					cur_node.parent.height = new_height
				self.inspect_insertion(cur_node.parent, path)

	def inspect_deletion(self, cur_node):
		if cur_node:
			left_height = self.get_height(cur_node.left_son)
			right_height = self.get_height(cur_node.right_son)

			if abs(left_height - right_height) > 1:
				y = self.taller_son(cur_node)
				z = self.taller_son(y)
				self.rebalance_node(cur_node, y, z)

			self.inspect_deletion(cur_node.parent)

	def rebalance_node(self, x, y, z):
		if y == x.left_son and z == y.left_son:
			self.right_rotate(x, y)

		elif y == x.left_son and z == y.right_son:
			self.left_rotate(y, z)
			self.right_rotate(x, z)

		elif y == x.right_son and z == y.right_son:
			self.left_rotate(x, y)

		elif y == x.right_son and z == y.left_son:
			self.right_rotate(y, z)
			self.left_rotate(x, z)

	def right_rotate(self, x, y):
		parent = x.parent
		son = y.right_son
		y.right_son = x
		x.parent = y
		x.left_son = son
		if son:
			son.parent = x
		y.parent = parent
		if not y.parent:
			self.root = y
		else:
			if y.parent.left_son == x:
				y.parent.left_son = y
			else:
				y.parent.right_son = y

		x.height = 1+max(self.get_height(x.left_son),
					     self.get_height(x.right_son))
		y.height = 1+max(self.get_height(y.left_son),
					     self.get_height(y.right_son))

	def left_rotate(self, x, y):
		parent = x.parent 
		son = y.left_son
		y.left_son = x
		x.parent = y
		x.right_son = son
		if son:
			son.parent = x
		y.parent = parent
		if not y.parent: 
			self.root = y
		else:
			if y.parent.left_son == x:
				y.parent.left_son = y
			else:
				y.parent.right_son = y

		x.height = 1+max(self.get_height(x.left_son),
						 self.get_height(x.right_son))
		y.height = 1+max(self.get_height(y.left_son),
						 self.get_height(y.right_son))

	def get_height(self, cur_node):
		if not cur_node:
			return 0
		return cur_node.height

	def taller_son(self, cur_node):
		left_height = self.get_height(cur_node.left_son)
		right_height = self.get_height(cur_node.right_son)
		if left_height >= right_height:
			return cur_node.left_son
		return cur_node.right_son 

	def min(self, cur_node):
		cur = cur_node
		while cur.left_son:
			cur = cur.left_son
		return cur

	def max(self, cur_node):
		cur = cur_node
		while cur.right_son:
			cur = cur.right_son
		return cur