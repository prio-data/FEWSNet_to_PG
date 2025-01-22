

def merge_ipc_with_boundaries(ipc, spatial_data):
    # Merge the DataFrames on 'fnid'
    merged_df = ipc.merge(spatial_data, on='fnid', how='left')

    # Check for unmatched 'fnid' in subset_df (primary DataFrame)
    unmatched_fnid = ipc[~ipc['fnid'].isin(merged_df['fnid'])]
    return(merged_df, unmatched_fnid)

def evaluate_merge_completness(merged_data, original_ipc, unmatched):
        # Calculate completeness
        total_fnid = len(original_ipc['fnid'].unique())
        matched_fnid = len(merged_data['fnid'].dropna().unique())
        unmatched_fnid_count = total_fnid - matched_fnid
        completeness_percentage = (matched_fnid / total_fnid) * 100

        # Display results
        print("Merged DataFrame:")
        print(merged_data.head(3))

        print("\nUnmatched FNIDs:")
        print(unmatched)

        print(f"\nCompleteness of the merge: {completeness_percentage:.2f}%")
        print(f"Unmatched FNID count: {unmatched_fnid_count}")