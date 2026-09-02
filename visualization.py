import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


def plot_visualizations(df):
    st.subheader("Visualizations")
    c1, c2 = st.columns(2)
    with c1:
        st.write("Survival by Sex")
        fig, ax = plt.subplots()
        sns.barplot(x="Sex", y="Survived", data=df.replace({"Sex": {0: "male", 1: "female"}}), ax=ax)
        st.pyplot(fig)

    with c2:
        st.write("Survival by Pclass")
        fig, ax = plt.subplots()
        sns.barplot(x="Pclass", y="Survived", data=df, ax=ax)
        st.pyplot(fig)

    c3, c4 = st.columns(2)
    with c3:
        st.write("Age distribution by Survival")
        fig, ax = plt.subplots()
        sns.kdeplot(data=df, x="Age", hue="Survived", common_norm=False, ax=ax)
        st.pyplot(fig)

    with c4:
        st.write("Fare distribution by Survival")
        fig, ax = plt.subplots()
        sns.boxplot(x="Survived", y="Fare", data=df, ax=ax)
        st.pyplot(fig)
    st.write("Heat map of correlations")
    fig, ax = plt.subplots()
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    st.write("Pair plot of features")
    fig = sns.pairplot(df, hue="Survived", diag_kind="kde", corner=True)   
    st.pyplot(fig)

    st.write("Count plot of Embarked by Survival")
    fig, ax = plt.subplots()        
    sns.countplot(x="Embarked", hue="Survived", data=df, ax=ax)
    st.pyplot(fig)