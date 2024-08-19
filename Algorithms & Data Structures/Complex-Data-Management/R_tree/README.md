# R-tree
R-tree is a tree data structure used for **spatial access methods**, i.e., for indexing **multi-dimensional information** such as geographical coordinates, rectangles or polygons.

The key idea of the data structure is to group nearby objects and represent them with their Minimum Bounding Rectangle(MBR) in the next higher level of the tree; the "R" in R-tree is for rectangle. Since all objects lie within this bounding rectangle, a query that does not intersect the bounding rectangle also cannot intersect any of the contained objects. At the leaf level, each rectangle describes a single object; at higher levels the aggregation includes an increasing number of objects. This can also be seen as an increasingly coarse approximation of the data set.

For more info check [R-tree on wikipedia](https://en.wikipedia.org/wiki/R-tree).

----------------------------------------------------------------------
## R_tree.py
Bulk-loads the R-tree using the [Z-order](https://en.wikipedia.org/wiki/Z-order_curve) value of the center of a rectangle for sorting. 

Output:
* Writes the resulted R-tree on Rtree.txt
* Prints as output the number of nodes of each tree level.

An example output is [Rtree.txt](https://github.com/kasselouris/Complex-Data-Management/blob/main/R_tree/assets/Rtree.txt).  
The output is in this form ```[isnonleaf, node-id, [[id1, MBR1], [id2, MBR2], …, [idn, MBRn]]]```

## range_queries.py
Finds the rectangles of the R-tree that intersect a querys rectangle(window).

* An example output is ```0 (7): 2527,2712,8371,5042,7080,7656,7944```.  
* The output is in this form ```query_num (num_of_MBRs_that_intersect_query): MBR_id1, MBR_id2, ...```

## kNNqueries.py
Finds the K Nearest Neighbors(rectangles) from a querys point.

* An example output for K=10 is ```0: 9311,7001,803,5361,6764,3905,1642,3260,4669,5762```.  
* The output is in this form ```query_num: MBR_id1, MBR_id2, ... ```


> You can find example files to test the above algorithms on [assets folder](https://github.com/kasselouris/Complex-Data-Management/tree/main/R_tree/assets).
