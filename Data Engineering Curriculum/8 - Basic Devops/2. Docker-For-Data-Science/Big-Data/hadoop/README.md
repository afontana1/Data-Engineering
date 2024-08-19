This file will need to be replaced where the "hdfs-site.xml" is. 

This by going to the terminal and run:
1. First you need to find the file, it is almost always at etc/hadoop
```python 
docker exec namenode-1 ls etc/hadoop
```
2. Then copy/replace the file in the hadoop folder with the file in the docker namenode config
```python 
docker exec namenode-1 cp hadoop/hdfs-site.xml etc/hadoop/hdfs-site.xml
```


This file will help add big amounts of data to the HDFS by connecting to the hive metastore
