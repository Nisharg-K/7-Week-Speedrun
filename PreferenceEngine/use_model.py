from pathlib import Path

import joblib
import numpy as np
import pandas as pd


ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"


def prompt_list(prompt_text):
    raw_value = input(prompt_text).strip()
    return [item.strip() for item in raw_value.split(",") if item.strip()]


def prompt_score(prompt_text):
    while True:
        raw_value = input(prompt_text).strip()
        try:
            value = float(raw_value)
        except ValueError:
            print("Enter a number between 1 and 5.")
            continue

        if 1 <= value <= 5:
            return value

        print("Enter a number between 1 and 5.")


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


def prompt_for_movie(director_choices):
    print("\n===== MOVIE QUESTIONS =====")
    print("Enter genres and writers as comma-separated values.")
    print(f"Known directors include: {', '.join(director_choices[:10])}")
    print("If the director is new, the model will still predict, but confidence may be lower.")

    genres = prompt_list("Genres: ")
    director = input("Director: ").strip()
    writers = prompt_list("Writers: ")
    acting = prompt_score("Acting score (1-5): ")
    story = prompt_score("Story score (1-5): ")
    music = prompt_score("Music score (1-5): ")

    return pd.DataFrame([
        {
            "Genre": genres,
            "Director": director,
            "Writers": writers,
            "Acting": acting,
            "Story": story,
            "Music": music,
        }
    ])


def main():
    reg_model = joblib.load(ARTIFACTS_DIR / "rating_model.joblib")
    clf_model = joblib.load(ARTIFACTS_DIR / "liked_model.joblib")
    genre_encoder = joblib.load(ARTIFACTS_DIR / "genre_encoder.joblib")
    writer_encoder = joblib.load(ARTIFACTS_DIR / "writer_encoder.joblib")
    director_encoder = joblib.load(ARTIFACTS_DIR / "director_encoder.joblib")
    scaler = joblib.load(ARTIFACTS_DIR / "numeric_scaler.joblib")
    director_choices = joblib.load(ARTIFACTS_DIR / "director_choices.joblib")

    while True:
        movie_df = prompt_for_movie(director_choices)
        movie_features = build_feature_matrix(
            movie_df,
            genre_encoder,
            writer_encoder,
            director_encoder,
            scaler,
        )

        predicted_rating = float(reg_model.predict(movie_features)[0])
        liked_probability = float(clf_model.predict_proba(movie_features)[0][1])
        predicted_liked = "Yes" if liked_probability >= 0.5 else "No"

        print("\n===== PREDICTION =====")
        print(f"Predicted rating: {predicted_rating:.2f}/5")
        print(f"Predicted liked: {predicted_liked}")
        print(f"Like probability: {liked_probability:.1%}")

        again = input("\nTry another movie? (y/n): ").strip().lower()
        if again not in {"y", "yes"}:
            break


if __name__ == "__main__":
    main()
