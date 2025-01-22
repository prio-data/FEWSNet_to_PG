def calculate_weighted_values(group):
    """
    Calculate the weighted values for each row, group by pg_id, and sum the weighted values.

    Args:
        group (DataFrame): A DataFrame or grouped DataFrame with 'pg_id', 'value', and 'Proportional_area' columns.

    Returns:
        DataFrame: A DataFrame with 'pg_id' and the summed weighted values as 'dissolved_value'.
    """
    # Step 1: Calculate the weighted value for each row
    group['weighted_value'] = group['value'] * group['Proportional_area']
    
    # Step 2: Group by pg_id and sum the weighted values
    dissolved_df = group.groupby('pg_id', as_index=False)['weighted_value'].sum()
    
    # Step 3: Rename the column for clarity
    dissolved_df.rename(columns={'weighted_value': 'dissolved_value'}, inplace=True)
    
    return dissolved_df