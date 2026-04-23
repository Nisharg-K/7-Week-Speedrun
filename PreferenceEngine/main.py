from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, MultiLabelBinarizer, OneHotEncoder
from xgboost import XGBClassifier, XGBRegressor


ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"


def split_multi_value(text):
    if pd.isna(text):
        return []
    return [item.strip() for item in str(text).split(",") if item.strip()]


def make_director_encoder():
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def build_feature_matrix(dataframe, genre_encoder, writer_encoder, director_encoder, scaler):
    genre_encoded = genre_encoder.transform(dataframe["Genre"])
    writer_encoded = writer_encoder.transform(dataframe["Writers"])
    director_encoded = director_encoder.transform(dataframe[["Director"]])
    numeric_scaled = scaler.transform(dataframe[["Acting", "Story", "Music"]])

    return np.hstack([
        genre_encoded,
        writer_encoded,
        director_encoded,
        numeric_scaled,
    ])


def main():
    data_path = Path(__file__).resolve().parent / "PatelTalkiesFilms.csv"
    df = pd.read_csv(data_path, encoding="latin-1")

    df["Liked"] = df["Liked"].map({"Yes": 1, "No": 0})
    df["Genre"] = df["Genre"].apply(split_multi_value)
    df["Writers"] = df["Writers"].apply(split_multi_value)

    genre_encoder = MultiLabelBinarizer()
    writer_encoder = MultiLabelBinarizer()
    director_encoder = make_director_encoder()
    scaler = MinMaxScaler()

    genre_encoder.fit(df["Genre"])
    writer_encoder.fit(df["Writers"])
    director_encoder.fit(df[["Director"]])
    scaler.fit(df[["Acting", "Story", "Music"]])

    X = build_feature_matrix(df, genre_encoder, writer_encoder, director_encoder, scaler)
    y_rating = df["Rating"]
    y_liked = df["Liked"]

    X_train, X_test, y_r_train, y_r_test, y_l_train, y_l_test = train_test_split(
        X,
        y_rating,
        y_liked,
        test_size=0.2,
        random_state=42,
    )

    reg_model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
    )
    reg_model.fit(X_train, y_r_train)

    clf_model = XGBClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="logloss",
    )
    clf_model.fit(X_train, y_l_train)

    y_pred_r = reg_model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_r_test, y_pred_r))

    y_pred_l = clf_model.predict(X_test)
    accuracy = accuracy_score(y_l_test, y_pred_l)

    ARTIFACTS_DIR.mkdir(exist_ok=True)
    joblib.dump(reg_model, ARTIFACTS_DIR / "rating_model.joblib")
    joblib.dump(clf_model, ARTIFACTS_DIR / "liked_model.joblib")
    joblib.dump(genre_encoder, ARTIFACTS_DIR / "genre_encoder.joblib")
    joblib.dump(writer_encoder, ARTIFACTS_DIR / "writer_encoder.joblib")
    joblib.dump(director_encoder, ARTIFACTS_DIR / "director_encoder.joblib")
    joblib.dump(scaler, ARTIFACTS_DIR / "numeric_scaler.joblib")
    joblib.dump(sorted(df["Director"].dropna().unique().tolist()), ARTIFACTS_DIR / "director_choices.joblib")

    print("\n===== MODEL RESULTS =====")
    print(f"RMSE (Rating): {rmse:.3f}")
    print(f"Accuracy (Liked): {accuracy:.3f}")
    print(f"Saved trained models and preprocessors to: {ARTIFACTS_DIR}")


if __name__ == "__main__":
    main()
