require 'byebug'

require_relative 'vertex'
require_relative 'edge'
require 'set'

class Graph
	def self.create(start_positions, end_positions, path)
		start_position_set = Set.new(start_positions)
		end_position_set = Set.new(end_positions)
		vertex_tracker = {}
		start_vertices = []
		end_vertices = []

		path.each_index do |idx|
			new_vertex = Graph.create_vertex(
				idx,
				start_positions,
				end_positions,
				start_vertices,
				end_vertices
			)
			vertex_tracker[idx] = new_vertex
		end

		Graph.add_edges_to_vertices(vertex_tracker, path, end_position_set)
		Graph.new(start_vertices, end_vertices)
	end

	def self.add_edges_to_vertices(vertex_tracker, path, end_position_set)
		seen_indices = Set.new
		path.each.with_index do |room, room_idx|
			next if end_position_set.include?(room_idx)
			room.each.with_index do |corridor_capacity, to_room_idx|
				if corridor_capacity != 0
					from_vertex = vertex_tracker[room_idx]
					to_vertex = vertex_tracker[to_room_idx]
					new_edge = Edge.new(from_vertex, to_vertex, corridor_capacity)
					seen_indices << to_room_idx
				end
			end
		end
	end

	def self.create_vertex(idx, start_positions, end_positions, start_vertices, end_vertices)
		if start_positions.include?(idx)
			new_vertex = Vertex.new(Float::INFINITY)
			start_vertices << new_vertex
			new_vertex
		elsif end_positions.include?(idx)
			new_vertex = Vertex.new(0, Float::INFINITY)
			end_vertices << new_vertex
			new_vertex
		else
			Vertex.new
		end
	end


	attr_reader :start_vertices, :end_vertices
	def initialize(start_vertices, end_vertices)
		@start_vertices = start_vertices
		@end_vertices = end_vertices
		find_effective_capacities
	end

	def find_effective_capacities
		q = @end_vertices.dup + find_to_nowhere_vertices
		explored_vertices = Set.new(q)
		count = 0
		until q.empty?
			curr_vertex = q.shift
			explored_vertices << curr_vertex
			curr_vertex.in_edges.each do |in_edge|
				min = [in_edge.weight, curr_vertex.mec].min
				from_vertex = in_edge.from_vertex
				from_vertex.mec += min
				in_edge.effective_weight = curr_vertex.mec if curr_vertex.mec < in_edge.effective_weight
				curr_vertex.sum_ieew += in_edge.effective_weight
				curr_vertex.update_needed_bunnies!
				from_vertex.used_out_edge_count += 1
				if from_vertex.used_out_edge_count == from_vertex.out_edges.length &&
					!explored_vertices.include?(from_vertex)
					q << from_vertex
				end
			end
			count += 1
		end
	end

	def find_to_nowhere_vertices
		end_vertices_set = Set.new(@end_vertices)
		seen_vertices = Set.new
		to_nowhere_vertices = []
		q = []
		@start_vertices.each do |vertex|
			q << vertex
			seen_vertices << vertex
		end
		until q.empty?
			curr_v = q.shift
			curr_v.out_edges.each do |edge|
				next if seen_vertices.include?(edge.to_vertex)
				if edge.to_vertex.out_edges.length == 0 && !end_vertices_set.include?(edge.to_vertex)
					to_nowhere_vertices << edge.to_vertex
				end
				seen_vertices << edge.to_vertex
				q << edge.to_vertex
			end
		end

		to_nowhere_vertices
	end

	# def find_max_bunnies_in_end_vertices
	# 	q = @start_vertices.dup
	# 	explored_vertices = Set.new(q)
	# 	count = 0
	# 	until q.empty?
	# 		curr_vertex = q.shift
	# 		explored_vertices << curr_vertex
	# 		curr_vertex.out_edges.each do |out_edge|
	# 			# debugger
	# 			min = [curr_vertex.current_bunnies, out_edge.effective_weight].min
	# 			to_vertex = out_edge.to_vertex
	# 			to_vertex.current_bunnies += min
	# 			curr_vertex.current_bunnies -= min
	# 			curr_vertex.current_bunnies = 0 if curr_vertex.current_bunnies < 0
	# 			to_vertex.current_bunnies = to_vertex.mec if to_vertex.mec < to_vertex.current_bunnies
	# 			to_vertex.used_in_edge_count += 1
	# 			if to_vertex.used_in_edge_count == to_vertex.in_edges.length &&
	# 				!explored_vertices.include?(to_vertex)
	# 				q << to_vertex
	# 			end
	# 		end
	# 		count += 1
	# 	end
	#
	# 	@end_vertices.reduce(0){|acc, vertex| acc + vertex.current_bunnies}
	# end

	def find_max_bunnies_in_end_vertices
		queue = []
		@start_vertices.each do |vertex|
			add_edges_to_queue(vertex, queue)
		end

		until queue.empty?
			curr_edge = queue.shift
			# if curr_edge.weight == 58
			# 	debugger
			# end
			to_vertex, from_vertex = curr_edge.to_vertex, curr_edge.from_vertex

			if from_vertex.current_bunnies == 0 || to_vertex.current_bunnies == to_vertex.mec
				to_vertex.used_in_edge_count += 1
				add_edges_to_queue(to_vertex, queue) if to_vertex.ins_equal?
				next
			end

			if curr_edge.used
				send_amt = [
					from_vertex.current_bunnies,
					curr_edge.effective_weight,
					to_vertex.mec - to_vertex.current_bunnies
				].min
				curr_edge.send_bunnies(send_amt)
				to_vertex.used_in_edge_count += 1
				add_edges_to_queue(to_vertex, queue) if to_vertex.ins_equal?
				next
			end

			requested_bunnies = curr_edge.effective_weight + to_vertex.needed_bunnies
			if requested_bunnies > 0
				send_amt = [requested_bunnies,
										curr_edge.effective_weight,
										from_vertex.current_bunnies
									].min
				curr_edge.send_bunnies(send_amt)
			end
			if curr_edge.effective_weight > 0
				curr_edge.used = true
				queue << curr_edge
			else
				to_vertex.used_in_edge_count += 1
				add_edges_to_queue(to_vertex, queue) if to_vertex.ins_equal?
			end
		end

		sum_end_vertices_capacity
	end

	def add_edges_to_queue(vertex, queue)
		vertex.out_edges.each do |edge|
			queue << edge
		end
	end

	def sum_end_vertices_capacity
		total = 0
		@end_vertices.each do |vertex|
			total += vertex.current_bunnies
		end

		total
	end
end

# g1 = Graph.create([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
# p g1.find_max_bunnies_in_end_vertices
# # Answer is 16

# g2 = Graph.create([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]])
# p g2.find_max_bunnies_in_end_vertices
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
# p g3.find_max_bunnies_in_end_vertices
# debugger;
# 1 + 2

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
# p g4.find_max_bunnies_in_end_vertices










# g5 = Graph.create(
# 	[0, 1, 2, 3, 14],
# 	[15, 16, 17, 20, 21],
# 	[
# 		[0, 0, 0, 0, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 60, 5, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 14, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 10, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 44, 47, 88, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 90, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 35, 58, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 57, 95, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 23, 50, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 72, 61, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 62],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 	]
# )
# p g5.find_max_bunnies_in_end_vertices
# Answer is 73

g6 = Graph.create(
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

p g6.find_max_bunnies_in_end_vertices
