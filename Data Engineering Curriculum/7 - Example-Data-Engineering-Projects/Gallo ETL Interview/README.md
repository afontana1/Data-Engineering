## Profile remote data

1. Retrieve Iris data (csv) from remote site
2. Store locally in parquet format
3. Generate profile of data

## Data flow design for high volume

Most websites use Google Analytics for tracking click streams data of visitors.  Both anonymous and named.  Data from Google Analytics cannot be queried direct.  Instead, the data is pushed into Google Cloud (Big Query), where it can then be queried or exported.  We want to join the Google Analytics data with our own internal marketing data, which is all stored within AWS.  The Google Data is in avro format as a complex record (nested objects).  The rest of the marketing data is stored within a structured RedShift database.

Design a flow diagram of how you might retrieve, parse, clean and publish the Google Analytics data, so that a Data Analyst can easily build reports that join the data together.  Please include which language and tools you’d use, and where translations or conversions would occur.  Additionally, what is the frequency of the jobs or trigger.

### Running the Project
1. Create and run Virtual Environment
```
python -m venv etl_venv

```
- On windows
```
etl_venv\Scripts\activate.bat
```
2. pip install requirements.txt
3. Open jupyter notebook, run the code.

### Iris Dataset Information

- Information taken from https://archive.ics.uci.edu/ml/machine-learning-databases/iris/

1. Attribute Information:
   1. sepal length in cm
   2. sepal width in cm
   3. petal length in cm
   4. petal width in cm
   5. class: 
      -- Iris Setosa
      -- Iris Versicolour
      -- Iris Virginica

### ETL Best Practices

1. understand the data consumer (who will be consuming the product)
2. understand the data (the product itself)
3. keep the data in its raw form

-Create reference data: create a dataset that defines the set of permissible 
values your data may contain. For example, in a country data field, specify the 
list of country codes allowed.

4. do not delete or move your raw data

- Extract data from different sources: 
the basis for the success of subsequent ETL steps is to extract data correctly. 
Take data from a range of sources, such as APIs, non/relational databases, 
XML, JSON, CSV files, and convert it into a single format for standardized processing.

- Validate data: Keep data that have values in the expected ranges and reject any that do not.
 For example, if you only want dates from the last year, 
reject any values older than 12 months. Analyze rejected records, 
on an on-going basis, to identify issues, correct the source data, 
and modify the extraction process to resolve the problem in future batches.

5. validate the extracted data before saving
6. transform your data over all time
7. separate your E-TL

- Transform data: Remove duplicate data (cleaning), apply business rules, 
check data integrity (ensure that data has not been corrupted or lost), and 
create aggregates as necessary. For example, if you want to analyze revenue, 
you can summarize the dollar amount of invoices into a daily or monthly total. 
You need to program numerous functions to transform the data automatically. 

8. minimize the number of data and compute nodes (simplicity)
9. store all of the data, and data generated from the process, and any metadata associated with the flow
10. make your ETL acyclical
11. validate your data before giving it to consumers (staging)

- Stage data: You do not typically load transformed data directly into the target data warehouse. 
Instead, data first enters a staging database which makes it easier to roll back if something goes wrong. 
At this point, you can also generate audit reports for regulatory compliance, or diagnose and repair data problems.

12. join the data at the database level
13. monitor your data