# Return the rightmost node and its position with respect to root for a binary tree
class Node:
	def __init__(self, value = '', position = 0, right = None, left = None):
		self.value = value
		self.position = position
		self.right = right
		self.left = left


def AssignPosition(node, position):
	node.position = position
	if isinstance(node.right, Node):
		AssignPosition(node.right, position + 1)

	if isinstance(node.left, Node):
		AssignPosition(node.left, position - 1)


def FindRMN(node):
	maxNode = node
	if isinstance(node.right, Node):
		r = FindRMN(node.right)
		if r.position > maxNode.position:
			maxNode = r
	if isinstance(node.left, Node):
		l = FindRMN(node.left)
		if l.position > maxNode.position:
			maxNode = l
	return maxNode


n1 = Node('1')
n2 = Node('2')
n3 = Node('3')
n4 = Node('4')
n5 = Node('5')
n6 = Node('6')
n7 = Node('7')
n8 = Node('8')
n9 = Node('9')
n10 = Node('10')
n1.right = n2
n1.left = n3
n2.right = n4
n2.left = n5
n3.right = n6
n3.left = n7
n5.right = n8
n8.right = n9
n9.right = n10
AssignPosition(n1, 0)

print FindRMN(n1).position
print FindRMN(n1).value