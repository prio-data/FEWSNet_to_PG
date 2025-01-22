import os
from pathlib import Path

def pg_shapefile_exists(folder_path=None, shapefile_name = 'pg_viewser_extent.shp'):
    """
    Check if a specific shapefile exists in a given folder, with a default programmatically generated path.

    Args:
        shapefile_name (str): The name of the shapefile (e.g., 'example.shp').
        folder_path (str, optional): The path to the folder to check. If None, a default folder path is used.

    Returns:
        bool: True if the shapefile exists, False otherwise.
    """
    # Set the default folder path if none is provided
    if folder_path is None:
        project_root = Path(__file__).resolve().parent.parent
        folder_path = project_root / 'Data' / 'Processed' / 'extent_shapefile'

    # Construct the full path to the shapefile
    shapefile_path = os.path.join(folder_path, shapefile_name)

    # Check if the shapefile exists and return the result
    return os.path.exists(shapefile_path)