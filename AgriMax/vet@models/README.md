---
license: gpl-3.0
language:
- en
metrics:
- accuracy
pipeline_tag: text-classification
tags:
- climate
---

# 🌾 Crop Recommendation Models

This repository contains a set of crop recommendation models for making optimal crop predictions based on soil, climate, and environmental factors. Each model provides probabilities for recommended crops based on the input data.

---

## Table of Contents

1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [Model Usage](#model-usage)
4. [Input Features](#input-features)
5. [Functions Overview](#functions-overview)
6. [Example Usage](#example-usage)
7. [Contributing](#contributing)
8. [License](#license)

---

## Overview

The crop recommendation models in this repository include classifiers trained on various environmental factors such as soil nutrients (N, P, K), temperature, humidity, pH, and rainfall to recommend the most suitable crops. These models are stored as `.pkl` files and can be loaded for predictions with the helper functions provided.

## Installation & Setup

First, install the required libraries:

```bash
pip install joblib numpy pandas
```

Clone the repository and download the models:

```bash
git clone https://github.com/skye-waves/CropRecommendation
cd CropRecommendation
```

Ensure you place your `.pkl` models in the specified `models` directory path or update the script to match your model path.

## Model Usage

To load and use the models, follow these steps:

### Load Models

The models are loaded from the specified path using `joblib`:

```python
import joblib

# Load the models
model_DC_63sm = joblib.load('models/DecisionTree063.05.pkl', mmap_mode='r')
model_RFC_63 = joblib.load('models/RFClassifier063.74.pkl', mmap_mode='r')
model_DC_63lg = joblib.load('models/DecisionTree.pkl', mmap_mode='r')
```

### Available Models

- **model_DC_63sm**: Decision Tree with version `063.05`
- **model_RFC_63**: Random Forest Classifier version `063.74`
- **model_DC_63lg**: A generalized Decision Tree model

## Input Features

Each model requires the following environmental and soil-related inputs:

- `N` - Soil Nitrogen level
- `P` - Soil Phosphorus level
- `K` - Soil Potassium level
- `temperature` - Environmental temperature in °C
- `humidity` - Environmental humidity in %
- `pH` - Soil pH level
- `rainfall` - Rainfall level in mm

## Functions Overview

### `predict_crop`

This function generates crop recommendations based on probabilities derived from the model:

```python
def predict_crop(model, N, P, K, temperature, humidity, ph, rainfall, n=10):
    # Input as DataFrame
    input_data = pd.DataFrame({
        'N': [N],
        'P': [P],
        'K': [K],
        'temperature': [temperature],
        'humidity': [humidity],
        'pH': [ph],
        'rainfall': [rainfall]
    })

    # Predict crop probabilities
    probabilities = model.predict_proba(input_data)
    labels = model.classes_

    # Top N recommendations sorted by probability
    recommendations = [(labels[i], probabilities[0][i]) for i in np.argsort(probabilities[0])[-n:]]
    recommendations.sort(key=lambda x: x[1], reverse=True)
    
    return recommendations
```

### `controller`

The `controller` function allows you to select a specific model or to predict using all models, returning the top crop recommendations:

```python
def controller(n, p, k, t, h, ph, r, _N=3, model=None):
    result = {}

    # Select a specific model
    if model:
        model_dict = {
            "model_RFC_63": model_RFC_63,
            "model_DC_63sm": model_DC_63sm,
            "model_DC_63lg": model_DC_63lg
        }
        model = model_dict.get(model)
        res = predict_crop(model, n, p, k, t, h, ph, r)
        result = dict(res)

    # Use all models if no specific one is chosen
    else:
        models = [model_DC_63sm, model_RFC_63, model_DC_63lg]
        for model in models:
            res = predict_crop(model, n, p, k, t, h, ph, r)
            result.update(dict(res))

    # Return sorted results by highest probability
    sorted_result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True)[:_N])
    for label, prob in sorted_result.items():
        print(f"{label}: {prob * 100:.2f}%")
    
    return sorted_result
```

## Example Usage

Using the `controller` function, you can easily make predictions with any of the models:

```python
# Define environmental and soil conditions
n, p, k = 10, 5, 5
temperature, humidity, ph, rainfall = 25.0, 60.0, 6.5, 150.0

# Run the controller for top 3 crop recommendations
recommendations = controller(n, p, k, temperature, humidity, ph, rainfall, _N=3, model="model_RFC_63")
print("Top Crop Recommendations:", recommendations)
```

## Contributing

We welcome contributions! Please submit pull requests or open issues to suggest improvements or report bugs.

## License

Distributed under the GPL License. See `LICENSE` for more details.

---

This `README.md` should serve as a comprehensive guide to using and understanding the crop recommendation model. Happy farming!