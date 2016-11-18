require 'byebug'


# Game plan:
# * Create a directed graph of the input. Rooms are vertices and corridors are weighted edges, the weight being the number of bunnies tha can fit through it. Don't add any edges whose @from_vertex would be an @end_vertex. The graph should have an array of @start_vertices and an array of @end_vertices. See below for properties of Graph, Vertex, and Edge
#
# * Phase 1: Traverse through the graph backwards to find the @max_effective_capacity of all vertices
# 		NB @max_effective_capacity: Property of a vertex such that if it was a start vertex and the only start vertex, this many bunnies could leave the exit pods at one time
# 	* Each @end_vertex should start with a @max_effective_capacity of infinity, all other vertices 0
# 	* Create a queue, populated at first with the @end_vertices
# 	* Create a set of explored_vertices that contains our @end_vertices
# 	* Until the queue is empty:
# 		* Pop out the first item of the queue and put it into our explored_vertices set
# 		* For each @in_edge of the vertex:
# 			* Get the min of the edge's @weight and the current vertex's @mec and add that min to the @mec of the edge's @from_vertex
# 			* If the current vertex's @mec is less than the current edge's @weight, change
# 					the current edge's @effective_weight to the current vertex's @mec
# 			* Add one to the @used_out_edge_count of the edge's @from_vertex
# 			* If the @used_out_edge_count and the @out_edges.length of the @from_vertex are equal and the @from_vertex is not included in the explored_vertices:
# 				* Put the @from_vertex into the queue
#
# * Phase 2: Traverse through the graph forwards to find the maximum possible bunnies
# 	that can leave the exit pods at one time
# 	* Each @start_vertex should start with a @current_bunnies of infinity, all other vertices 0
# 	* Create a queue, populated at first with the @start_vertices
# 	* Create a set of explored_vertices that contains our @start_vertices
# 	* Until the queue is empty:
# 		* Pop out the first item of the queue and put it into our explored_vertices set
# 		* For each @out_edge of the vertex:
# 			* Get the min of the edge's @effective_weight and the current vertex's @current_bunnies and add that min to the @current_bunnies of the edge's @to_vertex
# 			* Subtract the min from the current vertex's @current_bunnies
# 			* If the @to_vertex's @current_bunnies is greater than its @mec, reduce the value of its @current_bunnies to match the @mec
# 			* Add one to the @used_in_edge_count of the edge's @to_vertex
# 			* If the @used_in_edge_count and the @in_edges.length of the @to_vertex are equal and the @to_vertex is not included in the explored_vertices:
# 				* Put the @to_vertex into the queue
# 	* Return the sum of the @end_vertices' @current_bunnies

* Reset all vertices' @used_in_edge_count to 0

* Get the @mec of each vertex minus the sum of its incoming edges' @effective_weights
	* Call that value @needed_bunnies and have that as a property on all vertices
* Get the sum of every edge's @effective_weight and its @to_vertex's @needed_bunnies
	* Call that value @send_at_least and have that as a property on all edges

* Create an empty max heap to store edges
* Go through the graph forwards
	* For each @start_vertex
		* Go through the vertex's @out_edges
			* Insert the @out_edge into the max heap based on its @send_at_least property
	* Until the heap is empty:
		* Extract the max edge
			* Get the min of its @from_vertex's @current_bunnies, its own @effective_weight, and its @to_vertex's @mec
			* Add that many bunnies to its @to_vertex's @current_bunnies
			* Subtract that amount from its @from_vertex's @current_bunnies
			* For each edge coming from its @from_vertex that have @effective_weights greater than the @from_vertex's @current_bunnies:
				* Reduce its @effective_weights to match the @current_bunnies of its @from_vertex
				* Add that reduced amount to the @needed_bunnies of the @to_vertex
				* For each @in_edge of the @to_vertex:
					* Recalculate the edge's @send_at_least and reheapify if included in the heap
			* Add 1 to the @to_vertex's @used_in_edge_count
			* If the @to_vertex's @used_in_edge_count equals its @in_edges.length:
				* Add all of the @to_vertex's @out_edges to the heap
* Return the sum of the @end_vertices' @current_bunnies


# * Graph properties and methods:
# 	* @start_vertices (initializes to empty array)
# 	* @end_vertices (initializes to empty array)
#
# * Vertex properties:
# 	* @out_edges (initializes to empty array)
# 	* @in_edges (initializes to empty array)
# 	* @max_effective_capacity (initializes to 0 unless specified)
# 	* @current_bunnies (initializes to 0)
# 	* @used_out_edge_count (initializes to 0)
# 	* @used_in_edge_count (initializes to 0)
#
# * Edge properties:
# 	* @from_vertex (must be specified)
# 	* @to_vertex (must be specified)
# 	* @weight (must be specified)
# 	* @effective_weight (initializes to @weight)
