def get_process_selection(default_process=6):
    """
    Prompt the user to select a process from options 1, 2, 3, 4, 5, or 6.
    Defaults to process 6 if no input is provided, with a detailed explanation of each option.
    Includes an option to quit the process.

    Args:
        default_process (int): The default process to use if no input is provided.

    Returns:
        int: The selected process number (1, 2, 3, 4, 5, or 6), or None if the user quits.
    """
    # Define the process descriptions
    process_descriptions = {
        1: """- First checks for rows meeting both a proportional area threshold and a critical value.
  - Assigns the maximum value from the filtered rows if conditions are met.
  - Otherwise, calculates a fallback weighted sum of values by proportional area.""",
        2: """- Assigns the value that occupies the largest proportion of area within each `pg_id`.
  - Uses the row with the highest `Proportional_area` as the dominant value.""",
        3: """- Multiplies each row’s value by its proportional area to compute a weighted value.
  - Groups data by `pg_id` and sums the weighted values to produce a dissolved value.""",
        4: """- Assigns the maximum value if its proportional area exceeds a specified threshold.
  - If no rows meet the threshold, calculates a fallback weighted sum of values by proportional area.""",
        5: """- Uses the row with the greatest population proportion within each `pg_id`.
  - Combines population and area proportions to calculate weighted values, summing these at the `pg_id` level.""",
        6: """- Applies custom weights to population and area proportions based on population percentiles.
  - Calculates a weighted value for each row and aggregates by `pg_id`. (default)"""
    }

    # Display the descriptions to the user
    print("\nProcess Selection Options:\n")
    for key, description in process_descriptions.items():
        print(f"{key}: {description}\n")

    # Prompt for user selection
    while True:
        try:
            print(f"Please select a process: 1, 2, 3, 4, 5, or 6 (default: {default_process})")
            print("Type 'q' to quit the process.")
            user_input = input("Enter your selection (or press Enter to use the default): ").strip()

            # Handle quit option
            if user_input.lower() == 'q':
                print("Process quit. Goodbye!")
                return None

            # Use default if input is empty
            if not user_input:
                print(f"No input provided. Using default process: {default_process}")
                return default_process

            # Convert input to integer and validate
            process_selection = int(user_input)
            if process_selection in process_descriptions.keys():
                return process_selection
            else:
                print("Invalid selection. Please enter 1, 2, 3, 4, 5, or 6.")
        except ValueError:
            print("Invalid input. Please enter a number (1, 2, 3, 4, 5, or 6) or 'q' to quit.")


# Ensure this runs only when executed directly, not when imported
if __name__ == "__main__":
    process_selection = get_process_selection()
    if process_selection is not None:
        print(f"You selected process: {process_selection}")
    else:
        print("No process was selected. Exiting.")
