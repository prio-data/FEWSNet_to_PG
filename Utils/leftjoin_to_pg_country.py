import geopandas as gpd

def left_join_geodataframes(df1, df2, join_column="pg_id"):
    """
    Perform a left join between two GeoDataFrames based on a shared column.
    Retain the geometry column from df1 and ensure the result is a valid GeoDataFrame.

    Args:
        df1 (gpd.GeoDataFrame): The left GeoDataFrame.
        df2 (gpd.GeoDataFrame): The right GeoDataFrame.
        join_column (str): The column to join on. Defaults to 'pg_id'.

    Returns:
        gpd.GeoDataFrame: The resulting GeoDataFrame after the left join.
    """
    # Drop the geometry column from df2 to avoid conflicts
    df2_no_geometry = df2.drop(columns=['geometry'], errors='ignore')

    # Perform the left join
    merged_df = df1.merge(df2_no_geometry, on=join_column, how="left")

    # Ensure the result is a GeoDataFrame with the geometry from df1
    merged_gdf = gpd.GeoDataFrame(merged_df, geometry=df1.geometry.name, crs=df1.crs)

    return merged_gdf

