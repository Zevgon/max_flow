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
