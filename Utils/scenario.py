def define_scenario(merged_df, scenario='Current Situation'):
    """
    Filter the DataFrame for the specified scenario. If the scenario doesn't exist,
    offer the user the option to select from available scenarios or quit.

    Args:
        merged_df (DataFrame): The DataFrame containing a 'scenario_name' column.
        scenario (str): The desired scenario to filter for. Defaults to 'Current Situation'.

    Returns:
        DataFrame: A filtered DataFrame for the specified scenario.
    """
    # Check if the scenario exists in the DataFrame
    if scenario not in merged_df['scenario_name'].unique():
        print(f"The specified scenario '{scenario}' does not exist.")
        
        # Display available scenarios
        available_scenarios = merged_df['scenario_name'].unique().tolist()
        print("Available scenarios:")
        for idx, available_scenario in enumerate(available_scenarios, start=1):
            print(f"{idx}: {available_scenario}")
        
        # Offer the user the option to select or quit
        user_choice = input("Enter the number of your chosen scenario, or 'q' to quit: ").strip()
        
        if user_choice.lower() == 'q':
            print("Exiting the function.")
            return None
        
        try:
            # Validate user choice
            chosen_index = int(user_choice) - 1
            if chosen_index < 0 or chosen_index >= len(available_scenarios):
                print("Invalid selection. Exiting the function.")
                return None
            else:
                scenario = available_scenarios[chosen_index]
                print(f"You selected: {scenario}")
        except ValueError:
            print("Invalid input. Exiting the function.")
            return None

    # Filter the DataFrame for the specified scenario
    merged_df_scenario = merged_df[merged_df['scenario_name'] == scenario]
    return merged_df_scenario
