import pandas as pd
from clean import clean_data


def test_drop_columns():
    df = pd.DataFrame({
        'PassengerId': [1],
        'Name': ['a'],
        'Ticket': ['x'],
        'Cabin': ['C23'],
        'Age': [22],
        'Sex': ['male'],
        'Embarked': ['S'],
        'Fare': [7.25],
    })
    out = clean_data(df)
    for c in ['PassengerId', 'Name', 'Ticket', 'Cabin']:
        assert c not in out.columns


def test_fill_missing_values():
    df = pd.DataFrame({
        'Age': [None, 30],
        'Fare': [None, 15.0],
        'Embarked': [None, 'C'],
        'Sex': ['female', 'male'],
    })
    out = clean_data(df)
    assert out['Age'].isnull().sum() == 0
    assert out['Fare'].isnull().sum() == 0
    assert out['Embarked'].isnull().sum() == 0


def test_map_sex_and_embarked():
    df = pd.DataFrame({
        'Sex': ['male', 'female'],
        'Embarked': ['S', 'Q']
    })
    out = clean_data(df)
    assert set(out['Sex'].unique()) <= {0, 1}
    assert set(out['Embarked'].unique()) <= {0, 1, 2}
