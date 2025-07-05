import cdsapi
import xarray as xr
import pandas as pd
import json

# Télécharger en NetCDF
c = cdsapi.Client()
c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': '2m_temperature',
        'year': '2024',
        'month': '01',
        'day': '01',
        'time': '12:00',
        'area': [11.75, -0.80, 11.19, -0.30],
    },
    'test_output.nc'
)

# Convertir vers JSON/TXT
ds = xr.open_dataset('test_output.nc')

# Conversion vers JSON
data_dict = ds.to_dict()
with open('test_output.json', 'w') as f:
    json.dump(data_dict, f, indent=2, default=str)

# Conversion vers CSV/TXT
df = ds.to_dataframe().reset_index()
df.to_csv('test_output.csv', index=False)
df.to_csv('test_output.txt', index=False, sep='\t')

print("Fichiers créés : test_output.nc, test_output.json, test_output.csv, test_output.txt")