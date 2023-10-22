from itertools import combinations

"""
association rule X => Y
    - conf c: c% of transactions in D that contain X also contain Y
    - sup  s: s% of transactions in D contain XUY
"""

def get_l1_itemsets(baskets, min_sup):
    """
    Input:
        baskets (list of lists): 
            A list of baskets, where each transaction is represented as a list of items.
        min_sup (float): 
            The minimum support threshold for an itemset to be considered frequent.
    Output:
        L1 (dictionary): 
            A dictionary where each key is a frequent itemset of length 1 (tuple), 
            and the corresponding value is a tuple containing the count and support of the itemset.
    """
    L1 = {} # dictionary to store frequent itemsets of length 1
    counter = {} # dictionary to count occurrence of each item in baskets

    # count occurrence of each item in baskets
    for basket in baskets:
        for item in basket:
            if not item in counter:
                counter[item] = 0
            counter[item] += 1

    # check which items meet the minimum support threshold
    for item_name, item_count in counter.items():
        sup = float(item_count) / len(baskets) # compute support
        if  sup >= min_sup:
            L1[(item_name,)] = (item_count, sup) # add frequent itemset to L1
    
    return L1

def apriori_prune(candidate, Lk):
    """
    Input:
        candidate (list of tuples): 
            A list of candidate itemsets, where each itemset is represented as a tuple.
        Lk (dictionary): 
            A dictionary where each key is a frequent itemset (represented as a tuple), 
            and the corresponding value is a tuple containing the count and support of the itemset.
    Output:
        pruned (list of tuples): 
            A list of candidate itemsets that pass the pruning step, 
            where each itemset is represented as a tuple.
    """
    pruned = [] # list to store candidate itemsets that pass the pruning step
    if len(candidate) == 0:
        return pruned
    k = len(candidate[0]) - 1 # size of subsets to check against Lk

    for itemset in candidate:
        delete_item = False # flag to indicate if itemset should be deleted
        # iterate over all subsets of size k-1 in the itemset
        for subset in combinations(itemset, k): 
            subset = tuple(sorted(subset)) # subset is tuple and sorted
            if not subset in Lk.keys():
                delete_item = True
                break
        if not delete_item:
            pruned.append(itemset)
    return pruned
        
def apriori_gen(Lk):
    """
    Input:
        Lk (dictionary): 
            Each key is a frequent itemset (represented as a tuple), 
            corresponding value is a tuple containing the count and support of the itemset.
    Output:
        pruned_candidate (list of tuples): 
            A list of candidate itemsets that have been pruned, 
            where each itemset is represented as a tuple.
    """
    candidate = [] # list to store candidate itemsets
    # pair each 2 itemsets in Lk
    for p, q in combinations(Lk.keys(), 2):
        if p[:-1]==q[:-1]: # if the first k-1 items are the same
            if p[-1] < q[-1]: # add the larger item to the tuple, this makes sure increasing order
                candidate.append(p + (q[-1],))
            if p[-1] > q[-1]:
                candidate.append(q + (p[-1],))

    # prune candidate itemsets
    pruned_candidate = apriori_prune(candidate, Lk)
    return pruned_candidate

def get_lk_itemsets(baskets, min_sup, Ck):
    """
    Input:
        baskets (list of lists): 
            Each list represents a basket of items.
        min_sup (float): 
            Representing the minimum support threshold.
        Ck (list of tuples):
            Each tuple represents a candidate itemset.
    Output:
        Lk (dictionary):
            Keys are tuples representing frequent itemsets, 
            and the values are tuples of the form (item_count, support).
    """
    Lk = {}
    counter = {}
    if len(Ck) == 0:
        return Lk
    k = len(Ck[0])

    # count all items co-occurance
    for basket in baskets:
        if len(basket) >= k:
            # iterate all subset in basket that has size k
            for subset in combinations(basket, k): 
                subset = tuple(sorted(subset)) # subset is tuple and sorted
                # subset in Ck equals to subset in Ct=Ck.intersect(bascket)
                if subset in Ck:
                    if subset not in counter:
                        counter[subset] = 0
                    counter[subset] += 1

    # check which items meet the minimum support threshold
    for items, items_count in counter.items():
        sup = float(items_count) / len(baskets)
        if sup >= min_sup:
            Lk[items] = (items_count, sup)
    return Lk

def get_frequent_itemsets(baskets, min_sup):
    """
    Input:
        baskets (list of lists):
            Each list represents a basket of items.
        min_sup (float): 
            Representing the minimum support threshold for a frequent itemset.
    Output:
        freq_itemsets (dictionary):
            Keys are frequent itemsets and the values are tuples containing 
            the count of the itemset in the baskets and the itemset's support value.
    """
    freq_itemsets = {}

    # generate L1
    Lk = get_l1_itemsets(baskets, min_sup)

    while len(Lk) != 0:
        # add recent generated Lk to freq_itemsets
        freq_itemsets.update(Lk)
        
        # generate new Lk
        Ck = apriori_gen(Lk) # Ck is a list
        Lk = get_lk_itemsets(baskets, min_sup, Ck)
    
    return freq_itemsets

def get_association_rules(freq_itemsets, min_conf):
    """
    Input:
        freq_itemsets (dictionary): 
            A dictionary of frequent itemsets and their supports.
        min_conf (float): 
            Minimum confidence threshold for generating association rules.
    Output:
        rules (dictionary):
            A dictionary of association rules and their supports and confidence
    """
    rules = {}
    for itemset in freq_itemsets.keys(): # itemset is tuple
        k = len(itemset)
        # since one on the right &. at least one on the left
        if k < 2:
            continue
        for i in range(k):
            # generate right & left part of association rule
            right = itemset[i]
            left = itemset[:i] + itemset[i+1:]
            # compute support and confidence
            sup = freq_itemsets[itemset][1]
            conf = freq_itemsets[itemset][0] / freq_itemsets[left][0]
            if conf >= min_conf:
                rules[(left, right)] = (sup, conf)
    return rules


        




    