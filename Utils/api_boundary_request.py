import requests
import geopandas as gpd
from io import BytesIO




def construct_boundary_api_url(country_code):
    """
    Constructs the FEWS NET API URL for features with the given country code.

    Args:
        country_code (str): The country code to include in the API request.

    Returns:
        str: The constructed API URL.
    """
    base_url = "https://fdw.fews.net/api/feature/"
    url = (
        f"{base_url}?format=geojson&fields=with_attributes&country_code={country_code}"
        "&unit_type=idp_camp&unit_type=livelihood_zone&unit_type=national_park"
        "&unit_type=fsc_admin&unit_type=fsc_admin_lhz&unit_type=fsc_lhz&unit_type=fsc_rm_admin"
    )

    # URL of the GeoJSON file
    # Fetch the GeoJSON file
    response = requests.get(url)

    if response.status_code == 200:
        # Load the GeoJSON into a GeoPandas DataFrame
        gdf__fscunits = gpd.read_file(BytesIO(response.content))
        print(f'The API call constructed: {url}')
        print()
        print("Data downloaded and saved as ipc_data.csv to folder Data/Generated/ipc_data.csv")
        print()
        return(gdf__fscunits)
    else:
        print(f"Failed to fetch data: {response.status_code}")



    #unique_countries = sorted(gdf__fscunits['country_code'].unique().tolist())
    #unique_countries