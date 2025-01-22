import rasterio
from rasterio.mask import mask
import numpy as np

def calculate_feature_population(clipped_path, intersected_gdf):
    """
    Calculate the population sum for each feature in a GeoDataFrame using a clipped population raster.

    Args:
        clipped_path (str): Path to the clipped population raster file.
        intersected_gdf (GeoDataFrame): A GeoDataFrame containing geometries to intersect with the raster.

    Returns:
        GeoDataFrame: The updated GeoDataFrame with 'feature_id' and 'feature_population' columns.
    """
    try:
        # Create a new column in intersected_gdf to store the population sum
        intersected_gdf['feature_population'] = 0

        # Add a unique 'feature_id' column based on the index
        intersected_gdf['feature_id'] = intersected_gdf.index

        # Open the clipped population raster
        with rasterio.open(clipped_path) as src:
            # Iterate through each feature in the GeoDataFrame
            for idx, row in intersected_gdf.iterrows():
                # Get the geometry of the current feature
                geom = [row['geometry']]

                try:
                    # Mask the raster with the feature's geometry
                    out_image, out_transform = mask(src, geom, crop=True)
                    
                    # Flatten the masked raster and remove NoData values
                    out_image = out_image[0]  # Assuming a single band raster
                    out_image = out_image[out_image != src.nodata]
                    
                    # Sum the population values and assign to the GeoDataFrame
                    population_sum = np.sum(out_image)
                    intersected_gdf.at[idx, 'feature_population'] = population_sum

                except Exception as e:
                    # Handle any errors (e.g., empty geometries or mask issues)
                    print(f"Error processing feature {idx}: {e}")

        print("Population calculation completed successfully.")
        return intersected_gdf

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def aggregate_population_to_pg(intersected_gdf):
    """
    Group by 'pg_id', calculate the sum of population for each group,
    and merge the aggregated population back into the original GeoDataFrame.

    Args:
        intersected_gdf (GeoDataFrame): GeoDataFrame containing 'pg_id' and 'feature_population' columns.

    Returns:
        GeoDataFrame: Updated GeoDataFrame with a new 'Cell_population' column.
    """
    try:
        # Step 1: Group by 'pg_id' and sum the population for each group
        cell_population = intersected_gdf.groupby('pg_id')['feature_population'].sum().reset_index()

        # Step 2: Rename the column to 'Cell_population'
        cell_population.rename(columns={'feature_population': 'Cell_population'}, inplace=True)

        # Step 3: Merge the 'Cell_population' back into the original GeoDataFrame
        population_at_id_and_level = intersected_gdf.merge(cell_population, on='pg_id')

        print("Population aggregation and merging completed successfully.")
        return population_at_id_and_level

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

