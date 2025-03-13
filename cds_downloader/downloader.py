import cdsapi
import os

# Default variable mapping from descriptive parameter names to ERA5 short names
DEFAULT_PARAM_MAPPING = {
    "10m_u_component_of_wind": "10u",
    "10m_v_component_of_wind": "10v",
    "2m_dewpoint_temperature": "2d",
    "2m_temperature": "2t",
    "mean_sea_level_pressure": "msl",
    "surface_pressure": "sp",
    "total_precipitation": "tp",
    "total_cloud_cover": "tcc",
    "lake_cover": "lc",
    "lake_depth": "ld",
    "lake_mix_layer_temperature": "lmlt",
    "convective_precipitation": "cp",
    "convective_rain_rate": "crr",
    "total_column_rain_water": "tcrw",
    "volumetric_soil_water_layer_1": "swvl1",
    "high_vegetation_cover": "cvh",
    "low_vegetation_cover": "cvl",
    "skin_temperature": "skt",
    "evaporation": "e",
    "runoff": "ro",
    "surface_runoff": "sro",
    "total_column_water_vapour": "tcwv"
}

def download_monthly_data(
    adm_0_name: str,
    year: int,
    month: str,
    days: list,
    area: list,
    data_dir: str,
    param_mapping: dict = DEFAULT_PARAM_MAPPING
) -> str:
    """
    Downloads ERA5 data for a specific (year, month), storing in a GRIB file.

    :param adm_0_name: Country or area name, used in the output file name
    :param year: Year (int)
    :param month: Month string, e.g. '01', '02' ...
    :param days: List of day strings, e.g. ['01', '02', ..., '31']
    :param area: [North, West, South, East] bounding box
    :param data_dir: Directory to store downloaded GRIB file
    :param param_mapping: Dict mapping descriptive weather vars to ERA5 short codes
    :return: Path to the downloaded GRIB file
    """
    client = cdsapi.Client()

    request = {
        "product_type": ["reanalysis"],
        "variable": list(param_mapping.keys()),  # e.g. ["10u", "10v", "2t", ...]
        "year": [str(year)],
        "month": [month],
        "day": days,
        "time": ["00:00", "06:00", "12:00", "18:00"],
        "data_format": "grib",
        "download_format": "unarchived",
        "area": area
    }

    os.makedirs(data_dir, exist_ok=True)
    file_name = f"{adm_0_name}_{year}_{month}.grib"
    file_path = os.path.join(data_dir, file_name)

    print(f"Downloading ERA5 data for {adm_0_name} ({year}-{month}), area={area} ...")
    client.retrieve("reanalysis-era5-single-levels", request).download(file_path)
    print(f"Downloaded monthly GRIB file: {file_path}")
    return file_path

def download_meteorological_data(
    adm_0_name: str,
    start_year: int,
    end_year: int,
    months: list,
    days: list,
    area: list,
    data_dir: str,
    param_mapping: dict = DEFAULT_PARAM_MAPPING
) -> list:
    """
    Iterates over each year & month, downloads monthly data, and returns a list of GRIB file paths.

    :param adm_0_name: Country or area name (for file naming)
    :param start_year: Start of date range
    :param end_year: End of date range
    :param months: e.g. ['01','02','03'] ...
    :param days: e.g. ['01','02', ..., '31']
    :param area: bounding box [North, West, South, East]
    :param data_dir: Directory to store all monthly GRIBs
    :return: List of GRIB file paths
    """
    all_files = []
    for year in range(start_year, end_year + 1):
        for month in months:
            grib_path = download_monthly_data(
                adm_0_name, year, month, days, area, data_dir, param_mapping
            )
            all_files.append(grib_path)
    return all_files

if __name__ == "__main__":
    # Example usage
    start_year = 2020
    end_year = 2021
    months = ["01", "02"]
    days = [f"{d:02d}" for d in range(1, 32)]
    # Example bounding box (Sierra Leone) [North, West, South, East]
    area = [9.996, -13.301, 6.919, -10.282]
    data_dir = "./data"

    files = download_meteorological_data("Sierra_Leone", start_year, end_year, months, days, area, data_dir)
    print("Downloaded files:", files)
