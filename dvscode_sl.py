import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Streamlit page config
st.set_page_config(page_title="CSV Data Visualizer", layout="centered")
st.title("📊 CSV Data Visualizer")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Display basic info using StringIO
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()

    st.subheader("📌 DataFrame Info")
    st.text(info_str)

    st.subheader("📌 Preview of Your Data")
    st.write(df.head())

    st.subheader("📈 Descriptive Statistics")
    st.write(df.describe())

    st.subheader("🧼 Missing Values")
    st.write(df.isnull().sum())

    st.markdown("---")
    st.subheader("📊 Create Charts")

    chart_type = st.selectbox("Choose chart type", ["Histogram", "Bar Chart", "Line Chart", "Pie Chart"])

    fig, ax = plt.subplots()

    if chart_type == "Histogram":
        col = st.selectbox("Choose column for Histogram", df.select_dtypes(include=['float', 'int']).columns)
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        st.pyplot(fig)

    elif chart_type == "Bar Chart":
        col = st.selectbox("Choose column for Bar Chart", df.columns)
        df[col].value_counts().plot(kind="bar", ax=ax)
        st.pyplot(fig)

    elif chart_type == "Line Chart":
        x_col = st.selectbox("X-axis", df.columns)
        y_col = st.selectbox("Y-axis", df.select_dtypes(include=['float', 'int']).columns)
        sns.lineplot(x=df[x_col], y=df[y_col], ax=ax)
        st.pyplot(fig)

    elif chart_type == "Pie Chart":
        col = st.selectbox("Choose column for Pie Chart", df.columns)
        df[col].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_ylabel('')
        st.pyplot(fig)

    # Save chart as image
    st.markdown("---")
    st.subheader("📁 Save Current Graph")
    save = st.checkbox("Save the above chart as an image")
    if save:
        filename = st.text_input("Enter filename (without extension):", value="my_chart")
        if filename:
            fig.savefig(f"{filename}.png")
            st.success(f"Chart saved as {filename}.png in your current directory.")
