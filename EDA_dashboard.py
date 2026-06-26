import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="Professional Analytics Dashboard", layout="wide", page_icon="📊")

# 2. Custom CSS for Dark PowerBI-style Aesthetics
st.markdown("""
    <style>
        /* Main background */
        .stApp {
            background-color: #0d1b2a;
            color: #ffffff;
        }
        /* Style KPI Cards */
        .metric-container {
            background-color: #1b263b;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
            text-align: center;
            border: 1px solid #415a77;
        }
        .metric-title {
            font-size: 14px;
            color: #e0e1dd;
            margin-bottom: 5px;
        }
        .metric-value {
            font-size: 28px;
            font-weight: bold;
            color: #00b4d8;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Title Banner
st.markdown("<h1 style='text-align: center; color: #00b4d8; margin-bottom: 30px;'>Ecommerce Sales Dashboard</h1>", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Using your excel dataset
    df = pd.read_excel("C:/Users/Joy/Desktop/VDR/EDA/final_df.xlsx")
    # Ensuring mock columns exist if adapting to the screenshot style,
    # but let's assume we map your restaurant data to this layout.
    return df

final_df = load_data()

# 4. Global Interactive Filters (Top Row Right-aligned)
# Any change here automatically re-runs the script and updates all visuals instantly.
filter_col1, filter_col2, filter_col3 = st.columns([6, 3, 3])

with filter_col2:
    # Example Categorical Filter 1
    online_opt = ["All"] + list(final_df["Has Online delivery"].unique())
    selected_online = st.selectbox("Online Delivery Filter", options=online_opt)

with filter_col3:
    # Example Categorical Filter 2
    booking_opt = ["All"] + list(final_df["Has Table booking"].unique())
    selected_booking = st.selectbox("Table Booking Filter", options=booking_opt)

# Apply global filtering
filtered_df = final_df.copy()
if selected_online != "All":
    filtered_df = filtered_df[filtered_df["Has Online delivery"] == selected_online]
if selected_booking != "All":
    filtered_df = filtered_df[filtered_df["Has Table booking"] == selected_booking]


# 5. Top Row: 4 KPI Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"<div class='metric-container'><div class='metric-title'>Total Votes</div><div class='metric-value'>{filtered_df['Votes'].sum():,}</div></div>", unsafe_allow_html=True)
with kpi2:
    st.markdown(f"<div class='metric-container'><div class='metric-title'>Avg Cost for Two</div><div class='metric-value'>${filtered_df['Average Cost for two'].mean():.2f}</div></div>", unsafe_allow_html=True)
with kpi3:
    st.markdown(f"<div class='metric-container'><div class='metric-title'>Average Rating</div><div class='metric-value'>{filtered_df['Aggregate rating'].mean():.2f} ⭐</div></div>", unsafe_allow_html=True)
with kpi4:
    st.markdown(f"<div class='metric-container'><div class='metric-title'>Total Records</div><div class='metric-value'>{len(filtered_df):,}</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# 6. Middle Grid Layout (3 Columns)
mid_col1, mid_col2, mid_col3 = st.columns([4, 4, 4])

with mid_col1:
    st.markdown("### Top Cuisines (Horizontal Bar)")
    top_cuisines = filtered_df['Cuisines'].value_counts().head(5).reset_index()
    fig1 = px.bar(top_cuisines, x='count', y='Cuisines', orientation='h', template='plotly_dark')
    fig1.update_traces(marker_color='#00b4d8')
    fig1.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

with mid_col2:
    st.markdown("### Rating Text Mix (Donut Chart)")
    rating_mix = filtered_df['Rating text'].value_counts().reset_index()
    fig2 = px.pie(rating_mix, values='count', names='Rating text', hole=0.5, template='plotly_dark')
    fig2.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2, use_container_width=True)

with mid_col3:
    st.markdown("### Cost Trend (Vertical Bar)")
    fig3 = px.bar(filtered_df.groupby('Aggregate rating')['Average Cost for two'].mean().reset_index(), x='Aggregate rating', y='Average Cost for two', template='plotly_dark')
    fig3.update_traces(marker_color='#52b788')
    fig3.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig3, use_container_width=True)


# 7. Bottom Grid Layout (3 Columns)
bot_col1, bot_col2, bot_col3 = st.columns([4, 4, 4])

with bot_col1:
    st.markdown("### Rating Colors Count")
    fig4 = px.bar(filtered_df['Rating color'].value_counts().reset_index(), x='Rating color', y='count', template='plotly_dark')
    fig4.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig4, use_container_width=True)

with bot_col2:
    st.markdown("### Booking Split (Donut Chart)")
    booking_mix = filtered_df['Has Table booking'].value_counts().reset_index()
    fig5 = px.pie(booking_mix, values='count', names='Has Table booking', hole=0.5, template='plotly_dark', color_discrete_sequence=['#ffb703', '#219ebc'])
    fig5.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig5, use_container_width=True)

with bot_col3:
    st.markdown("### Votes distribution")
    fig6 = px.line(filtered_df.sort_values(by="Aggregate rating"), x="Aggregate rating", y="Votes", template='plotly_dark')
    fig6.update_traces(line_color='#e63946')
    fig6.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig6, use_container_width=True)
