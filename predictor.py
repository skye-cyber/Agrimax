import joblib
import numpy as np
import pandas as pd

# Load the model with mmap_mode='r' (read-only)
model1_DC_63 = joblib.load(
    '/home/skye/skye@fieldmanagement/vet@models/DecisionTree063.05.pkl', mmap_mode='r')

model1_RFC_63 = joblib.load(
    '/home/skye/skye@fieldmanagement/vet@models/RFClassifier063.74.pkl', mmap_mode='r')

model2_DC_63 = joblib.load(
    '/home/skye/skye@fieldmanagement/vet@models/DecisionTree.pkl', mmap_mode='r')

model = joblib.load(
    '/home/skye/skye@fieldmanagement/super@models/LightGBM.pkl', mmap_mode='r')

N = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
P = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
K = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
T = [10, 12, 14, 16, 17, 20, 22, 25, 27, 29, 31, 33]
H = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
PH = [5.0, 5.5, 5.7, 6.0, 6.2, 6.5, 6.8, 7.2, 7.5, 8, 8.5, 8.7]
R = [100, 200, 290, 350, 400, 480, 670, 850, 1000, 1500, 1800, 2000]


def predict_crop(N, P, K, temperature, humidity, ph, rainfall, n=10):
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


def controller(model=None, _N: int = 3):
    result = {}
    models = [model1_RFC_63, model1_DC_63]
    for model in models:
        for n, p, k, t, h, ph, r in zip(N, P, K, T, H, PH, R):
            res = predict_crop(model,  n, p, k, t, h, ph, r, n=10)
            # max_label, max_prob = res  # key=lambda x: x[1])  # x[1] is the probability
            result = dict(res)

    # print(result)
    s_result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True)[:_N])
    for label, prob in s_result.items():
        print(f"\033[1;92m{label}: \033[1;94m{prob * 100:.2f}%\033[0m")


def evaluate_soil_health(N, P, K, temperature, humidity, ph, rainfall):
    # Sample thresholds for nutrient levels, pH, and other environmental variables
    N_threshold = 50
    P_threshold = 30
    K_threshold = 20
    pH_ideal = 6.5
    temperature_ideal = 25
    humidity_ideal = 60
    rainfall_ideal = 100

    # Create a dictionary to store the evaluation and suggestions
    soil_report = {}

    # Nitrogen evaluation
    if N < N_threshold:
        soil_report['Nitrogen'] = f"Low Nitrogen levels. Consider adding more nitrogen (N={
            N})"
    else:
        soil_report['Nitrogen'] = f"Good Nitrogen levels (N={N})"

    # Phosphorus evaluation
    if P < P_threshold:
        soil_report['Phosphorus'] = f"Low Phosphorus levels. Consider adding more phosphorus (P={
            P})"
    else:
        soil_report['Phosphorus'] = f"Good Phosphorus levels (P={P})"

    # Potassium evaluation
    if K < K_threshold:
        soil_report['Potassium'] = f"Low Potassium levels. Consider adding more potassium (K={
            K})"
    else:
        soil_report['Potassium'] = f"Good Potassium levels (K={K})"

    # pH evaluation
    if ph < pH_ideal - 0.5 or ph > pH_ideal + 0.5:
        soil_report['pH'] = f"Non-ideal pH levels. Adjust pH closer to {
            pH_ideal} (Current pH={ph})"
    else:
        soil_report['pH'] = f"Good pH levels (pH={ph})"

    # Temperature evaluation
    if temperature < temperature_ideal - 5 or temperature > temperature_ideal + 5:
        soil_report['Temperature'] = f"Non-ideal temperature. Try to maintain around {
            temperature_ideal}°C (Current={temperature}°C)"
    else:
        soil_report['Temperature'] = f"Good temperature (Current={
            temperature}°C)"

    # Humidity evaluation
    if humidity < humidity_ideal - 10 or humidity > humidity_ideal + 10:
        soil_report['Humidity'] = f"Non-ideal humidity. Ideal is around {
            humidity_ideal}% (Current={humidity}%)"
    else:
        soil_report['Humidity'] = f"Good humidity (Current={humidity}%)"

    # Rainfall evaluation
    if rainfall < rainfall_ideal - 50 or rainfall > rainfall_ideal + 50:
        soil_report['Rainfall'] = f"Rainfall levels are not ideal. Ideal is around {
            rainfall_ideal} mm (Current={rainfall} mm)"
    else:
        soil_report['Rainfall'] = f"Good rainfall (Current={rainfall} mm)"

    return soil_report


def get_valid_input(prompt):
    while True:
        try:
            val = float(input(prompt))
            return val
        except ValueError:
            print("\033[31mInvalid input. Please enter a numeric value.\033[0m")


def main():
    try:
        # Collect inputs with validation
        N = get_valid_input(
            "\033[94mPlease Enter N(Nitrogen Level): \033[0;1m")
        P = get_valid_input(
            "\033[94mPlease Enter P(Phosphorous Level): \033[0;1m")
        K = get_valid_input(
            "\033[94mPlease Enter K(Potassium Level): \033[0;1m")
        temperature = get_valid_input(
            "\033[94mPlease Enter temperature: \033[0;1m")
        humidity = get_valid_input("\033[94mPlease Enter humidity: \033[0;1m")
        ph = get_valid_input("\033[94mPlease Enter pH: \033[0;1m")
        rainfall = get_valid_input("\033[94mPlease Enter rainfall: \033[0;1m")

        # Evaluate soil health
        soil_report = evaluate_soil_health(
            N, P, K, temperature, humidity, ph, rainfall)
        print("\033[1mSoil Health Report:\033[0m")
        for key, value in soil_report.items():
            print(f"\033[93m{key}: \033[94m{value}\033[0m")

        # Predict the crop
        recommendations = predict_crop(
            N, P, K, temperature, humidity, ph, rainfall)
        print("\033[1mRecommendations:\033[0m")
        for label, prob in recommendations:
            print(f"\033[92m{label}: \033[94m{prob * 100:.2f}%\033[0m")

    except KeyboardInterrupt:
        print("\n\033[1mQuit!\033[0m")
        exit(0)

    except Exception as e:
        print(f"\033[91m{e}\033[0m")


def test():

    print('*' * 100)
    print("\033[4;1mRecom1:\033[0m")
    print('*' * 100)
    for n, p, k, t, h, ph, r in zip(N, P, K, T, H, PH, R):
        recommendations = predict_crop(n, p, k, t, h, ph, r)
        print("\033[3;1mn \tp \tk \tt \th \tph \tr\033[0m")
        print(f"\033[93m{n} \t{p} \t{k} \t{t} \t{h} \t{ph} \t{r}\033[0m")
        for label, prob in recommendations:
            print(f"\033[1;92m{label}: \033[1;94m{prob * 100:.2f}%\033[0m")

    print('\n')
    print('*' * 100)
    print("\033[4;1mRecom2:\033[0m")
    print('*' * 100)
    for n, p, k, t, h, ph, r in zip(reversed(N), P, reversed(K), T, reversed(H), PH, reversed(R)):
        recommendations = predict_crop(n, p, k, t, h, ph, r)
        print("\033[3;1mn \tp \tk \tt \th \tph \tr\033[0m")
        print(f"\033[93m{n} \t{p} \t{k} \t{t} \t{h} \t{ph} \t{r}\033[0m")
        for label, prob in recommendations:
            print(f"\033[1;92m{label}: \033[1;94m{prob * 100:.2f}%\033[0m")

    print('\n')
    print('*' * 100)
    print("\033[4;1mRecom3:\033[0m")
    print('*' * 100)
    for n, p, k, t, h, ph, r in zip(reversed(N), reversed(P), reversed(K), T, reversed(H), PH, reversed(R)):
        recommendations = predict_crop(n, p, k, t, h, ph, r)
        print("\033[3;1mn \tp \tk \tt \th \tph \tr\033[0m")
        print(f"\033[93m{n} \t{p} \t{k} \t{t} \t{h} \t{ph} \t{r}\033[0m")
        for label, prob in recommendations:
            print(f"\033[1;92m{label}: \033[1;94m{prob * 100:.2f}%\033[0m")


if __name__ == "__main__":
    # controller()
    test()
    # while True:
    # main()
