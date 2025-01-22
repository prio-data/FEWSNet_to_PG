
def desirable_attributes(ipc_data, spatial_boundaries):
    # Subset desirable fields from gdf__fscunits
    gdf_fscunits_attributes = spatial_boundaries[['fnid', 'geometry']]

    # Subset desirable fields from subset_df
    subset_IPC_attributes = ipc_data[['fnid', 'scenario_name', 'value', 'reporting_date']]

    return(subset_IPC_attributes, gdf_fscunits_attributes)

    # Display the first few rows to verify
    print("gdf__fscunits subset:")
    print(gdf_fscunits_attributes.head())

    print("\nsubset_df subset:")
    print(subset_IPC_attributes.head())