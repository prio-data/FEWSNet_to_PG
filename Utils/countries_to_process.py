def select_country_codes(ipc):
    """
    Display a vertical list of available country codes and their associated country names.
    Prompt the user to select one or more country codes, or all countries.

    Args:
        ipc (DataFrame): The input DataFrame containing 'country_code' and 'country' columns.

    Returns:
        tuple: A tuple containing the filtered DataFrame and a list of selected country codes.
    """
    # Step 1: Create a dictionary of unique country codes and names
    country_dict = ipc[['country_code', 'country']].drop_duplicates().set_index('country_code')['country'].to_dict()

    # Step 2: Sort the dictionary by country code
    country_dict = dict(sorted(country_dict.items()))

    # Step 3: Print the available codes with their associated country names
    print("Available country codes and names:")
    for code, name in country_dict.items():
        print(f"{code}: {name}")

    # Step 4: Prompt the user for a selection
    while True:
        user_input = input(
            "\nEnter one or more country codes separated by commas, or type 'All' to select all countries: "
        ).strip().upper()

        if user_input == "ALL":
            print("You selected all countries.")
            return ipc, list(country_dict.keys())

        # Split the input into a list of codes
        selected_codes = [code.strip() for code in user_input.split(",")]

        # Validate the input
        invalid_codes = [code for code in selected_codes if code not in country_dict]
        if invalid_codes:
            print(f"Invalid country codes: {', '.join(invalid_codes)}. Please try again.")
        else:
            print("You selected the following countries:")
            for code in selected_codes:
                print(f"{code}: {country_dict[code]}")
            ipc_filtered = ipc[ipc['country_code'].isin(selected_codes)]
            return ipc_filtered, selected_codes
