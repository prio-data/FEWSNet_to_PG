
def aggregate_by_greatest_population(df):
    # Ensure proportional_population column exists and handle NaN
    if 'Proportion_population' not in df.columns:
        raise KeyError("Column 'proportional_population' is missing in the DataFrame.")
    df['Proportion_population'] = df['Proportion_population'].fillna(0)

    # Find the row with the greatest population proportion for each pg_id
    max_population_rows = df.loc[df.groupby('pg_id')['Proportion_population'].idxmax()]

    # Create a dictionary to map the greatest population proportion row for each pg_id
    max_population_dict = max_population_rows.set_index('pg_id').to_dict(orient='index')

    # Apply the weighted value calculation directly within the DataFrame
    def calculate_weighted_value(row):
        max_population_row = max_population_dict[row['pg_id']]
        if max_population_row['feature_population'] > 0:  # If the greatest population proportion is valid
            return row['Proportion_population'] * row['value'] if row['feature_population'] > 0 else 0
        else:  # Fallback to proportional area if no population in pg_id
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