import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Namma Metro EDA Dashboard",
    layout="wide"
)

st.title("🚇 Namma Metro – Exploratory Data Analysis Dashboard")

# ---------------- DATA LOADING ----------------
EXCEL_PATH = "dataset/namma_metro_dataset_10000.xlsx"

@st.cache_data
def load_data():
    df = pd.read_excel(EXCEL_PATH)
    return df

df = load_data()

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio(
    "Select Section",
    [
        "Dataset Overview",
        "Sample Records",
        "Numeric Analysis",
        "Categorical Analysis",
        "Correlation Analysis"
    ]
)

# ---------------- DATASET OVERVIEW ----------------
if menu == "Dataset Overview":
    st.subheader("📊 Dataset Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", df.shape[0])
        st.metric("Columns", df.shape[1])

    with col2:
        st.write("### Column Names")
        st.code(list(df.columns))

    st.write("### Data Types")
    st.dataframe(
        df.dtypes.astype(str)
        .reset_index()
        .rename(columns={"index": "Column", 0: "Data Type"})
    )

    st.write("### Missing Values")
    st.dataframe(
        df.isna().sum()
        .reset_index()
        .rename(columns={"index": "Column", 0: "Missing Values"})
    )

    st.write("### Duplicate Rows")
    st.write(df.duplicated().sum())

# ---------------- SAMPLE DATA ----------------
elif menu == "Sample Records":
    st.subheader("🧾 Sample Records")

    st.write("First 5 Rows")
    st.dataframe(df.head())

    st.write("Last 5 Rows")
    st.dataframe(df.tail())

# ---------------- NUMERIC ANALYSIS ----------------
elif menu == "Numeric Analysis":
    st.subheader("📈 Numeric Feature Analysis")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if not numeric_cols:
        st.warning("No numeric columns found in dataset.")
    else:
        selected_col = st.selectbox(
            "Select Numeric Column",
            numeric_cols
        )

        col1, col2 = st.columns(2)

        # Histogram
        with col1:
            st.write("Histogram with Distribution")
            fig, ax = plt.subplots()
            sns.histplot(df[selected_col].dropna(), kde=True, ax=ax)
            ax.set_xlabel(selected_col)
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

        # Boxplot
        with col2:
            st.write("Outlier Detection (Box Plot)")
            fig, ax = plt.subplots()
            sns.boxplot(x=df[selected_col].dropna(), ax=ax)
            ax.set_xlabel(selected_col)
            st.pyplot(fig)

        st.info(
            "📌 **Explanation:** Histogram shows data distribution, "
            "while box plot highlights outliers and spread."
        )

# ---------------- CATEGORICAL ANALYSIS ----------------
elif menu == "Categorical Analysis":
    st.subheader("📊 Categorical Feature Analysis")

    cat_cols = df.select_dtypes(exclude="number").columns.tolist()

    if not cat_cols:
        st.warning("No categorical columns found.")
    else:
        selected_cat = st.selectbox(
            "Select Categorical Column",
            cat_cols
        )

        top_values = df[selected_cat].astype(str).value_counts().head(15)

        st.bar_chart(top_values)

        st.info(
            "📌 **Explanation:** This chart shows frequency distribution "
            "of categories. It helps identify dominant passenger behavior "
            "such as popular stations, routes, or payment modes."
        )

# ---------------- CORRELATION ----------------
elif menu == "Correlation Analysis":
    st.subheader("🔗 Correlation Analysis")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if len(numeric_cols) < 2:
        st.warning("Not enough numeric columns for correlation.")
    else:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.heatmap(
            df[numeric_cols].corr(),
            annot=True,
            cmap="coolwarm",
            ax=ax
        )
        st.pyplot(fig)

        st.info(
            "📌 **Explanation:** Correlation heatmap shows relationships "
            "between numeric features. Strong correlation helps identify "
            "factors influencing ticket count or revenue."
        )

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("📌 Namma Metro EDA Dashboard | Built using Streamlit & Python")
