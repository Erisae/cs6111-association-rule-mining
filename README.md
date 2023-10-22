# cs6111-pj3

## Name and Uni
Yuhan Xia yx2729

Jenny Liu jl6093

## Files submitting
```shell
association_rule_mining.py
main.py
output_format.py

example-run.txt
INTEGRATED-DATASET.csv
```

## How to Run Program
```shell
pip install pandas
python main.py INTEGRATED-DATASET.csv 0.01 0.35
```

## Data Set Definition

### NYC Open Data Used
- https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh
- This is street tree data from the TreesCount! 2015 Street Tree Census. Each row in the original data is a tree with a unique tree_id. It then has many columns with more data. The two relevant columns that ended up being used are listed below:
  - block_id (identifier linking each tree to the block in the blockface table/shapefile that it is mapped on)
  - spc_common (the commone name for tree species like "red maple")

### How to Map Into INTEGRATED-DATASET
- After downloading the data from the website, I only kept the block_id and spc_common columns. I then sorted the the table by block_id using the sort feaure.
- Since the end goal is to learn which types of trees are usually planted together on a block, I removed any duplicates. That meant if a block had multiples of the same tree, I would remove the duplicates since I only care about the types of trees, not the quantity of each type. This was done using Data > Table Tools > Remove Duplicates.
- There were also many blanks, as sometimes a row didn't contain the common name of a tree because the tree was a stump or dead. So, I removed the blanks by going to Home > Find & Select > Go To Special... > Blanks. This selected all the rows that contained blanks. I then just right clicked and pressed delete. This deleted all the rows with blanks.
- The goal was to create a table where each row represented a different block and each column having a different species planted in that block. In order to do this, I first copied over all of the block id's, and then removed duplicates (using the same method as before). 
- Then, I used the following formula on the cell to the right of each block id:
  - = TEXTJOIN(",", TRUE, IF(A1 = 'clean data'!A1:A5000, 'clean data'!B1:B5000, "") )
  - This was done on another sheet, so 'clean data' refers to the sheet the cleaned up data is kept
  - This was done for each row, so A1 would increment to A2
  - Since there was so much data, this was done in chunks because the computer could not handle it otherwise. A1:A5000 only looks at those cells to see if they match the block id. At the end, I would then go onto the next block.  
  - It joins the text together in one cell by "," seperating each phrase
  - TRUE ignores the empty cells
  - IF only adds the text in cells that meet a condition
  - "A1 = 'clean data'!A1:A5000" searches for the cells in column A that match the block id in A1
  - 'clean data'!B1:B5000 is the text that would be joined by "," if the condition listed above was met by the A in its row
- In order to streamline the data, I then used =LOWER(A1) and then =SUBSTITUTE(C1," ", "_") so that a tree species name like "Callery pear" would become "callery_pear"
- Now each row only had two column, the block id and the tree types seperated by commas. Using Data > Text to Columns, I selected "," as the delimiter, and now each type occupies its own column.
- Finally, the block_id is deleted and the data is downloaded as a csv file. The only use of the block_id was to make sure that each row was a unique block.

### Why This Data
Trees are a really important part of a city as they bring a wide array of social, economic and environmental benefits. They improve air quality by removing carbon dioxide, improve health by reducing air pollutants, reduce crime, capture storm water, lower the summer air temperature, and many more. (https://www.nyc.gov/html/mancb3/downloads/resources/NYC%20Street%20Tree%20Overview.pdf)
In order to have these benefits, the trees not only have to be planted, but be kept alive. So, an important part of planting trees is ensuring if they are well suited to their environment. One of the crucial factors is the tree species, and if it will grow well next to existing trees.
So, this data, and any associations derived from it will be helpful to the foresters in deciding the species of new trees to plant in a block.

## Project Design

### Files
- `main.py`: contains function `main()`, where we defined the program flow, from reading in the data, obtaining frequent itemsets, obtaining association rules, and finally writing the results.
- `output_format.py`: contains functions `output_freq_itemsets()` and `output_assciation_rules()`, which would output frequent itemsets and association rules to target file with format required.
- `association_rule_mining.py`: contains functions `get_l1_itemsets()`, `apriori_prun()`, `apriori_gen()`, `get_lk_itemsets()`, `get_frequent_itemsets()` and `get_association_rules()` which generate frequent itemset and association rules.

### Funtions
- `get_frequent_itemsets(baskets, min_sup)`
  - **input**: 
    - `baskets`(list) indicating all data rows
    - `min_sup`(float) indicating the mininal support
  - **output**: 
    - `freq_itemsets`(dict): the key represents the frequent itemsets generated, and value is a tuple (itemset_count, itemset_support) indicating the count and support of relavant itemset
  - **flow**:
    - call `get_l1_itemsets(baskets, min_sup)`: takes a list of `baskets` and a minimum support threshold `min_sup` as input. It counts the frequency and support of each individual item in the baskets and returns a dictionary of frequent 1-itemsets along with their appearance count and support values.
    - do the following while the recent `Lk` is not empty.
    - update `Lk` to `freq_itemsets`, `Lk` is the set of large k-itemset, and `freq_itemsets` is the all large itemsets.
    - call `apriori_gen(Lk)`: takes a dictionary of frequent itemsets Lk as input. It generates a list of candidate itemsets by joining pairs of frequent itemsets from Lk that have the same prefix. It then prunes the candidate list using `apriori_prune(candidate, Lk)` (by removing candidates which have subset not in `Lk`) and returns the pruned list.
    - call `get_lk_itemsets(basckets, min_sup, Ck)`: takes a list of `baskets`, a minimum support threshold `min_sup`, and a list of candidate itemsets `Ck` as input. It counts the frequency of each candidate itemset in the baskets and returns a dictionary of frequent itemsets along with their appearance count and support values.

- `get_association_rules(freq_itemsets, min_conf)`
  - **input**: 
    - `freq_itemsets`(dict): a dictionary whose keys are frequent itemsets and values are appearance count and support values of relavent itemsets
    - `min_conf`(float): the minimal confidence threshhold for association rules
  - **output**:
    - `rules`(dict): keys are the interesting association rules in the form of `((left), (right))`, values are support of all items and confidence of rule the `(sup, conf)`
  - **flow**
    - The function iterates through each frequent itemset in freq_itemsets and generates all possible association rules by considering each item in the itemset as the right-hand side of the rule and all other items as the left-hand side. 
    - For each rule, the function computes the support and confidence.
    - If the confidence of a rule is greater than or equal to the minimum confidence threshold `min_conf`, the rule is considered interesting and is added to the `rules` dictionary along with its support and confidence.

- `main()`
  - read dataset file using `pd.read_csv`, fill all empty(nan) tokens with "", convert Dataframe to list and filter out all ""s.
  - call `get_frequent_itemsets` to generate frequent itemsets.
  - call `output_freq_itemsets` to output formatted frequent itemsets.
  - call `get_association_rules` to generate association rules.
  - call `output_assciation_rules` to output formatted association rules.

## Results

```shell
python main.py INTEGRATED-DATASET.csv 0.01 0.35
```

Running the command line specifications above resulted in some compelling results. Overall, we learned a lot about which trees grow together well, and specifically, what tree species is likely to be present if a combination of trees is found on a block. 

[northern_red_oak] => [pin_oak] (Conf: 41.5%, Supp: 1.9%)
For example, the line above says that if a Northern Red Oak Tree is planted on block, then a Pin Oak is likely to also be planted on that block.

[littleleaf_linden, norway_maple] => [london_planetree]
This indicates that a block with both Little Leaf Linden and Norway Maple is likely to also have a London Planetree.

This sort of data is really helpful, because in planting new trees, the species is one of the biggest decisions. Since NYC is so developed, it is likely that any spot someone would want to grow a tree would already have trees. The data used for the association rules only includes alive trees, not stumps or dead one, meaning that these tree combinations have proven to be successful. So, if someone were to plant a new tree on a block with existing trees, finding a LHS representative of what a block already has would help them predict what the best new tree species to plant on that tree is. Biodiversity is an important factor as it supports a richer ecosystem, and increases resileance towards any diseases or climate change.

Similar to how association rules can help a store decide what to advertise based on what's in someone's basket, these tree association rules can help a forester predict and decide what new tree species should be introduceced to a block based on what's already there.
