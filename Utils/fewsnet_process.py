import geopandas as gpd
import pandas as pd
from pathlib import Path

from Utils.api_ipc_request import construct_ipc_api_url
from Utils.api_boundary_request import construct_boundary_api_url
from Utils.temporal_coverage import plot_fewsnet_scenario_coverage
from Utils.countries_to_process import select_country_codes
from Utils.check_shapefile import pg_shapefile_exists
from Utils.input_base_requirements import get_date_range, select_ipc_classification

# Feature Engineering
from Utils.filter_tables import desirable_attributes
from Utils.merge_and_report import merge_ipc_with_boundaries, evaluate_merge_completness
from Utils.scenario import define_scenario

# Plot
from Utils.plot_ipc_orig_boundaries import plot_historical_ipc

# Load PG
from Utils.give_PG_reference import provide_reference_frame


#Compute area features
from Utils.area_attributes import define_area_attributes


#Perform Intersection
from Utils.perform_intersection import intersect
from Utils.build_envelope import envelope_buffer


#Define process to conver FEWSNET to PG
from Utils.select_process import define_process
from Utils.user_process_selection import get_process_selection


#Rejoin data to PG shapefile (GPD)
from Utils.rejoin_pg_data import rejoin_to_pg

from Utils.cumulative_population_attribution import engineer_population_attributes
from Utils.pg_country_extent import create_country_geodataframe
from Utils.leftjoin_to_pg_country import left_join_geodataframes
from Utils.select_dates import get_dates_to_process

# Save the data
from Utils.csv_naming_conventions import apply_naming_convention

def run_fewsnet_processing_workflow(path):
    """
    Execute the full workflow for processing FEWSNET data, including IPC classifications, 
    country-level processing, and final results aggregation.
    """
    path = Path(path)


    if pg_shapefile_exists():
        print("The PG reference shapefile has already been produced!")
    else:
        print(
        "The PG Shapefile does not exist. This process must be completed before integrating FEWSNET data.\n"
        "I will produce and save the PG reference file now. Once complete, it can be accessed in Data/Processed/extent_shapefile/"
        )
        
        provide_reference_frame()

    ipc_classification = select_ipc_classification()
    s, e = get_date_range()
    ipc = construct_ipc_api_url(s, e, ipc_classification)
    print(list(ipc))
    #Print all country_codes:
    #country_code_list = sorted(ipc['country_code'].unique().tolist())

    ipc_country, selected_country_codes = select_country_codes(ipc)

    endyear = e.split('-')[0]

    icp_country_result = plot_fewsnet_scenario_coverage(ipc, endyear)

    process_selection = get_process_selection()

    all_country_results = []

    for country_code in selected_country_codes:

        # identify country associated with country code:

        country_name = ipc.loc[ipc['country_code'] == country_code, 'country'].iloc[0]

        print(f"Processing country: {country_code} ({country_name})")

        boundaries = construct_boundary_api_url(country_code)

        ipc_filtered, spatial_filtered = desirable_attributes(ipc_country, boundaries)

        merge, unmatched = merge_ipc_with_boundaries(ipc_filtered, spatial_filtered)

        evaluate_merge_completness(merge, ipc_filtered, unmatched)

        scenario = define_scenario(merge)

        merged_df_current = gpd.GeoDataFrame(scenario, geometry='geometry')

        plot_historical_ipc(merged_df_current)

        result_dfs = []

        # Get unique dates from the dataset
        dataset_dates = sorted(merged_df_current['reporting_date'].unique().tolist())
        print(dataset_dates)

        dates_to_process = get_dates_to_process(dataset_dates)

        # Loop through each date in the dataset_dates
        for i, processing_date in enumerate(dates_to_process):  # Enumerate gives both index and value
            print()
            print(f"Processing date: {processing_date}")
            print()

            # Extract the year from the current processing date
            year = processing_date.split('-')[0]
            year_int = int(processing_date.split('-')[0])

            # Filter the dataset for the current date
            merged_df_current_lim = merged_df_current[merged_df_current['reporting_date'] == processing_date]

            # Generate a buffered envelope for the filtered dataset
            envelope_gdf_buffered = envelope_buffer(merged_df_current_lim, distance=25000)

            # Ensure only valid geometry types
            merged_df_current_lim = merged_df_current_lim[merged_df_current_lim.geom_type.isin(['Polygon', 'MultiPolygon'])]

            # Perform the intersection
            intersected_gdf = intersect(merged_df_current_lim)

            # Ensure area attributes are defined
            intersected_gdf = define_area_attributes(intersected_gdf)

            # Check if the selected process requires population data
            if process_selection in [5, 6]:
                intersected_gdf = engineer_population_attributes(year, country_code, intersected_gdf, envelope_gdf_buffered)

            # Define the process and generate the result
            result = define_process(process_selection, intersected_gdf)

            # Rejoin the result to the priogrid
            # Applies the data frame containing a pg attribute to the spatial pg extent
            result_gdf = rejoin_to_pg(result)
            
            # Add processing_date and country_code fields to result_gdf
            result_gdf['processing_date'] = processing_date
            result_gdf['country_code'] = country_code

            # Trim results to PG (viewser defined) country extent
            gpd_country_extent_df = create_country_geodataframe(country_name, year_int, shapefile_path=None)
            
            print()

            country_joined=left_join_geodataframes(gpd_country_extent_df, result_gdf)

            # Append the result_gdf to the list
            result_dfs.append(country_joined)

            print(f"Completed processing for {processing_date}. Result saved.")

        # Concatenate the results for the current country
        country_result_df = pd.concat(result_dfs, ignore_index=True)

        # Rename and drop columns
        # Check if 'final_weighted_value' exists before renaming
        if 'final_weighted_value' in country_result_df.columns:
            country_result_df = country_result_df.rename(columns={'final_weighted_value': 'IPC_value'})

        # Check if 'original_sum_value' exists before dropping
        if 'original_sum_value' in country_result_df.columns:
            country_result_df = country_result_df.drop(columns=['original_sum_value'])


        # Append to the all-country results list
        all_country_results.append(country_result_df)

    # Concatenate results for all countries
    final_result_df = pd.concat(all_country_results, ignore_index=True)

    # Naming Conventions:
    naming_conventions = apply_naming_convention(dates_to_process, selected_country_codes, process_selection)

    csv_path_with_naming = path.with_name(path.name + naming_conventions + '.csv')

    # The final_result_df now contains data for all countries and dates
    final_result_df.to_csv(csv_path_with_naming)
    return(final_result_df)