import os 
from pathlib import Path
import geopandas as gpd

def rejoin_to_pg(result_df):
    
    project_root = Path(__file__).resolve().parent.parent

    #--------------------------------------
    # Location to save geodataframe (as shapefile)
    #--------------------------------------

    ref_shapefile_path = project_root / 'Data' / 'Processed' / 'extent_shapefile' 
    os.makedirs(ref_shapefile_path, exist_ok=True)


    gdf = gpd.read_file(f"{ref_shapefile_path}/pg_viewser_extent.shp")


    # Merge the shapefile GeoDataFrame with the `result` DataFrame on the `pg_id` column
    merged_gdf = gdf.merge(result_df, on='pg_id', how='inner')
    return(merged_gdf)



