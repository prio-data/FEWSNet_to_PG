# Difference Between `Time Series Data` and `List of Data Series`

## 1. Time Series Data (`https://fdw.fews.net/api/ipcphase/`)
- **Purpose:** Provides a detailed, temporal view of acute food insecurity classifications over time.
- **Structure:**
  - Data is organized as a time series, where each entry represents a single observation at a specific time and location.
  - Includes attributes such as:
    - **Geographic unit:** The area where the observation applies.
    - **Date:** The time period for the classification.
    - **Phase classification:** The level of acute food insecurity.
  - Designed for analyses that require tracking changes over time, such as trends or historical comparisons.
- **Use Case:** Suitable for tasks like:
  - Identifying trends in food insecurity over time.
  - Analyzing temporal patterns or anomalies in specific regions.
  - Creating visualizations like line charts or heatmaps.

---

## 2. List of Data Series (`https://fdw.fews.net/api/ipcclassification/`)
- **Purpose:** Provides metadata or a higher-level summary of the different classifications available in the dataset.
- **Structure:**
  - Data is presented as a catalog or list of available classification series.
  - Contains attributes such as:
    - **Classification name or type:** A descriptor of the classification.
    - **Geographic coverage:** The areas associated with the classification series.
    - **Scale or methodology:** Information on how classifications were derived.
  - Focuses on providing an overview rather than granular, time-bound details.
- **Use Case:** Suitable for tasks like:
  - Exploring available classification datasets.
  - Understanding the scope and methodology behind classifications.
  - Selecting specific datasets to include in a more detailed analysis.

---

## Key Differences

| Feature                    | **Time Series Data**                            | **List of Data Series**                        |
|----------------------------|------------------------------------------------|-----------------------------------------------|
| **Level of Detail**         | Fine-grained, time-bound observations          | Summary-level metadata                        |
| **Focus**                  | Temporal changes and trends                    | Overview of classification datasets           |
| **Primary Use**            | Analysis of trends and temporal dynamics       | Exploring and selecting datasets              |
| **Data Structure**          | Chronological (time series format)             | Non-temporal, catalog-style                   |

---

## Summary
Use **`ipcphase`** for analyzing how food insecurity evolves over time and **`ipcclassification`** to understand the broader context of what classifications are available and how they are organized.
