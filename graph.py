'''
Author: Tate Thomas
CS 2420
Project 7: Graphs

Graph class:

    Methods:
    add_vertex(label): Takes a label for a vertex as a string and adds to graph. Graph
        verticies cannot have duplicate labels.
    add_edge(src, dest, weight): Takes a source and a destination, along with a weight,
        and adds that edge to the list. Weight must be int or float.
    get_weight(src, dest): Takes a source and a destination, and if that edge is in
        the graph, it will return the associated weight.
    dfs(starting_vertex): Takes a starting vertex and returns a generator, which will
        traverse in depth first order.
    bfs(starting_vertex): Takes a starting vertex and returns a generator, which will
        traverse in breadth first order.
    dsp(src, dest): Takes a source and a destination, and returns a tuple containing
        the length of the path and a list containing the verticies along that path. If
        no path exists, it will return a tuple containing math.inf and an empty list.
    dsp_all(src): Takes a source and returns a dictionary containing each vertex as
        a key, and a list containing the verticies along that path as the value. If
        no path exists to a vertex, the value associated with that will be an empty list.
    __str__(): Returns a string containing the graph info in GraphViz dot notation.
'''


import math


class Graph:
    '''Graph class:

    Methods:
    add_vertex(label)
    add_edge(src, dest, weight)
    get_weight(src, dest)
    dfs(starting_vertex)
    bfs(starting_vertex)
    dsp(src, dest)
    dsp_all(src)
    __str__()
    '''


    def __init__(self):
        '''Initializes a new graph. Takes 0 arguments'''

        self._graph = {}

        self._num_vertex = 0
        self._num_edges = 0


    def add_vertex(self, label):
        '''Takes a label and adds a vertex with that label into the graph if it isn't
        already there. Raises a ValueError otherwise
        '''

        if label in self._graph:
            raise ValueError(f"Vertex '{label}' already exists")

        if isinstance(label, str):

            self._graph[label] = {}
            self._num_vertex += 1
            return self

        raise ValueError("Vertex label must be of type str")


    def add_edge(self, src, dest, weight):
        '''Takes a source, destination, and weight, and creates an edge with that info.
        Raises a ValueError if one of the verticies aren't in the graph, or if the
        weight given isn't an int or float
        '''

        if not isinstance(weight, (int, float)):
            raise ValueError("Weight must be of type int or float")

        if src in self._graph:
            if dest not in self._graph:
                raise ValueError(f"Vertex '{dest}' does not exist")
            if dest in self._graph[src]:
                raise ValueError(f"Edge '[src]' -> '{dest}' already exists")

            self._graph[src][dest] = weight
            self._num_edges += 1
            return self

        raise ValueError(f"Vertex '{src}' does not exist")


    def get_weight(self, src, dest):
        '''Takes a source and a destination and returns the weight associated with
        that edge. Raises a value error if one of the verticies aren't in the graph,
        or if the edge isn't in the graph
        '''

        if src not in self._graph:
            raise ValueError(f"Vertex '{src}' does not exist")
        if dest not in self._graph:
            raise ValueError(f"Vertex '{dest}' does not exist")
        if dest not in self._graph[src]:
            return math.inf

        return self._graph[src][dest]


    def dfs(self, starting_vertex):
        '''Takes a starting vertex and returns a generator traversing the graph in
        depth first order
        '''

        if starting_vertex not in self._graph:
            raise ValueError(f"Vertex '{starting_vertex}' does not exist")

        visited = []
        found = []
        curr_vertex = starting_vertex

        yield starting_vertex

        while (len(visited) + 1) < self._num_vertex:
            visited.append(curr_vertex)
            keys = self._graph[curr_vertex].keys()

            if (len(keys) == 0) and (len(found) == 0):
                break

            for edge in keys:
                if (edge not in visited) and (edge not in found):
                    found.append(edge)

            curr_vertex = found.pop(-1)
            yield curr_vertex


    def bfs(self, starting_vertex):
        '''Takes a starting vertex and returns a generator traversing the graph in
        breadth first order
        '''

        if starting_vertex not in self._graph:
            raise ValueError(f"Vertex '{starting_vertex}' does not exist")

        visited = []
        found = []
        curr_vertex = starting_vertex

        yield starting_vertex

        while (len(visited) + 1) < self._num_vertex:
            visited.append(curr_vertex)
            keys = self._graph[curr_vertex].keys()

            if (len(keys) == 0) and (len(found) == 0):
                break
            for edge in keys:
                if (edge not in visited) and (edge not in found):
                    found.append(edge)

            curr_vertex = found.pop(0)
            yield curr_vertex


    def _dsp_helper(self, src):
        '''Takes a source and returns a generator used for finding the shortest path
        using Dijkstra's algorithm
        '''

        def _insert_helper(lyst, weight):
            '''Helper function to find the index of where to insert the new path'''

            i = 0
            while (i < len(lyst)) and (weight > lyst[i][1]):
                i += 1
            return i

        def _index_helper(lyst, num):
            '''Helper function to find the index of where a vertex is in the graph'''

            i = 0
            while i < len(lyst):
                if num == lyst[i][0]:
                    return i
                i += 1
            return -1

        if src not in self._graph:
            raise ValueError(f"Vertex '{src}' does not exist")

        visited = []
        potential = [(src, 0, [src])]

        while len(potential) > 0:
            curr_vertex = potential.pop(0)
            yield curr_vertex

            visited.append(curr_vertex[0])
            new_path = curr_vertex[2].copy()

            for edge in self._graph[curr_vertex[0]].keys():
                if edge in visited:
                    continue

                weight = self._graph[curr_vertex[0]][edge] + curr_vertex[1]
                new_potent = (edge, weight, new_path + [edge])
                index = _index_helper(potential, edge)

                if index == -1:
                    new_index = _insert_helper(potential, weight)
                    potential.insert(new_index, new_potent)

                else:
                    if weight < potential[index][1]:
                        potential.pop(index)
                        new_index = 0
                        new_index = _insert_helper(potential, weight)
                        potential.insert(new_index, new_potent)

        yield (None, math.inf, [])


    def dsp(self, src, dest):
        '''Takes a source and a destination and returns a tuple containing the length
        of the path and a list containing the verticies in that path. If no path exists,
        it will return a tuple containing math.inf and an empty list
        '''

        funct = self._dsp_helper(src)
        next_vertex = next(funct)

        while (next_vertex[0] != dest) and (next_vertex[0] is not None):
            next_vertex = next(funct)

        return next_vertex[1:]


    def dsp_all(self, src):
        '''Takes a source and returns a dictionary containing each vertex as keys and
        a list associated containing the verticies in that path. If a path doesn't
        exist, the list will be empty
        '''

        funct = self._dsp_helper(src)

        shortest_path = {}
        for vertex in self._graph.keys():
            shortest_path[vertex] = []

        for tup in funct:
            if tup[0] is None:
                break
            path = tup[2].copy()
            shortest_path[tup[0]] = path

        return shortest_path


    def __str__(self):
        '''Returns a string representing the graph data in GraphViz dot notation'''

        graph_viz_notat = "digraph G {"

        for vertex in self._graph.keys():
            for edge in self._graph[vertex].keys():
                weight = self._graph[vertex][edge]
                graph_viz_notat += f'\n   {vertex} -> {edge} [label="{weight}",weight="{weight}"];'

        graph_viz_notat += "\n}\n"
        return graph_viz_notat


def main():
    '''Main function for testing Graph class'''

    # Part 1
    a_graph = Graph()
    a_graph.add_vertex("A").add_vertex("B").add_vertex("C").add_vertex("D").add_vertex("E").add_vertex("F")
    a_graph.add_edge("A", "B", 2).add_edge("A", "F", 9).add_edge("B", "C", 2).add_edge("C", "D", 1).add_edge("B", "D", 15).add_edge("B", "F", 6).add_edge("F", "B", 6).add_edge("F", "E", 3).add_edge("E", "D", 3).add_edge("E", "C", 7)

    # Part 2
    print(a_graph)

    # Part 3
    for vertex in a_graph.dfs("A"):
        print(vertex, end="")
    print("\n")

    # Part 4
    for vertex in a_graph.bfs("A"):
        print(vertex, end="")
    print("\n")

    # Part 5
    path = str(a_graph.dsp("A", "F")[1])
    path = path.replace("'", "")
    print(f'<{path[1:-1]}>\n')

    # Part 6
    paths = a_graph.dsp_all("A")
    for path in paths.keys():
        path_str = str(paths[path])
        path_str = path_str.replace("'", "")
        print(f"<{path_str[1:-1]}>")


if __name__ == "__main__":
    main()
