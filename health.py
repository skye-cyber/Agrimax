import numpy as np
import pandas

# Define optimal conditions for each cropas pd

crop_requirements = {
    'rice': {'pH': (6.0, 7.0), 'N': (80, 120), 'P': (70, 90), 'K': (100, 120)},
    'wheat': {'pH': (6.0, 6.5), 'N': (50, 100), 'P': (30, 70), 'K': (50, 100)},
    'maize': {'pH': (6.0, 6.8), 'N': (100, 150), 'P': (90, 120), 'K': (100, 150)},
    'sugarcane': {'pH': (6.5, 7.5), 'N': (80, 120), 'P': (60, 90), 'K': (90, 130)},
    'barley': {'pH': (5.5, 6.5), 'N': (30, 60), 'P': (30, 50), 'K': (50, 80)},
    'potato': {'pH': (5.0, 6.5), 'N': (60, 90), 'P': (50, 70), 'K': (50, 100)},
    'soybean': {'pH': (6.0, 6.8), 'N': (80, 120), 'P': (50, 90), 'K': (80, 110)},
    'coffee': {'pH': (6.0, 6.8), 'N': (80, 110), 'P': (60, 90), 'K': (80, 100)},
    'tea': {'pH': (5.0, 6.5), 'N': (60, 90), 'P': (30, 60), 'K': (50, 80)},
    'peas': {'pH': (5.5, 6.5), 'N': (50, 70), 'P': (30, 50), 'K': (40, 60)},
    'cotton': {'pH': (6.0, 7.5), 'N': (60, 100), 'P': (40, 80), 'K': (50, 100)},
    'tomato': {'pH': (5.5, 6.8), 'N': (100, 140), 'P': (60, 100), 'K': (80, 120)},
    'onion': {'pH': (6.0, 7.0), 'N': (50, 80), 'P': (40, 70), 'K': (30, 60)},
    'banana': {'pH': (5.5, 7.5), 'N': (150, 200), 'P': (80, 120), 'K': (150, 200)},
    'pepper': {'pH': (5.5, 6.8), 'N': (100, 140), 'P': (40, 80), 'K': (80, 120)},
    'cassava': {'pH': (5.5, 7.0), 'N': (50, 100), 'P': (30, 60), 'K': (40, 80)}
}


class Health:
    def __init__(self):
        self = self

    def normalize_metric(self, value, ideal_range):
        lower, upper = ideal_range
        if lower <= value <= upper:
            return 100  # Perfect fit within the range
        elif value < lower:
            # Deviation below the lower bound
            deviation = lower - value
            score = max(0, 100 - (deviation / lower * 100))
        else:
            # Deviation above the upper bound
            deviation = value - upper
            score = max(0, 100 - (deviation / upper * 100))

        return score

    def calculate_condition_suitability(self, crop, N, P, K, pH):
        req = crop_requirements[crop]
        recommendations = {}
        for crop in crop_requirements.keys():

            score = 0
            score += self.normalize_metric(N, req['N'])
            score += self.normalize_metric(P, req['P'])
            score += self.normalize_metric(K, req['K'])
            score += self.normalize_metric(pH, req['pH'])

            # Average score across all metrics
            recommendations[crop] = score / 4

        return sorted(recommendations.items(), key=lambda x: x[1], reverse=True)

    def calculate_soil_health(self, _crop, N, P, K, pH):
        req = crop_requirements[_crop]

        _eval = {}
        N = self.normalize_metric(N, req['N'])
        P = self.normalize_metric(P, req['P'])
        K = self.normalize_metric(K, req['K'])
        pH = self.normalize_metric(pH, req['pH'])

        score = N + P + K + pH
        for val, _eval_ in zip(('N', 'P', 'K', 'pH'), (N, P, K, pH)):
            _eval[val] = _eval_

        return score / 4, _eval


if __name__ == "__main__":
    # Example soil conditions
    N, P, K, pH = 60, 40, 70, 5.6

    init = Health()
    score, _eval = init.calculate_soil_health('wheat',
                                              N, P, K, pH)
    for key, val in _eval.items():
        print(f"{key.capitalize()}: {val:.2f}%")
    print(f"Total: {score:.2f}%")

    '''print("Soil Health Scores (out of 100):")
    for crop, score in recommendations:
        print(f"{crop.capitalize()}: {score:.2f}/100")'''
