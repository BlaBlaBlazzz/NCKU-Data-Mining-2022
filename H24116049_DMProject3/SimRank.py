import numpy as np

def SimRank(graph, decay_factor=0.7, iteration=30):
    #get all nodes
    nodes = []
    for i in range(len(graph)):
        if graph[i][0] not in nodes:
            nodes.append(graph[i][0])
        if graph[i][1] not in nodes:
            nodes.append(graph[i][1])
    nodes_num = len(nodes)
    nodes.sort()
    #initialize SimRank matrix
    simrank = list(np.identity(nodes_num))

    #get parent nodes
    p_nodes = {}
    for node in nodes:
        tmp_parent = []
        for i in range(len(graph)):
            if graph[i][1] == node:
                tmp_parent.append(graph[i][0])
        p_nodes[node] = frozenset(tmp_parent)

    for i in range(iteration):
        new_simrank = list(np.identity(nodes_num))
        for a in nodes:
            for b in nodes:
                # the same node, return 1
                if a == b:
                    s_simrank = 1.0
                    continue
                #have no parents node, return 0
                if len(p_nodes[a]) == 0 or len(p_nodes[b]) == 0:
                    s_simrank = 0
                    continue

                #count S(a, b)
                similarity = 0
                p1_node = list(p_nodes[a])
                p2_node = list(p_nodes[b])
                for p1 in p1_node:
                    for p2 in p2_node:
                        p1_sim = nodes.index(p1)
                        p2_sim = nodes.index(p2)
                        similarity += simrank[p1_sim][p2_sim]

                #penalty
                penal = decay_factor / (len(p_nodes[a]) * len(p_nodes[b]))
                s_simrank = penal * similarity

                a_idx = nodes.index(a)
                b_idx = nodes.index(b)
                new_simrank[a_idx][b_idx] = s_simrank

        simrank = new_simrank

    #round to 6 decimal
    simrank = np.matrix.round(np.array(simrank), 6)
    simrank = simrank.tolist()

    for row in range(len(simrank)):
        simrank[row] = [round(item, 3) for item in simrank[row]]
    
    return simrank

# df = [[1, 2], [1, 3], [1, 4], [1, 5], [1, 7], [2, 1], [3, 1], [3, 2], [4, 2], [4, 3], [4, 5], [5, 1], [5, 3], [5, 4], [5, 6], [6, 1], [6, 5], [7, 5]]
# a = SimRank(df, 0.9, 30)
# print(a)