import pandas as pd

def assign_combined_threshold(df, proportional_threshold=0.3, critical_value=3, pg_id_column='pg_id'):
    """
    Assign a value based on combined threshold rules:
    1. If a value meets both the proportional threshold and critical value, assign it.
    2. If no value meets the thresholds, calculate the weighted sum of value by Proportional_area.

    Args:
        df (DataFrame): A DataFrame containing 'pg_id', 'value', and 'Proportional_area' columns.
        proportional_threshold (float): Minimum Proportional_area to qualify.
        critical_value (float): Minimum value threshold to qualify.
        pg_id_column (str): The column representing unique pg_ids.

    Returns:
        DataFrame: A DataFrame with 'pg_id' and 'dissolved_value'.
    """
    results = []

    # Group by pg_id and apply the logic for each group
    for pg_id, group in df.groupby(pg_id_column):
        # Step 1: Filter rows meeting both thresholds
        filtered = group[(group['Proportional_area'] >= proportional_threshold) & (group['value'] > critical_value)]

        if not filtered.empty:
            # Assign the maximum value from the filtered rows
            dissolved_value = filtered['value'].max()
        else:
            # Fallback: Calculate the weighted sum of value by Proportional_area
            dissolved_value = (group['value'] * group['Proportional_area']).sum()

        # Append result
        results.append({'pg_id': pg_id, 'dissolved_value': dissolved_value})

    # Convert results to a DataFrame
    result_df = pd.DataFrame(results)
    return result_df