import requests
import pandas as pd
from pathlib import Path

def construct_ipc_api_url(start_date, end_date, classification='IPC31'):
    # Base URL
    base_url = "https://fdw.fews.net/api/ipcphase.csv"

    project_root = Path(__file__).resolve().parent.parent

    #--------------------------------------
    # Location to save geodataframe (as shapefile)
    #--------------------------------------

    ref_ipc_csv_path = project_root / 'Data' / 'External' / 'IPC' 

    # Parameters
    params = {
        "start_date": start_date, # Specify in prompt (text) that the format must follow YYYY-MM-DD format
        "end_date": end_date, # Specify in prompt (text) that the format must follow YYYY-MM-DD format
        "classification_scale": classification # Specify that is default (for this purpose the parameter should not be changed)
    }

    # Construct the URL manually to maintain the structure
    url_csv = f"{base_url}?start_date={params['start_date']}&end_date={params['end_date']}&classification_scale={params['classification_scale']}"
    print(f'The API call constructed: {url_csv}')
    print()
    print("Data downloaded and saved as ipc_data.csv to folder Data/Generated/ipc_data.csv")
    print()
    response = requests.get(url_csv, params=params)
    with open(f"{ref_ipc_csv_path}/IPC_data.shp", "wb") as file:
        file.write(response.content)

    ipc_data = pd.read_csv(f"{ref_ipc_csv_path}/IPC_data.shp")
    return(ipc_data)

