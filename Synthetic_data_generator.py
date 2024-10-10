import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.preprocessing import MinMaxScaler

# Define the number of entries
print("\033[32mGenerating entries ...\033[0m")
num_entries = 23_520_000  # RFC  3_360_000->67.89%

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
    'spinach': {'temperature': (10, 20), 'rainfall': (200, 300), 'pH': (6.0, 7.0), 'N': (80, 120), 'P': (40, 70), 'K': (60, 90), 'humidity': (60, 80)},
    'kale': {'temperature': (15, 25), 'rainfall': (200, 300), 'pH': (6.0, 7.5), 'N': (80, 120), 'P': (40, 70), 'K': (60, 90), 'humidity': (60, 80)},
    'millet': {'temperature': (20, 30), 'rainfall': (300, 600), 'pH': (5.5, 7.0), 'N': (30, 60), 'P': (20, 40), 'K': (30, 50), 'humidity': (50, 70)},
    'sorghum': {'temperature': (20, 35), 'rainfall': (300, 600), 'pH': (5.5, 7.0), 'N': (40, 80), 'P': (20, 40), 'K': (30, 50), 'humidity': (50, 70)},
    'greengram': {'temperature': (20, 30), 'rainfall': (300, 500), 'pH': (6.0, 7.0), 'N': (40, 80), 'P': (20, 40), 'K': (30, 50), 'humidity': (50, 70)},
    'cowpea': {'temperature': (20, 30), 'rainfall': (300, 500), 'pH': (6.0, 7.0), 'N': (40, 80), 'P': (20, 40), 'K': (30, 50), 'humidity': (50, 70)},
    'sunflower': {'temperature': (20, 30), 'rainfall': (300, 600), 'pH': (6.0, 7.5), 'N': (60, 100), 'P': (40, 70), 'K': (60, 90), 'humidity': (50, 70)},
    'yam': {'temperature': (20, 30), 'rainfall': (100, 200), 'pH': (5.5, 7.0), 'N': (60, 100), 'P': (40, 70), 'K': (50, 80), 'humidity': (70, 90)},
    'oats': {'temperature': (10, 20), 'rainfall': (200, 400), 'pH': (6.0, 7.0), 'N': (50, 80), 'P': (30, 50), 'K': (40, 60), 'humidity': (50, 70)},
    'garlic': {'temperature': (15, 25), 'rainfall': (200, 300), 'pH': (6.0, 7.0), 'N': (60, 100), 'P': (40, 70), 'K': (50, 80), 'humidity': (50, 70)},
    'lettuce': {'temperature': (15, 20), 'rainfall': (200, 300), 'pH': (6.0, 7.0), 'N': (80, 120), 'P': (40, 70), 'K': (60, 90), 'humidity': (60, 80)},
    'cucumber': {'temperature': (20, 30), 'rainfall': (200, 300), 'pH': (6.0, 7.0), 'N': (80, 120), 'P': (40, 70), 'K': (60, 90), 'humidity': (60, 80)},
    'chickpea': {'temperature': (20, 30), 'rainfall': (200, 400), 'pH': (6.0, 7.0), 'N': (40, 80), 'P': (20, 40), 'K': (30, 50), 'humidity': (50, 70)},
    'blackgram': {'temperature': (20, 30), 'rainfall': (300, 500), 'pH': (6.0, 7.0), 'N': (40, 80), 'P': (20, 40), 'K': (30, 50), 'humidity': (50, 70)},
    'pomegranate': {'temperature': (20, 30), 'rainfall': (200, 400), 'pH': (6.0, 7.5), 'N': (60, 100), 'P': (40, 70), 'K': (60, 90), 'humidity': (50, 70)},
    'grapes': {'temperature': (15, 30), 'rainfall': (500, 800), 'pH': (6.0, 7.5), 'N': (50, 100), 'P': (30, 60), 'K': (60, 100), 'humidity': (50, 70)},
    'watermelon': {'temperature': (20, 30), 'rainfall': (200, 400), 'pH': (6.0, 7.0), 'N': (80, 120), 'P': (40, 70), 'K': (60, 90), 'humidity': (60, 80)},
    'apple': {'temperature': (15, 25), 'rainfall': (500, 800), 'pH': (6.0, 7.0), 'N': (80, 120), 'P': (40, 70), 'K': (60, 90), 'humidity': (50, 70)},
    'orange': {'temperature': (20, 30), 'rainfall': (500, 800), 'pH': (6.0, 7.5), 'N': (80, 120), 'P': (40, 70), 'K': (60, 90), 'humidity': (50, 70)},
    'lemon': {'temperature': (20, 30), 'rainfall': (500, 800), 'pH': (6.0, 7.5), 'N': (80, 120), 'P': (40, 70), 'K': (60, 90), 'humidity': (50, 70)},
    'mango': {'temperature': (25, 35), 'rainfall': (500, 1000), 'pH': (5.5, 7.5), 'N': (80, 120), 'P': (40, 70), 'K': (60, 90), 'humidity': (50, 70)},
    'pawpaw': {'temperature': (20, 30), 'rainfall': (100, 300), 'pH': (5.5, 7.0), 'N': (80, 120), 'P': (40, 70), 'K': (60, 90), 'humidity': (70, 90)},
    'coconut': {'temperature': (25, 35), 'rainfall': (1000, 2000), 'pH': (5.5, 8.0), 'N': (80, 120), 'P': (40, 70), 'K': (60, 90), 'humidity': (70, 90)},
    'pigeonpeas': {'temperature': (20, 30), 'rainfall': (300, 600), 'pH': (6.0, 7.0), 'N': (40, 80), 'P': (20, 40), 'K': (30, 50), 'humidity': (50, 70)},
}


# Generate synthetic data
X, y = make_classification(
    n_samples=num_entries,
    n_features=7,  # Features: N, P, K, temperature, humidity, pH, rainfall
    n_informative=6,
    n_redundant=1,
    n_repeated=0,
    n_classes=len(crop_conditions),
    n_clusters_per_class=1,
    weights=None,
    flip_y=0.01,
    class_sep=1.0,
    hypercube=True,
    shift=0.0,
    scale=1.0,
    shuffle=True,
    random_state=0
)

# Convert to DataFrame
df = pd.DataFrame(
    X, columns=['N', 'P', 'K', 'temperature', 'humidity', 'pH', 'rainfall'])
df['crop'] = y

# Map class labels to crop names
print("\033[32mMap class labels to crop names\033[0m")
crop_map = {i: crop for i, crop in enumerate(crop_conditions.keys())}
df['crop'] = df['crop'].map(crop_map)

# Define the min and max values for each feature based on crop_conditions
feature_ranges = np.array([
    [30, 200],  # N
    [20, 120],  # P
    [30, 150],  # K
    [10, 35],   # temperature
    [40, 100],  # humidity
    [5.0, 8.0],  # pH
    [50, 2000]  # rainfall
])

print("\033[32mScale the features to fit within the ranges of the crop conditions\033[0m")
# Scale the features to fit within the ranges of the crop conditions
for i in range(X.shape[1]):
    min_val, max_val = feature_ranges[i]
    # Scale the feature to the range [min_val, max_val]
    df.iloc[:, i] = (df.iloc[:, i] - df.iloc[:, i].min()) / (df.iloc[:, i].max() - df.iloc[:, i].min()) * (max_val - min_val) + min_val


# Save the synthetic data to a CSV
print("\033[32mSave the synthetic data to a CSV\033[0m")
df.to_csv('dataset/synthetic_dataset.csv', index=False)

# Remove duplicates and save the cleaned dataset
print("\033[32mRemove duplicates and save the cleaned dataset\033[0m")
clean_df = df.drop_duplicates()
clean_df.to_csv('dataset/synthetic_dataset.csv', index=False)
