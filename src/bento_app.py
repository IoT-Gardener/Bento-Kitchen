import bentoml
import json
import numpy as np
import pandas as pd
from bentoml.io import NumpyNdarray, JSON
from pydantic import BaseModel

model = bentoml.sklearn.get("random_forest:latest").to_runner()

service = bentoml.Service("iris_classifier", runners=[model])


class Iris(BaseModel):
    Sepal_Length: float
    Sepal_Width: float
    Petal_Length: float
    Petal_Width: float

class IrisOutput(BaseModel):
    Result: int
    Model: str


@service.api(input=JSON(pydantic_model=Iris), output=JSON(pydantic_model=IrisOutput))
def predict(data: Iris) -> dict:

    # Create dataframe from input data
    df = pd.DataFrame(data.dict(), index=[0])

    # Predict data
    result = model.run(df)

    # Return dictionary containing results
    return json.dumps({"Results": int(result[0]), "Model": "Random Forest"})