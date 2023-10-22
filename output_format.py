def output_freq_itemsets(freq_itemset, min_sup):
    # sort by 1st:sup 2nd:alphabet
    freq_itemset = dict(sorted(freq_itemset.items(), key= lambda x: (-x[1][1], x[0])))
    with open('example-run.txt', 'w') as file:
        # print header
        file.write("==Frequent itemsets (min_sup={:.3g}%)\n".format(min_sup*100))
        for itemset in freq_itemset.items():
            items = list(itemset[0])
            file.write("[{}], {:.3g}%\n".format(", ".join(str(i) for i in items), itemset[1][1]*100))
        file.write("\n\n")



def output_association_rules(rules, min_conf):
    # sort by 1st:conf 2nd:left alpha
    rules = dict(sorted(rules.items(), key=lambda x: (-x[1][1], x[0][0])))
    with open('output.txt', 'a') as file:
        # print header
        file.write("==High-confidence association rules (min_conf={:.3g}%)\n".format(min_conf*100))

        for rule in rules.items():
            left = list(rule[0][0])
            right = rule[0][1]
            file.write("[{}] => [{}] (Conf: {:.3g}%, Supp: {:.3g}%)\n".format(", ".join(str(i) for i in left), right, rule[1][1]*100, rule[1][0]*100))