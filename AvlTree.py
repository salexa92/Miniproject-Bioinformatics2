import AvlNode


class AVLTree:
	def __init__(self):
		self.rootNode = None
		self.elements_count = 0
		self.rebalance_count = 0

	def height(self):
		if self.rootNode:
			return self.rootNode.height
		else:
			return 0

	def insert(self, key):
		new_node = AvlNode (key)
		if not self.rootNode:
			self.rootNode = new_node
		else:
			if not self.find (key):
				self.elements_count += 1
				self.add_as_child (self.rootNode, new_node)

	def find(self, key):
		return self.find_in_subtree (self.rootNode, key)

	def rebalance(self, node_to_rebalance):
		self.rebalance_count += 1
		A = node_to_rebalance
		F = A.parent  # allowed to be NULL
		if node_to_rebalance.balance () == -2:
			if node_to_rebalance.rightChild.balance () <= 0:
				"""Rebalance, case RRC """
				B = A.rightChild
				C = B.rightChild
				assert (not A is None and not B is None and not C is None)
				A.rightChild = B.leftChild
				if A.rightChild:
					A.rightChild.parent = A
				B.leftChild = A
				A.parent = B
				if F is None:
					self.rootNode = B
					self.rootNode.parent = None
				else:
					if F.rightChild == A:
						F.rightChild = B
					else:
						F.leftChild = B
					B.parent = F
				self.recompute_heights (A)
				self.recompute_heights (B.parent)
			else:
				"""Rebalance, case RLC """
				B = A.rightChild
				C = B.leftChild
				assert (not A is None and not B is None and not C is None)
				B.leftChild = C.rightChild
				if B.leftChild:
					B.leftChild.parent = B
				A.rightChild = C.leftChild
				if A.rightChild:
					A.rightChild.parent = A
				C.rightChild = B
				B.parent = C
				C.leftChild = A
				A.parent = C
				if F is None:
					self.rootNode = C
					self.rootNode.parent = None
				else:
					if F.rightChild == A:
						F.rightChild = C
					else:
						F.leftChild = C
					C.parent = F
				self.recompute_heights (A)
				self.recompute_heights (B)
		else:
			assert (node_to_rebalance.balance () == +2)
			if node_to_rebalance.leftChild.balance () >= 0:
				B = A.leftChild
				C = B.leftChild
				"""Rebalance, case LLC """
				assert (not A is None and not B is None and not C is None)
				A.leftChild = B.rightChild
				if (A.leftChild):
					A.leftChild.parent = A
				B.rightChild = A
				A.parent = B
				if F is None:
					self.rootNode = B
					self.rootNode.parent = None
				else:
					if F.rightChild == A:
						F.rightChild = B
					else:
						F.leftChild = B
					B.parent = F
				self.recompute_heights (A)
				self.recompute_heights (B.parent)
			else:
				B = A.leftChild
				C = B.rightChild
				"""Rebalance, case LRC """
				assert (not A is None and not B is None and not C is None)
				A.leftChild = C.rightChild
				if A.leftChild:
					A.leftChild.parent = A
				B.rightChild = C.leftChild
				if B.rightChild:
					B.rightChild.parent = B
				C.leftChild = B
				B.parent = C
				C.rightChild = A
				A.parent = C
				if F is None:
					self.rootNode = C
					self.rootNode.parent = None
				else:
					if (F.rightChild == A):
						F.rightChild = C
					else:
						F.leftChild = C
					C.parent = F
				self.recompute_heights (A)
				self.recompute_heights (B)

	def recompute_heights(self, start_from_node):
		changed = True
		node = start_from_node
		while node and changed:
			old_height = node.height
			node.height = (node.max_children_height () + 1 if (node.rightChild or node.leftChild) else 0)
			changed = node.height != old_height
			node = node.parent

	def add_as_child(self, parent_node, child_node):
		node_to_rebalance = None
		if child_node.key < parent_node.key:
			if not parent_node.leftChild:
				parent_node.leftChild = child_node
				child_node.parent = parent_node
				if parent_node.height == 0:
					node = parent_node
					while node:
						node.height = node.max_children_height () + 1
						if not node.balance () in [-1, 0, 1]:
							node_to_rebalance = node
							break  # we need the one that is furthest from the root
						node = node.parent
			else:
				self.add_as_child (parent_node.leftChild, child_node)
		else:
			if not parent_node.rightChild:
				parent_node.rightChild = child_node
				child_node.parent = parent_node
				if parent_node.height == 0:
					node = parent_node
					while node:
						node.height = node.max_children_height () + 1
						if not node.balance () in [-1, 0, 1]:
							node_to_rebalance = node
							break  # we need the one that is furthest from the root
						node = node.parent
			else:
				self.add_as_child (parent_node.rightChild, child_node)

		if node_to_rebalance:
			self.rebalance (node_to_rebalance)

	def find_in_subtree(self, node, key):
		if node is None:
			return None  # key not found
		if key < node.key:
			return self.find_in_subtree (node.leftChild, key)
		elif key > node.key:
			return self.find_in_subtree (node.rightChild, key)
		else:  # key is equal to node key
			return node
