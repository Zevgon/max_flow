class Vertex
	attr_accessor :capacity, :to_edges, :from_edges, :is_start, :is_end
	def initialize(capacity = 0)
		@capacity = capacity
		@to_edges = []
		@from_edges = []
		@is_start = false
		@is_end = false
	end
end

class Edge
	attr_reader :from_vertex, :to_vertex, :weight
	def initialize(from_vertex, to_vertex, weight)
		@weight = weight
		@from_vertex = from_vertex
		@to_vertex = to_vertex
	end
end

class Graph
	attr_accessor :start_vertices
	def self.create_graph(entrances, exits, path)
		vertex_tracker = {}
		all_vertices = []
		path.each.with_index do |room, idx|
			vertex = vertex_tracker[idx]
			unless vertex
				vertex = Vertex.new
				vertex_tracker[idx] = vertex
			end
			room.each.with_index do |corridor_capacity, to_room_idx|
				if corridor_capacity != 0
					destination_vertex = vertex_tracker[to_room_idx]
					unless destination_vertex
						destination_vertex = Vertex.new
						vertex_tracker[to_room_idx] = destination_vertex
					end
					edge = Edge.new(vertex, destination_vertex, corridor_capacity)
					vertex.to_edges << edge
					destination_vertex.from_edges << edge
					vertex.capacity += corridor_capacity
				end
			end
			all_vertices << vertex
		end

		graph = Graph.new
		exits.each do |room|
			vertex_tracker[room].is_end = true
		end

		entrances.each do |room|
			vertex = vertex_tracker[room]
			vertex.is_start = true
			graph.start_vertices << vertex
		end

		graph
	end

	def initialize
		@start_vertices = []
	end
end



g = Graph.create_graph([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
p g
