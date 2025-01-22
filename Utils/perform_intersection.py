import geopandas as gpd
import os

def intersect(gdf2):
    """
    Perform the intersection of two GeoDataFrames using a dynamically constructed path.

    Args:
        gdf2 (GeoDataFrame): The second GeoDataFrame.

    Returns:
        GeoDataFrame: The resulting GeoDataFrame after performing the intersection.
    """
    try:
        # Dynamically construct the path to extent_shapefile directory
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the current script
        base_dir = os.path.abspath(os.path.join(script_dir, "../"))  # Navigate to FEWSnet root
        shapefile_path = os.path.join(base_dir, "Data/Processed/extent_shapefile/pg_viewser_extent.shp")
        
        # Load the first GeoDataFrame
        gdf1 = gpd.read_file(shapefile_path)
        
        # Perform the intersection
        intersected_gdf = gpd.overlay(gdf1, gdf2, how='intersection')
        
        # Reset the index of the resulting GeoDataFrame
        intersected_gdf.reset_index(drop=True, inplace=True)
        
        return intersected_gdf
    except Exception as e:
        print(f"An error occurred during the intersection: {e}")
        return None