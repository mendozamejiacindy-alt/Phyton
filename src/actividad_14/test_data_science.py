from pathlib import Path

import pandas as pd

from .data import (
    clean_data,
    get_features_and_target,
    load_data,
)
from .inference import predict
from .model import (
    load_model,
    save_model,
    train_model,
)


def test_load_and_clean_data() -> None:
    data = load_data()
    cleaned = clean_data(data)

    assert isinstance(cleaned, pd.DataFrame)
    assert not cleaned.isnull().values.any()
    assert len(cleaned) > 0


def test_get_features_and_target() -> None:
    data = clean_data(load_data())

    features, target = get_features_and_target(data)

    assert list(features.columns) == ["edad", "ingresos", "compras"]
    assert len(features) == len(target)


def test_train_model() -> None:
    data = clean_data(load_data())

    model = train_model(data)

    assert hasattr(model, "predict")


def test_inference() -> None:
    data = clean_data(load_data())
    model = train_model(data)

    features, _ = get_features_and_target(data)
    predictions = predict(model, features)

    assert len(predictions) == len(data)
    assert all(value in (0, 1) for value in predictions)


def test_save_and_load_model(tmp_path: Path) -> None:
    data = clean_data(load_data())
    model = train_model(data)

    model_path = tmp_path / "modelo.joblib"

    save_model(model, model_path)

    assert model_path.exists()

    loaded_model = load_model(model_path)

    features, _ = get_features_and_target(data)

    original_predictions = predict(model, features)
    loaded_predictions = predict(loaded_model, features)

    assert original_predictions == loaded_predictions
