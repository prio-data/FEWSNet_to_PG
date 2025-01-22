def get_date_range():
    """
    Prompt the user for a start date and an end date in the YYYY-MM-DD format.

    Returns:
        tuple: A tuple containing start_date and end_date as strings.
    """
    import datetime

    # Prompt for start date
    while True:
        print("Please supply a start date in the YYYY-MM-DD format (e.g., 2004-01-01):")
        start_date = input("Start Date: ").strip()
        try:
            # Validate date format
            datetime.datetime.strptime(start_date, "%Y-%m-%d")
            print(f'Your selected start date is: {start_date}')
            break
        except ValueError:
            print("Invalid date format. Please use the YYYY-MM-DD format.")

    # Prompt for end date
    while True:
        print("Please supply an end date in the YYYY-MM-DD format (e.g., 2012-12-31):")
        end_date = input("End Date: ").strip()
        print(f'Your selected end date is: {end_date}')

        try:
            # Validate date format
            datetime.datetime.strptime(end_date, "%Y-%m-%d")
            # Check if the end date is after the start date
            if end_date >= start_date:
                break
            else:
                print("End date must be later than or equal to the start date.")
        except ValueError:
            print("Invalid date format. Please use the YYYY-MM-DD format.")

    return start_date, end_date

def select_ipc_classification():
    """
    Prompt the user to select an IPC classification from IPC 2.0, IPC 3.0, or IPC 3.1.
    Converts the selection to the corresponding format (IPC20, IPC30, or IPC31).
    Allows the user to quit the process by typing 'q'.

    Returns:
        str: The selected IPC classification in the format IPC20, IPC30, or IPC31, or None if the process is quit.
    """
    print("Type 'q' at any time to quit the process.")
    print("\nGeneral date ranges associated with each IPC classification:")
    print("1. IPC 2.0: ~2004–2012")
    print("2. IPC 3.0: ~2013–2018")
    print("3. IPC 3.1: ~2019–Present")
    print("\nPlease choose an IPC classification from the options above.")

    # Mapping for user input to program-specific classifications
    classification_mapping = {
        "IPC 2.0": "IPC20",
        "IPC 3.0": "IPC30",
        "IPC 3.1": "IPC31",
    }

    while True:
        selected_ipc_classification = input("Enter your choice (IPC 2.0, IPC 3.0, IPC 3.1): ").strip().upper()
        if selected_ipc_classification.lower() == 'q':
            print("Process quit. Goodbye!")
            return None
        elif selected_ipc_classification in classification_mapping:
            ipc_classification = classification_mapping[selected_ipc_classification]
            print(f"Selected IPC classification: {selected_ipc_classification} ({ipc_classification})")
            return ipc_classification
        else:
            print("Invalid input. Please enter one of the following: IPC 2.0, IPC 3.0, or IPC 3.1.")
