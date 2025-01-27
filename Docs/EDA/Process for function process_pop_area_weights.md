#### Process for function `process_pop_area_weights.py` 

------------------------------------------------------------------
Questions to answer before completing (27-01-2025)

- how does task 5 differ from task 6?
------------------------------------------------------------------


**Considerations:**

This function **DOES** account for the *influence* of population. That is there is no metric on whether the population proportion that is derived from the total priogrid population is 10 or 10,000 people. This consideration is built up in the next process `process_pop_area_weights.py`.


**What this does ask** is:


Here are three example tables to reference to track the workflow:

Table 1 is above the highest (n) population threhsold

Table 2 is between the n and N population threshold

Table 3 is below the n population threshold


#### Table 1 (`cell_population = 100,000`)
| pg_id | feature_id | cell_population | feature_proportional_population | feature_proportional_area | value |
|-------|------------|-----------------|---------------------------------|---------------------------|-------|
| 1     | 1          | 100000          | 0.65                            | 0.25                      | 4     |
| 1     | 2          | 100000          | 0.30                            | 0.45                      | 3     |
| 1     | 3          | 100000          | 0.15                            | 0.10                      | 3     |
| 1     | 4          | 100000          | 0.00                            | 0.20                      | 1     |


#### Table 2 (`cell_population = 10,000`)
| pg_id | feature_id | cell_population | feature_proportional_population | feature_proportional_area | value |
|-------|------------|-----------------|---------------------------------|---------------------------|-------|
| 1     | 1          | 10000           | 0.65                            | 0.25                      | 4     |
| 1     | 2          | 10000           | 0.30                            | 0.45                      | 3     |
| 1     | 3          | 10000           | 0.15                            | 0.10                      | 3     |
| 1     | 4          | 10000           | 0.00                            | 0.20                      | 1     |


#### Table 3 (`cell_population = 100`)
| pg_id | feature_id | cell_population | feature_proportional_population | feature_proportional_area | value |
|-------|------------|-----------------|---------------------------------|---------------------------|-------|
| 1     | 1          | 100             | 0.65                            | 0.25                      | 4     |
| 1     | 2          | 100             | 0.30                            | 0.45                      | 3     |
| 1     | 3          | 100             | 0.15                            | 0.10                      | 3     |
| 1     | 4          | 100             | 0.00                            | 0.20                      | 1     |

**Now we will investigate how the function treats each value mapped to a pg_id**

Table 1:

| feature_id | proportional_population | proportional_area | value | weighted_value              |
|------------|--------------------------|-------------------|-------|----------------------------|
| 1          | 0.65                     | 0.25              | 4     | `0.65 * 4 = 2.6`           |
| 2          | 0.30                     | 0.45              | 3     | `0.30 * 3 = 0.9`           |
| 3          | 0.15                     | 0.10              | 3     | `0.15 * 3 = 0.45`          |
| 4          | 0.00                     | 0.20              | 1     | `0.00 * 1 = 0.0`           |

**Result**: **`2.6 + 0.9 + 0.45 + 0.0 = 3.95`**


Table 2: uses a weight of .75 for population and .25 for area

| feature_id | proportional_population  | proportional_area | value | weighted_value                      |
|------------|--------------------------|-------------------|-------|-------------------------------------|
| 1          | 0.65                     | 0.25              | 4     | `0.75×(0.65×4)+0.25×(0.25×4)=2.25`  |
| 2          | 0.30                     | 0.45              | 3     | `0.75×(0.30×3)+0.25×(0.45×3)=0.975` |
| 3          | 0.15                     | 0.10              | 3     | `0.75×(0.15×3)+0.25×(0.10×3)=0.4125`|
| 4          | 0.00                     | 0.20              | 1     | `0.75×(0.15×3)+0.25×(0.10×3)=0.4125`|

**Result**: **`2.25 + 0.975 + 0.4125 + 0.05 = 3.6875`**

Table 3:

| feature_id | proportional_population  | proportional_area | value | weighted_value             |
|------------|--------------------------|-------------------|-------|----------------------------|
| 1          | 0.65                     | 0.25              | 4     | `0.25 * 4 = 1.0`           |
| 2          | 0.30                     | 0.45              | 3     | `0.45 * 3 = 1.35`          |
| 3          | 0.15                     | 0.10              | 3     | `0.10 * 3 = 0.3`           |
| 4          | 0.00                     | 0.20              | 1     | `0.20 * 1 = 0.2`           |

**Result**: **`1.0 + 1.35 + 0.3 + 0.2 = 2.85`**


**The process:**


**Step 1:** Prompt for Population Thresholds

- Goal: Define the thresholds (e.g., 50th and 85th percentiles) to segment the population data dynamically.
- Details:
The function get_population_thresholds interacts with the user to define custom percentiles. If no input is provided, it defaults to [50, 85]. This ensures the subsequent percentile calculation aligns with user-defined criteria.

```
thresholds = get_population_thresholds(default_thresholds=[50, 85])
```

**Step 2:** Calculate Population Percentiles

- Goal: Compute the percentile values for the specified thresholds in the population data.

- Details:
The function calculate_population_percentiles ensures the Cell_population column exists in the DataFrame. It computes the percentiles dynamically based on user thresholds (e.g., 50th, 85th) and returns them as a dictionary {threshold}th: value.
This prepares the population data for weighted aggregation.

```
population_percentiles = calculate_population_percentiles(df, column='Cell_population', percentiles=thresholds)
```

**Step 3:** Prompt for Weight Assignments

- Goal: Allow users to define weights for population and area proportions for each threshold.
- Details:
The function get_user_defined_weights iterates through the percentiles computed earlier and prompts the user for weights. For each threshold (e.g., 85th, 50th), the user specifies a population weight and an area weight. These weights are stored in a dictionary and later applied to compute weighted values.

``` 
user_defined_weights = get_user_defined_weights(population_percentiles.keys())
```

**Step 4:** Define Upper and Lower Threshold Keys

- Goal: Identify the highest and second-highest thresholds dynamically to apply weights.
- Details:
The percentile dictionary is sorted by the numeric values of its keys (e.g., 85th and 50th). This step ensures that the weights and population thresholds are applied in descending order of importance.

``` 
upper_key, lower_key = sorted(population_percentiles.keys(), key=lambda x: int(x.rstrip('th')), reverse=True)
```

**Step 5:** Assign Weights Based on Population Percentiles

- Goal: Apply the user-defined weights to compute weighted values for each row dynamically.
- Details:
For each row, the Cell_population is compared against the upper and lower threshold values. The respective weights (population and area) are then applied. If a row’s population value does not meet the thresholds, a default weight of (0.0, 1.0) is applied, assigning full influence to the area.

``` 
if row['Cell_population'] >= population_percentiles[upper_key]:
    weight_population, weight_area = user_defined_weights[upper_key]
elif row['Cell_population'] >= population_percentiles[lower_key]:
    weight_population, weight_area = user_defined_weights[lower_key]
else:
    weight_population, weight_area = (0.0, 1.0)
```

**Step 6:** Compute Weighted Values for Each Row

- Goal: Calculate a weighted value based on population and area proportions.
- Details:
For each row, the weights are multiplied by the proportional population and area values, along with the value column. This ensures that the final weighted value reflects the relative influence of population and area proportions for each spatial unit (pg_id).

``` 
weighted_value = (
    weight_population * row['Proportion_population'] * row['value'] +
    weight_area * row['Proportional_area'] * row['value']
)
```

**Step 7:** Add Weighted Values to the DataFrame

- Goal: Store the calculated weighted values in the DataFrame for further aggregation.
- Details:
The weighted value calculation is applied row-by-row and stored in a new column, weighted_value. This column represents the intermediate result before aggregating values at the pg_id level.

```  
df['weighted_value'] = df.apply(calculate_weighted_value, axis=1)
```

**Step 8:** Aggregate by pg_id

- Goal: Summarize the weighted and original values for each pg_id.
- Details:
The DataFrame is grouped by the pg_id column. Both the weighted_value and value columns are summed within each group. This step ensures that all rows within a pg_id contribute to the final values proportionally.

```  
aggregated_df = df.groupby('pg_id').agg({
    'weighted_value': 'sum',
    'value': 'sum'
}).reset_index()
```


**Step 9:** Rename Output Columns for Clarity

- Goal: Standardize column names in the output for ease of interpretation.
- Details:
The aggregated DataFrame’s columns are renamed to final_weighted_value (summed weighted values) and original_sum_value (summed original values). This provides a clear distinction between weighted and unweighted results.

```  
aggregated_df.rename(columns={
    'weighted_value': 'final_weighted_value',
    'value': 'original_sum_value'
}, inplace=True)
```

**Step 10:** Return the Aggregated DataFrame

- Goal: Provide the final output with aggregated results.
- Details:
The aggregated DataFrame, now containing the summarized results for each pg_id, is returned for further analysis or visualization.

**Advantages of this selection**

- Custom Weight Assignment:
The ability to assign unique weights to population and area thresholds allows users to emphasize the importance of population data over area proportions (or vice versa) based on the specific context. For example:
In highly populated areas, population proportions may take precedence (as seen in Table 1).
In sparsely populated areas, area proportions might hold more significance (as seen in Table 3).

- Adaptability to Thresholds:
By dynamically adjusting weights based on population percentiles, this approach ensures flexibility for different scenarios (e.g., urban vs. rural regions).

- Contextual Relevance:
Allows users to incorporate domain-specific knowledge into the model by customizing how population and area influence values. This is particularly useful for spatial data where the significance of population density varies.

- Captures Variability Across Scales:
This approach demonstrates how the influence of population versus area can vary significantly between scales (e.g., Table 1 vs. Table 3) and adjusts the results accordingly.

**limitations**

- Overemphasis on Thresholds:
The reliance on static thresholds (e.g., 85th and 50th percentiles) may oversimplify complex population-area relationships, especially in transitional regions (e.g., Table 2).

- Non-Additive Influence:
Custom weights introduce subjectivity, as the influence of population and area proportions is additive rather than multiplicative. This could skew results if one weight (e.g., population) is disproportionately high.

**Decisions for use**

- Need to prioritize population influence in areas with high population densities while still accounting for spatial extent in less populated areas.

- Aim to capture the impact of population density variations across different regions or scenarios (e.g., rural vs. urban).