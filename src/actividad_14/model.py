from pathlib import Path

import joblib
from sklearn.linear_model import LogisticRegression  # type: ignore[import-untyped]
from sklearn.pipeline import Pipeline  # type: ignore[import-untyped]
from sklearn.preprocessing import StandardScaler  # type: ignore[import-untyped]

from .data import get_features_and_target


def create_model() -> Pipeline:
    """Crea el clasificador."""
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(random_state=42)),
        ]
    )


def train_model(data) -> Pipeline:
    """Entrena el modelo con los datos proporcionados."""
    features, target = get_features_and_target(data)

    model = create_model()
    model.fit(features, target)

    return model


def save_model(model: Pipeline, path: Path) -> None:
    """Guarda el modelo utilizando joblib."""
    joblib.dump(model, path)


def load_model(path: Path) -> Pipeline:
    """Carga un modelo previamente guardado."""
    return joblib.load(path)
