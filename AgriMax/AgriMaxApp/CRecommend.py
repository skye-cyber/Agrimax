import joblib
import numpy as np
import pandas as pd

# Load the model with mmap_mode='r' (read-only)
model_DC_65 = joblib.load(
    '../AgriMax/vet@models/DecisionTree65.35.pkl', mmap_mode='r')

model_RFC_63 = joblib.load(
    '../AgriMax/vet@models/RFClassifier063.74.pkl', mmap_mode='r')

model_DC_63 = joblib.load(
    '../AgriMax/vet@models/DecisionTree63.pkl', mmap_mode='r')


def predict_crop(model, N, P, K, temperature, humidity, ph, rainfall, n=10):
    # Prepare input data for prediction as a DataFrame
    input_data = pd.DataFrame({
        'N': [N],
        'P': [P],
        'K': [K],
        'temperature': [temperature],
        'humidity': [humidity],
        'pH': [ph],
        'rainfall': [rainfall]
    })

    # Make the prediction probabilities
    probabilities = model.predict_proba(input_data)

    # Get labels from the model classes
    labels = model.classes_

    # Get the indices of the top N probabilities
    top_indices = np.argsort(probabilities[0])[-n:]

    # Get the corresponding labels and probabilities

    recommendations = [(labels[i], probabilities[0][i]) for i in top_indices]
    recommendations.sort(key=lambda x: x[1], reverse=True)

    return recommendations


def controller(n, p, k, t, h, ph, r, _N: int = 3, model=None):
    result = {}

    if model:
        model_dict = {
            "model_RFC_63": model_RFC_63,
            "model_DC_65": model_DC_65,
            "model_DC_63": model_DC_63
        }
        model = model_dict.get(model)
        res = predict_crop(model,  n, p, k, t, h, ph, r)
        result = dict(res)

    else:
        models = [model_DC_65, model_RFC_63, model_DC_63]
        for model in models:
            # for n, p, k, t, h, ph, r in zip(N, P, K, T, H, PH, R):
            res = predict_crop(model,  n, p, k, t, h, ph, r)

            # max_label, max_prob = res  # key=lambda x: x[1])  # x[1] is the probability
            result.update(dict(res))

    s_result = dict(
        sorted(result.items(), key=lambda item: item[1], reverse=True)[:_N])
    for label, prob in s_result.items():
        print(f"\033[1;92m{label}: \033[1;94m{prob * 100:.2f}%\033[0m")

    return s_result
