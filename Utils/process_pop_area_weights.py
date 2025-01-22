import pandas as pd

def get_population_thresholds(default_thresholds=[50, 85]):
    """
    Prompt the user to define specific population thresholds or use the default thresholds.

    Args:
        default_thresholds (list): The default list of percentiles to calculate.

    Returns:
        list: A list of user-defined or default thresholds.
    """
    print("\nWould you like to define specific population thresholds?")
    print(f"If not, the default thresholds ({', '.join(map(str, default_thresholds))} percentiles) will be used.")

    while True:
        user_input = input("Enter thresholds as a comma-separated list (e.g., 40, 90) or press Enter to use default: ").strip()
        
        if not user_input:  # Use default thresholds
            print(f"Using default thresholds: {default_thresholds}")
            return default_thresholds
        
        try:
            # Parse user input into a list of integers
            user_thresholds = [int(x) for x in user_input.split(',')]
            # Validate that thresholds are within 0 to 100
            if all(0 <= t <= 100 for t in user_thresholds):
                print(f"Using user-defined thresholds: {user_thresholds}")
                return user_thresholds
            else:
                print("Thresholds must be between 0 and 100. Please try again.")
        except ValueError:
            print("Invalid input. Please enter thresholds as a comma-separated list of integers.")


def calculate_population_percentiles(df, column='Cell_population', percentiles=[50, 85]):
    """
    Calculate specified percentiles for a given column in the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame containing the column to analyze.
        column (str): The column name for which to calculate percentiles (default is 'population').
        percentiles (list): List of percentiles to calculate (e.g., [50, 85]).

    Returns:
        dict: A dictionary with percentile keys and their corresponding values.
    """
    # Ensure the column exists in the DataFrame
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in the DataFrame.")

    # Calculate percentiles
    percentile_values = {
        f"{percentile}th": df[column].quantile(percentile / 100) for percentile in percentiles
    }

    return percentile_values

def get_user_defined_weights(percentiles):
    """
    Prompt the user to define weights for population and area for each percentile.

    Args:
        percentiles (list): List of percentiles (e.g., ['85th', '50th']).

    Returns:
        dict: A dictionary with keys as percentiles and values as (population_weight, area_weight) tuples.
    """
    weights = {}
    for percentile in percentiles:
        print(f"\nFor the {percentile} percentile:")

        # Get the population weight
        while True:
            try:
                pop_weight = float(input(f"Enter the population weight for the {percentile} percentile (e.g., 1.0): ").strip())
                break
            except ValueError:
                print("Invalid input. Please enter a valid numeric value.")

        # Get the area weight
        while True:
            try:
                area_weight = float(input(f"Enter the area weight for the {percentile} percentile (e.g., 0.0): ").strip())
                break
            except ValueError:
                print("Invalid input. Please enter a valid numeric value.")

        # Store weights as a tuple
        weights[percentile] = (pop_weight, area_weight)

    return weights


def aggregate_with_weighted_proportions(df, population_percentiles, user_defined_weights):
    """
    Aggregate values with weighted proportions using user-defined weights for each percentile.

    Args:
        df (pd.DataFrame): Input DataFrame with necessary columns.
        population_percentiles (dict): A dictionary with percentiles as keys and their values.
        user_defined_weights (dict): A dictionary with user-defined weights for each percentile.

    Returns:
        pd.DataFrame: Aggregated DataFrame with weighted values.
    """
    def calculate_weighted_value(row):
        # Identify upper and lower percentiles dynamically
        upper_key, lower_key = sorted(population_percentiles.keys(), key=lambda x: int(x.rstrip('th')), reverse=True)

        # Apply user-defined weights
        if row['Cell_population'] >= population_percentiles[upper_key]:
            weight_population, weight_area = user_defined_weights[upper_key]
        elif row['Cell_population'] >= population_percentiles[lower_key]:
            weight_population, weight_area = user_defined_weights[lower_key]
        else:
            weight_population, weight_area = (0.0, 1.0)

        return (
            weight_population * row['Proportion_population'] * row['value'] +
            weight_area * row['Proportional_area'] * row['value']
        )

    # Apply the weighted value calculation row-by-row
    df['weighted_value'] = df.apply(calculate_weighted_value, axis=1)

    # Aggregate by `pg_id`
    aggregated_df = df.groupby('pg_id').agg({
        'weighted_value': 'sum',
        'value': 'sum'
    }).reset_index()

    # Rename columns for clarity
    aggregated_df.rename(columns={
        'weighted_value': 'final_weighted_value',
        'value': 'original_sum_value'
    }, inplace=True)
    return aggregated_df


# def calculate_weights(row, pop_percentiles):
#     """
#     Calculate weights for a row based on population percentiles.

#     Args:
#         row (pd.Series): A row of the DataFrame containing 'Cell_population'.
#         pop_percentiles (dict): A dictionary with percentile keys (e.g., '50th', '85th') and their values.

#     Returns:
#         tuple: A tuple of two weights (weight_population, weight_area).
#     """
#     # Get the highest and second-highest percentiles dynamically
#     upper_key, lower_key = sorted(pop_percentiles, key=lambda x: int(x.rstrip('th')), reverse=True)

#     # Apply the logic based on the dynamically identified keys
#     if row['Cell_population'] >= pop_percentiles[upper_key]:
#         # user input
#         # Determine the weighting influece for food insecurity data contained within boundaries that are in the {upper key} (85th) percentile
#         return 1.0, 0.0
#     elif row['Cell_population'] >= pop_percentiles[lower_key]:
#         # user input
#         return 0.75, 0.25
#     else:
#         # user input
#         return 0.0, 1.0


# def calculate_weighted_value(row, population_percentiles):
#     weight_population, weight_area = calculate_weights(row, population_percentiles)
#     return (
#         weight_population * row['Proportion_population'] * row['value'] +
#         weight_area * row['Proportional_area'] * row['value']
#     )

# def aggregate_with_weighted_proportions(df, population_percentiles):
#     df['weighted_value'] = df.apply(lambda row: calculate_weighted_value(row, population_percentiles), axis=1)
#     aggregated_df = df.groupby('pg_id').agg({
#         'weighted_value': 'sum',
#         'value': 'sum'
#     }).reset_index()
    
#     aggregated_df.rename(columns={
#         'weighted_value': 'final_weighted_value',
#         'value': 'original_sum_value'
#     }, inplace=True)
#     return aggregated_df

