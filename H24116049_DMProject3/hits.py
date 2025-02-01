
def HITS(graph, iter):
    #get the num of the node
    # num_node = max(map(max, graph))
    node = []
    for i in range(len(graph)):
        if graph[i][0] not in node:
            node.append(graph[i][0])
        if graph[i][1] not in node:
            node.append(graph[i][1])
    node.sort()
    
    
    #initialize authorities and hubs
    auth = {}
    hubs = {}
    for i in node:
        auth[i] = 1
        hubs[i] = 1

    # walk through the iterations
    for i in range(iter):
        #update authorities
        for j in node:
            new_auth = 0
            for k in range(len(graph)):
                #second element link to the next node
                if graph[k][1] == j:
                    new_auth += hubs[graph[k][0]]
            auth[j] = new_auth 
        
        #normalize
        auth_sum = sum(auth.values())
        for j in node:
            auth[j] /= auth_sum
        
        #update hubs
        for j in node:
            new_hubs = 0
            for k in range(len(graph)):
                if graph[k][0] == j:
                    new_hubs += auth[graph[k][1]]
            hubs[j] = new_hubs
        
        #normalize
        hubs_sum = sum(hubs.values())
        for j in node:
            hubs[j] /= hubs_sum
    
    authority = list(auth.values())
    hubs = list(hubs.values())

    #round to 3 decimal
    authority = [round(item, 3) for item in authority]
    hubs = [round(item, 3) for item in hubs]
    
    return authority, hubs, node

# a, b, c= HITS(graph5, 30)
# print("auth: {}".format(a))
# print("hubs: {}".format(b))