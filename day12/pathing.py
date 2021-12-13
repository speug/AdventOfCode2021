import time


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


path_input = """xx-end
EG-xx
iy-FP
iy-qc
AB-end
yi-KG
KG-xx
start-LS
qe-FP
qc-AB
yi-start
AB-iy
FP-start
iy-LS
yi-LS
xx-AB
end-KG
iy-KG
qc-KG
FP-xx
LS-qc
FP-yi
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


def find_paths_single(graph, start_node):
    # simple DFS
    paths = []

    def inner(graph, node, route):
        # add current node to route
        route += [node]
        # if at the end, append path to path collection and stop
        if node == 'end':
            paths.append(route)
            return
        # otherwise, get valid neighbors and recursively call for each
        else:
            valid_visits = graph[node].get_neighbors()
            valid_visits = {x for x in valid_visits
                            if graph[x].type != 'start'}
            valid_visits = {x for x in valid_visits
                            if not ((graph[x].type == 'small')
                                    and (graph[x].name in route))}
            if valid_visits:
                for n in valid_visits:
                    inner(graph, n, route.copy())
            else:
                # reached a dead end, return
                return
    inner(graph, start_node, [])
    return paths


start = time.time()
paths = find_paths_single(graph, 'start')
end = time.time()
print(f'Part 1 paths {len(paths)} (command ran for {end-start:.3f} s)')


def count_small_appearances(graph, route):
    out = {}
    for n in route:
        if graph[n].type == 'small':
            if n in out:
                out[n] += 1
            else:
                out[n] = 1
    return out


def find_paths_double(graph, start_node):
    # overly complicated DFS
    paths = []

    def inner(graph, node, route):
        route += [node]
        if node == 'end':
            paths.append(route)
            return
        else:
            valid_visits = graph[node].get_neighbors()
            valid_visits = {x for x in valid_visits
                            if graph[x].type != 'start'}
            valid_visits = {x for x in valid_visits
                            if not ((graph[x].type == 'small')
                                    and (route.count(graph[x].name) >= 1))}
            # check if not yet visited any small cave twice on route
            small_counts = count_small_appearances(graph, route)
            double_visit_available = 2 not in small_counts.values()
            single_visit = {}
            # split neighbors into two classes
            if double_visit_available:
                single_visit = {k for k in small_counts.keys()
                                if k in graph[node].get_neighbors()}
                valid_visits = {x for x in valid_visits if x not in
                                single_visit}
            if valid_visits:
                for n in valid_visits:
                    inner(graph, n, route.copy())
            if single_visit:
                for n in single_visit:
                    inner(graph, n, route.copy())
            else:
                return
    inner(graph, start_node, [])
    return paths


# so slowwwwwww
start = time.time()
paths = find_paths_double(graph, 'start')
end = time.time()
print(f'Part 2 paths {len(paths)} (command ran for {end-start:.3f} s)')
