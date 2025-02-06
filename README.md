# Azure_Cars_Data_Analytics_Project
=====================================

Day-01 
Date: 04th Feb 2035
====================

DataEngineering Project Architecture Diagram :
======================================
--ADD Diagram

Technologies and Concepts Implemented :
===================================
	1) ADF  (Parametrized Data Pipeline)
	2) Azure SQL DB 
	3) ADLS GEN2 
	4) Azure Databricks 
	5) Parquet format 
	6) Delta Lake 
	7) Incremental Data Loading 
	8) Implement Start Schema 
	9) Implement the medallion architecture 
	10) Unity catalog for data governance 
  11)Azure Key vault for storing the credentials

Steps to be followed for implementing the Project
===================================================

Step1) Firstly we will create our azure resource groups 
       just search for resource group -> click on + button to create a new one

       Name of resource group that we have created : RG-Azure_Car_Project

Step2) Now we will create a Azure Data Lake from storage account 
       just search for azure storage account in azure and click on create to create a new adls gen2 account 
       Note: click on the checkbox enable hierarchichal namespace otherwise blob storage account gets created 
       select the resource group as you have created in step1 only 
           
            Name of the storage account name : caramritdatalake (this should be unique)

Step3) Now we will create our Azure Data Factory just go to search and search for ADF 
       click on create button 

       Name of the datafactory : ADF-cars-Project-1997

Step4) Now we will create our Azure SQL db and while creation of azure sql db you will also create your sql server 
       Name of sql db: 
       Name of sql server: server-cars-project

       login name for server : adminamrit
       password: XXXXXXXXXX

Step5) Now we will create 3 containers named bronze,silver,gold in the data lake 

Step6) Now let us create our table inside the sql db that we have created and that will be our source 
            Name of the table: source_cars_data

             using the below command:
	     
             CREATE TABLE source_cars_data
             (
               Branch_ID varchar(200),
               Dealer_ID varchar(200),
               Model_ID varchar(200),
               Revenue BIGINT,
               Units_Sold BIGINT,
               Date_ID varchar(200),
               Day INT,
               Month INT,
               Year INT,
               BranchName varchar(2000),
               DealerName varchar(2000),
               ProductName varchar(2000)
             )

Day-02
Date: 05th Feb 2025
====================
Step7) Now let us create our adf pipeline to ingest data into azure sql db from github 
             this pipeline will load all the past data till today to load at once 
             but for the next days we will create another pipeline to just load the incremental data 

      ![image](https://github.com/user-attachments/assets/af3cdf48-40f1-4e71-a449-38120b6325d6)

      Name of the pipeline: source_preparation_pipeline
             

 -> use the copy data activity and add it into the canvas but it requires source and sink location so we first need to create a linked service for both source and sink service as our source will be github and sink will be azure sql 

A)For github repository select http connection in linked service 
    name of the linked service: ls_github
   base url : https://raw.githubusercontent.com/
   authentication_type = anonymous

	• then click on test connection and click on create  so our connection with github and adf is done now

B)For Azure sql we need to create another linked service
     name of the linked service:  ls_sqlDB
     Azure subscription : Azure Learning Subscription (db1641a9-535f-457a-a683-7382817098d0)
     Server name: server-cars-project
    Database name : DB-Cars-Project
    authentication : sql type
  
**Note: While creating the linked service for connection with azure sql you may face a connection issue like firewall not allowing the connection so what you need to resolve this issue just go the server that you have created and go to security tab-> networking tab -> click on the checkbox allow azure service and resource to access the server 

Step8) Let us configure our copy data activity for the source_preparation_pipeline

	•             Now we need to create a dynamic source dataset 
                   type: http
                   format: csv
                   name of the source dataset : ds_git
                  linked service : ls_github
                  relative url : anshlambagit/Azure-DE-Project-Resources/refs/heads/main/Raw%20Data/SalesData.csv
           
	• then click on advanced button of the datset and then you will be in the edit place for the dataset this is the best place to do any such edits for your dataset that you have created

	• Go to parameter tab and click on to create a new parameter 
        name of the parameter: load_flag
         value: <leave it as it is>
  
	• Then again go to connection tab of the dataset and go to relative url and click on add dynamic content 
	Expression for the dynamic content will be : 

anshlambagit/Azure-DE-Project-Resources/refs/heads/main/Raw%20Data/@{dataset().load_flag}  //here highlited one will be treated as a variable

	• Now go to the pipeline and in the pipeline go to the source tab now you can able to see that inside your source dataset a new parameter is there just give your value as salesdata.csv and just preview your data 

	• Now we need to create our sink dataset 
    Type: azure sql db
    name of the source dataset : ds_sqlDB
    Linked service : ls_sqlDB
    Table name : dbo.source_cars_data

       • After that just click on debug button of your pipeline to see if the pipeline run is success or not 
Once your pipeline is success just go the database and try to query your table you will able to see that data is loaded now into the table from github to sql db

![image](https://github.com/user-attachments/assets/82faf5c7-3d96-4308-a3fe-fd3c8a7e4e39)

Day-03
Date: 06th Feb 2025
==================
Step9) Now let us create a new data pipeline in adf for implementing the logic of loading data incrementally 
             
             Name of the pipeline : Incremental_data_pipeline
             
	•  Now our source is sql db and we want  to incrementally load data from sql db to the bronze container via the   pipeline
	• Incremental pipeline means two pipeline
     
	• one pipeline means initial load pipeline that means we need to pull all the data from sql db to the datalake bronze container 

	• After first pipeline all the pipeline runs will be considered as incremental load pipeline run 

![image](https://github.com/user-attachments/assets/8ff7d68c-3f28-4d92-8a17-8854ed8d2846)

Now the concept behind the incremental data load is that we will use two date parameter 

 Ø one of the parameter will tell initial load start date that means what will be the last date when i have loaded the data into data lake but you might ask we do not have  any last date when we have loaded the data for the first run correct suppose we have our data from 2017 so the last load date should be any date before 2017 so in real scenario we do not use one or two year date we took more previous date 
	
 So let us take last load date as 2000-01-01 so will this data will bring all the data if we have used the query as select * from 2000-01-01 the answer is yes it will bring all the data 


	Ø Second date parameter is maximum of current date that means if we have condition 
	Select * from date > last_load_date(2000-01-01) and date <= (2020-05-31 assume this to be current date) so in the first run it will bring all the data using this pipeline

	Ø Once our data is loaded into the data lake for the first time then we will create a stored procedure in sql db what it will do is that from where the last load date is coming from it is coming from stored procedure and the maximum current date is coming from source data so once the pipeline is succesfull run for the first time then in the stored procedure we need to update our last_load_Date with the maximum_current_Date such that the query that we have in our copy data activity that is select * from table where date > last_load_date and date <=maximum_current_date so that it will only load data from june 1st 2020


![image](https://github.com/user-attachments/assets/64a59c49-ca59-4d7b-b2b1-7f5fdbf76657)

Implementing the Incremental Data Pipeline Logic in ADF
 
Step10) So now let us implement the logic for incremental data pipeline so before creating the stored procedure let us first create a watermark table and the watermark table is used to just hold that value that is the intial date 

	Ø As shown below we use the below query to create the water mark table name water_table


CREATE TABLE water_table
(
 last_load Varchar(2000)
)

	Ø In real scenario we can use data type for the last load date as date type but here we have date_id as varchar in the source data so that is unique identifier for all the dates so basically that is identifier for date dimension 


	Ø After creating the water mark table we need to insert the value into the watermark table column last_load but what we want as date 2000-01-01 but what we have is date_id like DT0000 so we need to insert minimum of date_id that we can find using the below query and then the date will be more before that such that it can load all the data for the first run of the pipeline


select min(Date_ID) from [dbo].[source_cars_data];

Output: DT00001 SO this is first date of data from where the sales started so what we will put as last_load_date for the first time is DT00000 

INSERT INTO water_table
VALUES('DT00000');

	Ø So now if we try to just check using the below query if we are able to fetch all the data from the source table or not the query is 


SELECT COUNT(*) FROM [dbo].[source_cars_data] where Date_Id > 'DT00000';

OUTPUT: 1849 which is actually the total number of records in the source  table 


Step11) So now we will be creating a stored procedure so that will be actually updating the last_load value in the watermark table























       




