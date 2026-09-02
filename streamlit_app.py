import streamlit as st
import pandas as pd

from clean import clean_data
from visualization import plot_visualizations
from models import train_and_compare
from test import render_prediction_form


@st.cache_data
def load_data(path="titanic.csv"):
    return pd.read_csv(path)


def initial_metrics(df):
    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing values": int(df.isnull().sum().sum()),
    }


def main():
    st.set_page_config(page_title="Titanic Data Prediction", layout="wide")
    st.title("Titanic Data Prediction")

    nav = st.sidebar.radio("Navigation", ["Home", "Data File", "Data Cleaning", "Data Visualization", "Model Creation", "Predict"])

    # quick links
    st.sidebar.markdown("---")
    st.sidebar.markdown("[App README](README.md)")

    df = load_data()

    if nav == "Home":
        st.write("Welcome to the Titanic data prediction app. Use the sidebar to navigate.")

    if nav == "Data File":
        st.subheader("Dataset")
        st.write(initial_metrics(df))
        st.dataframe(df)

    if nav == "Data Cleaning":
        st.subheader("Data Cleaning")
        if "cleaned_df" not in st.session_state:
            st.session_state["cleaned_df"] = None

        if st.button("Clean data"):
            st.session_state["cleaned_df"] = clean_data(df)
            st.success("Data cleaned and stored in session")

        if st.session_state.get("cleaned_df") is not None:
            with st.expander("View cleaned dataframe"):
                st.dataframe(st.session_state["cleaned_df"])

    if nav == "Data Visualization":
        st.subheader("Data Visualization")
        cleaned = st.session_state.get("cleaned_df")
        viz_df = cleaned if cleaned is not None else clean_data(df)
        plot_visualizations(viz_df)

    if nav == "Model Creation":
        st.subheader("Train models and compare")
        cleaned = st.session_state.get("cleaned_df")
        work_df = cleaned if cleaned is not None else clean_data(df)
        candidate_features = [c for c in work_df.columns if c != "Survived"]
        st.write("Select features to use for training")
        chosen = st.multiselect("Features", candidate_features, default=["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"])

        if st.button("Train and compare"):
            if not chosen:
                st.error("Choose at least one feature")
            else:
                results_df, best_model = train_and_compare(work_df, chosen)
                st.dataframe(results_df)
                st.session_state["best_model"] = best_model
                st.session_state["feature_cols"] = chosen
                st.success("Training complete — best model saved in session")

    if nav == "Predict":
        st.subheader("Make a prediction")
        if "best_model" not in st.session_state or st.session_state["best_model"] is None:
            st.info("No trained model found. Train a model first in 'Model Creation'.")
        else:
            model = st.session_state["best_model"]
            features = st.session_state.get("feature_cols", [])
            render_prediction_form(features, model)


if __name__ == "__main__":
    main()
