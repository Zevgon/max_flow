from collections import Set, deque

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

class Graph:
	@classmethod
	def create(self, start_positions, end_positions, path):
		start_position_set = set(start_positions)
		end_position_set = set(end_positions)
		vertex_tracker = {}
		start_vertices = []
		end_vertices = []

		for idx in range(len(path)):
			new_vertex = Graph.create_vertex(
				idx,
				start_position_set,
				end_position_set,
				start_vertices,
				end_vertices
			)
			vertex_tracker[idx] = new_vertex

		Graph.add_edges_to_vertices(vertex_tracker, path, end_position_set)
		return Graph(start_vertices, end_vertices)

	@classmethod
	def add_edges_to_vertices(self, vertex_tracker, path, end_position_set):
		seen_indices = set()
		for room_idx, room in enumerate(path):
			if room_idx in end_position_set:
				continue
			for to_room_idx, corridor_capacity in enumerate(room):
				if corridor_capacity != 0:
					from_vertex = vertex_tracker[room_idx]
					to_vertex = vertex_tracker[to_room_idx]
					new_edge = Edge(from_vertex, to_vertex, corridor_capacity)
					seen_indices.add(to_room_idx)

	@classmethod
	def create_vertex(self, idx, start_positions, end_positions, start_vertices, end_vertices):
		if idx in start_positions:
			new_vertex = Vertex(float('inf'))
			start_vertices.append(new_vertex)
			return new_vertex
		elif idx in end_positions:
			new_vertex = Vertex(0, float('inf'))
			end_vertices.append(new_vertex)
			return new_vertex
		else:
			return Vertex()


	def __init__(self, start_vertices, end_vertices):
		self.start_vertices = start_vertices
		self.end_vertices = end_vertices
		self.find_effective_capacities()

	def find_effective_capacities(self):
		q = deque(list(self.end_vertices) + self.find_to_nowhere_vertices())
		explored_vertices = set(q)
		count = 0
		while q:
			curr_vertex = q.popleft()
			explored_vertices.add(curr_vertex)
			for in_edge in curr_vertex.in_edges:
				minimum = min([in_edge.weight, curr_vertex.mec])
				from_vertex = in_edge.from_vertex
				from_vertex.mec += minimum
				if curr_vertex.mec < in_edge.effective_weight:
					in_edge.effective_weight = curr_vertex.mec
				curr_vertex.sum_ieew += in_edge.effective_weight
				curr_vertex.update_needed_bunnies()
				from_vertex.used_out_edge_count += 1
				if from_vertex.used_out_edge_count == len(from_vertex.out_edges) and not from_vertex in explored_vertices:
					q.append(from_vertex)
			count += 1

	def find_to_nowhere_vertices(self):
		end_vertices_set = set(self.end_vertices)
		seen_vertices = set()
		to_nowhere_vertices = []
		q = deque()
		for vertex in self.start_vertices:
			q.append(vertex)
			seen_vertices.add(vertex)

		while q:
			curr_v = q.popleft()
			for edge in curr_v.out_edges:
				if edge.to_vertex in seen_vertices:
					continue
				if len(edge.to_vertex.out_edges) == 0 and not edge.to_vertex in end_vertices_set:
					to_nowhere_vertices.append(edge.to_vertex)
				seen_vertices.add(edge.to_vertex)
				q.append(edge.to_vertex)

		return to_nowhere_vertices

	def find_max_bunnies_in_end_vertices(self):
		queue = deque()
		for vertex in self.start_vertices:
			self.add_edges_to_queue(vertex, queue)

		while queue:
			curr_edge = queue.popleft()
			to_vertex, from_vertex = curr_edge.to_vertex, curr_edge.from_vertex

			if from_vertex.current_bunnies == 0 or to_vertex.current_bunnies == to_vertex.mec:
				to_vertex.used_in_edge_count += 1
				if to_vertex.ins_equal():
					self.add_edges_to_queue(to_vertex, queue)
				continue

			if curr_edge.used:
				send_amt = min([
					from_vertex.current_bunnies,
					curr_edge.effective_weight,
					to_vertex.mec - to_vertex.current_bunnies
				])
				curr_edge.send_bunnies(send_amt)
				to_vertex.used_in_edge_count += 1
				if to_vertex.ins_equal():
					self.add_edges_to_queue(to_vertex, queue)
				continue

			requested_bunnies = curr_edge.effective_weight + to_vertex.needed_bunnies
			if requested_bunnies > 0:
				send_amt = min([requested_bunnies,
										curr_edge.effective_weight,
										from_vertex.current_bunnies
									])
				curr_edge.send_bunnies(send_amt)

			if curr_edge.effective_weight > 0:
				curr_edge.used = True
				queue.append(curr_edge)
			else:
				to_vertex.used_in_edge_count += 1
				if to_vertex.ins_equal():
					self.add_edges_to_queue(to_vertex, queue)

		return self.sum_end_vertices_capacity()

	def add_edges_to_queue(self, vertex, queue):
		for edge in vertex.out_edges:
			queue.append(edge)

	def sum_end_vertices_capacity(self):
		total = 0
		for vertex in self.end_vertices:
			total += vertex.current_bunnies

		return total




def answer(entrances, exits, path):
    graph = Graph.create(entrances, exits, path)
    return graph.find_max_bunnies_in_end_vertices()


# print(answer([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))
g = [
	[0, 0, 4, 6, 0, 0],
	[0, 0, 5, 2, 0, 0],
	[0, 0, 0, 0, 4, 4],
	[0, 0, 0, 0, 6, 6],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0]
]
s = [0, 1]
e = [4, 5]
print answer(s, e, g)
