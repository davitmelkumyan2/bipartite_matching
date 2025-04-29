import numpy as np
import networkx as nx


def hungarian_algorithm(cost_matrix):
    # cost_matrix = np.array(cost_matrix)
    cost_matrix = np.array(cost_matrix, dtype=float)

    n = len(cost_matrix)
    u = [0] * (n + 1)
    v = [0] * (n + 1)
    p = [0] * (n + 1)
    way = [0] * (n + 1)

    for i in range(1, n + 1):
        p[0] = i
        minv = [float('inf')] * (n + 1)
        used = [False] * (n + 1)
        j0 = 0

        while True:
            used[j0] = True
            i0 = p[j0]
            delta = float('inf')
            j1 = -1

            for j in range(1, n + 1):
                if not used[j]:
                    cur = cost_matrix[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j

            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta

            j0 = j1
            if p[j0] == 0:
                break

        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break

    return [(p[j] - 1, j - 1) for j in range(1, n + 1)]


def maximum_weight_matching_bipartite(G):
    if not nx.is_bipartite(G):
        raise ValueError("Graph must be bipartite")

    X, Y = map(list, nx.bipartite.sets(G))
    n = max(len(X), len(Y))
    cost_matrix = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(len(X)):
        for j in range(len(Y)):
            if G.has_edge(X[i], Y[j]):
                cost_matrix[i][j] = -G[X[i]][Y[j]]['weight']

    result = hungarian_algorithm(cost_matrix)

    matching = set()
    total_weight = 0

    for i, j in result:
        if i < len(X) and j < len(Y):
            u, v = X[i], Y[j]
            if G.has_edge(u, v):
                matching.add((u, v))
                total_weight += G[u][v]['weight']

    return matching, total_weight