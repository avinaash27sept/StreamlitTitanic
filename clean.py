import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for c in ["PassengerId", "Name", "Ticket", "Cabin"]:
        if c in df.columns:
            df.drop(columns=c, inplace=True)

    if "Age" in df.columns:
        df["Age"] = df["Age"].fillna(df["Age"].median())

    if "Embarked" in df.columns:
        df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode().iat[0])

    if "Fare" in df.columns:
        df["Fare"] = df["Fare"].fillna(df["Fare"].median())

    if "Sex" in df.columns:
        df["Sex"] = df["Sex"].map({"male": 0, "female": 1}).astype(int)

    if "Embarked" in df.columns:
        df["Embarked"] = df["Embarked"].map({"S": 0, "C": 1, "Q": 2}).fillna(0).astype(int)

    # return df
