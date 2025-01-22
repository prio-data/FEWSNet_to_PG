def define_area_attributes(intersected_gdf):

    #-----------------------------------------------------------------------
    # Ensure the GeoDataFrame has a projected CRS for accurate area calculations
    if not intersected_gdf.crs.is_projected:
        intersected_gdf = intersected_gdf.to_crs(epsg=3857)
    #-----------------------------------------------------------------------

    # Calculate the area and store it in a new attribute 'area_sq_km'
    intersected_gdf['Feature_area_sq_km'] = intersected_gdf.geometry.area / 1e6  # Convert from square meters to square kilometers

    # Group by 'pg_id' and calculate the sum of areas for each group
    cell_area = intersected_gdf.groupby('pg_id')['Feature_area_sq_km'].sum().reset_index()

    # Rename the area column to 'Cell_Area'
    cell_area.rename(columns={'Feature_area_sq_km': 'Cell_Area'}, inplace=True)

    # Merge the 'Cell_Area' back into the original GeoDataFrame
    intersected_gdf = intersected_gdf.merge(cell_area, on='pg_id')

    intersected_gdf['Proportional_area'] = intersected_gdf['Feature_area_sq_km'] / intersected_gdf['Cell_Area']


    if intersected_gdf.crs != "EPSG:4326":
        intersected_gdf = intersected_gdf.to_crs("EPSG:4326") 

    return(intersected_gdf)