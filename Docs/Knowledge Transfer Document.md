# Steps:

## Phase 1:
- complete at merged_df_current. This can be reviewed in Ethiopia_pilot.ipynb

## Phase 2:
- iterate through the collection dates of the specified country

- intersect the merged data (which merges the IPC food classification with the spatial boundary) to the PG units
```
intersected_gdf = gpd.overlay(gdf1, gdf2, how='intersection')

```
### Measurement by *Area*

- Ensure the GeoDataFrame has a projected CRS for accurate area calculations
- Compute area based statistics (reference: define_area_params.py)
```
# Calculate the area and store it in a new attribute 'area_sq_km'
intersected_gdf['Feature_area_sq_km'] = intersected_gdf.geometry.area / 1e6  # Convert from square meters to square kilometers

# Group by 'pg_id' and calculate the sum of areas for each group
cell_area = intersected_gdf.groupby('pg_id')['Feature_area_sq_km'].sum().reset_index()

# Rename the area column to 'Cell_Area'
cell_area.rename(columns={'Feature_area_sq_km': 'Cell_Area'}, inplace=True)

# Merge the 'Cell_Area' back into the original GeoDataFrame
intersected_gdf = intersected_gdf.merge(cell_area, on='pg_id')
```

- Calculate Proportion_area: feature_area / cell_area
```
intersected_gdf['Proportion_area'] = intersected_gdf['Feature_area_sq_km'] / intersected_gdf['Cell_Area']
```

- Create a new GeoDataFrame with the specified fields in order
```
final_gdf = intersected_gdf[[
    'feature_id',          # Unique feature ID
    'fnid',                # Admin unit description
    'pg_id',               # Unique priogrid ID
    'Feature_area_sq_km',  # Area of each individual feature
    'Cell_Area',           # Area of the entire PG cell
    'Proportion_area',     # Feature area / cell area
    'geometry'             # Spatial attribute to map the data
]]
```

- establish rules for assinging value to pg_id

1. Proportioanl AREA:
```
# Step 1: Calculate the weighted value for each row
df['weighted_value'] = df['value'] * df['Proportion_area']

# Step 2: Group by pg_id and sum the weighted values
dissolved_df = df.groupby('pg_id', as_index=True)['weighted_value'].sum().reset_index()

# Step 3: Rename the column for clarity
dissolved_df.rename(columns={'weighted_value': 'dissolved_value'}, inplace=True)
```

2. Maximum Value Above a Threshold

Description: Assign the maximum value if its Proportional_area exceeds a specified threshold (e.g., 20%).
Purpose: Prioritizes rare but significant values when they meet the area threshold.

3. Combined Threshold Rules

Description: Combine multiple rules into a hierarchical decision-making process:
If a value meets both a proportional threshold (e.g., 30%) and a critical threshold (e.g., value > 3), assign it.
Otherwise, assign based on a fallback rule like majority overlap or maximum value.
Purpose: Provides flexibility by considering multiple factors in a structured way.

4. Majority Overlap (Mode)

Description: Assign the value that occupies the largest proportion of the area (highest Proportional_area).
Purpose: Identifies the dominant value in terms of spatial coverage.


5. Spatial Clustering -- unlikely to incorporate

Description: Use spatial contiguity to refine the assignment. For example, assign the dominant value in contiguous sub-areas within a pg_id.
Purpose: Useful for reducing noise from small, fragmented areas with different values.

### Measurement by *Population*

- Access population data (reference: get_population_data_url) this should match the collection date (year) that is currently being run

- Generate the envelope (bounding box) from the GeoDataFrame (reference: build_envelope.py)

# Calculate Proportion_population: feature_population / cell_population
intersected_gdf['Proportion_population'] = intersected_gdf['feature_population'] / intersected_gdf['Cell_population']



