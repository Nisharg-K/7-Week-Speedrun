import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=env_path)

import joblib
import numpy as np
import pandas as pd


ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"
OMDB_BASE_URL = "https://www.omdbapi.com/"
api_key = os.getenv("api_key")

def parse_multi_value(text):
    if not text or text == "N/A":
        return []
    return [item.strip() for item in text.split(",") if item.strip()]


def clamp_score(value):
    return max(1.0, min(5.0, value))


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


def fetch_movie_details(title, api_key = api_key):
    query = urlencode({
        "apikey": api_key,
        "t": title,
        "type": "movie",
        "plot": "short",
        "r": "json",
    })
    url = f"{OMDB_BASE_URL}?{query}"

    try:
        with urlopen(url) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raw_message = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw_message)
            error_message = payload.get("Error") or raw_message
        except json.JSONDecodeError:
            error_message = raw_message or str(exc)
        raise ValueError(f"OMDb request failed ({exc.code}): {error_message}") from exc
    except URLError as exc:
        raise ValueError(f"Could not reach OMDb: {exc.reason}") from exc

    if payload.get("Response") != "True":
        raise ValueError(payload.get("Error", "Movie not found in OMDb."))

    return payload


def extract_rotten_tomatoes_score(movie_data):
    for rating in movie_data.get("Ratings", []):
        if rating.get("Source") == "Rotten Tomatoes":
            value = rating.get("Value", "").replace("%", "")
            try:
                return float(value) / 20.0
            except ValueError:
                return None
    return None


def infer_component_scores(movie_data):
    imdb_value = movie_data.get("imdbRating", "N/A")
    imdb_score = None if imdb_value == "N/A" else float(imdb_value) / 2.0

    metascore_value = movie_data.get("Metascore", "N/A")
    metascore = None if metascore_value == "N/A" else float(metascore_value) / 20.0

    rotten_score = extract_rotten_tomatoes_score(movie_data)

    available_scores = [score for score in [imdb_score, metascore, rotten_score] if score is not None]
    base_score = sum(available_scores) / len(available_scores) if available_scores else 3.0

    acting_score = clamp_score((base_score * 0.7) + ((imdb_score or base_score) * 0.3))
    story_score = clamp_score((base_score * 0.5) + ((metascore or base_score) * 0.5))
    music_score = clamp_score((base_score * 0.8) + ((rotten_score or base_score) * 0.2))

    return {
        "Acting": acting_score,
        "Story": story_score,
        "Music": music_score,
        "base_score": base_score,
        "imdb_score": imdb_score,
        "metascore_score": metascore,
        "rotten_score": rotten_score,
    }


def movie_payload_to_features(movie_data):
    inferred = infer_component_scores(movie_data)
    directors = parse_multi_value(movie_data.get("Director", ""))

    return pd.DataFrame([
        {
            "Genre": parse_multi_value(movie_data.get("Genre", "")),
            "Director": directors[0] if directors else "",
            "Writers": parse_multi_value(movie_data.get("Writer", "")),
            "Acting": inferred["Acting"],
            "Story": inferred["Story"],
            "Music": inferred["Music"],
        }
    ]), inferred


def load_artifacts():
    return {
        "reg_model": joblib.load(ARTIFACTS_DIR / "rating_model.joblib"),
        "clf_model": joblib.load(ARTIFACTS_DIR / "liked_model.joblib"),
        "genre_encoder": joblib.load(ARTIFACTS_DIR / "genre_encoder.joblib"),
        "writer_encoder": joblib.load(ARTIFACTS_DIR / "writer_encoder.joblib"),
        "director_encoder": joblib.load(ARTIFACTS_DIR / "director_encoder.joblib"),
        "scaler": joblib.load(ARTIFACTS_DIR / "numeric_scaler.joblib"),
    }


def get_api_key():
    api_key = os.getenv("api_key", "").strip()
    if api_key:
        return api_key

    api_key = input("Enter your OMDb API key: ").strip()
    if not api_key:
        raise ValueError("OMDb API key is required.")
    return api_key


def main():
    artifacts = load_artifacts()
    api_key = get_api_key()

    while True:
        title = input("\nMovie name: ").strip()
        if not title:
            print("Enter a movie name.")
            continue

        try:
            movie_data = fetch_movie_details(title, api_key)
            movie_df, inferred = movie_payload_to_features(movie_data)
            movie_features = build_feature_matrix(
                movie_df,
                artifacts["genre_encoder"],
                artifacts["writer_encoder"],
                artifacts["director_encoder"],
                artifacts["scaler"],
            )
        except Exception as exc:
            print(f"Could not fetch movie details: {exc}")
            continue

        predicted_rating = float(artifacts["reg_model"].predict(movie_features)[0])
        liked_probability = float(artifacts["clf_model"].predict_proba(movie_features)[0][1])
        predicted_liked = "Yes" if liked_probability >= 0.5 else "No"

        print("\n===== FETCHED DETAILS =====")
        print(f"Title: {movie_data.get('Title', 'N/A')} ({movie_data.get('Year', 'N/A')})")
        print(f"Genres: {movie_data.get('Genre', 'N/A')}")
        print(f"Director: {movie_data.get('Director', 'N/A')}")
        print(f"Writers: {movie_data.get('Writer', 'N/A')}")
        print(f"IMDb rating: {movie_data.get('imdbRating', 'N/A')}")
        print(f"Metascore: {movie_data.get('Metascore', 'N/A')}")

        print("\n===== MODEL INPUT USED =====")
        print(f"Acting proxy: {inferred['Acting']:.2f}/5")
        print(f"Story proxy: {inferred['Story']:.2f}/5")
        print(f"Music proxy: {inferred['Music']:.2f}/5")

        print("\n===== PREDICTION =====")
        print(f"Predicted rating: {predicted_rating:.2f}/5")
        print(f"Predicted liked: {predicted_liked}")
        print(f"Like probability: {liked_probability:.1%}")

        again = input("\nTry another movie? (y/n): ").strip().lower()
        if again not in {"y", "yes"}:
            break


if __name__ == "__main__":
    main()
