class Vertex
	attr_accessor :capacity, :to_edges, :from_edges, :is_start, :is_end
	def initialize(capacity = 0)
		@capacity = capacity
		@to_edges = []
		@from_edges = []
		@is_start = false
		@is_end = false
	end

	def children
		children = []
		self.to_edges.each do |to_edge|
			children << to_edge.to_vertex
		end

		children
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

def escape_pods(entrances, exits, path)
	vertices = []
	vertex_tracker = {}
	path.each.with_index do |room, room_idx|
		vertex = vertex_tracker[room_idx]
		vertex ||= Vertex.new
		room.each.with_index do |corridor_capacity, to_room|
			if corridor_capacity != 0
				vertex.capacity += corridor_capacity
				vertex_tracker[to_room] ||= Vertex.new
				vertex.children << vertex_tracker[to_room]
				vertices << vertex
			end
		end
	end

	exits.each do |exit_room|
		vertex_tracker[exit_room].is_end = true
	end

	vertices
end

p escape_pods([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
