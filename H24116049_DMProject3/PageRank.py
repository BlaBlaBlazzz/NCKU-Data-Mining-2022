
def PageRank(graph, damping_factor, iteration=30):
    #create page set dictionary
    node = []
    for i in range(len(graph)):
        if graph[i][0] not in node:
            node.append(graph[i][0])
        if graph[i][1] not in node:
            node.append(graph[i][1])
    node_num = len(node)
    node.sort()

    #initialize pagerank 
    pagerank = {}
    for page in node:
        pagerank[page] = 1 / node_num
    
    #create an outdegree list
    outdegree = {}
    for page in node:
        outdegree[page] = 0
    for i in graph:
        outdegree[i[0]] += 1

    for i in range(iteration):
        for j in node:
            new_pg = 0
            for k in range(len(graph)):
                if graph[k][1] == j:
                    new_pg += pagerank[graph[k][0]] / outdegree[graph[k][0]]
            pagerank[j] = (damping_factor / node_num) + (1-damping_factor) * new_pg
        
        #Normalization
        pagerank_sum = sum(pagerank.values())
        for j in node:
            pagerank[j] /= pagerank_sum
    
    pagerank = list(pagerank.values())
    # round pagerank list to 3 decimal
    pagerank = [round(item, 3) for item in pagerank]
            
    return pagerank


# a = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]
# pg = PageRank(a, 0.15, 100)
# print(pg)