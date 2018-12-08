from node import node


class ABB:
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
			else:
				self.insert(cur_node.left_son, title, score)
		elif score > cur_node.score:
			if cur_node.right_son == None:
				cur_node.right_son = node(title, score)
				cur_node.right_son.parent = cur_node
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
		elif score < cur_node.score and cur_node.left_son != None:
			return self.find(cur_node.left_son, score)
		elif score > cur_node.score and cur_node.right_son != None:
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