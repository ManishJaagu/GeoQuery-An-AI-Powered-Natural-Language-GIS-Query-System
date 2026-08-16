import re
import time
import geopandas as gpd
from database import engine


def execute(sql):
    # display query (LIMIT 500) # 
    start = time.perf_counter()
    display_gdf = gpd.read_postgis(
        sql,
        engine,
        geom_col="geom"
    )

    end = time.perf_counter()
    elapsed = round(end - start, 3)
    if display_gdf.empty:
        return {
            "success": False,
            "message": "No records found.",
            "gdf": None,
            "download_gdf": None,
            "info": {
                "execution_time": elapsed,
                "records": 0,
                "geometry": None,
                "layer": None
            }
        }


    # Download query without record limitation
    download_sql = re.sub(
        r"LIMIT\s+\d+\s*;?",
        "",
        sql,
        flags=re.IGNORECASE
    )
    download_gdf = gpd.read_postgis(
        download_sql,
        engine,
        geom_col="geom"
    )


    # Information
    geometry = display_gdf.geometry.iloc[0].geom_type
    layer = sql.split("FROM")[1].split()[0].strip()
    return {
        "success": True,
        "message": f"{len(download_gdf)} record(s) found.",
        "gdf": display_gdf,
        "download_gdf": download_gdf,
        "info": {
            "execution_time": elapsed,
            "records": len(download_gdf),
            "display_records": len(display_gdf),
            "geometry": geometry,
            "layer": layer
        }
    }