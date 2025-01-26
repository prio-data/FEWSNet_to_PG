def aggregate_by_greatest_population(df):
    """
    Aggregate values to PG-id resolution using either proportional population or proportional area.
    
    This function determines whether to use Proportional_population or Proportional_area for weighting
    based on the presence of valid population data (non-zero max population proportion or total population).

    Args:
        df (pd.DataFrame): Input DataFrame with columns:
            - pg_id: Priogrid identifier.
            - Proportion_population: Proportional population per feature.
            - Proportional_area: Proportional area per feature.
            - feature_population: Feature-level population.
            - Cell_population: Total priogrid cell population.
            - value: Value to be aggregated.

    Returns:
        pd.DataFrame: Aggregated DataFrame at the `pg_id` level.
    """
    # Ensure necessary columns exist
    required_columns = ['pg_id', 'Proportion_population', 'Proportional_area', 'feature_population', 'Cell_population', 'value']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"Required column '{col}' is missing in the DataFrame.")
    
    # Fill NaN values with 0
    df.fillna({'Proportion_population': 0, 'Proportional_area': 0, 'feature_population': 0, 'Cell_population': 0}, inplace=True)

    # Create a dictionary to determine whether to use population or area for each pg_id
    pg_decision = {}
    grouped = df.groupby('pg_id')
    
    for pg_id, group in grouped:
        max_population_proportion = group['Proportion_population'].max()
        total_cell_population = group['Cell_population'].max()
        
        if max_population_proportion > 0 or total_cell_population > 0:
            pg_decision[pg_id] = 'population'
        else:
            pg_decision[pg_id] = 'area'

    # Apply the weighted value calculation based on the decision for each pg_id
    def calculate_weighted_value(row):
        if pg_decision[row['pg_id']] == 'population':
            return row['Proportion_population'] * row['value']
        else:
            return row['Proportional_area'] * row['value']
    
    # Add the weighted value column
    df['weighted_value'] = df.apply(calculate_weighted_value, axis=1)

    # Aggregate the new weighted values at the pg_id level
    aggregated_df = df.groupby('pg_id').agg({
        'weighted_value': 'sum',  # Sum of weighted values for the pg_id
        'value': 'sum'  # Original sum of values for comparison
    }).reset_index()

    # Rename columns for clarity
    aggregated_df.rename(columns={
        'weighted_value': 'final_weighted_value',
        'value': 'original_sum_value'
    }, inplace=True)

    return aggregated_df
