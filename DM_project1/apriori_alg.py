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
    

def C1_candidate(transaction_item):
    C1 = []
    c1 = []
    for data in transaction_item:
        for c1_candidate in data:
            if not c1_candidate in c1:
                c1.append(c1_candidate)
    for i in c1:
        C1.append([i])
    return C1


def generate_itemsets(transactions, k_candidates, min_support, prune_cand):
    #Ck_itemset
    k_it = []

    #calculate the support_num of each itemset
    for item in k_candidates:
        support = count_support(transactions, item)
        if support >= min_support:
            k_it.append(item)
        else:
            prune_cand.append(item)

    return k_it, prune_cand


def count_support(transaction, item):
    count = 0
    for a_trans in transaction:
        itemset = set(item)
        if itemset.issubset(set(a_trans)):
            count += 1
    support = count / len(transaction)
    
    return support


#self_joining    
def generate_candidates(previous_itemsets, k):
    k_candidates = []
    len_item = len(previous_itemsets)

    if k == 2:
        for i in range(len_item):
            for j in range(i+1, len_item):
                cand = set(previous_itemsets[i]) | set(previous_itemsets[j])
                k_candidates.append(list(cand))
        
        return k_candidates

    for i in range(len_item):
        for j in range(i+1, len_item):
            #find the intersections of two itemsets
            inter_of_item =  set(previous_itemsets[i]).intersection(set(previous_itemsets[j]))
            if len(inter_of_item) > 0:
                candidate = set(previous_itemsets[i]) | set(previous_itemsets[j])
                if len(candidate) == k and list(candidate) not in k_candidates:
                    #if not prune_data.issubset(candidate):
                    k_candidates.append(list(candidate))

    return k_candidates
    

def apriori_algorithm(dataset, min_support):
    #get C1 and it1
    final_itemsets = []

    #calculate C1 and it1
    prunek = []
    Ck = C1_candidate(dataset)
    itk, prunek = generate_itemsets(dataset, Ck, min_support, prunek)
    k = 1

    while len(itk) != 0:
        k += 1
        Ck = generate_candidates(itk, k)
        itk, prunek = generate_itemsets(dataset, Ck, min_support, prunek)
        for item in itk:
            item.sort()
            if item not in final_itemsets:
                final_itemsets.append(item)

    return final_itemsets


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


def association_rule(dataset, min_sup, min_conf):
    itemsets = apriori_algorithm(dataset, min_sup)
    output_format = []

    for i in range(len(itemsets)):
        subset_of_item = get_all_subsets(itemsets[i])
            
        for s in subset_of_item:
            tmp_output_format = []
            current_set = set(s)
            remain_set = set(itemsets[i]) - current_set
                
            sup_item = count_support(dataset, itemsets[i])
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







































"""
def load_transactions(file_path):
    with open(file_path,"r") as f:
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
        
        count = 1
        #store numbers of a class
        store_list = []
        #append each class to a list
        transactions = []
        for cls in range(len(lines)):
            if int(tmp_ls[cls][0]) == count:
                store_list.append(tmp_ls[cls][2])
            else:
                transactions.append(store_list)
                count += 1
                store_list = []
                store_list.append(tmp_ls[cls][2])
        transactions.append(store_list)

        return transactions
"""