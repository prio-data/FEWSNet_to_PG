import geopandas as gpd
import rasterio
from rasterio.mask import mask
from pathlib import Path
import os

def clip_and_save_geotiff(tiff_path, envelope_gdf, country_code, year, save_folder=None):
    """
    Clips a GeoTIFF using a buffered envelope and saves the clipped raster to a structured folder.

    Args:
        tiff_path (str): Path to the input GeoTIFF file.
        envelope_gdf (GeoDataFrame): A GeoDataFrame containing the buffered envelope geometry.
        country_code (str): The country code to use for folder and file naming.
        year (int or str): The year to include in the filename.
        save_folder (str or None): The base folder path where files are stored. If None, defaults to 
                                   "Data/External/Population/<country_code>".

    Returns:
        str: Path to the saved clipped GeoTIFF file.
    """
    try:
        # Determine the save folder
        if save_folder is None:
            # Map the default location programmatically
            project_root = Path(__file__).resolve().parent.parent
            save_folder = project_root / 'Data' / 'External' / 'Population' / 'country_extent' / country_code

        # Ensure the folder exists
        os.makedirs(save_folder, exist_ok=True)

        # Construct the filename and save path
        filename = f"{country_code}_{year}.tif"
        output_tiff_path = save_folder / filename

        # Open the GeoTIFF
        with rasterio.open(tiff_path) as src:
            # Ensure the buffered envelope is in the same CRS as the raster
            if envelope_gdf.crs != src.crs:
                print("Reprojecting envelope GeoDataFrame to match raster CRS.")
                envelope_gdf = envelope_gdf.to_crs(src.crs)

            # Convert the geometry of the buffered envelope to GeoJSON format
            envelope_geometry = [feature["geometry"] for feature in envelope_gdf.__geo_interface__["features"]]

            # Clip the raster using the envelope geometry
            clipped_data, clipped_transform = mask(src, envelope_geometry, crop=True)

            # Update the metadata for the clipped raster
            clipped_meta = src.meta.copy()
            clipped_meta.update({
                "driver": "GTiff",
                "height": clipped_data.shape[1],
                "width": clipped_data.shape[2],
                "transform": clipped_transform
            })

            # Write the clipped raster to the specified location
            with rasterio.open(output_tiff_path, "w", **clipped_meta) as dst:
                dst.write(clipped_data)

        print(f"Clipped raster saved to: {output_tiff_path}")
        return str(output_tiff_path)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
