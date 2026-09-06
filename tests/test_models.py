import pandas as pd
import numpy as np
from models import train_and_compare


def make_dummy_df(n=50):
    rng = np.random.RandomState(42)
    df = pd.DataFrame({
        'Pclass': rng.randint(1, 4, size=n),
        'Sex': rng.randint(0, 2, size=n),
        'Age': rng.normal(30, 10, size=n).clip(1),
        'Fare': rng.exponential(1.0, size=n) * 20,
        'Embarked': rng.randint(0, 3, size=n),
    })
    df['Survived'] = rng.randint(0, 2, size=n)
    return df


def test_train_and_compare_returns():
    df = make_dummy_df(100)
    feature_cols = ['Pclass', 'Sex', 'Age', 'Fare', 'Embarked']
    results_df, best_model = train_and_compare(df, feature_cols)
    assert hasattr(results_df, 'loc')
    assert results_df.shape[0] >= 1
    assert hasattr(best_model, 'predict')


def test_best_model_predicts_on_full_set():
    df = make_dummy_df(60)
    feature_cols = ['Pclass', 'Sex', 'Age', 'Fare', 'Embarked']
    _, best_model = train_and_compare(df, feature_cols)
    X = df[feature_cols]
    preds = best_model.predict(X)
    assert len(preds) == len(X)
