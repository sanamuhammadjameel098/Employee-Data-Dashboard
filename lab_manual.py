
import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Employee Data Dashboard",
    page_icon="📊",
    layout="wide"
)

# Black Theme CSS
st.markdown("""
<style>
.stApp {
    background-color: #000000;
    color: white;
}

[data-testid="stHeader"] {
    background-color: #000000;
}

[data-testid="stSidebar"] {
    background-color: #111111;
}

h1, h2, h3, p, label {
    color: white !important;
}

[data-testid="stMetric"] {
    background-color: #171717;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #333333;
}

.stButton button {
    background-color: #333333;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)


# Load Dataset
st.title("📊 Employee Data Dashboard")
st.write("Welcome to Employee Data Analysis System")

try:
    df = pd.read_csv("Employee.csv")

    # Clean Column Names
    df.columns = df.columns.str.strip()

    st.success("Employee dataset loaded successfully!")

    # Interactive Widget 1
    search = st.text_input("Search Employee")

    # Interactive Widget 2
    selected_column = st.selectbox(
        "Select Column for Analysis",
        df.columns.tolist()
    )

    # Filter Employee Records
    filtered_df = df.copy()

    if search:
        mask = filtered_df.astype(str).apply(
            lambda col: col.str.contains(
                search,
                case=False,
                na=False
            )
        ).any(axis=1)

        filtered_df = filtered_df[mask]

    # Employee Summary
    st.subheader("Employee Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Employees", len(df))

    with col2:
        st.metric("Displayed Records", len(filtered_df))

    # Display DataFrame
    st.subheader("Employee Data Table")
    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    # Display Chart
    st.subheader("Employee Data Chart")

    if pd.api.types.is_numeric_dtype(df[selected_column]):

        chart_data = (
            df[selected_column]
            .dropna()
            .value_counts()
            .sort_index()
        )

        st.bar_chart(chart_data)

    else:

        chart_data = (
            df[selected_column]
            .value_counts()
            .head(10)
        )

        st.bar_chart(chart_data)


except FileNotFoundError:

    st.error(
        "Employee.csv file not found. "
        "Please keep Employee.csv in the same folder "
        "as lab_manual.py."
    )


except Exception as e:

    st.error(f"Error: {e}")
