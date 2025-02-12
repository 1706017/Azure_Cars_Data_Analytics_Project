%md
#Data Reading 

 df = spark.read.format('parquet')\
          .option('inferSchema',True)\
          .load('abfs://bronze@amrit_storage_Account.dfs.core.windows.net/rawdata')

%md
#Data Transformation 

#Number1) Here we are adding a new column from the existing column and we are just splitting the column and getting the first value before the delimiter 

 from pyspark.sql.functions import *

 df =  df.withColumn('model_category',split(col('model_id'),'-')[0])

#Number 2 ) Here we want to just change the data type of the column from int to string 

 from pyspark.sql.types import *
 df.withColumn('Units_sold',col('Units_sold').cast(StringType()))


#Number 3) Here we want to calculate revenue per units sold

df = df.withColumn('Rev_per_unit',col('Revenue')/col('Units_sold'))

#Some Aggregations to be performed
===============================
#Number4) need to calculate units sold by year and the branch name from which it sold the most 

 df.groupBy('year','BranchName')
    .agg(sum('Units_sold').alias('Total_units_sold'))
    .sort('Year','Total_units_sold',ascending=[1,0])
    .display()


#Data Writing 
=============
 df.write.format('parquet')\
               .mode('overwrite')\
               .option('path','abfs://silver@a_dlake.dfs.core.net/carsales')\
               .save() 

#Querying silver datafile
====================
%sql
Select * from parquet.`abfss://silver@a_dlake.dfs.core.net/carsales`





