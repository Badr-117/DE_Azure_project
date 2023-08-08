*Air Quality Data Warehouse ETL Project*


**Overview:**

This is an end-to-end ETL project where the goal is to build a SQL data warehouse about Air quality in multiple cities across Canada, the US, and Europe, based on data extracted from different API’s.

This project was mainly focused on using the different data tools that Azure propose, including Blob storage, ADLS gen2 storage, Azure data factory, Azure Databricks, and an Azure SQL database.


**Project Architecture:**

![](Aspose.Words.ca54e59c-b0fc-4635-a010-001453464c24.001.png)


**Project Steps**

***Part 1: Data Extraction and Preparation***

- Identified the environmental domain and the problem to be solved: constructing a data warehouse for air quality data.
- Extracted data from Amber API, including Air Quality, Weather, Forest Fire, and Pollen data.
- Discovered limitations of the Ambee API's free tier and switched to the "Beijing Air Quality API."
- Focused data collection on 30 cities across Canada, the US, and Europe.
- Utilized VisualCrossin.com API for weather data.
- Employed the "For Each" activity in Azure Data Factory to extract air quality and weather data for each city during the current date.
- Stored the extracted data into Blob storage.

***Part 2: Data Processing with Azure Databricks***

- Utilized Azure Databricks for data processing tasks.
- Extracted desired columns from weather JSON data stored in Blob storage and merged results into a single CSV file.
- Undertook data processing on air quality data, addressing challenges with non-common "iaqi" columns in JSON files.
- Developed a custom function to handle dynamic "iaqi" columns, ensuring a consistent structure for data transformation.
- Merged data frames and cross-joined with "Part1\_df" to assemble a unified row with all desired columns.
- Appended processed data into a list for later merging.
- Saved the resulting output files into ADLS gen2 storage.

***Part 3: Data Warehouse Construction and Enrichment***

- Established an Azure SQL Database to serve as the core data warehouse.
- Designed and built SQL tables to accommodate processed air quality and weather data from ADLS gen2.
- Attempted to find data sources for main pollution sourcesin each city, but opted for generating fake pollution source data using ChatGPT.
- Enriched the data model with detailed location data and pollution sources using ChatGPT.
- Uploaded pollution sources and location data directly into ADLS gen2.
- Constructed location and pollution source tables and inserted corresponding data.

***Part 4: Pipeline Deployment and Optimization***

- Ensured the functionality of the pipelines to retrieve, process, and insert data into SQL tables daily.
- Modified sink during API data extraction to store new data in subfolders by current date.
- Addressed pipeline issues with the list of output files post-data processing.
- Utilized the "Get Metadata" activity to retrieve output file list for accurate selection in copy-to-SQL activity.
- Successfully established working pipelines for both air quality and weather data.
- Implemented daily triggers for automated data extraction and processing.
- Resolved pull request discrepancies between the main and collaborative branches.

**Conclusion**

This ETL project showcases the power of Azure's data tools in creating an end-to-end solution for aggregating, processing, and storing air quality and weather data from various sources. By employing Blob storage, ADLS gen2, Azure Data Factory, Azure Databricks, and Azure SQL Database, the project efficiently constructs a comprehensive data warehouse, enabling in-depth analysis and insights into air quality trends across diverse cities.
