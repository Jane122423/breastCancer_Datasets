import streamlit as st
st.set_page_config(page_title="Breast Cancer Dashboard", layout="centered")  # MUST be at the top

import pandas as pd
import plotly.express as px

# --- Load & clean the dataset ---
@st.cache_data
def load_data():
    df = pd.read_csv("breastCancer.csv")
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# --- Function to identify column types ---
def grab_col_names(dataframe, cat_th=10, car_th=20):
    cat_cols = [col for col in dataframe.columns if dataframe[col].dtype == "object"]
    num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique() < cat_th and dataframe[col].dtype != "object"]
    cat_but_car = [col for col in dataframe.columns if dataframe[col].nunique() > car_th and dataframe[col].dtype == "object"]
    cat_cols = list(set(cat_cols + num_but_cat) - set(cat_but_car))
    num_cols = [col for col in dataframe.columns if dataframe[col].dtype != "object" and col not in num_but_cat]
    return cat_cols, num_cols

# --- Get categorical and numerical columns ---
cat_cols, num_cols = grab_col_names(df)

# --- Streamlit layout ---
st.title("🧬 Breast Cancer Data Dashboard")

# --- Dropdowns for user input ---
target_var = st.selectbox("🎯 Select Target Variable (Categorical):", cat_cols)
numeric_col = st.selectbox("📈 Select Numerical Feature:", num_cols)

# --- Box Plot ---
st.subheader(f"📊 Boxplot of {numeric_col} by {target_var}")
box_fig = px.box(df, x=target_var, y=numeric_col, color=target_var,
                 title=f"Boxplot of {numeric_col} by {target_var}")
st.plotly_chart(box_fig, use_container_width=True)

# --- Histogram ---
st.subheader(f"📉 Distribution of {numeric_col} by {target_var}")
hist_fig = px.histogram(df, x=numeric_col, color=target_var, barmode='overlay',
                        marginal="box", nbins=30,
                        title=f"Distribution of {numeric_col} by {target_var}")
st.plotly_chart(hist_fig, use_container_width=True)
