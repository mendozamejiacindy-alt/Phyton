from io import StringIO

import pandas as pd

CSV_DATA = """edad,ingresos,compras,cliente
22,15000,2,0
25,18000,3,0
28,22000,5,1
30,25000,6,1
35,30000,8,1
40,35000,10,1
23,16000,2,0
27,21000,4,0
32,28000,7,1
45,40000,12,1
"""


def load_data() -> pd.DataFrame:
    """Carga los datos de ejemplo en un DataFrame."""
    return pd.read_csv(StringIO(CSV_DATA))


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """Limpia los datos eliminando registros incompletos."""
    cleaned = data.dropna().copy()

    cleaned["edad"] = pd.to_numeric(cleaned["edad"])
    cleaned["ingresos"] = pd.to_numeric(cleaned["ingresos"])
    cleaned["compras"] = pd.to_numeric(cleaned["compras"])
    cleaned["cliente"] = pd.to_numeric(cleaned["cliente"])

    return cleaned


def get_features_and_target(
    data: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    """Separa las características de la variable objetivo."""
    features = data[["edad", "ingresos", "compras"]]
    target = data["cliente"]

    return features, target
