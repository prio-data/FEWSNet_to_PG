import pandas as pd
import geopandas as gpd
from pathlib import Path
from ingester3.extensions import *


def create_country_geodataframe(country_name, year, shapefile_path=None):
    """
    Create a GeoDataFrame for a specific country and year by merging data from priogrid and a reference shapefile.

    Args:
        country_name (str): The name of the country to filter.
        year (int): The year to filter.
        shapefile_path (str, optional): Path to the reference shapefile. Defaults to a constructed path.

    Returns:
        gpd.GeoDataFrame: A GeoDataFrame containing priogrid and geometry for the specified country and year.
    """
    try:
        # Construct the default shapefile path if none is provided
        if shapefile_path is None:
            project_root = Path(__file__).resolve().parent.parent
            shapefile_path = project_root / 'Data' / 'Processed' / 'extent_shapefile' / 'pg_viewser_extent.shp'

        # Load the shapefile
        print()
        print(f"Loading shapefile from: {shapefile_path}.")
        print(f'We will use this geodataframe to define an extent that matches global pg_ids to those located in {country_name}.')
        print()
        gpd_df = gpd.read_file(shapefile_path)

        # Generate priogrid data for Africa (up to max year)
        new_country_year = pd.DataFrame.cy.new_africa(max_year=year + 1)
        new_country_year['name'] = new_country_year.c.name

        # Get unique countries
        countries = sorted(pd.unique(new_country_year['name'].tolist()))
        print(f"Available countries: {countries}")

        # Filter the DataFrame for the specified country and year
        filtered_df = new_country_year[(new_country_year['name'] == country_name) & (new_country_year['year_id'] == year)]
        print(f"Filtered country information from viewser for {country_name} in year {year} and supplying a sample dataframe:\n{filtered_df}")
        print()
        # Get priogrid IDs
        filtered_df_pg = filtered_df.cy.pg_id

        # Merge priogrid IDs with the shapefile data
        merged_df = pd.merge(filtered_df_pg, gpd_df, on='pg_id', how='inner')

        # Convert to GeoDataFrame if 'geometry' column exists
        if 'geometry' in merged_df.columns:
            gdf = gpd.GeoDataFrame(merged_df, geometry=merged_df['geometry'])

            # Ensure CRS is set
            if gdf.crs is None:
                gdf.set_crs("EPSG:4326", inplace=True)  # Assuming WGS84 CRS (latitude/longitude)

            print("Conversion to GeoDataFrame successful!")
            print()
            return gdf
        else:
            raise ValueError("Error: 'geometry' column not found in the merged DataFrame.")

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Example usage
# if __name__ == "__main__":
    # country_name = "Ethiopia"
    # year = 2020
    # gdf = create_country_geodataframe(country_name, year)
    # if gdf is not None:
    #     print(gdf.head())
