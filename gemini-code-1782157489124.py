import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="FSS PGR Research Methods Training",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Modern Safe Styling via st.html (Boutique Academic Theme)
st.html("""
    <style>
    /* Main Background & Text Styling */
    .stApp {
        background-color: #F8F9FA !important;
        color: #2D3748 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Sidebar Gradient Styling */
    [data-testid="stSidebar"] {
        background-image: linear-gradient(180deg, #E0F2FE 0%, #DCFCE7 100%) !important;
    }
    h1, h2, h3 {
        color: #1E293B !important;
    }
    </style>
""")

# 3. Data Loading Function
@st.cache_data
def load_data():
    filepath = "FSS_Research_Methods_Catalogue.xlsx"
    overview_df = pd.read_excel(filepath, sheet_name='1. Overview', skiprows=1)
    weekly_df = pd.read_excel(filepath, sheet_name='2. Weekly Content', skiprows=1)
    return overview_df, weekly_df

try:
    overview_df, weekly_df = load_data()
except Exception as e:
    st.error(f"Error loading the Excel file: {e}")
    st.stop()

# 4. Sidebar Navigation
st.sidebar.title("📌 Navigation")
st.sidebar.markdown("### Curriculum Mapping 2026")
st.sidebar.write("University of York | Faculty of Social Sciences")
page = st.sidebar.radio("Go to:", ["📊 Overview Dashboard", "📅 Interactive Weekly Timeline", "🌳 Prerequisites & Risk Analysis"])

# ---------------------------------------------
# PAGE 1: OVERVIEW DASHBOARD
# ---------------------------------------------
if page == "📊 Overview Dashboard":
    st.title("📊 PGR Research Methods Training — Module Catalogue")
    st.markdown("A structural framework mapping social science research methods. Completed modules are interactive below.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.caption("🔹 SOC — SOC00011M (Advanced)")
            st.subheader("Advanced Methods in Social Research")
            st.markdown("**Philosophy:** Quantitative | **Credits/Hours:** 30 contact hours")
            st.info("💡 **Analyst Notes:** The course is interactive, offering diverse approaches. A one-hour lecture may mean that the content is only a partial introduction and requires subsequent self-study.")
        
    with col2:
        with st.container(border=True):
            st.caption("🔸 SOC — SOC00026M (Beginner)")
            st.subheader("Introduction to Qualitative Methods and Data Analysis")
            st.markdown("**Philosophy:** Qualitative | **Level:** Beginner")
            st.success("💡 **Analyst Notes:** This module provides an in-depth study of qualitative research, covering its various types with practical and applied examples.")

    st.write("---")
    st.subheader("📉 Catalogue Mapping Progress")
    
    all_modules = ["Advanced Methods", "Intro Qualitative", "Researching Digital Life", "Intro Quantitative", "Research Design"]
    status = ["Completed", "Completed", "Pending VLE Access", "Pending VLE Access", "Pending VLE Access"]
    status_df = pd.DataFrame({"Module": all_modules, "Status": status, "Count": [1, 1, 1, 1, 1]})
    
    fig_status = px.bar(
        status_df, 
        x="Module", 
        y="Count", 
        color="Status",
        color_discrete_map={"Completed": "#BAE6FD", "Pending VLE Access": "#FCE7F3"},
        title="Visualizing Project Progress & Data Readiness"
    )
    fig_status.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", yaxis_visible=False)
    st.plotly_chart(fig_status, use_container_width=True)

# ---------------------------------------------
# PAGE 2: INTERACTIVE WEEKLY TIMELINE
# ---------------------------------------------
elif page == "📅 Interactive Weekly Timeline":
    st.title("📅 Weekly Content Timeline Analysis")
    st.markdown("Switch between completed modules to dynamically explore weekly topics, methods, and core readings.")
    
    selected_module = st.selectbox(
        "Select a Module to Inspect:",
        ["Advanced Methods in Social Research", "Introduction to Qualitative Methods and Data Analysis"]
    )
    
    # Secure data filtering & cleaning text-based rows out of numeric timeline
    module_weeks = weekly_df[weekly_df['Module Name'].str.contains(selected_module, na=False, case=False)].copy()
    
    if not module_weeks.empty:
        # Crucial Fix: Convert Week No to numeric and drop rows that are headers or empty text
        module_weeks['Week No.'] = pd.to_numeric(module_weeks['Week No.'], errors='coerce')
        module_weeks = module_weeks.dropna(subset=['Week No.'])
        module_weeks = module_weeks.sort_values(by='Week No.')
        
        # Using Safe px.line with markers to completely bypass update_traces values errors
        fig_timeline = px.line(
            module_weeks,
            x="Week No.",
            y="Skill Level This Week",
            markers=True,
            hover_data=["Week Title / Topic", "Methods Introduced", "Core Readings"],
            title=f"Learning Journey Timeline: {selected_module}",
            color_discrete_sequence=["#0284C7" if "Advanced" in selected_module else "#16A34A"]
        )
        
        fig_timeline.update_layout(
            plot_bgcolor="#F8F9FA",
            xaxis=dict(title="Week Number", tickmode="linear", dtick=1),
            yaxis=dict(title="Target Focus / Skill Progression"),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        st.markdown("### 📋 Syllabus Details & Readings Table")
        st.dataframe(
            module_weeks[["Week No.", "Week Title / Topic", "Methods Introduced", "Core Readings"]].set_index("Week No."),
            use_container_width=True
        )
    else:
        st.info("Detailed weekly mapping for this module will automatically render once data is added to the Excel file.")

# ---------------------------------------------
# PAGE 3: PREREQUISITES & RISK ANALYSIS
# ---------------------------------------------
elif page == "🌳 Prerequisites & Risk Analysis":
    st.title("🌳 Access Level & Mismatch Risk Matrix")
    st.markdown("Analyst assessment on course accessibility for non-specialist PGR students.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.error("🔺 Advanced Level")
            st.subheader("Advanced Methods (SOC00011M)")
            st.markdown("**Accessible to Non-Specialists?** ❌ No")
            st.markdown("**Risk of Mismatch:** ⚠️ Medium Risk")
            st.write("---")
            st.caption("**Implicit Prerequisites:** Requires advanced knowledge of research methodologies, intermediate statistics, and philosophy of social sciences.")
        
    with col2:
        with st.container(border=True):
            st.success("🟢 Beginner Level")
            st.subheader("Intro Qualitative (SOC00026M)")
            st.markdown("**Accessible to Non-Specialists?** Yes")
            st.markdown("**Risk of Mismatch:** ✅ Low Risk")
            st.write("---")
            st.caption("**Stated Prerequisites:** The module makes no assumptions about students’ prior knowledge of qualitative methods.")

    st.write("---")
    st.markdown("💡 *Strategic Note: As more rows are completed in the catalogue, this section will automatically scale to generate a network graph mapping student journeys.*")
