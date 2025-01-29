
# FEWSNET to PrioGrid Data Processing

This repository contains tools and resources for translating FEWSNET data into the PRIOGrid resolution format. It includes scripts, data, and documentation to facilitate preprocessing, analysis, and ingestion into the VIEWSER system.

### Purpose

The utility of performing this translation to a standardized PRIOGrid resolution is to ensure consistency with other meaningful conflict datasets and align with the global grid architecture developed by the Peace Science Infrastructure research at the University of Oslo. By reformatting FEWSNET’s raw resolution, this process enables more rigorous spatial analyses in peace and conflict research, as well as humanitarian science. Standardizing food insecurity data within PRIOGrid enhances comparability across spatial datasets, allowing researchers to investigate correlations between food insecurity, conflict, and other geospatial factors with greater methodological rigor—particularly in the context of machine learning applications.

### Navigating the Repo (Structure):
*Folders and Contents*. This information is also provided in a .md file present within each unique folder

#### Folders and Contents

#### `/Data`
- **`/External`**: Raw data files obtained from external sources. These are unprocessed and should remain unchanged.
  - **`/External/IPC`**: Contains the IPC file generated from the user defined parameters and sets the variable `ipc` within the `main.py` function.

- **`/Processed`**: Cleaned and processed data files, ready for analysis or further manipulation.
  - **`/Processed/Population`**: Contains the population data retrieved from WorldPop for the desired year
    - will countain global population datasets following the filename profile ppp_`year`_1km_Aggreagted.tif
    - **`/Proccessed/ccountry_extent`**: So that the same population data can be recycled without reproducing it. 

#### `/Docs`
- **`/ADR`**: Architecture Decision Reports.
- **`/EDA`**: Exploratory Data Analysis (EDA) outputs, including visualizations, descriptive statistics, and insights generated during the preprocessing stage.

#### `/Notebooks`

contains the file `procedure_outline.ipynb` which contains an updated workflow consistent with main.py and fewsnet_process.py (located in utils). This allows for checks and tests to be conducted in a safe space before incorporating improvements to the other functions which call upon this process.

The primary purpose of producing the fewsnet_process.py file is functionality to work through the process within a notebook. 

- **`/Tests`**
  - `Ethiopia_pilot.ipynb`: supported much of the development and key considerations that are now featuring in the main.py script. This is kept primarily for posterity.
  - `Process_Compariosn.ipynb`: This is a notebook that calls the primary function (fewsnet_process.py). Working in a notebook environment would allow a user to try out numerous different parameter combinations then reference their csv and plot examples to contrast the advantages and limitations of available processes.

#### `/Reports`
- Contains generated reports summarizing analysis results or findings related to the FEWSNET-PRIOGrid translation process.

#### `/Utils`
- All utility scripts and reusable functions for data processing and analysis are stored here. This includes Python scripts for:
  - Data cleaning
  - Resampling to PRIOGrid resolution
  - IPC classification handling
  - Population attribution

### Dependencies and steps before proceeding to running the main function

1. The user must have access to `viewser`
2. With access, a connection to the VPN must be made
3. *(do you require a FEWSNET login for the API?)*


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

| **IPC Version** | **Timeframe**   | **Details**                                                                                                                                         |
|------------------|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| **IPC2.0**      | ~2004–2012      | IPC2.0 was one of the earlier versions widely adopted during this period. It established a standardized scale for classifying food security phases but lacked some of the refinements present in later versions. |
| **IPC3.0**      | ~2013–2018      | IPC3.0 introduced significant methodological improvements, including better-defined thresholds and improved guidelines for acute food insecurity analysis. It became the primary classification method for food security assessments during this period. |
| **IPC3.1**      | ~2019–Present   | IPC3.1 represents the latest iteration, with enhanced methodologies for acute food insecurity, chronic food insecurity, and malnutrition assessments. It has been widely adopted for recent analyses, with data available primarily from 2019 onward. |


2. *Start Date:*

3. *End Date:*

4. *Do you want to generate an IPC completeness graphic:*

5. *Enter one or more country codes seperated by commas, or type 'All' to select all countries:*

6. *Please select a process: 1, 2, 3, 4, 5, or 6 (default: 6)*

The present status (Jan 27, 2025) allows for flexibility between the translation procedure from mapping the original resolution of FEWSNet data to the standard PRIOGRID Unit. 

#### Resources for selecting a process and understanding tool functionality
#### `/Docs/EDA`

-----CLEAN THIS UP-----
A unique document has been developed for each process (function) modelled to assign the raw values, with unqique administrative boundaries, to the standard PG-Cell resolution. The file name references the python code function used for ease of access: `Process for function (function name)`:

- *Docs/EDA/Process for function aggregate_by_greatest_population.md*
- *Docs/EDA/Process for function process_pop_area_weights.md*
- *Docs/EDA/.....md*
- *Docs/EDA/.....md*
- *Docs/EDA/.....md*
- *Docs/EDA/.....md*
- *Docs/EDA/.....md*

In future versions of this repo, some of these methods may be removed to limit (constrain) available processes to more robust and rigorously tested options. 
-----------CLEAN THIS UP------------

Simplest to explain and process: *Select process **4***

7. *Do you want to generate IPC historical maps?:*

8. *Enter one of the following options:*
    - Type a specific date from the above list.
    - Type 'All' to process all dates.
    - Type 'Quit' to exit the program.

9. Complete! You can reference the saved .csv file in the folder /<...>/FEWSnet/Data/Processed/csv

#### With this awareness of the embedded processes, execute the `main.py` function:
***In command line:***

``` 
conda activate viewser
```
- Navigate to the repos base directory
- Execute the primary function

``` 
python main.py
```

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

