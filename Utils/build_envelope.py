import geopandas as gpd
from shapely.geometry import box

def envelope_buffer(intersected_gdf, distance=25000):
    """
    Generate a buffered bounding box (envelope) for the entire extent of a GeoDataFrame.

    Args:
        intersected_gdf (GeoDataFrame): The input GeoDataFrame whose spatial extent will be used to calculate the envelope.
        distance (float, optional): The buffer distance to apply around the envelope in meters.
                                    Defaults to 25000 (25 km).

    Returns:
        GeoDataFrame: A GeoDataFrame containing a single polygon representing the buffered envelope of the input GeoDataFrame.

    Description:
        This function calculates the bounding box (envelope) of the input GeoDataFrame, ensures the CRS is in a projected
        system with meters as units, applies a buffer around the envelope, and returns the buffered result.

    Example:
        ```python
        import geopandas as gpd
        from shapely.geometry import Point

        # Create a sample GeoDataFrame
        data = {'geometry': [Point(0, 0), Point(10, 10), Point(20, 20)]}
        gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")  # WGS 84

        # Generate the buffered envelope
        buffered_envelope = envelope_buffer(gdf, distance=5000)

        print(buffered_envelope)
        ```
    """
    # Ensure the GeoDataFrame is in a projected CRS
    if intersected_gdf.crs.is_geographic:
        print("Reprojecting GeoDataFrame to a projected CRS (UTM).")
        intersected_gdf = intersected_gdf.to_crs(intersected_gdf.estimate_utm_crs())

    # Generate the envelope (bounding box) for the entire GeoDataFrame
    envelope = intersected_gdf.total_bounds  # Returns (minx, miny, maxx, maxy)

    # Create a GeoDataFrame containing the envelope as a polygon
    envelope_gdf = gpd.GeoDataFrame(geometry=[box(*envelope)], crs=intersected_gdf.crs)

    # Add a buffer to the envelope
    envelope_gdf['geometry'] = envelope_gdf.geometry.buffer(distance)

    return envelope_gdf
