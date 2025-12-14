### Merge join 
--------------------------------------------
* Merge join two sorted files. 
* Output must have duplicate rows appear once.
* Files should NOT load to memory.

```Output example: R_sorted = ['aa', 33], S_sorted = ['aa', 45] the output will be ['aa', 33, 45]```

### Union
--------------------------------------------
* Union of two sorted files. 
* Output must have duplicate rows appear once.
* Files should NOT load to memory.

### Intersect 
--------------------------------------------
* Intersect of two sorted files. 
* Output must have duplicate rows appear once.
* Files should NOT load to memory.

### Set Difference
--------------------------------------------
* Difference of two sorted files. 
* Output must have duplicate rows appear once.
* Files should NOT load to memory.

### Group by and Sum
--------------------------------------------
* Merge sort an unsorted file.
* Duplicate rows must appear once after sort and their value must be the sum of all their duplicates.

```e.g: R = ['aa', 33], also R = ['aa', 45] the output will be ['aa', 78]```

> You can find examples of tsv files to test the above algorithms on [tests folder](https://github.com/kasselouris/Complex-Data-Management/tree/main/database_operators/tests).
