# GeoQuery: An AI-Powered Natural Language GIS Query System

GeoQuery is a Summer of Science (SoS) 2026 project that combines Large Language Models with GIS and spatial databases to make geospatial data easier to query. Instead of writing SQL queries or navigating traditional GIS software, users can ask questions such as **"Show hospitals in Hyderabad"** in natural language.

The system uses **Llama 3.3 70B** through the Groq API to understand the user's query and convert it into a structured JSON representation. This is then translated into spatial SQL and executed on a **PostgreSQL/PostGIS** database. The retrieved features are processed using GeoPandas and displayed through an interactive Streamlit/Folium interface. :contentReference[oaicite:0]{index=0} :contentReference[oaicite:1]{index=1}

## Features

- **Natural-language GIS queries** using Llama 3.3 70B
- **Structured query planning** using JSON before SQL generation
- **PostgreSQL/PostGIS spatial database** for storing and querying geospatial data
- **India-wide OSM/Geofabrik datasets** including POIs, waterways, water bodies, railways, transport, land use, natural features and protected areas
- **Automatic location resolution** across states, districts and subdistricts
- **Spatial SQL generation** using PostGIS functions such as `ST_Intersects()`
- **Interactive map visualization** using Folium with OpenStreetMap and Google Satellite basemaps
- **Administrative boundary display** for the queried location
- **Attribute tables and query information** for retrieved features
- **CSV export** for further analysis in GIS or spreadsheet software
- **GiST spatial indexing** to support efficient spatial queries :contentReference[oaicite:2]{index=2} :contentReference[oaicite:3]{index=3}

## How It Works

```text
Natural Language Query
        ↓
Llama 3.3 70B
        ↓
Structured JSON
        ↓
Query Validation
        ↓
Location Resolution
        ↓
Spatial SQL Generation
        ↓
PostgreSQL / PostGIS
        ↓
GeoPandas
        ↓
Folium Interactive Map
        ↓
Results + CSV Export
