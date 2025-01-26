#### Process for function `aggregate_by_greatest_population.py` 

The primary goal of this function is to calculate a weighted value for each pg_id (a unique identifier, likely representing spatial units). It achieves this by prioritizing rows with the highest population proportion within each pg_id group. If no valid population data exists, it falls back to using the proportional area to calculate the weighted value. The final output is an aggregated DataFrame with a summarized weighted value (final_weighted_value) and the original sum of all values (original_sum_value) for each pg_id.

**Considerations:**

This function **DOES NOT** account for the *influence* of population. That is there is no metric on whether the population proportion that is derived from the total priogrid population is 10 or 10,000 people. This consideration is built up in the next process `process_pop_area_weights.py`.


**What this does ask** is: *Are there population values existing within the PRIOGrid cell*

This is considered by first identifying the max value within the 'feature_population' column. *This could also be achieved by referencing the cell_population column*. **If** population exists, then function proceeds by the proportion. This is unique from the `process_pop_area_weights.py`, which takes more of a dynamic approach to considering *both* population proportionality, area_proportionality, and considers a reference to the population threshold appearing within that priogrid cell (ie. is population in the 10th, 50th, or 90th percentile of the country). 

**The process:**

**Step 1:** Identify Rows with the Greatest Population Proportion:

```
max_population_rows = df.loc[df.groupby('pg_id')['Proportion_population'].idxmax()]
```



**Step 2:** Determine the Aggregation Metric (Population or Area)
- Purpose: Decide whether Proportional_population or Proportional_area will be used for each pg_id.
- Action:
    - Identify the row with the maximum Proportion_population within each pg_id.
    - Use feature_population or Cell_population to determine if population data exists.
    - Create a dictionary (pg_decision) mapping each pg_id to use population or area as the metric.

```
max_population_rows = df.loc[df.groupby('pg_id')['Proportion_population'].idxmax()]
pg_decision = max_population_rows.set_index('pg_id').apply(
    lambda row: 'population' if row['feature_population'] > 0 else 'area', axis=1
).to_dict()
```

**Step 3:** Calculate Weighted Values
- Purpose: Apply the appropriate weighting (population or area) for each row based on pg_decision.
- Action:
    - If the metric is population, calculate: weighted_value = Proportion_population * value
    - If the metric is area, calculate: weighted_value = Proportional_area * value
    - Add a new column weighted_value to the DataFrame.

``` 
def calculate_weighted_value(row):
    if pg_decision[row['pg_id']] == 'population':
        return row['Proportion_population'] * row['value']
    else:
        return row['Proportional_area'] * row['value']

df['weighted_value'] = df.apply(calculate_weighted_value, axis=1)
```

**Step 4:** Aggregate Weighted Values at the pg_id Level
- Purpose: Summarize the calculated weights and original values for each pg_id.
- Action:
    - Group the DataFrame by pg_id.
    - Aggregate:
        - weighted_value is summed to produce final_weighted_value.
        - value is summed to produce original_sum_value.

``` 
aggregated_df = df.groupby('pg_id').agg({
    'weighted_value': 'sum',  # Sum of weighted values for the pg_id
    'value': 'sum'           # Original sum of values for comparison
}).reset_index()
```

**Step 5:** Rename and Return Results
- Purpose: Clean up column names for clarity.
- Action:
    - Rename weighted_value to final_weighted_value.
    - Rename value to original_sum_value.
- Output: Return the cleaned and aggregated DataFrame.

``` 
aggregated_df.rename(columns={
    'weighted_value': 'final_weighted_value',
    'value': 'original_sum_value'
}, inplace=True)

return aggregated_df
```