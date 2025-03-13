import os
import tempfile
import numpy as np
import pygrib
import geopandas as gpd
import pandas as pd
from shapely import vectorized
from cds_downloader.country_utils import get_country_bounding_box
from cds_downloader.downloader import download_meteorological_data, DEFAULT_PARAM_MAPPING

def process_grib_in_temp(
    country: str,
    adm2_shp_source: str,
    start_year: int,
    end_year: int,
    months: list,
    days: list,
    param_mapping: dict,
    output_pickle: str
) -> pd.DataFrame:
    """
    1. Use 'download_meteorological_data' to get monthly GRIB files into a temp dir.
    2. For each subregion (based on ADM2 shapefile):
       - Combine or process each monthly file's GRIB messages
       - Mask by bounding box & subregion geometry
       - Stack daily 2D grids into a 3D tensor
    3. Return a MultiIndex DataFrame (indexed by region, month) with columns per variable.
    """

    # Get bounding box from 'country_utils'
    bbox = get_country_bounding_box(country)
    print(f"[process_grib_in_temp] Country={country}, BBOX={bbox}")

    # Create a temporary directory for monthly GRIB files
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Using temp dir: {tmpdir}")
        # Download data in monthly chunks
        monthly_files = download_meteorological_data(
            country.replace(" ", "_"),
            start_year,
            end_year,
            months,
            days,
            bbox,
            tmpdir,
            param_mapping
        )
        print("All monthly files:", monthly_files)

        # Load ADM2 shapefile (2nd-level admin boundaries)
        gdf_adm2 = gpd.read_file(adm2_shp_source).to_crs(epsg=4326)
        print("Loaded ADM2 shapefile with", len(gdf_adm2), "subregions.")

        # Prepare data structure: region_data[region_name][month_str][variable] = [2D array, ...]
        region_data = {}
        variables = list(param_mapping.keys())

        # Process each monthly GRIB file
        for file_path in monthly_files:
            # Derive year-month from file name
            base = os.path.basename(file_path)  # e.g. 'Sierra_Leone_2020_01.grib'
            parts = base.split('_')
            year_part = parts[-2]
            month_part = parts[-1].split('.')[0]  # e.g. '01'
            month_str = f"{year_part}-{month_part}"

            print(f"Processing {file_path} => {month_str}")

            with pygrib.open(file_path) as grbs:
                grb_messages = list(grbs)
            print(f"  Loaded {len(grb_messages)} GRIB messages")

            # For each subregion
            for _, region_row in gdf_adm2.iterrows():
                region_name = region_row["shapeName"]  # or an appropriate field name
                if region_name not in region_data:
                    region_data[region_name] = {}
                if month_str not in region_data[region_name]:
                    region_data[region_name][month_str] = {}

                region_geom = region_row.geometry  # shapely geometry

                # For each variable (by name)
                for var_name in variables:
                    # Filter GRIB messages for this variable
                    var_msgs = [grb for grb in grb_messages if var_name in grb.name]
                    if not var_msgs:
                        continue
                    var_msgs.sort(key=lambda g: g.validDate)

                    # Initialize list if not present
                    if var_name not in region_data[region_name][month_str]:
                        region_data[region_name][month_str][var_name] = []

                    # Process each GRIB message (timestamp)
                    for grb in var_msgs:
                        data_values = grb.values  # 2D numpy array
                        lats, lons = grb.latlons()

                        # Convert temperature from K to °C if 'temperature' in var_name
                        if "temperature" in var_name.lower():
                            data_values = data_values - 273.15

                        # Clip to bounding box
                        global_mask = (
                            (lons >= bbox[1]) & (lons <= bbox[3]) &
                            (lats >= bbox[2]) & (lats <= bbox[0])
                        )
                        data_values = np.where(global_mask, data_values, np.nan)

                        # Further mask by subregion polygon
                        subregion_mask = vectorized.contains(region_geom, lons, lats)
                        data_values_region = np.where(subregion_mask, data_values, np.nan)

                        region_data[region_name][month_str][var_name].append(data_values_region)

        # Convert lists of 2D arrays to 3D arrays
        for region_name, month_dict in region_data.items():
            for month_str, var_dict in month_dict.items():
                for var_name, array_list in var_dict.items():
                    # Stack the daily/timestamp 2D arrays along axis=0 => shape = (num_timestamps, rows, cols)
                    region_data[region_name][month_str][var_name] = np.stack(array_list, axis=0)

        # Build a DataFrame with MultiIndex (region, month)
        rows = []
        for region_name, month_dict in region_data.items():
            for month_str, var_dict in month_dict.items():
                row = {"region": region_name, "month": month_str}
                for var_name in variables:
                    row[var_name] = var_dict.get(var_name, None)
                rows.append(row)

        df_result = pd.DataFrame(rows).set_index(["region", "month"])
        df_result.to_pickle(output_pickle)

        print(f"Processing complete! Pickled DataFrame at: {output_pickle}")
        return df_result

if __name__ == "__main__":
    # Example usage (dummy example bounding box, start/end years, etc.)
    country = "Sierra Leone"
    adm2_shp_source = "./data/geoBoundaries-BGD-ADM2-all/geoBoundaries-BGD-ADM2.shp"
    start_year = 2020
    end_year = 2020
    months = ["01", "02"]
    days = [f"{d:02d}" for d in range(1, 32)]
    output_pickle = "./region_monthly_weather_tensors.pkl"

    df = process_grib_in_temp(
        country,
        adm2_shp_source,
        start_year,
        end_year,
        months,
        days,
        DEFAULT_PARAM_MAPPING,
        output_pickle
    )
    print("Final DataFrame shape:", df.shape)
