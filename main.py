import pandas as pd
import sys

import association_rule_mining as mining
import output_format as myformat

file_name = sys.argv[1]
min_sup = float(sys.argv[2])
min_conf = float(sys.argv[3])

def main():
    # read csv
    dtypes = {i: str for i in range(54)}
    df = pd.read_csv(file_name, header=None, names=range(54), dtype=dtypes)
    df.fillna(value='', inplace=True)
    
    # change to list
    baskets = []
    for line in df.values.tolist():
        line = list(filter(lambda elem: elem != '', line))
        baskets.append(line)

    # baskets = [["pen","ink","diary","soap"], ["pen","ink","diary"], ["pen","diary"], ["pen","ink","soap"]]
    # baskets = [["I1","I2","I3"], ["I2","I3","I4"], ["I4","I5"], ["I1","I2","I4"], ["I1", "I2","I3","I5"], ["I1", "I2","I3","I4"]]

    freq_itemsets = mining.get_frequent_itemsets(baskets, min_sup)
    myformat.output_freq_itemsets(freq_itemsets, min_sup)

    rules = mining.get_association_rules(freq_itemsets, min_conf)
    myformat.output_association_rules(rules, min_conf)


if __name__=="__main__":
    main()