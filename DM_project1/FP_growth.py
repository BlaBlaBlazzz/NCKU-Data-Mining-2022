import utils

def load_data(file_path):
    data = utils.read_file(file_path)
    transaction = []
    store_list = []
    count = 1

    for i in range(len(data)):
        if data[i][0] == count:
            store_list.append(data[i][2])
        else:
            transaction.append(store_list)
            count += 1
            store_list = []
            store_list.append(data[i][2])
    transaction.append(store_list)
    return transaction

def get_sorted_item1(dataset, min_sup_count):
    it1 = {}
    sorted_data = []
    #create c1
    for transaction in dataset:
        for item in transaction:
            if item not in it1:
                it1[item] = 1
            else:
                it1[item] += 1
    #sorted c1
    it1 = dict(sorted(it1.items(), key = lambda x:x[1], reverse = True))
    for k in list(it1.keys()):
        if it1[k] < min_sup_count:
            del(it1[k])

    #first scan to prune data < min_sup
    data = []  
    for trans in dataset:
        tmp_data = []
        for it in trans:
            if it1.get(it):
                tmp_data.append(it)
        data.append(tmp_data)
    
    for trans in data:
        sort_c = sorted(trans)
        #sort
        for i in range(len(sort_c)-1):
            for j in range(len(sort_c)-i-1):
                if it1[sort_c[j]] < it1[sort_c[j+1]]:
                    sort_c[j], sort_c[j+1] = sort_c[j+1], sort_c[j]
        
        if len(trans) > 0:
            sorted_data.append(sort_c)

    return it1, sorted_data


class Node:
    def __init__(self, item, freq, parent):
        self.item = item       # name of node
        self.freq = freq       # frequence of the item
        self.parent = parent   # parent node
        self.child = {}        # child node
        self.next = None       # linked list

    def disp(self, index = 1):  
        print('  '*index, self.item, ' ', self.freq)  
        for child in self.child.values():  
            child.disp(index + 1) 


def fp_tree_constructor(transactions, item, min_sup):
    # construct root of the fp-tree
    tree_root = Node("root", 1, None)

    # item: sorted frequent itemset > min_support (type = dict)
    # transaction: sorted data that pruned the item < min_sup (type = list)

    # linked the occerences of item  (type = dict)
    linked_occurence = {}
    for it in list(item.keys()):
        linked_occurence[it] = None
    for trans in transactions:
        update_fp_tree(tree_root, trans, linked_occurence)

    return tree_root, linked_occurence


def linked_to_occurence_item(linked_occurence, node):
    # Traversing 
    while linked_occurence.next != None:
        linked_occurence = linked_occurence.next
    linked_occurence.next = node


def update_fp_tree(node, trans, linked_occurence):
    elem = trans[0]
    if elem in node.child:
        node.child[elem].freq += 1
    else:
        #if not, create a branch
        node.child[elem] = Node(elem, 1, node)    # Node(item, freq, parent)
        
        if linked_occurence[elem] == None:
            linked_occurence[elem] = node.child[elem]
        else:

            # linked to the occurence item
            linked_to_occurence_item(linked_occurence[elem], node.child[elem])
            
            # while linked_occurence[elem].next != None:
            #     linked_occurence[elem] = linked_occurence[elem].next
            # linked_occurence[elem].next = node.child[elem]

    # if the remain trans != None, do the recursion
    if len(trans[1:]) > 0:
        update_fp_tree(node.child[elem], trans[1:], linked_occurence)


def find_prefix(node, prefix_route, initial_nodeItem):
    if node.parent != None:
        # record the path excluding the first item
        if node.item == initial_nodeItem:
            node = node.parent
        else:
            prefix_route.append(node.item)
            #climb to the upper node
            node = node.parent
        find_prefix(node, prefix_route, initial_nodeItem)


def create_freq_path_item(prefix_route, min_sup, count_ls):
    freq_path_item = {}
    count = 0
    # create a dict counting the freq of prefix patterns
    for route in prefix_route:
        for elem in route:
            if elem in list(freq_path_item.keys()):
                freq_path_item[elem] += count_ls[count][elem]
            else:
                # initialize the freq with the leaf node's freq
                freq_path_item[elem] = count_ls[count][elem]
        count += 1
    #print("freq_path_item: ", freq_path_item)

    for item in list(freq_path_item.keys()):
        if freq_path_item[item] < min_sup:
            del freq_path_item[item]
    
    return freq_path_item


def record_prefix(freq_item, min_sup, link_occurence):
    # store the occurence linked list
    node = link_occurence[freq_item]
    count_ls = []
    freq_path_item = []
    prefix_route = []
    while node != None:
        freq = node.freq
        single_prefix_route = []
        find_prefix(node, single_prefix_route, node.item)
        
        # record the freq of the leaf node, which will be used to count the freq of each prefix nodes
        leaf_node_count = {}
        for path_node in single_prefix_route:
            leaf_node_count[path_node] = freq
        #record every path of the node
        count_ls.append(leaf_node_count)
        # next occurence item
        node = node.next
        # record the path
        prefix_route.append(single_prefix_route)
    # we want to delete path node whose freq < min_sup
    condi_freq_path_item = create_freq_path_item(prefix_route, min_sup, count_ls)
    # store freq pattern
    for key in list(condi_freq_path_item.keys()):
        freq_path_item.append(key)
    
    freq_prefix_route = []
    for route in prefix_route:
        tmp_prefix_route = []
        for elem in route:
            if condi_freq_path_item.get(elem):
                tmp_prefix_route.append(elem)
        freq_prefix_route.append(tmp_prefix_route)
    
    return freq_prefix_route, condi_freq_path_item, count_ls


# construct cond fp-tree of a single item
def construct_conditional_fp_tree(prefix_route, count_ls, item):
    Tree = Node("root", 1, None)
    count = 0
    link_occ = {}
    for it in list(item.keys()):
        link_occ[it] = None
    
    # the prefix route contain occurence items
    # triverse all the occurence items [[1st], [2nd], .....]
    for path in prefix_route:
        if len(path) == 0:
            count += 1
            continue
        #the order of prefix is oppisite
        path.reverse()
        update_condi_fp_tree(Tree, path, count_ls[count], link_occ)
        count += 1
    for it in list(item.keys()):
        if link_occ[it] == None:
            del link_occ[it]
            
    if link_occ == {}: 
        return None, None
    return Tree, link_occ

def update_condi_fp_tree(node, path, count, link_occ): 
    elem = path[0]
    
    if elem in node.child:
        node.child[elem].freq += count[elem]
    else:
        node.child[elem] = Node(elem, count[elem], node)
        
        if link_occ[elem] == None:
            link_occ[elem] = node.child[elem]
        else:
            # linked to the occurence item
            linked_to_occurence_item(link_occ[elem], node.child[elem])
    
    if len(path[1:]) > 0:
        update_condi_fp_tree(node.child[elem], path[1:], count, link_occ)


def mine_condi_fptree(link_occurence, items, minSup, prefix, freq_item):  
    sorted_item = []
    tmp_sorted_item = dict(sorted(items.items(), key = lambda x:x[1])) #(sort header table)  
    for it in list(tmp_sorted_item.keys()):
        sorted_item.append(it)
    #print("sorted_item: ", sorted_item)
    
    #triverse the FPtree with the oppisite order
    for basePat in sorted_item: 
        tmp_freq_item = prefix + [basePat] 
        #print('tmp_freq_item: ', tmp_freq_item)  
        freq_item.append(tmp_freq_item) 

        # record the prefix path
        # prefix_route: prefix paths of an item (list)
        # freq_path_item: frequent item (dict)
        # count_ls: prefix_route with the frequence (dict)
        prefix_route, freq_path_item, count_ls = record_prefix(basePat, minSup, link_occurence)
        
        #construct the conditional FPtree  
        condi_fptree, li_oc = construct_conditional_fp_tree(prefix_route, count_ls, items) 
        #print('li_oc: ', li_oc)
        
        if li_oc != None: 
            #condi_fptree.disp()              
            mine_condi_fptree(li_oc, freq_path_item, minSup, tmp_freq_item, freq_item)
    return freq_item
    
#get subsets
def get_all_subsets(items):
    subset_ls = [[]]
    
    for item in items:
        for i in subset_ls[:]:
            sub = i[:]
            #put k+1 into k subset
            sub.append(item)
            subset_ls.append(sub[:])
    
    #remove [] and item[:]
    subset_ls.remove([])
    subset_ls.remove(items)

    return subset_ls

def count_support(transaction, item):
    count = 0
    for a_trans in transaction:
        itemset = set(item)
        if itemset.issubset(set(a_trans)):
            count += 1
    support = count / len(transaction)
    
    return support

def association_rule(dataset, min_sup, min_conf):
    min_sup_count = min_sup * len(dataset)
    item, sorted_data = get_sorted_item1(dataset, min_sup_count)
    FPtree, link_occurence = fp_tree_constructor(sorted_data, item, min_sup_count)
    prefix = []
    freq_item = []
    itemsets = mine_condi_fptree(link_occurence, item, min_sup_count, prefix, freq_item)

    # delete single freq_item
    freq_itemsets = []
    for it in itemsets:
        if len(it) > 1:
            freq_itemsets.append(it)
    #print(len(freq_itemsets))
    
    output_format = []
    for i in range(len(freq_itemsets)):
        subset_of_item = get_all_subsets(freq_itemsets[i])
            
        for s in subset_of_item:
            tmp_output_format = []
            current_set = set(s)
            remain_set = set(freq_itemsets[i]) - current_set
                
            sup_item = count_support(dataset, freq_itemsets[i])
            sup_cur = count_support(dataset, list(current_set))
            sup_rem = count_support(dataset, list(remain_set))
            conf_cur = sup_item / sup_cur
            lift = sup_item / (sup_cur * sup_rem)

            if conf_cur >= min_conf and sup_item >= min_sup:
                tmp_output_format.append(current_set)
                tmp_output_format.append(remain_set)
                tmp_output_format.append(round(sup_item, 3))
                tmp_output_format.append(round(conf_cur, 3))
                tmp_output_format.append(round(lift, 3))

                output_format.append(tmp_output_format)

            # if conf_cur >= min_conf and sup_item >= min_sup:
            #     print("{} -> {}         |  support: {:.3f},  confidence: {:.3f}, lift: {:.3f} \n".format(list(current_set), list(remain_set), sup_item, conf_cur, lift))  
    return output_format




