
import os
import requests
from pathlib import Path


def check_if_population_local(year, save_folder=None):
    """
    Check if population data for a specific year has been downloaded to a folder.

    Args:
        year (int or str): The year to check for (e.g., 2020).
        save_folder (str or None): The folder path where files are stored. If None, defaults to 
                                   "Data/External/Population" relative to the project root.

    Returns:
        bool: True if the file for the specified year exists, False if not.
    """
    try:
        # Determine the save folder
        if save_folder is None:
            # Map the default location programmatically
            project_root = Path(__file__).resolve().parent.parent
            save_folder = project_root / 'Data' / 'External' / 'Population'

        # Check if the folder exists
        if not os.path.exists(save_folder):
            print(f"Folder does not exist: {save_folder}")
            return False

        # List all files in the folder
        files = os.listdir(save_folder)

        # Check if any file contains the year as part of its name
        for file in files:
            if f"ppp_{year}_1km" in file and file.endswith(".tif"):
                return True

        # No matching file found
        return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False




def get_population_data(year, save_folder=None):
    """
    Get the full path to a population data file with the specified year in its name.

    Args:
        year (int or str): The year to check for in the filename (e.g., 2020).
        save_folder (str or None): The folder path where files are stored. If None, defaults to 
                                   "Data/External/Population" relative to the project root.

    Returns:
        str or None: The full path to the file if it exists, or None if not found.
    """
    try:
        # Determine the save folder
        if save_folder is None:
            # Map the default location programmatically
            project_root = Path(__file__).resolve().parent.parent
            save_folder = project_root / 'Data' / 'External' / 'Population'

        # Check if the folder exists
        if not os.path.exists(save_folder):
            print(f"Folder does not exist: {save_folder}")
            return None

        # List all files in the folder
        files = os.listdir(save_folder)

        # Look for the file with the specified year
        for file in files:
            if f"ppp_{year}_1km" in file and file.endswith(".tif"):
                return os.path.join(save_folder, file)

        # No matching file found
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def get_url_for_year(year, dict_path=None):
    """
    Retrieve the URL associated with a specific year from a text file.
    If the year is greater than 2020, return the URL for 2020.

    Args:
        year (int): The year to search for.
        dict_path (str, optional): Path to the text file containing year-to-URL associations.
                                   Defaults to a pre-mapped location.

    Returns:
        str: The URL associated with the specified year, or the 2020 URL if the year > 2020.
    """
    try:
        # Ensure year is an integer
        year = int(year)
        print(f"Starting function for year {year}")

        # Determine the dictionary file path
        if dict_path is None:
            project_root = Path(__file__).resolve().parent.parent
            dict_path_file = project_root / 'Data' / 'External' / 'Population_Reference.txt'
        else:
            dict_path_file = Path(dict_path)

        url_2020 = None  # Store the 2020 URL for fallback
        with open(dict_path_file, 'r') as file:
            print("Opened file successfully.")
            for line in file:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    try:
                        file_year = int(parts[0].strip())  # Convert year to int
                        url = parts[1].strip()            # Extract URL

                        # Debug: Show the mapping
                        print(f"DEBUG: Found mapping: {file_year} -> {url}")

                        # Save the 2020 URL for fallback
                        if file_year == 2020:
                            url_2020 = url
                            print("DEBUG: Saved 2020 URL for fallback.")

                        # Return URL if it matches the exact year
                        if file_year == year:
                            print(f"DEBUG: Found URL for year {year}: {url}")
                            return url

                    except ValueError:
                        print(f"DEBUG: Skipping invalid entry in file: {line.strip()}")
                        continue
        
        # If year > 2020, return the 2020 URL
        if year > 2020 and url_2020:
            print(f"DEBUG: Year {year} is greater than 2020. Using 2020 URL as fallback.")
            return url_2020

        # Debug: No matching URL found
        print(f"DEBUG: No URL found for year {year}, and no fallback available.")
        return None

    except FileNotFoundError:
        print(f"Error: File not found at {dict_path_file}")
        return None
    except ValueError as ve:
        print("Error: Invalid year format. Ensure the input year is a valid integer.")
        print(f"DEBUG: ValueError - {ve}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"DEBUG: Exception - {e}")
        return None




def download_worldpop_data(url, save_folder=None):
    """
    Download a file from a given URL and save it to a specified or default folder.

    Args:
        url (str): The URL of the file to be downloaded.
        save_folder (str or None): The folder path where the file should be saved. 
                                   Defaults to "Data/External/Population/<filename.tif>" relative to the project root.

    Returns:
        str: The full path to the downloaded file.
    """
    try:
        # Extract the filename from the URL
        filename = url.split('/')[-1]

        # Determine the save folder
        if save_folder is None:
            # Map the default location programmatically
            project_root = Path(__file__).resolve().parent.parent
            save_folder = project_root / 'Data' / 'External' / 'Population'

        # Ensure the save folder exists
        os.makedirs(save_folder, exist_ok=True)

        # Construct the full save path
        save_path = os.path.join(save_folder, filename)

        # Download the file
        print("Downloading WorldPop population data...")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad responses

        # Save the file in chunks
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

        print(f"File downloaded successfully to: {save_path}")
        return save_path

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during download: {e}")
        return None
