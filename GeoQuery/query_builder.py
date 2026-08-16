from location_resolver import resolve_location


def build_query(plan):

    layer = plan["layer"]
    fclass = plan.get("fclass")
    location = plan.get("location")
    reference = plan.get("reference")
    distance = plan.get("distance")
    limit = plan.get("limit", 1000000)

    location_type = None

    if location:
        location_type = resolve_location(location)

    sql = f"""
    SELECT
        {layer}.*
    FROM {layer}
    """

    where = []

    # Proximity Query
    if reference and distance:
        sql += f"""
        JOIN (
            SELECT geom
            FROM poi
            WHERE LOWER(name)=LOWER('{reference}')
            LIMIT 1
        ) ref
        ON TRUE
        """

        where.append(
            f"""
            ST_DWithin(
                {layer}.geom::geography,
                ref.geom::geography,
                {distance}
            )
            """
        )


    # Administrative Boundary
    if location:
        if location_type == "state":
            boundary_table = "states"

        elif location_type == "subdistrict":
            boundary_table = "subdistricts"

        else:
            boundary_table = "districts"

        sql += f"""
        JOIN {boundary_table} b
        ON ST_Intersects(
            {layer}.geom,
            b.geom
        )
        """

        where.append(
            f"LOWER(b.name)=LOWER('{location}')"
        )


    # Feature Class
    if fclass:
        if isinstance(fclass, list):
            values = ", ".join(
                [f"LOWER('{x}')" for x in fclass]
            )
            where.append(
                f"LOWER({layer}.fclass) IN ({values})"
            )

        else:
            where.append(
                f"LOWER({layer}.fclass)=LOWER('{fclass}')"
            )

       # WHERE
    if where:
        sql += "\nWHERE\n"
        sql += "\nAND\n".join(where)


    # LIMIT to reduce the complexity and time
    sql += f"\nLIMIT {limit}"
    return sql