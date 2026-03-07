# containment_queries.py

I implement 4 different methods for retrieving the transactions that **contain** a querys items.

### 1) Naive Method:

Checks every transaction if it contains all the querys items.

### 2) Exact Signature File Method:

Uses a bitmap signature for every transaction to find all the transactions that contain all the querys items. An example bitmap signature file you can find [hear](https://github.com/kasselouris/Complex-Data-Management/blob/main/dataset_retrieval/assets/sigfile.txt).

*Example of a signature:* ```2201170739200```  
This translates to binary in ```100000000010000000000000000000000000000000```, which by the positions of the ```1's``` you can find the item ids, in this case item 41 and 31.


### 3) Exact Bitslice Signature File Method:

Uses a bitslice signature for every item to find all the transactions that contain all the querys items. An example bitslice signature file you can find [hear](https://github.com/kasselouris/Complex-Data-Management/blob/main/dataset_retrieval/assets/bitslice.txt).

*Example of a signature:* ```137818996163554428655764602091926697859...``` , which if translated to binary we can find by the positions of the ```1's``` what transactions contain an item.

### 4) Inverted File Method:

Uses a sorted inverted file list for every item to find all the transactions that contain all the querys items. An example inverted file you can find [hear](https://github.com/kasselouris/Complex-Data-Management/blob/main/dataset_retrieval/assets/invfile.txt).

Example of an inverted list for an item: ```0: [4, 6, 7, 8, 13, 16, 18, 20, ..., 9999]```  
This translates as item 0 is in transaction 4, 6, 7, ..., 9999.
 
 ----------------------------------------------------------
 
* Example output:
> Results are of type {transaction322, transaction5923, ...}
```
$ python3 containment_queries.py transactions.txt queries.txt 0 0
Naive method results:
{322, 5923, 6596, 8131, 8838, 1258, 77, 7182, 2063, 2289, 9650, 2227, 5523, 2454, 4854, 9752, 7641}
Naive Method computation time = 0.0016491413116455078


$ python3 containment_queries.py transactions.txt queries.txt 0 -1
Naive method results:
{322, 5923, 6596, 8131, 8838, 1258, 77, 7182, 2063, 2289, 9650, 2227, 5523, 2454, 4854, 9752, 7641}
Naive Method computation time = 0.0013041496276855469
 
Signature File result:
{322, 5923, 6596, 8131, 8838, 1258, 77, 7182, 2063, 2289, 9650, 2227, 5523, 2454, 4854, 9752, 7641}
Signature File computation time = 0.0010459423065185547
 
Bitsliced Signature File result:
{322, 5923, 6596, 8131, 8838, 1258, 77, 7182, 2063, 2289, 9650, 2227, 5523, 2454, 4854, 9752, 7641}
Bitsliced Signature File computation time = 0.0005888938903808594
 
Inverted File result:
{322, 5923, 6596, 8131, 8838, 1258, 77, 7182, 2063, 2289, 9650, 2227, 5523, 2454, 4854, 9752, 7641}
Inverted File Computation time = 0.0007894039154052734


$ python3 containment_queries.py transactions.txt queries.txt -1 -1
Naive Method computation time = 0.17543888092041016
Signature File computation time = 0.10915470123291016
Bitsliced Signature File computation time = 0.07157063484191895
Inverted File Computation time = 0.3201167583465576
```

-----------------------------------------------------
-----------------------------------------------------

# relevance_queries.py

I implement 2 different methods for retrieving the **K most relevant** transactions(in descending order) for a query. 

The relation(rel) of a transaction to a query is calculated with this formula: ```rel(τ,q)=Σi ∈ q(occ(i,τ)∙|T|/trf(i,T))```, where:
* τ is a transaction from all T transactions
* q is a query
* i is an item in a query
* |T| is the total number of transactions
* occ(i,τ) is the occurrence of an item in a transaction
* trf(i,T) is the number of transactions an item appears.

Before we use the methods below we create two lists. One contains the occ(i, τ) for all items(inverted_occ_list) and the other contains the |T| / trf(i,T) for all items(T_trf_list).  

An example output of this two lists can be found on [invfileocc](https://github.com/kasselouris/Complex-Data-Management/blob/main/dataset_retrieval/assets/invfileocc.txt).  
Eg: ```0: 2.515090543259557, [[4, 2], [6, 3], [7, 1], [8, 2], [13, 2], ..., [9999, 1]```  
This translates as item 0 with |T|/trf(i,T) = 2.515090543259557 is found in transaction 4 two times, in transaction 6 tree times, in transaction 7 one time, etc.

### 1) Naive Method:

Parses all transactions and for each transaction finds the occurrence for all querys items in this transaction to calculate the relevance. It also uses the T_trf_list. For returing the K most relevant transactions it uses the heapq.nlargest() function.

### 2) Inverted File Method:

Union merges the inverted_occ_list for all query items using also the T_trf_list to calculate the relations. It also uses for returing the K most relevant transactions the heapq.nlargest() function.

----------------------------------------------------------------------

* Example output:
> Results are of type [[rel(transaction8346, query0), transaction8346], [rel(transaction7641, query0), transaction7641]]
```
$ python3 relevance_queries.py transactions.txt queries.txt 0 -1 2
Naive method results:
[[263.1578947368421, 8346], [145.0651240373354, 7641]] 
Naive Method computation time = 0.007457256317138672
 
Inverted File result:
[[263.1578947368421, 8346], [145.0651240373354, 7641]]
Inverted File Computation time = 0.0014948844909667969


$ python3 relevance_queries.py transactions.txt queries.txt -1 -1 10
Naive Method computation time = 1.133357048034668
Inverted File Computation time = 0.5592758655548096
```

> An example of transactions, queries, signature files etc you can find on [assets folder.](https://github.com/kasselouris/Complex-Data-Management/tree/main/dataset_retrieval/assets)

