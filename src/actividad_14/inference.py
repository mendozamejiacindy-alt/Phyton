import pandas as pd
from sklearn.pipeline import Pipeline  # type: ignore[import-untyped]


def predict(model: Pipeline, data: pd.DataFrame) -> list[int]:
    """Realiza predicciones con el modelo entrenado."""
    predictions = model.predict(data)

    return [int(value) for value in predictions]
