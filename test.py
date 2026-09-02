import streamlit as st
import pandas as pd


def render_prediction_form(features, model):
    with st.form("predict_form"):
        inputs = {}
        for f in features:
            if f == "Pclass":
                inputs[f] = st.selectbox("Pclass", [1, 2, 3], index=0)
            elif f == "Sex":
                s = st.radio("Sex", ["male", "female"]) 
                inputs[f] = 0 if s == "male" else 1
            elif f == "Embarked":
                e = st.selectbox("Embarked", ["S", "C", "Q"], index=0)
                inputs[f] = {"S": 0, "C": 1, "Q": 2}[e]
            elif f in ["Age", "Fare"]:
                inputs[f] = st.number_input(f, value=30.0)
            else:
                inputs[f] = st.number_input(f, value=0)

        submit = st.form_submit_button("Predict")

    if submit:
        x = pd.DataFrame([inputs])
        pred = model.predict(x)[0]
        prob = None
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(x)[0, 1]

        st.write("Prediction:", "Survived" if pred == 1 else "Not survived")
        if prob is not None:
            st.write(f"Survival probability: {prob:.2f}")
