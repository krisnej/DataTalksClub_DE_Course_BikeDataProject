# DataTalk Course on Data Engineering
# Final Project - Berlin Bike Thefts Data

## Problem description
The used dataset concerns information around bike thefts. It is published by the Berlin police department. 
Bike thefts are a common problem in Berlin, as in many large cities.
The dataset contains data on the time and location of the crime, as well as the type and value of the bike stolen.

The police uploads new data every day at 12 p.m. Included are the data for the current year up to the day before the update, as well as the data for the entire previous year.

In a first step (this project), the available file is processed in a batch ingestion pipeline.
A second iteration could aim at persisting data in the data warehouse that is not in the police's file anymore 
(i.e. data which is older than the previous year).

Interesting questions around the dataset are: Where and when are bikes stolen more often? 
(daily or seasonal patterns, differences in the districts of the city)
What kinds of bikes are stolen? What is their value?

## Technical Description

1. Data ingestion - Airflow to download the dataset and place it in a GCP bucket
2. Data warehouse - Host db tables on BigQuery, setup BQ using terraform
3. Transformations - Use dbt to transform the data to a suitable schema and store in BigQuery efficiently (partitioned and clustered)
4. Dashboard - Build a dashboard in Google Data studio to visualize the results

## Set up Infrastructure using Terraform

- Set up Google Cloud Platform project following these instructions [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_1_basics_n_setup/1_terraform_gcp/2_gcp_overview.md#initial-setup)
- A [terraform file](terraform/main.tf) sets up Airflow using Google Cloud Composer, BigQuery: 
```shell
# Refresh service-account's auth-token for this session
gcloud auth application-default login

# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan -var="project=<your-gcp-project-id>"
```

```shell
# Create new infra
terraform apply -var="project=<your-gcp-project-id>"
```

```shell
# Delete infra after your work, to avoid costs on any running services
terraform destroy
```
- Get the Airflow DAG files into Composer: ...
- Use [these](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/dbt_cloud_setup.md)
instructions to set up a dbt project.Then deploy a dbt job to transform the data in BigQuery.
- To visualise the data, Data Studio was used, utilizing the two views created in the dbt core model. 
The final Data Studio dashboard can be found [here](https://datastudio.google.com/u/2/reporting/4b982c64-0df8-417a-8ba9-67f5ee78f065/page/ligqC) 
(access request required).

## Project Description
### 1. Data Ingestion
**Data Source:**
The bike theft data is as a csv file provided [here](https://daten.berlin.de/datensaetze/fahrraddiebstahl-berlin) on the Berlin Open Data platform.
The information on LORs and districts (see description of data in [data_ingestion.py](airflow/dags/data_ingestion.py)) can also be found on this platform,
but is taken from ODIS (Open Data Informationsstelle), a further service by the Berlin government, as it is already in csv format there.

**Frequency of data download:**
- The bike data is updated once a day by the data provider, so the ETL pipeline needs to downloads this data daily. 
- The districts data file is static, so it only has to be downloaded once.
- The LOR data file changes sometimes, but not in a regular interval, so the url needs to be adapted to the most recent file.
(A more precise approach would be to match the date of the bike data with the version of the LOR file, but that's out of scope of this project.)

**Technology choice:**
Google Cloud Composer, GCP's managed Airflow service, was chosen instead of a dockerized setup. 
We're already using BigQuery as a Data Warehouse, and a managed service on the same platform will
in most cases be easier to maintain.

**Airflow DAGs:**
There are two different dags, each created 3 times (bike, lor, districts). 
1. The first dag is a simply one task with a bash operator, which downloads the dataset 
from an url directly into the Composer's data directory. From there, it can be accessed from other dags.
2. The second dag uses a GoogleCloudStorageToBigQueryOperator, which takes the csv file from this folder,
and writes it to a table in BigQuery, using a specified schema. The data is left as it is, as
this allows us to keep the raw data in the data warehouse, and transform it afterwards using dbt.

### 2. Data Warehouse
Explain how BQ is set up using TF
We're using BigQuery as a Data Warehouse in Google Cloud Platform. The Terraform scripts run in the 
setup step of this project already created the necessary dataset, called `berlin_bike_dataset`.

In this database, we store all our raw and transformed data, which we can then use for analytics and visualisations.

### 3. Transformations using dbt

The dbt repository for the data transformations can be found [here](https://github.com/krisnej/dtc-de-project-dbt).

The staging models clean the raw data by only selecting the relevant columns and renaming them.
The table with the bike data is partitioned on the `time_of_crime_start_day` column 
and clustered on the `LOR` column, as these are frequently queried columns, often used 
for filtering.

The core models create the basis of the visualization, one showing details of the bike data 
by district, the other focusing on the aggregation by hour of the day.
These models join the information on the LOR with the district names, as they are more 
informative on a higher level.

### 4. Dashboards

A pdf of the resulting dashboard can be found [here](berlin_bike_data_dashboard.pdf).

The dashboard can be filtered on district name and date.

The first tile shows the number of carried out thefts per district and month.
The second theft shows the average number of thefts per hour of the day.
The third tile (pie chart) shows the share of the types of bikes stolen.

