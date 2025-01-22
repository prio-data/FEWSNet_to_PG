import sys

def get_dates_to_process(dataset_dates):
    """
    Allow the user to select either all dates or a single date from the list.
    Repeats the prompt until a valid date is provided or the user chooses to quit.

    Args:
        dataset_dates (list): Sorted list of available dates.

    Returns:
        list: A list of dates to process (either all dates or a single selected date).
    """
    print("Available dates:")
    for idx, date in enumerate(dataset_dates):
        print(f"{idx + 1}. {date}")

    while True:
        print("\nEnter one of the following options:")
        print("1. Type a specific date from the above list.")
        print("2. Type 'All' to process all dates.")
        print("3. Type 'Quit' to exit the program.")

        user_input = input("Your selection: ").strip()

        # Handle 'All' input
        if user_input.lower() == "all":
            return dataset_dates  # All dates to process

        # Handle 'Quit' input
        if user_input.lower() == "quit":
            print("Exiting the program. Goodbye!")
            sys.exit()

        # Handle valid date input
        if user_input in dataset_dates:
            return [user_input]  # Single date to process as a list

        # Invalid input: Repeat available options
        print("\nInvalid selection. Please type a valid date, 'All', or 'Quit'.")
        print("Available dates:")
        for idx, date in enumerate(dataset_dates):
            print(f"{idx + 1}. {date}")
