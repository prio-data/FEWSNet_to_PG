

#### Overview of the process and main functions:

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

