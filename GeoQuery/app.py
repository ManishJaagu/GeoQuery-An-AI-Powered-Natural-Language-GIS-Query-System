import streamlit as st
from map import show_map
from planner import create_plan
from parser import parse
from query_builder import build_query
from executor import execute
from boundary import get_boundary

# --------------------------------------------------------
# Page
# --------------------------------------------------------

st.set_page_config(
    page_title="GeoQuery",
    layout="wide"
)

# --------------------------------------------------------
# Session State
# --------------------------------------------------------

DEFAULTS = {
    "query": "",
    "results": None,
    "gdf": None,
    "info": None,
    "sql": None,
    "download": None,
    "boundary": None
}

for key, value in DEFAULTS.items():
    st.session_state.setdefault(key, value)
    
# --------------------------------------------------------
# CSS
# --------------------------------------------------------

st.markdown("""
<style>

html,
body,
[data-testid="stAppViewContainer"]{
    height:100vh;
    overflow:hidden;
}

section.main{
    height:100vh;
    overflow:hidden;
}

.block-container{
    padding-top:0.4rem;
    padding-bottom:0rem;
    padding-left:1.5rem;
    padding-right:1.5rem;
}

div[data-testid="stVerticalBlock"]{
    gap:0.25rem;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------
# Logo
# --------------------------------------------------------

st.markdown(
    "<div style='margin-top:65px; margin-bottom:10px;'></div>",
    unsafe_allow_html=True
)

st.image(
    "assets/logo.png",
    width=120
)

# --------------------------------------------------------
# Main Layout
# --------------------------------------------------------

left, right = st.columns([1.05, 1.25], gap="large")

# ========================================================
# LEFT PANEL
# ========================================================

with left:

    with st.form("query_form", clear_on_submit=False):

        question = st.text_input(
            "GIS Query",
            key=f"query_{st.session_state.get('clear_counter', 0)}",
            placeholder="Example: Show hospitals in Hyderabad",
            label_visibility="collapsed"
        )

        st.markdown(
            "<div style='height:10px'></div>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([4,1])

        with col1:
            run = st.form_submit_button(
                "Execute Query",
                use_container_width=True
            )

        with col2:
            clear = st.form_submit_button(
                "Clear",
                use_container_width=True
            )
    # ----------------------------------------------------
    # Execute
    # ----------------------------------------------------

    if run and question.strip():
        with st.spinner("Running query..."):
            try:
                # Planner
                planner_output = create_plan(question)

                # Parse JSON
                plan = parse(planner_output)
                
                # ------------------------------------
                # Boundary
                # ------------------------------------

                location = plan.get("location")
                if location:
                    st.session_state.boundary = get_boundary(location)

                else:
                    st.session_state.boundary = None
                    
                # SQL
                sql = build_query(plan)

                # Execute SQL
                result = execute(sql)

                if result["success"]:
                    st.session_state.sql = sql
                    st.session_state.gdf = result["gdf"]
                    st.session_state.results = (
                        result["gdf"]
                        .drop(columns="geom", errors="ignore")
                    )
                    st.session_state.info = result["info"]

                    download_cols = [
                        c for c in [
                            "name",
                            "fclass",
                            "code",
                            "osm_id"
                        ]
                        if c in result["download_gdf"].columns
                    ]

                    st.session_state.download = (
                        result["download_gdf"][download_cols]
                        .fillna("")
                        .to_csv(index=False)
                    )

                    st.rerun()

                else:
                    st.session_state.results = None
                    st.session_state.gdf = None
                    st.session_state.info = None
                    st.session_state.download = None
                    st.session_state.sql = None
                    
                    st.warning(result["message"])

            except Exception as e:
                st.session_state.results = None
                st.session_state.gdf = None
                st.session_state.info = None
                st.session_state.download = None
                st.session_state.sql = None

                st.error(f"Error: {e}")
    # ----------------------------------------------------
    # Clear
    # ----------------------------------------------------
    if clear:

        # Clear results
        for key in ["results", "gdf", "info", "sql", "download", "boundary"]:
            st.session_state[key] = None
            
        st.session_state.clear_counter = (
            st.session_state.get("clear_counter", 0) + 1
        )

        st.rerun()

    # ----------------------------------------------------
    # Results
    # ----------------------------------------------------
    if st.session_state.results is None:
        st.subheader("Results")

    else:
        st.subheader(f"Results • Showing {len(st.session_state.results)} of {st.session_state.info['records']} Features")

    result_box = st.container(height=270)

    with result_box:
        if st.session_state.results is None:
            st.info("Results will appear here.")

        else:
            cols = [
                c
                for c in [
                    "name",
                    "fclass",
                    "code",
                    "osm_id"
                ]
                if c in st.session_state.results.columns
            ]

            st.dataframe(
                st.session_state.results[cols],
                width="stretch",
                hide_index=True,
                height=260
            )

st.markdown("""
<div style="
font-size:10px;
color:#7a7a7a;
padding-left:5px;
padding-top:2px;
">

Data source: Geofabrik OpenStreetMap • Data as of 10 July 2026
</div>
""", unsafe_allow_html=True)
        
# ========================================================
# RIGHT PANEL
# ========================================================

with right:
    show_map(
        gdf=st.session_state.gdf,
        boundary=st.session_state.boundary
    )
    st.markdown(
        "<div style='height:6px'></div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div style='height:10px'></div>",
        unsafe_allow_html=True
    )


    # Download
    if st.session_state.download:
        st.download_button(
            "Download CSV",
            st.session_state.download,
            file_name="results.csv",
            mime="text/csv",
            width="stretch"
        )

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # -------------------------
    # Information
    # -------------------------
    
    st.markdown("### Information")
    info = st.session_state.info
    if info:
        st.markdown(f"""

    <div style="
    display:flex;
    justify-content:space-evenly;
    align-items:center;
    padding:12px;
    border:1px solid #30363d;
    border-radius:10px;
    background:#161b22;
    ">

    <div style="flex:1;text-align:center;">
    <div style="font-size:12px;color:#8b949e;">Execution Time</div>
    <div style="font-size:16px;font-weight:600;">{info['execution_time']} sec</div>
    </div>

    <div style="flex:1;text-align:center;">
    <div style="font-size:12px;color:#8b949e;">Records</div>
    <div style="font-size:16px;font-weight:600;">{info['records']}</div>
    </div>

    <div style="flex:1;text-align:center;">
    <div style="font-size:12px;color:#8b949e;">Geometry</div>
    <div style="font-size:16px;font-weight:600;">{info['geometry']}</div>
    </div>

    <div style="flex:1;text-align:center;">
    <div style="font-size:12px;color:#8b949e;">Layer</div>
    <div style="font-size:16px;font-weight:600;">{info['layer']}</div>
    </div>

    </div>

    """, unsafe_allow_html=True)

    else:
        st.info("Information will appear here.")