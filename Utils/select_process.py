from Utils.process_area_combined_threshold import assign_combined_threshold
from Utils.process_area_majority_overlap import assign_majority_overlap
from Utils.process_area_proportional import calculate_weighted_values
from Utils.process_area_threshold import assign_max_above_threshold_with_fallback

from Utils.process_greatest_pop import aggregate_by_greatest_population
from Utils.process_pop_area_weights import calculate_population_percentiles, aggregate_with_weighted_proportions, get_population_thresholds, get_user_defined_weights 


def define_process(process_selection, intersected_gdf):
    """
    Execute a selected process based on user input and optional parameters.

    Args:
        process_selection (int): The selected process number (1, 2, 3, or 4).

    Returns:
        DataFrame: The result of the selected process.
    """

    if process_selection == 1:
        result = calculate_weighted_values(intersected_gdf)
        return result

    elif process_selection == 2:
        # Prompt user input for threshold with a default value
        try:
            threshold = float(input("Enter the threshold for Proportional_area (default is 0.2): ") or 0.2)
        except ValueError:
            print("Invalid input. Using default threshold of 0.2.")
            threshold = 0.2

        result = assign_max_above_threshold_with_fallback(intersected_gdf, threshold=threshold)
        return result

    elif process_selection == 3:
        # Prompt user input for both proportional threshold and critical value
        try:
            proportional_threshold = float(input("Enter the proportional threshold (default is 0.3): ") or 0.3)
        except ValueError:
            print("Invalid input. Using default proportional threshold of 0.3.")
            proportional_threshold = 0.3

        try:
            critical_value = float(input("Enter the critical value (default is 3): ") or 3)
        except ValueError:
            print("Invalid input. Using default critical value of 3.")
            critical_value = 3

        result = assign_combined_threshold(intersected_gdf, proportional_threshold=proportional_threshold, critical_value=critical_value)
        return result

    elif process_selection == 4:
        result = assign_majority_overlap(intersected_gdf)
        return result
    
    elif process_selection == 5:
        result = aggregate_by_greatest_population(intersected_gdf)
        return result
    
    elif process_selection == 6:

        # Step 1: Get population thresholds (user can modify or use defaults)
        thresholds = get_population_thresholds(default_thresholds=[50, 85])

        # Step 2: Calculate population percentiles based on the thresholds
        percentile_calc = calculate_population_percentiles(intersected_gdf, column='Cell_population', percentiles=thresholds)

        # Step 3: Dynamically identify percentile keys and get user-defined weights
        sorted_percentiles = sorted(percentile_calc.keys(), key=lambda x: int(x.rstrip('th')), reverse=True)
        print("\nDefine the weights for each population percentile.")
        user_defined_weights = get_user_defined_weights(sorted_percentiles)

        result = aggregate_with_weighted_proportions(intersected_gdf, percentile_calc, user_defined_weights)

        #result = aggregate_with_weighted_proportions(intersected_gdf, percentile_calc)
        return result


    else:
        print("Invalid process selection. Please select a number between 1 and 6.")
        return None
    
# Ensure this runs only when executed directly, not when imported
if __name__ == "__main__":
    process_selection = define_process()
    print(f"You selected process: {process_selection}")