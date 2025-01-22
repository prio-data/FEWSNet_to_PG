def apply_naming_convention(dates_to_process, selected_country_codes, process_selection):
    """
    Generate a filename string based on the naming conventions for dates, country codes, and process selection.

    Args:
        dates_to_process (list): A list of dates (strings in YYYY-MM-DD format) to process.
        selected_country_codes (list): A list of selected country codes.
        process_selection (int): The selected process number.

    Returns:
        str: A filename string following the naming convention.
    """
    # Handle dates
    if len(dates_to_process) > 1:
        start_date = dates_to_process[0].replace('-', '_')
        end_date = dates_to_process[-1].replace('-', '_')
        date_string = f"{start_date}__{end_date}"
    else:
        date_string = dates_to_process[0].replace('-', '_')

    # Concatenate country codes with underscores
    country_codes_string = '_'.join(selected_country_codes)

    # Convert process selection to string
    process_selection_string = str(process_selection)

    # Combine all elements into the final naming string
    filename = f"{date_string}_{country_codes_string}_{process_selection_string}.csv"

    return filename