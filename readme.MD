# Guide complet pour télécharger des données ERA5 avec Python

Ce guide vous explique comment télécharger des données météorologiques ERA5 depuis le Copernicus Climate Data Store (CDS) et les convertir en différents formats.

## Table des matières
1. [Création du compte CDS](#1-création-du-compte-cds)
2. [Installation des dépendances](#2-installation-des-dépendances)
3. [Configuration de l'API](#3-configuration-de-lapi)
4. [Utilisation du script](#4-utilisation-du-script)
5. [Paramètres disponibles](#5-paramètres-disponibles)
6. [Configuration dans Spyder](#6-configuration-dans-spyder)
7. [Exemples d'utilisation](#7-exemples-dutilisation)

## 1. Création du compte CDS

### Étape 1 : Inscription
1. Allez sur [https://cds.climate.copernicus.eu/user/register](https://cds.climate.copernicus.eu/user/register)
2. Remplissez le formulaire d'inscription
3. Vérifiez votre email et activez votre compte

### Étape 2 : Acceptation des licences
1. Visitez : [https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=download](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=download)
2. Cliquez sur l'onglet **"Download data"**
3. Descendez jusqu'au bas et chercher conditions d'utilisations / Terms of use (très important !)
3. Acceptez toutes les licences requises (très important !)

## 2. Installation des dépendances

### Sur macOS/Linux :
```bash
pip3 install cdsapi xarray pandas netcdf4 h5netcdf
```

### Sur Windows :
```bash
pip install cdsapi xarray pandas netcdf4 h5netcdf
```

## 3. Configuration de l'API

### Créer le fichier de configuration :

**Sur macOS/Linux :**
```bash
nano ~/.cdsapirc
```

**Sur Windows :**
Créez un fichier `.cdsapirc` dans le répertoire du projet (`C:\Users\repertoire\.cdsapirc`)

### Étape 3 : Récupération des identifiants API
1. Connectez-vous à votre compte : [https://cds.climate.copernicus.eu/user/login](https://cds.climate.copernicus.eu/user/login)
2. Allez dans votre profil utilisateur
3. Cliquez sur User guide
4. Copiez sur API Service(3e position)
5. Copiez votre **URL** et votre **API Key**

### Contenu du fichier à copier et coller :
```
url: https://cds.climate.copernicus.eu/api
key: VOTRE_UID:VOTRE_API_KEY
```

Après Avoir copier / coller dans le fichier .cdsapirc

## 4. Utilisation du script

### Script principal (`test.py`) :

```python
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
        'area': [11.75, -0.80, 11.19, -0.30],  # [Nord, Ouest, Sud, Est]
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
```

### Exécution sur MACOS:
```bash
python3 test.py
```

### Exécution sur WINDOWS:
```bash
python test.py
```

## 5. Paramètres disponibles

### Variables météorologiques principales :
```python
'variable': [
    '2m_temperature',           # Température à 2m (°C)
    'total_precipitation',      # Précipitations totales (mm)
    '10m_u_component_of_wind', # Composante U du vent à 10m (m/s)
    '10m_v_component_of_wind', # Composante V du vent à 10m (m/s)
    'surface_pressure',         # Pression de surface (Pa)
    'relative_humidity',        # Humidité relative (%)
    'solar_radiation',          # Radiation solaire (J/m²)
]
```

### Période temporelle :
```python
'year': ['2023', '2024'],  # Années
'month': ['01', '02', '03'],  # Mois (01-12)
'day': ['01', '02', '03'],    # Jours (01-31)
'time': ['00:00', '06:00', '12:00', '18:00'],  # Heures UTC
```

### Zone géographique (Burkina Faso) :
```python
'area': [15.08, -5.52, 9.40, 2.40],  # [Nord, Ouest, Sud, Est]
# Coordonnées pour le Burkina Faso complet
```

### Zone spécifique (Barrage de Bagré) :
```python
'area': [11.75, -0.80, 11.19, -0.30],  # Zone autour de Bagré
```

### Configuration dans Spyder :

1. **Ouvrir Spyder**
2. **Aller dans Tools > Preferences > Python Interpreter**
3. **Sélectionner l'interpréteur Python correct** (celui où vous avez installé les packages)
4. **Redémarrer Spyder**

### Utilisation dans Spyder :

1. **Créer un nouveau fichier** : `File > New File`
2. **Copier le code** du script
3. **Sauvegarder** : `Ctrl+S` (nommez le fichier `era5_download.py`)
4. **Exécuter** : `F5` ou cliquer sur le bouton "Run"


## 7. Exemples d'utilisation

### Exemple 1 : Téléchargement simple (1 jour)
```python
import cdsapi

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
    'temperature_bagre_2024_01_01.nc'
)
```

### Exemple 2 : Téléchargement multiple variables (1 mois)
```python
import cdsapi

c = cdsapi.Client()
c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': [
            '2m_temperature',
            'total_precipitation',
            '10m_u_component_of_wind',
            '10m_v_component_of_wind'
        ],
        'year': '2024',
        'month': '01',
        'day': [
            '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
            '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'
        ],
        'time': ['00:00', '06:00', '12:00', '18:00'],
        'area': [11.75, -0.80, 11.19, -0.30],
    },
    'meteo_bagre_2024_01.nc'
)
```

### Exemple 3 : Script complet avec conversion
```python
import cdsapi
import xarray as xr
import pandas as pd
import json
import os

def download_and_convert_era5(output_name, variables, year, month, day, area):
    """
    Télécharge des données ERA5 et les convertit en différents formats
    """
    
    # Téléchargement
    c = cdsapi.Client()
    nc_file = f"{output_name}.nc"
    
    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'variable': variables,
            'year': year,
            'month': month,
            'day': day,
            'time': ['00:00', '06:00', '12:00', '18:00'],
            'area': area,
        },
        nc_file
    )
    
    # Conversion
    if os.path.exists(nc_file):
        ds = xr.open_dataset(nc_file)
        
        # JSON
        data_dict = ds.to_dict()
        with open(f"{output_name}.json", 'w') as f:
            json.dump(data_dict, f, indent=2, default=str)
        
        # CSV
        df = ds.to_dataframe().reset_index()
        df.to_csv(f"{output_name}.csv", index=False)
        
        # TXT
        df.to_csv(f"{output_name}.txt", index=False, sep='\t')
        
        print(f"Fichiers créés : {output_name}.nc, {output_name}.json, {output_name}.csv, {output_name}.txt")
        
        # Informations sur les données
        print(f"Dimensions : {ds.dims}")
        print(f"Variables : {list(ds.variables.keys())}")
    else:
        print("Erreur lors du téléchargement")

# Utilisation
download_and_convert_era5(
    output_name="bagre_meteo_2024_01",
    variables=['2m_temperature', 'total_precipitation'],
    year='2024',
    month='01',
    day=['01', '02', '03'],
    area=[11.75, -0.80, 11.19, -0.30]
)
```

## Résolution de problèmes

### Erreur "command not found: python"
- Sur macOS : utilisez `python3` au lieu de `python`
- Installez Python depuis [python.org](https://www.python.org/downloads/)

### Erreur "Missing/incomplete configuration file"
- Vérifiez que le fichier `.cdsapirc` existe dans votre répertoire home
- Vérifiez le format du fichier (pas d'espaces supplémentaires)

### Erreur "403 Forbidden - required licences not accepted"
- Connectez-vous sur CDS et acceptez toutes les licences
- Attendez 5-10 minutes après acceptation

### Erreur "Module not found"
- Réinstallez les dépendances : `pip3 install --upgrade cdsapi xarray pandas netcdf4`
- Vérifiez que vous utilisez le bon environnement Python

## Ressources utiles

- **Documentation CDS API** : [https://cds.climate.copernicus.eu/api-how-to](https://cds.climate.copernicus.eu/api-how-to)
- **Catalogue ERA5** : [https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels)
- **Forum ECMWF** : [https://forum.ecmwf.int/](https://forum.ecmwf.int/)
- **Documentation