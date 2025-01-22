import pandas as pd

def assign_majority_overlap(df, pg_id_column='pg_id'):
    """
    Assign the value that occupies the largest proportion of the area (highest Proportional_area).

    Args:
        df (DataFrame): A DataFrame containing 'pg_id' and 'Proportion_area' columns.
        pg_id_column (str): The column representing unique pg_ids.

    Returns:
        DataFrame: A DataFrame with 'pg_id' and the dominant value.
    """
    results = []

    # Group by pg_id and find the value with the largest Proportional_area
    for pg_id, group in df.groupby(pg_id_column):
        # Identify the row with the maximum Proportional_area
        dominant_row = group.loc[group['Proportional_area'].idxmax()]
        dominant_value = dominant_row['value']

        # Append the result
        results.append({'pg_id': pg_id, 'dissolved_value': dominant_value})

    # Convert results to a DataFrame
    result_df = pd.DataFrame(results)
    return result_df