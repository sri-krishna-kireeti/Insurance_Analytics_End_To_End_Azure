# End-to-End Azure Data Engineering Pipeline  
### Azure Data Factory + Azure Data Lake + Azure Databricks (Medallion Architecture)

This project demonstrates how to build a **scalable end-to-end data engineering pipeline on Azure** using **Azure Data Factory, Azure Data Lake Storage Gen2, and Azure Databricks**.

The pipeline ingests data from a **PostgreSQL database**, stores raw datasets in the **Bronze layer of a data lake**, performs transformations using **Azure Databricks with Delta Lake**, and produces **Gold-layer analytical tables** optimized for reporting and analytics.

The architecture follows the **Medallion (Bronze → Silver → Gold) data lakehouse design**, which separates raw ingestion, data cleaning, and analytical modeling into structured layers.

To improve scalability, the ingestion pipeline is designed using a **metadata-driven framework**, allowing multiple source tables to be ingested dynamically without creating separate pipelines for each dataset.

---

## Architecture Overview

The pipeline consists of the following stages:

### 1️⃣ Data Ingestion (Azure Data Factory)

- Metadata-driven ingestion framework
- Incremental data extraction from PostgreSQL
- Raw data stored in ADLS Gen2 Bronze layer

### 2️⃣ Data Transformation (Azure Databricks)

- Bronze → Silver transformations using PySpark
- Data cleaning, standardization, and validation
- Storage using Delta Lake tables

### 3️⃣ Analytical Modeling (Gold Layer)

- Creation of fact and dimension tables
- Aggregated datasets for analytics and reporting

### 4️⃣ Orchestration (Azure Data Factory)

- End-to-end pipeline automation
- Databricks jobs triggered from ADF pipelines

---

## Tech Stack

- **Azure Data Factory (ADF)** – Data ingestion & orchestration  
- **Azure Data Lake Storage Gen2 (ADLS)** – Data lake storage  
- **Azure Databricks** – Distributed data processing with Spark  
- **Delta Lake** – Reliable storage layer for Silver & Gold datasets  
- **PostgreSQL** – Source system for ingestion  
- **PySpark** – Data transformation logic  

---

## Key Features

✔ Metadata-driven ingestion pipeline  
✔ Incremental data loading from PostgreSQL  
✔ Medallion architecture implementation  
✔ Bronze → Silver → Gold transformations  
✔ Delta Lake for reliable and scalable analytics  
✔ Automated orchestration using Azure Data Factory  

---

## Project Architecture
PostgreSQL

 ↓

Azure Data Factory (Metadata Ingestion Pipeline)

  ↓

Bronze Layer (ADLS Gen2 - Parquet)

  ↓
    
Azure Databricks (Bronze → Silver Transformations)

  ↓
    
Silver Layer (Delta Tables)

   ↓
    
Gold Layer (Fact & Dimension Tables)

   ↓

Analytics / Reporting

---

## Data Factory Pipeline
<img width="848" height="621" alt="image" src="https://github.com/user-attachments/assets/3118df8c-a64e-4c63-96e9-0c7fecc508dc" />

Inside ForEach loop:
<img width="1561" height="591" alt="image" src="https://github.com/user-attachments/assets/6531f90b-5007-4646-aa71-41aa69325631" />

Silver data pipeline inside databricks:
<img width="800" height="632" alt="image" src="https://github.com/user-attachments/assets/fbd601b1-3a55-43dc-9404-e1bcde9e402d" />

# Final pipeline combining above 2 pipelines:
<img width="800" height="429" alt="image" src="https://github.com/user-attachments/assets/36b2d71b-7489-427c-baa8-34fa6e33328e" />


---

## Learning Goals

This project demonstrates practical concepts used in **modern data engineering systems**, including:

- Building **metadata-driven pipelines**
- Implementing **incremental ingestion strategies**
- Designing **layered lakehouse architectures**
- Orchestrating **ADF and Databricks pipelines**
- Creating **scalable and maintainable data platforms**

---

💡 This project was built as a **hands-on implementation of a modern Azure data engineering pipeline**, demonstrating real-world design patterns used in production systems.
