class Edge:
	def __init__(self, from_vertex, to_vertex, weight):
		self.from_vertex = from_vertex
		self.to_vertex = to_vertex
		self.weight = weight
		self.effective_weight = weight
		self.used = False
		self.add_self_to_vertices()

	def add_self_to_vertices(self):
		self.from_vertex.out_edges.append(self)
		self.to_vertex.in_edges.append(self)

	def send_bunnies(self, num_bunnies):
		self.from_vertex.current_bunnies -= num_bunnies
		self.to_vertex.current_bunnies += num_bunnies
		self.effective_weight -= num_bunnies
		self.to_vertex.needed_bunnies -= num_bunnies
		self.effective_weight = min([self.from_vertex.current_bunnies, self.effective_weight])
