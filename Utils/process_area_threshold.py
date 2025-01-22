import pandas as pd

def assign_max_above_threshold_with_fallback(df, threshold=0.2, pg_id_column='pg_id'):
    """
    Assign the maximum value if its Proportional_area exceeds a threshold.
    If no values meet the threshold, calculate the weighted average as a fallback.

    Args:
        df (DataFrame): A DataFrame containing 'pg_id', 'value', and 'Proportion_area' columns.
        threshold (float): The Proportional_area threshold.
        pg_id_column (str): The column representing unique pg_ids.

    Returns:
        DataFrame: A DataFrame with 'pg_id' and 'dissolved_value'.
    """
    results = []

    # Group by pg_id and apply the logic for each group
    for pg_id, group in df.groupby(pg_id_column):
        # Filter rows where Proportional_area meets the threshold
        valid_values = group[group['Proportional_area'] >= threshold]

        if not valid_values.empty:
            # Assign the maximum value among the filtered rows
            dissolved_value = valid_values['value'].max()
        else:
            # Fallback: Calculate the weighted sum of value by Proportional_area
            dissolved_value = (group['value'] * group['Proportional_area']).sum()

        # Append result
        results.append({'pg_id': pg_id, 'dissolved_value': dissolved_value})

    # Convert results to a DataFrame
    result_df = pd.DataFrame(results)
    return result_df