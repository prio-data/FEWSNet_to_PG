
# FEWSNET to PrioGrid Data Processing

This repository contains tools and resources for translating FEWSNET data into the PRIOGrid resolution format. It includes scripts, data, and documentation to facilitate preprocessing, analysis, and ingestion into the VIEWSER system.

### Navigating the Repo (Structure):
*Folders and Contents*. This information is also provided in a .md file present within each unique folder

#### Folders and Contents

#### `/Data`
- **`/External`**: Raw data files obtained from external sources. These are unprocessed and should remain unchanged.
- **`/Processed`**: Cleaned and processed data files, ready for analysis or further manipulation.

#### `/Docs`
- **`/ADR`**: Architecture Decision Reports.
- **`/EDA`**: Exploratory Data Analysis (EDA) outputs, including visualizations, descriptive statistics, and insights generated during the preprocessing stage.

#### `/Reports`
- Contains generated reports summarizing analysis results or findings related to the FEWSNET-PRIOGrid translation process.

#### `/Utils`
- All utility scripts and reusable functions for data processing and analysis are stored here. This includes Python scripts for:
  - Data cleaning
  - Resampling to PRIOGrid resolution
  - IPC classification handling
  - Population attribution


### Overview of the process and main functions:
The user is requested to supply a response to a series of prompts that will influence the progression of the code.

These are the questions that will be presented and an overview of how to enter an appropriate and informed response:

1.  *Please choose an IPC classification from the options above.*

You will see the following lines generated, preceding this prompt

``` 
General date ranges associated with each IPC classification:
1. IPC 2.0: ~2004–2012
2. IPC 3.0: ~2013–2018
3. IPC 3.1: ~2019–Present
```

#### Selecting an IPC Classification
The Integrated Food Security Phase Classification (IPC) system has evolved through different versions (IPC2.0, IPC3.0, and IPC3.1). Each version corresponds to specific methodological updates and improvements. Here is an approximate range of dates typically associated with each IPC classification:

IPC2.0
Timeframe: ~2004–2012
Details:
IPC2.0 was one of the earlier versions widely adopted during this period.
It established a standardized scale for classifying food security phases but lacked some of the refinements present in later versions.
IPC3.0
Timeframe: ~2013–2018
Details:
IPC3.0 introduced significant methodological improvements, including better-defined thresholds and improved guidelines for acute food insecurity analysis.
It became the primary classification method for food security assessments during this period.
IPC3.1
Timeframe: ~2019–Present
Details:
IPC3.1 represents the latest iteration, with enhanced methodologies for acute food insecurity, chronic food insecurity, and malnutrition assessments.
It has been widely adopted for recent analyses, with data available primarily from 2019 onward.

2. *Start Date:*

3. *End Date:*

4. *Do you want to generate an IPC completeness graphic:*

5. *Enter one or more country codes seperated by commas, or type 'All' to select all countries:*

6. *Please select a process: 1, 2, 3, 4, 5, or 6 (default: 6)*

The present status (Jan 27, 2025) allows for flexibility between the translation procedure from mapping the original resolution of FEWSNet data to the standard PRIOGRID Unit. 

7. *Do you want to generate IPC historical maps?:*

8. *Enter one of the following options:*
    - Type a specific date from the above list.
    - Type 'All' to process all dates.
    - Type 'Quit' to exit the program.

9. Complete! You can reference the saved .csv file in the folder /<...>/FEWSnet/Data/Processed/csv


#### Resources for understanding the FEWSNet to PG translation
- Docs/EDA/<process>


#### Instructions for ingesting to VIEWSER:

run for all countries + all dates -- will iterate over IPC20, IPC30, and IPC31

There is not expected to be any overlap between these, but if so, the updated classification will take priority. 

#### How to contribute:

most revisions or new contributions are expected to be situated within the usere_defined_process function. 


#### Dictionary of resources -- responding to basic questions

1. How was population constructed
- consult access poplation resource.py and cumulative population attribution.py


-- how to aggregate to country level 
- we recommend just taking the average - there is already a country_id mapped to the data.

