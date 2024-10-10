import numpy as np
import pandas as pd

print("\033[32mGenerating entries ...\033[0m")
# Define the number of entries
num_entries = 3_000_000

# Generate data using realistic distributions
np.random.seed(0)  # For reproducibility

# Nutrient levels (N, P, K) - log-normal could be more realistic for these
N = np.round(np.random.lognormal(mean=4.5, sigma=0.3, size=num_entries), 4)
P = np.round(np.random.lognormal(mean=4.0, sigma=0.2, size=num_entries), 4)
K = np.round(np.random.lognormal(mean=4.2, sigma=0.25, size=num_entries), 4)

# Temperature in Celsius
temperature = np.round(np.random.normal(
    loc=28, scale=2.5, size=num_entries), 8)

# Humidity as a percentage
humidity = np.round(np.random.normal(loc=90, scale=5, size=num_entries), 8)

# pH value of soil
pH = np.round(np.random.normal(loc=6.5, scale=0.5, size=num_entries), 8)

# Rainfall in mm
rainfall = np.round(np.random.normal(loc=290, scale=50, size=num_entries), 8)

# Probability-based crop assignment

print("\033[32mAssign crop predictions...\033[0m")

# Define optimal conditions for each crop
crop_conditions = {
    'rice': {'temperature': (25, 35), 'rainfall': (250, 400), 'pH': (6.0, 7.0), 'N': (80, 120), 'P': (70, 90), 'K': (100, 120), 'humidity': (80, 100)},
    'wheat': {'temperature': (15, 25), 'rainfall': (100, 200), 'pH': (6.0, 6.5), 'N': (50, 100), 'P': (30, 70), 'K': (50, 100), 'humidity': (50, 70)},
    'maize': {'temperature': (20, 30), 'rainfall': (200, 300), 'pH': (6.0, 6.8), 'N': (100, 150), 'P': (90, 120), 'K': (100, 150), 'humidity': (60, 80)},
    'sugarcane': {'temperature': (20, 32), 'rainfall': (200, 300), 'pH': (6.5, 7.5), 'N': (80, 120), 'P': (60, 90), 'K': (90, 130), 'humidity': (80, 100)},
    'barley': {'temperature': (10, 20), 'rainfall': (50, 150), 'pH': (5.5, 6.5), 'N': (30, 60), 'P': (30, 50), 'K': (50, 80), 'humidity': (50, 70)},
    'potato': {'temperature': (15, 22), 'rainfall': (100, 250), 'pH': (5.0, 6.5), 'N': (60, 90), 'P': (50, 70), 'K': (50, 100), 'humidity': (50, 80)},
    'soybean': {'temperature': (20, 30), 'rainfall': (200, 300), 'pH': (6.0, 6.8), 'N': (80, 120), 'P': (50, 90), 'K': (80, 110), 'humidity': (60, 80)},
    'coffee': {'temperature': (20, 30), 'rainfall': (150, 300), 'pH': (6.0, 6.8), 'N': (80, 110), 'P': (60, 90), 'K': (80, 100), 'humidity': (60, 80)},
    'tea': {'temperature': (10, 20), 'rainfall': (200, 300), 'pH': (5.0, 6.5), 'N': (60, 90), 'P': (30, 60), 'K': (50, 80), 'humidity': (60, 80)},
    'peas': {'temperature': (12, 22), 'rainfall': (80, 180), 'pH': (5.5, 6.5), 'N': (50, 70), 'P': (30, 50), 'K': (40, 60), 'humidity': (50, 70)},
    'cotton': {'temperature': (22, 32), 'rainfall': (150, 250), 'pH': (6.0, 7.5), 'N': (60, 100), 'P': (40, 80), 'K': (50, 100), 'humidity': (60, 80)},
    'tomato': {'temperature': (20, 28), 'rainfall': (60, 150), 'pH': (5.5, 6.8), 'N': (100, 140), 'P': (60, 100), 'K': (80, 120), 'humidity': (60, 80)},
    'onion': {'temperature': (15, 25), 'rainfall': (50, 100), 'pH': (6.0, 7.0), 'N': (50, 80), 'P': (40, 70), 'K': (30, 60), 'humidity': (40, 60)},
    'banana': {'temperature': (20, 30), 'rainfall': (100, 300), 'pH': (5.5, 7.5), 'N': (150, 200), 'P': (80, 120), 'K': (150, 200), 'humidity': (75, 90)},
    'pepper': {'temperature': (18, 30), 'rainfall': (80, 150), 'pH': (5.5, 6.8), 'N': (100, 140), 'P': (40, 80), 'K': (80, 120), 'humidity': (60, 80)},
    'cassava': {'temperature': (20, 30), 'rainfall': (150, 250), 'pH': (5.5, 7.0), 'N': (50, 100), 'P': (30, 60), 'K': (40, 80), 'humidity': (50, 70)},
}

# Function to calculate probability for each crop based on environmental conditions


def calculate_weight(env_value, opt_range):
    min_val, max_val = opt_range
    if env_value < min_val:
        # Penalty for values lower than minimum
        return max(0, 1 - (min_val - env_value) / (min_val * 0.1))
    elif env_value > max_val:
        # Penalty for values higher than maximum
        return max(0, 1 - (env_value - max_val) / (max_val * 0.1))
    else:
        return 1  # Full score for values within the range


def assign_crop_probabilistic(N, P, K, temperature, humidity, pH, rainfall):
    crop_weights = {}

    defaults = 0
    for crop, conditions in crop_conditions.items():
        weight = 1
        weight *= calculate_weight(temperature, conditions['temperature'])
        weight *= calculate_weight(rainfall, conditions['rainfall'])
        weight *= calculate_weight(pH, conditions['pH'])
        weight *= calculate_weight(N, conditions['N'])
        weight *= calculate_weight(P, conditions['P'])
        weight *= calculate_weight(K, conditions['K'])
        weight *= calculate_weight(humidity, conditions['humidity'])

        crop_weights[crop] = weight

    # Normalize the weights
    total_weight = sum(crop_weights.values())
    if total_weight == 0:
        defaults += 1
        print(f"Defaults: {defaults}", end='\r')
        # Default to random crop if no conditions match
        return np.random.choice(list(crop_conditions.keys()))
    else:
        for crop in crop_weights:
            crop_weights[crop] /= total_weight

    return np.random.choice(list(crop_weights.keys()), p=list(crop_weights.values()))


# Apply the probabilistic crop recommendation logic
crops = [assign_crop_probabilistic(N[i], P[i], K[i], temperature[i], humidity[i],
                                   pH[i], rainfall[i]) for i in range(num_entries)]

# Create the DataFrame with enhanced crop recommendations
data = pd.DataFrame({
    'N': N,
    'P': P,
    'K': K,
    'temperature': temperature,
    'humidity': humidity,
    'pH': pH,
    'rainfall': rainfall,
    'crop': crops
})

# Save the synthetic data to a CSV or display it
data.to_csv('dataset/synthetic_dataset.csv', index=False)

# Remove duplicates and save the cleaned dataset
print("\n\033[32mCleaning data and removing duplicates...\033[0m")
clean_df = data.drop_duplicates()
clean_df.to_csv(
    'dataset/synthetic_dataset.csv', index=False)

print("✅ Completed!")
