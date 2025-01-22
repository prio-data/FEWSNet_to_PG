import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from viewser import Queryset, Column
import pandas as pd

from ingester3.extensions import *

# Step 7: Plot the results
def plot_results(icp_country_result, plotted_attribute='present'):
    """
    Plot the GeoDataFrame based on the selected attribute ('present' or 'count').

    Args:
        icp_country_result (GeoDataFrame): The GeoDataFrame containing the data.
        plotted_attribute (str): The attribute to plot ('present' or 'count').
    """


    fig, ax = plt.subplots(figsize=(8, 8))
    
    if plotted_attribute == 'present':
        # Plot 'present' with black and white mapping
        icp_country_result.plot(
            ax=ax,
            color=icp_country_result["present"].map({1: "black", 0: "white"}),
            edgecolor=None
        )
        ax.set_title("Reporting Dates Availability", fontsize=14)
    elif plotted_attribute == 'count':
        # Plot 'count' as a continuous scale
        icp_country_result.plot(
            ax=ax,
            column="count",
            cmap="viridis",  # Choose a colormap
            legend=True,     # Add a legend for the scale
            edgecolor=None
        )
        ax.set_title("Number of Reporting Dates per Country", fontsize=14)
    else:
        print(f"Invalid plotted_attribute: {plotted_attribute}. Choose 'present' or 'count'.")
        return

    # Show the plot
    plt.show()

def plot_fewsnet_scenario_coverage(
    ipc,
    target_year=2023,
    plotted_attribute = 'count', # this could also be 'present'
    shapefile_path="Data/Processed/extent_shapefile/pg_viewser_extent.shp"
):
    """
    Analyze and visualize the time and space availability of FEWSNET data for each classification.
    
    Args:
        ipc_start_date (str): Start date for IPC data retrieval.
        ipc_end_date (str): End date for IPC data retrieval.
        target_year (int): Year to filter the PG data.
        shapefile_path (str): Path to the shapefile containing PG and geometry attributes.
    
    Returns:
        GeoDataFrame: Merged GeoDataFrame with the analysis results.
    """

    # Prompt the user to decide whether to run the function
    user_input = input("Do you want to generate an IPC completeness graphic? (yes/no): ").strip().lower()

    if user_input not in ['yes', 'y']:
        print("Skipping IPC completeness graphic generation.")
        return

    print("Generating IPC completeness graphic...")

    # Step 1: Retrieve IPC data
    filtered_df = ipc[ipc['scenario_name'] == 'Current Situation']  # Filter by 'Current Situation'

    # Step 2: Group by country and aggregate reporting dates
    result = (
        filtered_df.groupby('country', group_keys=False)['reporting_date']
        .apply(list)
        .reset_index()
    )
    result.columns = ['country', 'reporting_dates']  # Rename columns

    # Step 3: Load and prepare PG structure
    queryset_base_PG = Queryset('Fatalities_fao_pgm', '')  # Replace with actual implementation
    df = queryset_base_PG.fetch().reset_index()
    df['year'] = df.m.year  # Extract year
    dflim = df[['priogrid_gid', 'year', 'country_name']].drop_duplicates()  # Filter fields
    dflim_year = dflim[dflim['year'] == target_year]  # Filter by target year

    # Step 4: Load shapefile and merge with PG data
    gdf = gpd.read_file(shapefile_path)  # Load shapefile
    merged_data = gdf.merge(dflim_year, left_on='pg_id', right_on='priogrid_gid', how='inner')

    # Step 5: Merge IPC data with spatial data
    icp_country_result = merged_data.merge(result, left_on='country_name', right_on='country', how='left')

    # Step 6: Add 'present' column
    icp_country_result['present'] = icp_country_result['reporting_dates'].notnull().astype(int)
    
    # Step 7: Ensure 'reporting_dates' contains only unique values
    icp_country_result['reporting_dates'] = icp_country_result['reporting_dates'].apply(
        lambda x: list(set(x)) if isinstance(x, list) else x
    )

    # Step 8: Add 'count' column
    # Count the number of unique elements in the cleaned 'reporting_dates'
    icp_country_result['count'] = icp_country_result['reporting_dates'].apply(
        lambda x: len(x) if isinstance(x, list) else 0
    )
    plot_results(icp_country_result, plotted_attribute)  # Replace 'count' with 'present' as needed

    # Return the final GeoDataFrame
    return icp_country_result
