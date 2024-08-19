# Project

1. [Download VS code](https://code.visualstudio.com/download) you don't already have it.
2. Display this markdown file with ctrl+v+shift

## Phase 1

- Much of data engineering involves being able to discover interesting datasets. This is the data discovery phase; being able to identify information that can yield insights. If you have a thorough understanding of machine learning algorithms and statistics but cannot discover useful data, you will struggle convincing stakeholders of the importance of your analysis. Therefore, the first phase of this Data Engineering challenge is **what data is available**, **where can I find it**, and **how can i get it**. This is open ended, because data engineering is open ended. There will be three requirements.
    * One source must be a big dataset. By "Big" I mean minimum 10GB.
    * One source must be difficult to acquire. Maybe you will have to webscrape.
    * One source must be non-conventional data. In particular, I am looking for non-tabular data such as natural language textual data. 

- Your first job will be to identify a dataset, justify why its worth acquiring, and extract the data, storing it somewhere. Write three scripts using your preferred language that Extracts (Transforms if necessary, like if the dataset is messy) and Loads (or save somewhere in a structure format), for each bullet point listed above. This will test your ability to identify data sources, interact with API's, scrape the web efficiently etc.

## Phase 2
- Once we have the data, we can start working with it. For each bullet point above, we will do a different type of analysis. 

1. For your larget dataset, we will do simple [data profiling](https://panoply.io/analytics-stack-guide/data-profiling-best-practices/). You can use any visualization library you prefer. We want to gain a high level understanding of the attributes of the dataset. One thing you will notice is that large datasets are difficult to fit into memory, so you will need to get creative with how to process the data.
    * [Take a look at this post](https://kestra.io/blogs/2023-08-11-dataframes) for various big data processing tools to experiment with. Choose one, and explain the performance tradeoffs between them. Use one for your data profiling exercise. 

2. For the difficult to acquire dataset, you can select anything you want. You can be creative, possibly even constructing your own dataset from information you find on the web. This is actually a very valuable skill to have. In finance, there is HUGE demand for [alternative datasets](https://alternativedata.org/alternative-data/). These are datasets that are not typically used to analyze market trends. In finance, analysts typically use economic data, financial data, market data etc. but alternative data could be geospatial datasets that track the foot-traffic of consumers (using GPS) or credit card transaction data (very granular datasets). These datasets give analysts, data scientists, and decision scientists HUGE leverage over market competitors, because the dataset provides additional predictive power over traditional datasets. You can be as creative as you want with this; it might be new to you. Skilled data scientists and data engineers can construct datasets and propose them to decision makers.
    * [Here are some Libraries that will Help](https://github.com/afontana1/Data-Engineering#webscraping)

3. This dataset can be small. I don't really care about the size. Now we are going to program an algorithm from scratch. I want you to identify a dataset that contains natural language. Once you acquire it, I want you to program from scratch the [term frequency–inverse document frequency](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) algorithm. This is one of the fundamental algorithms in natural language processing, so its gonna be good to have a grasp on it. **It measures how important a word is to a document within a corpus of text**. Search engines use this algorithm to determine "relevance" and "importance" of a query. You can search github or the internet to see how other people have implemented the algorithm, but just try doing it yourself first before you consult additional resources. 

## Resources
- https://github.com/awesomedata/awesome-public-datasets
- https://hadoopilluminated.com/hadoop_illuminated/Public_Bigdata_Sets.html
- https://www.kaggle.com/code/benhamner/competitions-with-largest-datasets