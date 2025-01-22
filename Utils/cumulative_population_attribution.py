from Utils.access_population_resource import get_population_data, download_worldpop_data, check_if_population_local, get_url_for_year
from Utils.process_geotiff import clip_and_save_geotiff

from Utils.calculate_population import calculate_feature_population, aggregate_population_to_pg

from Utils.build_envelope import envelope_buffer



# def engineer_population_attributes(year, country_code, intersected_gdf, envelope_gdf_buffered):



#     pop_identified = check_if_population_local(year)
#     print(pop_identified)
#     #else use functions to download the data
#     if pop_identified == False:

#         print(f'Population for {year} has not yet been downloaded...')
#         print()
#         print('Locating WorldPop API link...')
#         url = get_url_for_year(year)
#         download_worldpop_data(url)
#         print(url)

#     population_path=get_population_data(year)
#     print(population_path)
#     clipped_path = clip_and_save_geotiff(population_path, envelope_gdf_buffered, country_code, year)

#     #Process ID and PG level population data
#     population_at_id_level = calculate_feature_population(clipped_path, intersected_gdf)
#     population_at_id_and_pg_level = aggregate_population_to_pg(population_at_id_level)
#     # Calculate Proportion_population: feature_population / cell_population
#     population_at_id_and_pg_level['Proportion_population'] = population_at_id_and_pg_level['feature_population'] / population_at_id_and_pg_level['Cell_population']

#     return(population_at_id_and_pg_level)

def engineer_population_attributes(year, country_code, intersected_gdf, envelope_gdf_buffered):
    """
    Engineer population attributes for a given year, country, and intersected GeoDataFrame.

    Args:
        year (int or str): The year for which population data is required. Will be converted to an integer.
        country_code (str): The country code for the target data.
        intersected_gdf (GeoDataFrame): The GeoDataFrame with intersected data.
        envelope_gdf_buffered (GeoDataFrame): Buffered envelope GeoDataFrame.

    Returns:
        DataFrame: A DataFrame with population attributes aggregated to priogrid levels.
    """
    try:
        # Ensure year is an integer
        year = int(year)

        # Adjust year if it exceeds 2020
        if year > 2020:
            print("WorldPop data does not exceed 2020. "
                  "Incorporating population data from the most recent available year (2020).")
            year = 2020

        # Check if the population data for the adjusted year is available locally
        pop_identified = check_if_population_local(year)

        # If not available locally, download the data
        if not pop_identified:
            print(f"Population for {year} has not yet been downloaded...")
            print("Locating WorldPop API link...")
            url = get_url_for_year(year)
            print(f"Retrieved URL: {url}")

            if url:  # Ensure URL is not None
                download_worldpop_data(url)
                print(f"Downloaded WorldPop data!")
            else:
                print("Error: Failed to retrieve URL for the population data.")
                return None

        # Get the path to the population data and clip it using the buffered envelope
        population_path = get_population_data(year)
        print(f"Population data can be referenced in: {population_path}")
        clipped_path = clip_and_save_geotiff(population_path, envelope_gdf_buffered, country_code, year)

        # Process ID and priogrid-level population data
        population_at_id_level = calculate_feature_population(clipped_path, intersected_gdf)
        population_at_id_and_pg_level = aggregate_population_to_pg(population_at_id_level)

        # Calculate Proportion_population: feature_population / cell_population
        population_at_id_and_pg_level['Proportion_population'] = (
            population_at_id_and_pg_level['feature_population'] / population_at_id_and_pg_level['Cell_population']
        )

        return population_at_id_and_pg_level

    except ValueError:
        print("Error: The 'year' parameter must be a valid integer or a string representing an integer.")
        return None
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


