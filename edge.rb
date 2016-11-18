class Edge
	attr_reader :from_vertex, :to_vertex, :weight
	attr_accessor :effective_weight, :used
	def initialize(from_vertex, to_vertex, weight)
		@from_vertex = from_vertex
		@to_vertex = to_vertex
		@weight = weight
		@effective_weight = weight
		@used = false
		add_self_to_vertices
	end

	def add_self_to_vertices
		@from_vertex.out_edges << self
		@to_vertex.in_edges << self
	end

	def send_bunnies(num_bunnies)
		@from_vertex.current_bunnies -= num_bunnies
		@to_vertex.current_bunnies += num_bunnies
		@effective_weight -= num_bunnies
		@to_vertex.needed_bunnies -= num_bunnies
		@effective_weight = [@from_vertex.current_bunnies, @effective_weight].min
	end
end
