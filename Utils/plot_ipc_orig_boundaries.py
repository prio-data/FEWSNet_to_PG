# import geopandas as gpd
# import matplotlib.pyplot as plt

# def plot_historical_ipc(merged_df_current):

#     dataset_dates = sorted(merged_df_current['reporting_date'].unique().tolist())

#     # Ensure 'reporting_date' is in string format in the GeoDataFrame
#     merged_df_current['reporting_date'] = merged_df_current['reporting_date'].astype(str)

#     # Iterate over the dates and plot
#     for date in dataset_dates:
#         # Filter the GeoDataFrame for the current date
#         gdf_filtered = merged_df_current[merged_df_current['reporting_date'] == date]
        
#         # Plot the geometry with values
#         ax = gdf_filtered.plot(
#             column='value',     # Column to visualize
#             cmap='viridis',     # Color map
#             legend=True,        # Add a legend
#             figsize=(10, 6),    # Figure size
#         )
        
#         # Add title and labels
#         ax.set_title(f"Visualization for {date}", fontsize=16)
#         ax.set_xlabel("Longitude")
#         ax.set_ylabel("Latitude")
        
#         # Show the plot
#         plt.show()

import matplotlib.pyplot as plt
import geopandas as gpd

def plot_historical_ipc(merged_df_current):
    """
    Plot IPC data for historical reporting dates, allowing user input to run the function
    and coalescing all maps into a single graphic.

    Args:
        merged_df_current (GeoDataFrame): The input GeoDataFrame containing IPC data with
                                          'reporting_date' and 'value' columns.
    """
    # Prompt the user to decide whether to run the function
    user_input = input("Do you want to generate IPC historical maps? (yes/no): ").strip().lower()

    if user_input not in ['yes', 'y']:
        print("Skipping IPC historical maps generation.")
        return

    print("Generating IPC historical maps...")

    # Ensure 'reporting_date' is in string format in the GeoDataFrame
    merged_df_current['reporting_date'] = merged_df_current['reporting_date'].astype(str)

    # Get sorted unique reporting dates
    dataset_dates = sorted(merged_df_current['reporting_date'].unique().tolist())

    # Initialize a matplotlib figure with subplots
    num_dates = len(dataset_dates)
    ncols = 3  # Number of columns in the subplot grid
    nrows = (num_dates + ncols - 1) // ncols  # Calculate the required rows
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 5 * nrows))
    axes = axes.flatten()  # Flatten the axes array for easier indexing

    # Iterate over the dates and plot
    for idx, date in enumerate(dataset_dates):
        # Filter the GeoDataFrame for the current date
        gdf_filtered = merged_df_current[merged_df_current['reporting_date'] == date]

        # Plot the data on the corresponding subplot
        ax = gdf_filtered.plot(
            column='value',     # Column to visualize
            cmap='viridis',     # Color map
            legend=True,        # Add a legend
            ax=axes[idx],       # Use the corresponding subplot axis
        )

        # Add title and labels to each subplot
        ax.set_title(f"{date}", fontsize=10)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

    # Hide any unused subplots
    for idx in range(len(dataset_dates), len(axes)):
        axes[idx].axis('off')

    # Set the main title for the figure
    fig.suptitle("IPC Historical Maps", fontsize=16, y=0.92)

    # Adjust layout
    plt.tight_layout()

    # Show the coalesced plot
    plt.show()
