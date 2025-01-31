
# FEWSNET to PrioGrid Data Processing

This repository contains tools and resources for translating FEWSNET data into the PRIOGrid resolution format. It includes scripts, data, and documentation to facilitate preprocessing, analysis, and ingestion into the VIEWSER system.

### Purpose

The utility of performing this translation to a standardized PRIOGrid resolution is to ensure consistency with other meaningful conflict datasets and align with the global grid architecture developed by the Peace Science Infrastructure research at the University of Oslo. By reformatting FEWSNET’s raw resolution, this process enables more rigorous spatial analyses in peace and conflict research, as well as social and political science. Standardizing food insecurity data within PRIOGrid enhances comparability across spatial datasets, allowing researchers to investigate correlations between food insecurity, conflict, and other geospatial variables with greater methodological rigor in a format that enables machine learning applications.

### Navigating the Repo (Structure):
Each folder contains a corresponding `.md` file with more details on its contents and functionality.

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

The primary purpose of producing the fewsnet_process.py file is functionality to work through the process within a notebook. `fewsnet_process.py` enables the process to be run iteratively, allowing functions to be called multiple times within a notebook. This facilitates comparisons between outputs generated with different parameter specifications, ensuring that methodological adjustments are systematically evaluated before being finalized.

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
By running the `main.py` function, the user is requested to supply a response to a series of prompts that will influence the progression of the code.

These are the questions that will be presented within the function, allowing the user to make informed judgments, along with an overview of how to enter an appropriate and well-informed response.

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
Provide a start date in the format MM-DD-YY

3. *End Date:*
Provide an end date in the format MM-DD-YY

4. *Do you want to generate an IPC completeness graphic:*
This graphic will provide a perspective on the spatial and temporal data availability within the date range criteria entered and IPC Classification. 

5. *Enter one or more country codes seperated by commas, or type 'All' to select all countries:*
You will see a list of country codes associated with country names printed as a dictionary

``` 

```
As the prompt suggests, if your intention is to iterate through **All** available countries (considering the classification and time parameters entered) enter the string 'All' in the command line. You may also select one or multiple countries within the available dictionary. If you wish to select multiple, follow this format: ET, YE, KN
*where ET provides data for Ethiopia, YE for Yemen, and KN for Kenya*

6. *Please select a process: 1, 2, 3, 4, 5, or 6 (default: 6)*

The present status (Jan 27, 2025) allows for flexibility between the translation procedure from mapping the original resolution of FEWSNet data to the standard PRIOGRID Unit. There are several processes developed to demonstrate 

#### Resources for selecting a process and understanding tool functionality
#### `/Docs/EDA`

-----CLEAN THIS UP-----
A unique document has been developed for each process (function) modelled to assign the raw values, with unqique administrative boundaries, to the standard PG-Cell resolution. The file name references the python code function used for ease of access: `Process for function (function name)`:

- *Docs/EDA/Process for function aggregate_by_greatest_population.md*
- *Docs/EDA/Process for function process_pop_area_weights.md*
- *Docs/EDA/Process for function assign_combined_threshold*
- *Docs/EDA/Process for calculate_area_weighted_values.md* 
- *Docs/EDA/Process for assign_majority_overlap.md* 
- *Docs/EDA/Process for assign_max_above_threshold.md* 

In future versions of this repo, some of these methods may be removed to constrain available processes to more robust and rigorously tested options. 

Simplest to explain and process: *Select process **4***
Most robust measure: *Select process **6***

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

Run `main.py` three times, selecting between IPC 2.0, IPC 3.0, and IPC 3.1.
- The floor date ranges should follow the guide table provided above
  - To be conservative, you may designate `2024-12-31` as the end date for all IPC classifications to ensure the most recent data is retrieved. 
- In each process, enter criteria to iterate the scirpt over `All` countries.
- This will provide three csv files which can be referenced for ingestion into `viewser`.

There is not expected to be any overlap between the IPC classification dates, but if this appears **the updated classification should take priority.**


#### Update interval:
**Six month periodic updates are recommended**

FEWSNET updates are performed infrequently, and a six-month maintenance update is recommended. To facilitate this, the repository administrator should input the latest ingestion date (e.g., 2024-12-31) as the start date and set the end date six months later.

#### How to contribute:

Most revisions or new contributions are expected to be situated within the `user_defined_process`  function. 

This repository should not require much maintainence. **Anticipated errors may center around an API call.** If this occurs:

- Consult the FEWSNET website. *Note: As of Jan. 31, 2025 this portal is offline*
- A base API call looks like:
```
base_url = "https://fdw.fews.net/api/ipcphase.csv"
```
- We then add key features to assemble a database for use at VIEWS

```
url_csv = f"{base_url}?start_date={params['start_date']}&end_date={params['end_date']}&classification_scale={params['classification_scale']}"
```
**More information on this script can be found in the function:** `Utils/api_ipc_request.py`

*If a new process is developed*

1. Save the .py function the to the `Utils` folder
2. Ensure this new process communicates to the user selection in: `Utils/select_process.py`


#### Dictionary of resources -- responding to basic questions

1. How was population constructed
- consult access poplation resource.py and cumulative population attribution.py


2. how to aggregate to country level 
- VIEWS recommends taking average of `pgm` level data - there is already a country_id mapped to the data. This can be accomplished throught the `viewser6` architecture by developing a country level aggregation Querset. This looks like: my_new_queryset = `(Queryset(“sensible_name”, **"country_month"**)...)` 

```
my_new_queryset = (Queryset(“sensible_name”, "country_month") 
               .with_column(Column(<enter fewsnet column name for dataframe>", 
                  from_loa=“priogrid_month”, 
                  from_column=<enter original fewsnet column name uploaded to the server>) 
                            ) 
               )
```

