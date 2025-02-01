
def load_graph(file_path):
    with open(file_path, "r") as f:
        tmp = f.read()
        line = tmp.split('\n')
        graph = [item.split(',') for item in line]
        #convert str to int 
        for i in range(len(graph)):
            graph[i] = list(map(int, graph[i]))
    return graph


def load_ibm_graph(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
        tmp_ls = []
        for i in lines:
            insert_dim = []
            #filter the space in the front
            str = i.strip()
            #split first and delete the null list object
            str1 = str.split(' ')
            for word in str1:
                if len(word) != 0: 
                    insert_dim.append(word)
            tmp_ls.append(insert_dim)
        
        nodes = []
        for i in range(len(tmp_ls)):
            ls = list(map(int, tmp_ls[i][1:]))
            nodes.append(ls)
        return nodes