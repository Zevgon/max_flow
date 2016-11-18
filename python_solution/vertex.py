class Vertex:
	def __init__(self, current_bunnies = 0, mec = 0):
		self.in_edges = []
		self.out_edges = []
		self.current_bunnies = current_bunnies
		self.mec = mec
		self.used_out_edge_count = 0
		self.used_in_edge_count = 0
		self.needed_bunnies = 0
		self.sum_ieew = 0

	def ins_equal(self):
		return self.used_in_edge_count == len(self.in_edges)

	def outs_equal(self):
		return self.used_out_edge_count == len(self.out_edges)

	def update_needed_bunnies(self):
		self.needed_bunnies = self.mec - self.sum_ieew
