import pandas as pd
import dill

f = open("model.pickle", "rb")
data = dill.load(f)
f.close()

MODEL = data["model"]
MODEL_FEATURES = data["features"]
EXTRACT_FEATURES = data["extract_regular_features"]


def predict_rating(fen, solution):
    df = pd.DataFrame({
        "fen": [fen],
        "solution": [solution]
    })

    regular_features = EXTRACT_FEATURES(df).to_dict(orient="index")[0]

    all_features = pd.DataFrame([{
        **regular_features
    }])

    for c in set(MODEL_FEATURES) - set(all_features.columns):
        all_features[c] = 0

    return MODEL.predict(all_features[MODEL_FEATURES])[0]
