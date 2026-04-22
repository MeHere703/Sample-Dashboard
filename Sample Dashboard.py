import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image


# Load the Hypothetical Data
df = pd.read_excel("Hypothetical_Data.xlsx")


# Streamlit Layout
st.set_page_config(page_title="SDG Dashboard", layout="wide")


image = Image.open("Edited Banner.png")
st.image(image, width= 1200)


# Slider (Time Filter)
selected_year = st.slider(
    "Adjust slider to select the year",
    int(df["Year"].min()),
    int(df["Year"].max()),
    2010
)

filtered_df = df[df["Year"] == selected_year]


# Computing the Means to be presented in the Dashboard
avg_life = filtered_df["Life Expectancy"].mean()
avg_gdp = filtered_df["GDP per Capita"].mean()
avg_edu = filtered_df["Education Index"].mean()
avg_hea = filtered_df["Health Index"].mean()

# Presenting the KPIs withouth Loop
st.markdown(
    f"<p style='font-size:50px; color:#C6DCAB; font-weight:bold'>"
    f"📈 Mean Key Performance Indicators for Year {selected_year}"
    f"</p>",
    unsafe_allow_html=True
    )

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Mean Life Expectancy",
    f"{avg_life:.2f}",
    border=True
)

col2.metric(
    "Mean GDP per Capita",
    f"{avg_gdp:.0f}",
    border=1
)

col3.metric(
    "Mean Education Index",
    f"{avg_edu:.2f}",
    border=1
)

col4.metric(
    "Mean Health Index",
    f"{avg_hea:.2f}",
    border=1
)

# KPI Section
st.markdown(
    f"<p style='font-size:35px; color:#89ACA0; font-weight:bold'>"
    f"🗝️ Key Indicators by Country ({selected_year}) "
    f"</p>",
    unsafe_allow_html=True
    )

# Presenting the KPIs with Loop
for _, row in filtered_df.iterrows():

    st.markdown(f"## {row['Country']}")

    col5, col6, col7, col8 = st.columns(4)

    col5.markdown("#### Life Expectancy")
    col5.markdown(
    f"<p style='font-size:28px; color:#E9B8C9'>"
    f"{row['Life Expectancy']:.0f}"
    f"</p>",
    unsafe_allow_html=True
    )

    col6.markdown("##### GDP Per Capita")
    col6.markdown(
    f"<p style='font-size:28px; color:#93C193'>"
    f"{row['GDP per Capita']:.2f}"
    f"</p>",
    unsafe_allow_html=True
    )

    col7.markdown("##### Education Index")
    col7.markdown(
    f"<p style='font-size:28px; color:#F5CD6A'>"
    f"{row['Education Index']:.2f}"
    f"</p>",
    unsafe_allow_html=True
    )

    col8.markdown("##### Health Index")
    col8.markdown(
    f"<p style='font-size:28px; color:#EB8F48'>"
    f"{row['Health Index']:.2f}"
    f"</p>",
    unsafe_allow_html=True
    )

st.text("")
st.text("")

# Line Chart (Trend Over Time)
col9, col10 = st.columns(2)

with col9:
    st.markdown(
        f"<p style='font-size:30px; color:#C6DCAB; font-weight:bold;'>"
        f"Life Expectancy Trend 2000 - 2020"
        f"</p>",
        unsafe_allow_html=True
        )

    trend = df.groupby("Year")["Life Expectancy"].mean().reset_index()


    px.line()

    fig_line = px.line(
        trend,
        x="Year",
        y="Life Expectancy",
        color_discrete_sequence=["#C6DCAB"],
        title="Global Trend"
    )

    fig_line.update_layout(
        yaxis=dict(range=[0, trend["Life Expectancy"].max() + 10]) 
    )

    st.plotly_chart(fig_line, use_container_width=True)

st.text("")

# Bar Chart (Country Comparison)
with col10:
    st.markdown(
        f"<p style='font-size:30px; color:#5992C6; font-weight:bold;'>"
        f"Life Expectancy Comparison for {selected_year}"
        f"</p>",
        unsafe_allow_html=True
        )

    fig_bar = px.bar(
        filtered_df,
        x="Country",
        y="Life Expectancy",
        color="Country",
        title="Life Expectancy by Country"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

st.text("")


col11, col12 = st.columns(2)

# Scatter Plot (Drivers)

with col11:
    st.subheader("Relationship: GDP vs Life Expectancy")

    fig_scatter = px.scatter(
        df,
        x="GDP per Capita",
        y="Life Expectancy",
        color="Country",
        trendline="ols",
        title="GDP vs Life Expectancy"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

st.text("")

# Additional Visual (Bubble Chart)

with col12:
    st.subheader("Multi-variable View")

    fig_bubble = px.scatter(
        filtered_df,
        x="GDP per Capita",
        y="Life Expectancy",
        size="Education Index",
        color="Country",
        hover_name="Country",
        title="GDP, Education, and Life Expectancy"
    )

    st.plotly_chart(fig_bubble, use_container_width=True)


# Footer
st.markdown("## 💡 Insight")
st.markdown(
        f"<p style='font-size:60px; color:#F7BC60; font-weight:bold;'>"
        f"Higher GDP and education levels tend to be associated with higher life expectancy although other factors also play a role."
        f"</p>",
        unsafe_allow_html=True
        )
