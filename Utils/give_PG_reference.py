import pandas as pd
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
import os 


# Define the function to create a 0.5x0.5 degree grid cell around a center point
def create_grid_cell(lat, lon, cell_size=0.5):
    half_size = cell_size / 2
    # Define the corners of the grid cell
    return Polygon([
        (lon - half_size, lat - half_size),  # Bottom-left
        (lon + half_size, lat - half_size),  # Bottom-right
        (lon + half_size, lat + half_size),  # Top-right
        (lon - half_size, lat + half_size),  # Top-left
        (lon - half_size, lat - half_size)   # Close the polygon
    ])

from ingester3.extensions import *

def provide_reference_frame():

    project_root = Path(__file__).resolve().parent.parent

    #--------------------------------------
    # Location to save geodataframe (as shapefile)
    #--------------------------------------

    ref_shapefile_path = project_root / 'Data' / 'Processed' / 'extent_shapefile' 
    os.makedirs(ref_shapefile_path, exist_ok=True)

    # ------------------------
    # Construct PG scaffolder
    # ------------------------

    #add a print() line when building the scaffolders as this may take several minutes
    print()
    print('Generating empty PG shapefile saved to \FEWSNET\Data\Processed\extent_shapefile.')
    print('This is expected to take several minutes...')
    print()
    
    pg = pd.DataFrame.pg.new_structure()

    pg['lat'] = pg.pg.lat
    pg['long'] = pg.pg.lon

    geometry = pg.apply(lambda row: create_grid_cell(row['lat'], row['long']), axis=1)
    gdf = gpd.GeoDataFrame(pg, geometry=geometry, crs="EPSG:4326")
    # ------------------------
    # WHY DO DO FOLLOW THIS ORDER:
    # apply lat and long first 
    gdf.to_file(f"{ref_shapefile_path}/pg_viewser_extent.shp")  # Save as a shapefile if needed
    # ------------------------
# Ensure this runs only when executed directly, not when imported
if __name__ == "__main__":
    process_selection = provide_reference_frame()
    print(f"You selected process: {process_selection}")
# ----------------------------------------------------------------------------------------------------

