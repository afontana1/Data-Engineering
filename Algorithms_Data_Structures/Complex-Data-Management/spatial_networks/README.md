## california_road_network.py

Creates a data structure that holds for all the nodes from California Road Network its coordinates and an adjacency list with all its neighbor nodes and their edge distance from them. It then outputs this data structure on out.txt.

The data about the Californias Road Network and an example *out.txt* are in the [assets folder](https://github.com/kasselouris/Complex-Data-Management/tree/main/spatial_networks/assets) and are based on [this data set](http://www.cs.utah.edu/~lifeifei/SpatialDataset.htm).

The first line of *out.txt* is:
```0 -121.904167 41.974556 1 0.002025 6 0.005952``` 

and is meant to be readed like node 0 with latitude -121.904167 and longtitude 41.974556 has node 1 as neighbor with edge distance 0.002025 and node 6 with edge distance 0.005952.

----------------------------------------

## dijkstra_Astar.py

Based on the Californias Road Network above we find the shortest path distance between two nodes of the graph using two popular algorithms, [Dijkstra](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) and [A*](https://en.wikipedia.org/wiki/A*_search_algorithm) shortest path algorithms.

* Example output:
```
$ python3 dijkstra_Astar.py out.txt 0 55
Dijkstra algorithm statistics for path from node 0 to node 55:
Shortest path length = 123
Shortest path distance = 1.91227
Shortest path = [0, 6, 5, 8, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 388, 541, 540, 539, 538, 537, 536, 535, 534, 533, 532, 531, 530, 529, 528, 527, 526, 525, 524, 523, 480, 479, 478, 457, 456, 455, 454, 453, 452, 451, 450, 449, 448, 447, 446, 445, 444, 443, 442, 441, 440, 439, 438, 437, 436, 435, 58, 57, 56, 55]
Number of visited nodes = 905 

A* algorithm statistics for path from node 0 to node 55:
Shortest path length = 123
Shortest path distance = 1.91227
Shortest path = [0, 6, 5, 8, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 388, 541, 540, 539, 538, 537, 536, 535, 534, 533, 532, 531, 530, 529, 528, 527, 526, 525, 524, 523, 480, 479, 478, 457, 456, 455, 454, 453, 452, 451, 450, 449, 448, 447, 446, 445, 444, 443, 442, 441, 440, 439, 438, 437, 436, 435, 58, 57, 56, 55]
Number of visited nodes = 215 
```

----------------------------------

## topK_NRA.py

Based on the Californias Road Network above we find the best meeting node for a set of starting nodes. The best meeting node must selected so as the max shortest path distance from a starting node to this node is the smallest possible. Dijkstras shortest path and top K NRA algorithm are used.


* Example output:
```
$ python3 topK_NRA.py out.txt 1 2454 9999 5
Best meeting node for source nodes [1, 2454, 9999, 5] is node: 3781
Max shortest path distance = 4.079236000000001
```
