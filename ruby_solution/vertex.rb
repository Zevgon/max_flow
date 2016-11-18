class Vertex
	attr_accessor :in_edges,
		:out_edges,
		:current_bunnies,
		:mec,
		:used_out_edge_count,
		:used_in_edge_count,
		:needed_bunnies,
		:sum_ieew

	def initialize(current_bunnies = 0, mec = 0)
		@in_edges = []
		@out_edges = []
		@current_bunnies = current_bunnies
		@mec = mec
		@used_out_edge_count = 0
		@used_in_edge_count = 0
		@needed_bunnies = 0
		@sum_ieew = 0
	end

	def ins_equal?
		@used_in_edge_count == @in_edges.length
	end

	def outs_equal?
		@used_out_edge_count == @out_edges.length
	end

	def update_needed_bunnies!
		@needed_bunnies = @mec - @sum_ieew
	end
end
