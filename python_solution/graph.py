from vertex import Vertex
from edge import Edge
from collections import Set, deque

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
					if to_vertex != from_vertex:
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





# g1 = Graph.create([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
# print(g1.find_max_bunnies_in_end_vertices())
# # Answer is 16


# g2 = Graph.create([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]])
# print(g2.find_max_bunnies_in_end_vertices())
# # Answer is 6

# g3 = Graph.create(
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
# print(g3.find_max_bunnies_in_end_vertices())

# g4 = Graph.create(
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
# print(g4.find_max_bunnies_in_end_vertices())










g5 = Graph.create(
	[0, 1, 2, 3, 14],
	[15, 16, 17, 20, 21],
	[
		[0, 0, 0, 0, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 60, 5, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 14, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 10, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 44, 47, 88, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 90, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 35, 58, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 57, 95, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 23, 50, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 72, 61, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 62],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	]
)
print(g5.find_max_bunnies_in_end_vertices())
# Answer is 73

# g6 = Graph.create(
# 	[8, 9, 10],
# 	[0, 1],
# 	[
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 50, 30, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 70, 40, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 70, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 90, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 20, 0, 0, 0]
# 	]
# )
#
# print(g6.find_max_bunnies_in_end_vertices())
