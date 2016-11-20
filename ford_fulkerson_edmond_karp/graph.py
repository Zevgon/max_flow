from collections import Set, deque

class Vertex:
    def __init__(self):
        self.out_edges = []
        self.in_edges = []

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

class Graph:
    @classmethod
    def create(self, starts, ends, path):
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
            e1 = Edge(source, start_v, float('inf'))
            e2 = Edge(start_v, source, 0)
            e1.counterpart = e2
            e2.counterpart = e1
        for end_v in end_vs:
            e1 = Edge(end_v, sink, float('inf'))
            e2 = Edge(sink, end_v, 0)
            e1.counterpart = e2
            e2.counterpart = e1

        return Graph(source, sink)

    def __init__(self, source, sink):
        self.source = source
        self.sink = sink

    def augmenting_path_cycle(self):
        queue = deque([self.source])
        parent_map = {}
        seen_vs = set([self.source])

        found = False
        while queue and found == False:
            curr_v = queue.popleft()
            for edge in curr_v.out_edges:
                if edge.to_v not in seen_vs and edge.weight > 0:
                    parent_map[edge.to_v] = [edge.from_v, edge]
                    seen_vs.add(edge.to_v)
                    if edge.to_v == self.sink:
                        found = True
                    queue.append(edge.to_v)

        if not found:
            return 0
        min_flow = 10
        vertex = self.sink
        while vertex != self.source:
            min_flow = min([parent_map[vertex][1].weight, min_flow])
            vertex = parent_map[vertex][0]
        self.trace_back_and_update_weights(parent_map, min_flow)
        return min_flow

    def trace_back_and_update_weights(self, parent_map, min_flow):
        vertex = self.sink
        while vertex != self.source:
            edge = parent_map[vertex][1]
            edge.weight -= min_flow
            edge.counterpart.weight += min_flow
            vertex = parent_map[vertex][0]

    def ford_fulkerson(self):
        flow = 0
        while True:
            add_to_flow = self.augmenting_path_cycle()
            if add_to_flow == 0:
                break
            flow += add_to_flow

        return flow

def answer(start_positions, end_positions, path):
    graph = Graph.create(start_positions, end_positions, path)
    return graph.ford_fulkerson()

# print answer([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])

# g1 = Graph.create([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
# print(g1.ford_fulkerson())

# g2 = Graph.create([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]])
# print(g2.ford_fulkerson())

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
# print(g3.ford_fulkerson())

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
# print(g4.ford_fulkerson())

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
# print(g6.ford_fulkerson())

# g7 = Graph.create(
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
# print(g7.ford_fulkerson())
