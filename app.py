from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.linear_model import LogisticRegression
import numpy as np
import os

app = FastAPI()

X_train = np.array([[2, 6], [8, 7], [3, 5], [5, 8], [9, 8], [1, 4]])
# Klasy: 0 (nie zdał), 1 (zdał)
y_train = np.array([0, 1, 0, 1, 1, 0])

model = LogisticRegression()
model.fit(X_train, y_train)


class ModelInput(BaseModel):
    godziny_nauki: float
    godziny_snu: float


@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
    return {"message": "Witaj w API serwującym model Machine Learning!"}


@app.post("/predict")
def predict(data: ModelInput):
    features = np.array([[data.godziny_nauki, data.godziny_snu]])

    prediction = model.predict(features)

    return {
        "przewidywana_klasa": int(prediction[0]),
        "podane_dane": {
            "godziny_nauki": data.godziny_nauki,
            "godziny_snu": data.godziny_snu
        }
    }

#Dodatkowe endpointy

@app.get("/info")
def model_info():
    return {
        "typ_modelu": "LogisticRegression",
        "liczba_cech": 2,
        "cechy": ["godziny_nauki", "godziny_snu"],
        "klasy": {"0": "Nie zdał", "1": "Zdał"}
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/config")
def get_config():
    tajny_klucz = os.getenv("SECRET_API_KEY", "Brak klucza")

    return {
        "wiadomosc": "Testowanie zmiennych środowiskowych",
        "twoj_klucz_api": tajny_klucz
    }