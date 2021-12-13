class Node:

    def __init__(self, name, neighbors, type):
        self.name = name
        self.neighbors = neighbors
        self.type = type

    def add_neighbor(self, to_add):
        self.neighbors.add(to_add)

    def get_neighbors(self):
        return self.neighbors

    def __str__(self):
        out = (f'{self.name}: {self.type}, ' +
               f'neighbors: {self.neighbors}')
        return out


path_input = """start-A
start-b
A-c
A-b
b-d
A-end
b-end
""".split('\n')


def node_type(node):
    if node in ['start', 'end']:
        return node
    elif node.isupper():
        return 'big'
    else:
        return 'small'


graph = {}
for path_pair in path_input:
    if path_pair != '':
        a, b = path_pair.split('-')
        if a in graph:
            graph[a].add_neighbor(b)
        else:
            graph[a] = Node(a, {b}, node_type(a))
        if b in graph:
            graph[b].add_neighbor(a)
        else:
            graph[b] = Node(b, {a}, node_type(b))
[print(x) for x in graph.values()]


def find_paths_single(graph, start_node):

    paths = []

    def inner(graph, node, route):
        if 'end' in route:
            return
        route += [node]
        if node == 'end':
            # print(route)
            paths.append(route)
        else:
            valid_visits = graph[node].get_neighbors()
            valid_visits = {x for x in valid_visits
                            if graph[x].type != 'start'}
            valid_visits = {x for x in valid_visits
                            if not ((graph[x].type == 'small')
                                    and (graph[x].name in route))}
            # print(f'{node}: {valid_visits}')
            if valid_visits:
                for n in valid_visits:
                    inner(graph, n, route.copy())
                    # paths.append(inner(graph, n, route, paths))
            else:
                return
    inner(graph, start_node, [])
    return paths


paths = find_paths_single(graph, 'start')
# print(paths)
print(len(paths))


def count_small_apperances(graph, route):
    out = {}
    for n in route:
        if graph[n].type == 'small':
            if n in out:
                out[n] += 1
            else:
                out[n] = 1
    return out


def find_paths_double(graph, start_node):

    paths = []

    def inner(graph, node, route):
        if 'end' in route:
            return
        route += [node]
        if node == 'end':
            # print(route)
            paths.append(route)
        else:
            valid_visits = graph[node].get_neighbors()
            valid_visits = {x for x in valid_visits
                            if graph[x].type != 'start'}
            valid_visits = {x for x in valid_visits
                            if not ((graph[x].type == 'small')
                                    and (route.count(graph[x].name) == 2))}
            # print(f'{node}: {valid_visits}')
            small_counts = count_small_apperances(graph, route)
            print(small_counts)
            double_visit_available = 2 not in small_counts.values()
            print(double_visit_available)
            single_visit = {}
            if double_visit_available:
                single_visit = {k for k in small_counts.keys()}
                valid_visits = {x for x in valid_visits if x not in
                                single_visit}
            print(f'{node}: {valid_visits}')
            print(route)
            if valid_visits:
                for n in valid_visits:
                    inner(graph, n, route.copy())
                    # paths.append(inner(graph, n, route, paths))
            if single_visit:
                for n in single_visit:
                    inner(graph, n, route.copy())
            else:
                return
    inner(graph, start_node, [])
    return paths


paths = find_paths_double(graph, 'start')
# print(paths)
print(f'Part 2 paths {len(paths)}')