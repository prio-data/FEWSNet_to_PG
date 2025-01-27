# Steps to Download and Update Acute Food Insecurity Data

## Selection Criteria
1. What differentiates 'Scale'?
- IPC 2.0
- IPC 3.0
- IPC 3.1

| Feature                       | **IPC 2.0**                           | **IPC 3.0**                            | **IPC 3.1**                            |
|-------------------------------|---------------------------------------|----------------------------------------|----------------------------------------|
| **Introduction**              | Standardization of food insecurity phases | Improved methods for severity analysis  | Refinements for consistency and robustness |
| **Phases**                    | 5 phases (Minimal to Famine)          | Same phases, with better analysis tools | Same phases, with refined criteria     |
| **Data Integration**          | Limited                               | Advanced integration tools             | Improved handling of uncertainties      |
| **Chronic vs Acute**          | Limited differentiation               | Clearer separation                     | Further refined                        |
| **Focus on Early Warning**    | Basic                                 | Enhanced                               | Strengthened                           |
| **Stakeholder Engagement**    | Basic                                 | Broader                                | Even broader                           |
| **Refinements**               | Initial threshold definitions         | Improved validation protocols          | Handling qualitative and uncertain data|

2. Is the spatial accuracy homogenous?

When querying global data via the FEWS NET API, the spatial resolution of the data may vary by country or region. The API does not homogenize granularity but instead provides data as it exists for each country.
For example:

- Country A may have data available at the Admin 1 level (e.g., provinces or states).
- Country B may only have national-level data (country-wide aggregates).
- Country C may provide Admin 2 or Admin 3 granularity if local assessments were conducted.

This means the dataset retrieved from the API can include a mix of spatial resolutions. You’ll need to inspect the geographic unit metadata to determine the level of granularity for each record.

2.1 What do `unit_type` attributes represent:
['fsc_admin', 'fsc_admin_lhz', 'idp_camp', 'national_park', 'fsc_rm_admin']

3. Does FEWSNET manage a complete, temporal database of these changing boundaries?

- It would be inefficient to construct such a database from: https://fews.net/data/geographic-boundaries where data needs to be searched for by both time and geographic area. 

4. How can I develop a 'key' for each FEWSNET release? That is if the desire is to download new FEWSNET data each month / year, the spatial specificity may change within a country. ie. a country that was previously cataloged at the country scale may switch to admin 2 or 3 level (who can I confirm this with at FEWSNET? -- Paola has a reference). This would mean that before associating the FEWSNET csv data to the pg grid -- a new pg to admin key would need to be developed. A single boundary resource is thus not reliable for this dataset!


## Step 1: Initial Data Download

1. **Endpoint to Use**:  
   Use the **Time Series Data** endpoint:  
   `https://fdw.fews.net/api/ipcphase/`

2. **Query Parameters**:  
   Include filters to retrieve all relevant data. For example:
   - **Date Range:** Use `start_date` and `end_date` to specify a range up to the current date.
   - **Geographic Unit:** If you want specific regions, filter by `geographic_unit`.
   - **Classification Scale:** Use `classification_scale=IPC31` for IPC 3.1 classifications.

   Example:  
https://fdw.fews.net/api/ipcphase.csv?start_date=2000-01-01&end_date=2024-12-31&classification_scale=IPC31


3. **Output Format**:  
To download the data in a structured format (e.g., CSV or JSON), add a query parameter or file extension:
- CSV: `?format=csv` or `.csv`
- JSON (default): `?format=json` or `.json`

Example for CSV:  
https://fdw.fews.net/api/ipcphase.csv?start_date=2000-01-01&end_date=2024-12-31&classification_scale=IPC31

4. **Automate Download**:  
Use a script (e.g., Python) to fetch and store the data locally. Below is an example Python snippet:

```
python
import requests

url = "https://fdw.fews.net/api/ipcphase.csv"
params = {
    "start_date": "2000-01-01",
    "end_date": "2024-12-31",
    "classification_scale": "IPC31"
}

response = requests.get(url, params=params)
with open("ipc_data.csv", "wb") as file:
    file.write(response.content)

print("Data downloaded and saved as ipc_data.csv")
```  


