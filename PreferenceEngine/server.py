from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd
import joblib
import os
from typing import Optional

from use_model_api import fetch_movie_details, movie_payload_to_features
from use_model import ARTIFACTS_DIR, build_feature_matrix



app = FastAPI() 
app.mount("/static", StaticFiles(directory="static"), name="static")


class SubmitRequest(BaseModel):
    movie_name: Optional[str] = None
    genre: Optional[str] = None
    director: Optional[str] = None
    writers: Optional[str] = None
    acting_score: Optional[float] = None
    story_score: Optional[float] = None
    music_score: Optional[float] = None
    manual_entry: bool = True


def split_csv_values(raw_text: str):
    return [item.strip() for item in raw_text.split(",") if item.strip()]


reg_model = joblib.load(ARTIFACTS_DIR / "rating_model.joblib")
clf_model = joblib.load(ARTIFACTS_DIR / "liked_model.joblib")
genre_encoder = joblib.load(ARTIFACTS_DIR / "genre_encoder.joblib")
writer_encoder = joblib.load(ARTIFACTS_DIR / "writer_encoder.joblib")
director_encoder = joblib.load(ARTIFACTS_DIR / "director_encoder.joblib")
scaler = joblib.load(ARTIFACTS_DIR / "numeric_scaler.joblib")



@app.get("/")
def read_root():
   #Serve index.html using FastAPI's StaticFiles
   return FileResponse("static/index.html")


@app.post("/submit")
def submit_form(payload: SubmitRequest):
    if payload.manual_entry:
        missing_fields = [
            field_name
            for field_name, field_value in {
                "genre": payload.genre,
                "director": payload.director,
                "writers": payload.writers,
                "acting_score": payload.acting_score,
                "story_score": payload.story_score,
                "music_score": payload.music_score,
            }.items()
            if field_value is None or field_value == ""
        ]

        if missing_fields:
            raise HTTPException(
                status_code=400,
                detail=f"Missing manual entry fields: {', '.join(missing_fields)}",
            )

        # Convert user values into the same shape used during training.
        df = pd.DataFrame(
            {
                "Genre": [split_csv_values(payload.genre)],
                "Director": [payload.director],
                "Writers": [split_csv_values(payload.writers)],
                "Acting": [payload.acting_score],
                "Story": [payload.story_score],
                "Music": [payload.music_score],
            }
        )

        feature_matrix = build_feature_matrix(
            df,
            genre_encoder,
            writer_encoder,
            director_encoder,
            scaler,
        )
    else:
        if not payload.movie_name:
            raise HTTPException(status_code=400, detail="Movie name is required when manual entry is disabled.")

        api_key = os.getenv("api_key", "").strip()
        if not api_key:
            raise HTTPException(status_code=500, detail="OMDb API key is not configured on the server.")

        movie_data = fetch_movie_details(payload.movie_name, api_key)
        movie_df, _ = movie_payload_to_features(movie_data)
        feature_matrix = build_feature_matrix(
            movie_df,
            genre_encoder,
            writer_encoder,
            director_encoder,
            scaler,
        )

    predicted_rating = float(reg_model.predict(feature_matrix)[0])
    liked_probability = float(clf_model.predict_proba(feature_matrix)[0][1])
    predicted_liked = "Yes" if liked_probability >= 0.5 else "No"

    return {
        "message": "Form submitted successfully!",
        "predicted_rating": predicted_rating,
        "predicted_liked": predicted_liked,
        "like_probability": liked_probability,
    }
