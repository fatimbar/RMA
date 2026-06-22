import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(
    page_title="FSS PGR Research Methods Training",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Boutique Academic Theme Custom CSS (Pastel Gradients & White Background)
st.markdown("""
    <style>
    /* Main Background & Text Styling */
    .stApp {
        background-color: #F8F9FA;
        color: #2D3748;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Sidebar Gradient Styling */
    [data-testid="stSidebar"] {
        background-image: linear-gradient(180deg, #E0F2FE 0%, #DCFCE7 100%);
    }
    /* Custom Interactive Dashboard Cards */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        border-left: 5px solid #BAE6FD;
        margin-bottom: 15px;
    }
    .metric-card.qual {
        border-left: 5px solid #BBF7D0;
    }
    h1, h2, h3 {
        color: #1E293B !important;
    }
    </style>
""", unsafe_allow_index=True)

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
    st.error(f"Error loading the Excel file. Please ensure 'FSS_Research_Methods_Catalogue.xlsx' is in the same directory: {e}")
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
    
    # Completed Modules Display Cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <span style="color: #0284C7; font-weight: bold; font-size: 0.9rem;">SOC — SOC00011M (Advanced)</span>
            <h3 style="margin: 5px 0;">Advanced Methods in Social Research</h3>
            <p style="font-size: 0.9rem; color: #64748B;"><b>Philosophy:</b> Quantitative | <b>Credits/Hours:</b> 30 contact hours</p>
            <p style="font-size: 0.85rem; background: #F0F9FF; padding: 8px; border-radius: 6px;">💡 <b>Analyst Notes:</b> The course is interactive, offering diverse approaches. A one-hour lecture may mean that the content is only a partial introduction and requires subsequent self-study.</p>
        </div>
        """, unsafe_allow_index=True)
        
    with col2:
        st.markdown("""
        <div class="metric-card qual">
            <span style="color: #16A34A; font-weight: bold; font-size: 0.9rem;">SOC — SOC00026M (Beginner)</span>
            <h3 style="margin: 5px 0;">Introduction to Qualitative Methods and Data Analysis</h3>
            <p style="font-size: 0.9rem; color: #64748B;"><b>Philosophy:</b> Qualitative | <b>Level:</b> Beginner</p>
            <p style="font-size: 0.85rem; background: #F0FDF4; padding: 8px; border-radius: 6px;">💡 <b>Analyst Notes:</b> This module provides an in-depth study of qualitative research, covering its various types with practical and applied examples.</p>
        </div>
        """, unsafe_allow_index=True)

    st.write("---")
    st.subheader("📉 Catalogue Mapping Progress")
    
    # Mapping Data Gaps vs Filled to show expanding concept
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
    
    # Filter content based on user choice
    module_weeks = weekly_df[weekly_df['Module Name'].str.contains(selected_module, na=False, case=False)]
    
    if not module_weeks.empty:
        # Plotly Scatter Timeline
        fig_timeline = px.scatter(
            module_weeks,
            x="Week No.",
            y="Skill Level This Week",
            hover_data=["Week Title / Topic", "Key Content & Methods Covered", "Core Readings"],
            text="Week No.",
            title=f"Learning Journey Timeline: {selected_module}"
        )
        
        marker_color = "#BAE6FD" if "Advanced" in selected_module else "#BBF7D0"
        fig_timeline.update_traces(
            marker=dict(size=35, color=marker_color, line=dict(width=2, color='#94A3B8')),
            textposition="inside",
            font=dict(size=12, color='#1E293B')
        )
        fig_timeline.update_layout(
            plot_bgcolor="#F8F9FA",
            xaxis=dict(title="Week Number", tickmode="linear"),
            yaxis=dict(title="Target Focus / Skill Progression")
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
        st.markdown("""
        <div style="background-color: #FEF2F2; padding: 20px; border-radius: 12px; border: 1px solid #FCA5A5;">
            <span style="background-color: #EF4444; color: white; padding: 3px 8px; border-radius: 20px; font-size: 0.75rem; font-weight: bold;">Advanced Level</span>
            <h3 style="margin-top: 10px;">Advanced Methods (SOC00011M)</h3>
            <p><b>Accessible to Non-Specialists?</b> ❌ No</p>
            <p><b>Risk of Mismatch:</b> ⚠️ Medium Risk</p>
            <hr style="border: 0.5px solid #FCA5A5;">
            <p style="font-size: 0.9rem;"><b>Implicit Prerequisites:</b> Requires advanced knowledge of research methodologies, intermediate statistics, and philosophy of social sciences.</p>
        </div>
        """, unsafe_allow_index=True)
        
    with col2:
        st.markdown("""
        <div style="background-color: #F0FDF4; padding: 20px; border-radius: 12px; border: 1px solid #BBF7D0;">
            <span style="background-color: #22C55E; color: white; padding: 3px 8px; border-radius: 20px; font-size: 0.75rem; font-weight: bold;">Beginner Level</span>
            <h3 style="margin-top: 10px;">Intro Qualitative (SOC00026M)</h3>
            <p><b>Accessible to Non-Specialists?</b>  Yes</p>
            <p><b>Risk of Mismatch:</b> ✅ Low Risk</p>
            <hr style="border: 0.5px solid #BBF7D0;">
            <p style="font-size: 0.9rem;"><b>Stated Prerequisites:</b> The module makes no assumptions about students’ prior knowledge of qualitative methods.</p>
        </div>
        """, unsafe_allow_index=True)

    st.write("---")
    st.markdown("💡 *Strategic Note: As more rows are completed in the catalogue, this section will automatically scale to generate a network graph mapping student journeys from introductory to advanced methodologies without curriculum mismatch.*")