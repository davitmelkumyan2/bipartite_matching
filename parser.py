import networkx as nx
from collections import defaultdict


def parse_graph(text):
    G = nx.Graph()
    edges = defaultdict(dict)

    for line in text.strip().split('\n'):
        if not line.strip() or ':' not in line:
            continue

        vertex, neighbors = line.split(':', 1)
        vertex = vertex.strip()

        for pair in neighbors.split('),'):
            pair = pair.strip(' (),')
            if not pair or ',' not in pair:
                continue

            neighbor, weight = pair.split(',', 1)
            neighbor = neighbor.strip()

            try:
                edges[vertex][neighbor] = float(weight.strip())
            except ValueError:
                raise ValueError("Invalid weight value")

    for u in edges:
        for v, w in edges[u].items():
            if v not in edges or u not in edges[v]:
                raise ValueError("Missing reciprocal edge")
            if edges[v][u] != w:
                raise ValueError("Weight mismatch")

    for u in edges:
        for v, w in edges[u].items():
            G.add_edge(u, v, weight=w)

    return G


def parse_graph_from_file(file_path):
    with open(file_path, 'r') as f:
        return parse_graph(f.read())


def is_bipartite_graph(G):
    try:
        return nx.is_bipartite(G)
    except nx.NetworkXException:
        return False