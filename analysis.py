# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 10:42:21 2025

@author: nabil
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Suicide Rate Analysis", layout="wide")

# -----------------------------
# Theme Toggle
# -----------------------------
theme_choice = st.radio("🎨 Choose Theme:", ["Light", "Dark"], horizontal=True)

if theme_choice == "Dark":
    px.defaults.template = "plotly_dark"
else:
    px.defaults.template = "plotly_white"


# -----------------------------
# Title
# -----------------------------
st.title("📊 Suicide Rate Analysis")

# -----------------------------
# File Uploader
# -----------------------------
uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

# Cache function to improve performance
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    # Clean country names (avoid whitespace issues)
    df["country"] = df["country"].str.strip()
    return df

if uploaded_file:
    df = load_data(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # Show dataset info in expander
    with st.expander("ℹ About Dataset"):
        st.write(df.head())

    # -----------------------------
    # Visualizations
    # -----------------------------

    # 1. Total suicides per year
    st.subheader("📈 Total Suicides Per Year")
    suicides_per_year = df.groupby("year")["suicides_no"].sum().reset_index()
    fig_year = px.line(
        suicides_per_year, x="year", y="suicides_no", markers=True,
        title="Total Suicides Per Year"
    )
    st.plotly_chart(fig_year, use_container_width=True)

    # 2. Suicides by gender
    st.subheader("👥 Suicides by Gender")
    suicides_gender = df.groupby("sex")["suicides_no"].sum().reset_index()
    fig_gender = px.bar(
        suicides_gender, x="sex", y="suicides_no", color="sex",
        title="Total Suicides by Gender",
        color_discrete_map={"male":"skyblue","female":"pink"}
    )
    st.plotly_chart(fig_gender, use_container_width=True)

    # 3. Suicides by country (top 10)
    st.subheader("🌍 Suicides by Country (Top 10)")
    top_countries = df.groupby("country")["suicides_no"].sum().sort_values(ascending=False).head(10).reset_index()
    fig_country = px.bar(
        top_countries, x="country", y="suicides_no", color="country",
        title="Top 10 Countries by Total Suicides"
    )
    st.plotly_chart(fig_country, use_container_width=True)

    # 4. Age-wise analysis
    st.subheader("📊 Suicides by Age Group")
    if "age" in df.columns:
        suicides_age = df.groupby("age")["suicides_no"].sum().reset_index()
        fig_age = px.bar(
            suicides_age, x="age", y="suicides_no", color="age",
            title="Total Suicides by Age Group"
        )
        st.plotly_chart(fig_age, use_container_width=True)

    # 5. GDP vs suicides (if column exists)
    if "gdp_per_capita ($)" in df.columns:
        st.subheader("💰 GDP per Capita vs Suicides")
        fig_gdp = px.scatter(
            df, x="gdp_per_capita ($)", y="suicides_no", color="country",
            trendline="ols", title="GDP per Capita vs Suicides"
        )
        st.plotly_chart(fig_gdp, use_container_width=True)

    # 6. World map
    st.subheader("🗺 World Suicide Map")
    country_suicides = df.groupby("country")["suicides_no"].sum().reset_index()
    fig_map = px.choropleth(
        country_suicides, locations="country", locationmode="country names",
        color="suicides_no", hover_name="country",
        title="Total Suicides by Country"
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.subheader("📌 Filter by Country and Year")

    countries = st.multiselect(
        "Select countries:",
        df["country"].unique()
    )

    years = st.slider(
        "Select year range:",
        int(df["year"].min()), int(df["year"].max()),
        (int(df["year"].min()), int(df["year"].max()))
    )

    filtered_df = df[
        (df["year"].between(years[0], years[1]))
        & (df["country"].isin(countries) if countries else True)
    ]

    # 7. Filtered line chart
    st.subheader("📉 Filtered Country Trends")
    if not filtered_df.empty:
        fig_filtered = px.line(
            filtered_df, x="year", y="suicides_no", color="country",
            markers=True, title="Suicides in Selected Countries"
        )
        st.plotly_chart(fig_filtered, use_container_width=True)
    else:
        st.warning("⚠ No data available for selected filters.")

    # -----------------------------
    # Download Button
    # -----------------------------
    st.download_button(
        "💾 Download Filtered Data",
        filtered_df.to_csv(index=False),
        "filtered_data.csv",
        "text/csv"
    )

else:
    st.info("📌 Please upload a CSV file to start analysis.")