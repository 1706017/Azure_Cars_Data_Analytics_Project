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

Step7) Now we will create a adf pipeline to actually load the data into our table created in sql db that will actually pull the data from github and load into sql db table (source_cars_data)


       




