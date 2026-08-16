import geopandas as gpd
from database import engine
from location_resolver import resolve_location


def get_boundary(location):
    # Determine boundary type automatically
    location_type = resolve_location(location)
    if location_type is None:
        return None

    # Select appropriate table
    if location_type == "state":
        table = "states"

    elif location_type == "district":
        table = "districts"

    elif location_type == "subdistrict":
        table = "subdistricts"

    else:
        return None

    # Fetch boundary
    sql = f"""
    SELECT *
    FROM {table}
    WHERE LOWER(name)=LOWER('{location}')
    """
    gdf = gpd.read_postgis(
        sql,
        engine,
        geom_col="geom"
    )
    if gdf.empty:
        return None
    return gdf