import geopandas as gpd

def get_country_bounding_box(country_name: str):
    """
    Given a country name, fetch the country's geometry from an online GeoJSON source,
    and return the bounding box in the format [North, West, South, East] required by the CDS API.

    :param country_name: Name of the country (e.g., 'Sierra Leone')
    :return: [North, West, South, East]
    """
    url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
    world = gpd.read_file(url)

    # Look for the country in the "ADMIN" column, ignoring case
    country = world[world["ADMIN"].str.lower() == country_name.lower()]
    if country.empty:
        raise ValueError(f"Country '{country_name}' not found.")

    # total_bounds returns [minx, miny, maxx, maxy]
    minx, miny, maxx, maxy = country.total_bounds
    return [maxy, minx, miny, maxx]  # [North, West, South, East]
