import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen, MeasureControl


def show_map(
    gdf=None,
    boundary=None
):

    # --------------------------------------------------
    # Base Map
    # --------------------------------------------------

    m = folium.Map(
        location=[22.5, 79],
        zoom_start=5,
        control_scale=True,
        tiles=None
    )

    # --------------------------------------------------
    # Basemaps
    # --------------------------------------------------
    
    folium.TileLayer(
        "OpenStreetMap",
        name="OpenStreetMap"
    ).add_to(m)

    folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attr="Google",
        name="Google Satellite",
        overlay=False
    ).add_to(m)

    # --------------------------------------------------
    # Plugins
    # --------------------------------------------------
    
    Fullscreen().add_to(m)
    MeasureControl().add_to(m)

    # --------------------------------------------------
    # Selected District Boundary
    # --------------------------------------------------
    
    if boundary is not None and not boundary.empty:
        folium.GeoJson(
            boundary,
            name="Boundary",
            style_function=lambda feature: {
                "color": "yellow",
                "weight": 3,
                "fillOpacity": 0
            }
        ).add_to(m)

    # --------------------------------------------------
    # Query Results
    # --------------------------------------------------

    if gdf is not None and not gdf.empty:
        bounds = gdf.total_bounds
        m.fit_bounds([
            [bounds[1], bounds[0]],
            [bounds[3], bounds[2]]
        ])
        geom_type = gdf.geom_type.iloc[0]

        # ==================================================
        # POINTS
        # ==================================================

        if geom_type in ["Point", "MultiPoint"]:
            for _, row in gdf.iterrows():
                geom = row[gdf.geometry.name]
                popup = ""
                if "name" in gdf.columns and row["name"] is not None:
                    popup += f"<b>{row['name']}</b><br>"

                if "fclass" in gdf.columns and row["fclass"] is not None:
                    popup += row["fclass"]

                if geom.geom_type == "Point":
                    folium.CircleMarker(
                        location=[geom.y, geom.x],
                        radius=5,
                        color="red",
                        fill=True,
                        fill_color="red",
                        fill_opacity=0.9,
                        popup=popup
                    ).add_to(m)

                elif geom.geom_type == "MultiPoint":
                    for pt in geom.geoms:
                        folium.CircleMarker(
                            location=[pt.y, pt.x],
                            radius=5,
                            color="red",
                            fill=True,
                            fill_color="red",
                            fill_opacity=0.9,
                            popup=popup
                        ).add_to(m)

        # ==================================================
        # LINES & POLYGONS
        # ==================================================

        else:
            folium.GeoJson(
                gdf,
                name="Results",
                tooltip=folium.GeoJsonTooltip(
                    fields=[
                        c for c in gdf.columns if c != gdf.geometry.name
                    ][:6]
                ),
                
                style_function=lambda feature: {
                    "color": "#0066ff",
                    "weight": 2,
                    "fillColor": "#00aa00",
                    "fillOpacity": 0.25
                }
            ).add_to(m)

    # --------------------------------------------------
    # Layer Control
    # --------------------------------------------------

    folium.LayerControl(
        collapsed=False
    ).add_to(m)

    # --------------------------------------------------
    # Render
    # --------------------------------------------------

    st_folium(
        m,
        height=340,
        width="stretch",
        returned_objects=[],
        key="main_map"
    )