from collections import Set, deque

class Vertex:
	def __init__(self):
		self.out_edges = []
		self.in_edges = []
		self.height = 0
		self.excess = 0

class Edge:
	def __init__(self, from_v, to_v, weight):
		self.from_v = from_v
		self.to_v = to_v
		self.weight = weight
		self.add_self_to_vertices()
		self.counterpart = None

	def add_self_to_vertices(self):
		self.to_v.in_edges.append(self)
		self.from_v.out_edges.append(self)

	def send_excess(self):
		send_amt = min([self.weight, self.from_v.excess])
		self.to_v.excess += send_amt
		self.from_v.excess -= send_amt
		self.counterpart.weight += send_amt
		self.weight -= send_amt

class MaxHeap:
	def __init__(self):
		self.store = []

	def child_indices(self, idx):
		idxs = [(idx + 1) * 2 - 1, (idx + 1) * 2]
		if idxs[0] >= len(self.store):
			return []
		elif idxs[1] >= len(self.store):
			return [idxs[0]]
		else:
			return idxs

	def parent_idx(self, idx):
		if idx % 2 == 0:
			return idx / 2 - 1
		else:
			return idx / 2

	def parent(self, idx):
		parent_idx = self.parent_idx(idx)
		if parent_idx < 0:
			return None
		else:
			return self.store[parent_idx]

	def insert(self, vertex):
		self.store.append(vertex)
		self.heapify_up()

	def heapify_up(self):
		idx = len(self.store) - 1
		parent_idx = self.parent_idx(idx)
		v = self.store[idx]
		parent = self.parent(idx)
		while parent and parent.height < v.height:
			self.store[idx], self.store[parent_idx] = self.store[parent_idx], self.store[idx]
			idx = parent_idx
			parent_idx = self.parent_idx(idx)
			parent = self.parent(idx)

	def extract(self):
		last_idx = len(self.store) - 1
		self.store[0], self.store[last_idx] = self.store[last_idx], self.store[0]
		self.heapify_down()

	def heapify_down(self):
		v = self.store[0]
		self.store.pop()
		child_indices = filter(lambda v: self.store[v].height > self.store[0].height, self.child_indices(0))
		if child_indices:
			child_idx = max(child_indices, key = lambda idx: self.store[idx].height)
		idx = 0
		while child_indices:
			self.store[idx], self.store[child_idx] = self.store[child_idx], self.store[idx]
			child_idx = max(child_indices, key = lambda idx: self.store[idx].height)
			child_indices = filter(lambda v: self.store[v].height > self.store[idx].height, self.child_indices(idx))

		return v

	def first(self):
		return self.store[0]


class Graph:
	@classmethod
	def create_residual(self, starts, ends, path):
		all_vs = []
		for idx in range(0, len(path)):
			all_vs.append(Vertex())

		start_vs = []
		end_vs = []
		already_created = set()
		for path_idx, room in enumerate(path):
			for room_idx, cap in enumerate(room):
				if room_idx == path_idx or hash(str([path_idx, room_idx])) in already_created:
					continue
				if cap != 0:
					e1 = Edge(all_vs[path_idx], all_vs[room_idx], cap)
					e2 = Edge(all_vs[room_idx], all_vs[path_idx], path[room_idx][path_idx])
					e1.counterpart = e2
					e2.counterpart = e1
					already_created.add(hash(str([room_idx, path_idx])))

			if path_idx in starts:
				start_vs.append(all_vs[path_idx])
			elif path_idx in ends:
				end_vs.append(all_vs[path_idx])

		source = Vertex()
		sink = Vertex()
		for start_v in start_vs:
			e1 = Edge(source, start_v, 3000000)
			e2 = Edge(start_v, source, 3000000)
			e1.counterpart = e2
			e2.counterpart = e1
		for end_v in end_vs:
			e1 = Edge(end_v, sink, 3000000)
			e2 = Edge(sink, end_v, 3000000)
			e1.counterpart = e2
			e2.counterpart = e1

		source.height = len(path)
		for edge in source.out_edges:
			edge.to_v.excess += edge.weight
		return Graph(source, sink)

	def __init__(self, source, sink):
		self.source = source
		self.sink = sink

	def push_relabel(self):
		mh = MaxHeap()
		for edge in self.source.out_edges:
			mh.insert(edge.to_v)

		while mh.store:
			max_v = mh.first()
			downhill_v = False
			min_height = float('inf')
			curr_edge = None
			for edge in max_v.out_edges:
				min_height = min([min_height, edge.to_v.height])
				if max_v.height > edge.to_v.height and edge.weight > 0:
					edge.send_excess()
					if edge.to_v != self.source and edge.to_v != self.sink:
						mh.insert(edge.to_v)
					downhill_v = True
					break

			if not downhill_v:
				if max_v.height > min_height:
					max_v.height += 1
				else:
					max_v.height = min_height + 1
			if max_v.excess == 0:
				mh.extract()

		return self.sink.excess




def answer(start_positions, end_positions, path):
	 graph = Graph.create_residual(start_positions, end_positions, path)
	 return graph.push_relabel()


# print answer([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])

# g1 = Graph.create_residual([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
# print(g1.push_relabel())

# g2 = Graph.create_residual([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]])
# print(g2.push_relabel())

# g3 = Graph.create_residual(
# 	[0, 6, 2],
# 	[4, 5],
# 	[
# 		[0, 0, 0, 4, 0, 0, 0],
# 		[0, 0, 0, 6, 8, 0, 0],
# 		[0, 0, 0, 2, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 4, 0],
# 		[0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0],
# 		[0, 6, 0, 0, 0, 0, 0],
# 	]
# )
# print(g3.push_relabel())

# g4 = Graph.create_residual(
# 	[0, 1],
# 	[5, 6],
# 	[
# 		[0, 0, 5, 2, 3, 0, 0],
# 		[0, 0, 10, 16, 20, 0, 0],
# 		[0, 0, 0, 0, 0, 15, 5],
# 		[0, 0, 0, 0, 0, 7, 8],
# 		[0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0]
# 	]
# )
# print(g4.push_relabel())

g6 = Graph.create_residual(
	[8, 9, 10],
	[0, 1],
	[
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 50, 30, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 70, 40, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 70, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 90, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 20, 0, 0, 0]
	]
)

print(g6.push_relabel())

# g7 = Graph.create_residual(
# 	[0],
# 	[5],
# 	[
# 		[0, 5, 5, 0, 0, 0],
# 		[11, 0, 1, 0, 0, 0],
# 		[8, 3, 0, 4, 3, 0],
# 		[0, 12, 5, 0, 7, 5],
# 		[0, 0, 11, 0, 0, 0],
# 		[0, 0, 0, 15, 4, 0]
# 	]
# )
#
# print(g7.push_relabel())
