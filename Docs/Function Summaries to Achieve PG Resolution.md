# Function Summaries: Aggregating Data to Priogrid Structures

This document summarizes the unique approaches used by various functions to aggregate data from community or admin levels to priogrid structures.

## 1. `assign_combined_threshold`
- **Approach**:
  - First checks for rows meeting both a proportional area threshold and a critical value.
  - Assigns the maximum value from the filtered rows if conditions are met.
  - Otherwise, calculates a fallback weighted sum of values by proportional area.

## 2. `assign_majority_overlap`
- **Approach**:
  - Assigns the value that occupies the largest proportion of area within each `pg_id`.
  - Uses the row with the highest `Proportional_area` as the dominant value.

## 3. `calculate_weighted_values`
- **Approach**:
  - Multiplies each row’s value by its proportional area to compute a weighted value.
  - Groups data by `pg_id` and sums the weighted values to produce a dissolved value.

## 4. `assign_max_above_threshold_with_fallback`
- **Approach**:
  - Assigns the maximum value if its proportional area exceeds a specified threshold.
  - If no rows meet the threshold, calculates a fallback weighted sum of values by proportional area.

## 5. `aggregate_by_greatest_population`
- **Approach**:
  - Uses the row with the greatest population proportion within each `pg_id`.
  - Combines population and area proportions to calculate weighted values, summing these at the `pg_id` level.

## 6. `aggregate_with_weighted_proportions`
- **Approach**:
  - Applies custom weights to population and area proportions based on population percentiles.
  - Calculates a weighted value for each row and aggregates by `pg_id`.

