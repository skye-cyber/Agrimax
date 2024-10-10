import numpy as np
import pandas as pd

print("\033[32mGenerating entries ...\033[0m")
# Define the number of entries
num_entries = 3_000_000

# Generate data using more realistic distributions
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

# Enhanced crop recommendation logic


print("\033[32mAssign crop predictions...\033[0m")


def assign_crop(N, P, K, temperature, humidity, pH, rainfall):
    # Rice grows well in hot, humid conditions with high rainfall
    if temperature > 25 and rainfall > 300 and pH > 6.0:
        return 'rice'
    # Wheat prefers cooler temperatures and moderate rainfall
    elif temperature < 25 and rainfall < 200 and pH < 6.5:
        return 'wheat'
    # Corn needs high nutrients and rainfall
    elif N > 100 and P > 90 and K > 100 and rainfall > 250:
        return 'maize'
    # Sugarcane grows in hot and humid areas with slightly alkaline soil
    elif humidity > 80 and pH > 7.0 and rainfall > 200:
        return 'sugarcane'
    # Barley grows well in cooler temperatures and less rainfall
    elif temperature < 20 and rainfall < 150:
        return 'barley'
    # Potatoes need moderate pH, cooler temperature, and moderate rainfall
    elif 15 < temperature < 22 and 5.0 < pH < 6.5 and 100 < rainfall < 250:
        return 'potato'
    # Soybeans thrive in warm temperatures and need good nitrogen levels
    elif N > 80 and temperature > 20 and rainfall > 250:
        return 'soybean'
    # Coffee grows well in tropical climates with moderate rainfall and slightly acidic soil
    elif 20 < temperature < 30 and 6.0 < pH < 6.8 and 150 < rainfall < 300:
        return 'coffee'
    # Tea prefers cooler temperatures, high rainfall, and slightly acidic soils
    elif 10 < temperature < 20 and rainfall > 200 and 5.0 < pH < 6.5:
        return 'tea'
    # Peas grow well in cooler temperatures with moderate pH and lower rainfall
    elif 12 < temperature < 22 and 5.5 < pH < 6.5 and rainfall < 180:
        return 'peas'
    # Cotton needs warm temperatures, good soil, and moderate rainfall
    elif temperature > 22 and 6.0 < pH < 7.5 and 150 < rainfall < 250:
        return 'cotton'
    # Additional crops based on the combination of environmental factors
    elif temperature > 20 and humidity > 60 and rainfall > 150:
        return np.random.choice(["oats", "cassava", "millet", "sorghum", "quinoa"])
    elif pH < 6.0 and temperature > 25 and rainfall < 100:
        return np.random.choice(["groundnuts", "sweet potatoes", "yams", "taro"])
    elif pH < 6.5 and rainfall > 200:
        return np.random.choice(["cabbage", "carrots", "tomatoes", "peppers", "eggplant"])
    elif temperature > 25 and humidity < 50 and rainfall < 150:
        return np.random.choice(["garlic", "chilli peppers", "cucumbers", "lettuce"])
    elif pH > 6.5 and rainfall > 250:
        return np.random.choice(["broccoli", "spinach", "fennel", "asparagus", "artichoke"])
    # If none of the above conditions match, randomly assign a crop
    else:
        return np.random.choice(["oats", "millet", "cassava", "quinoa", 'sunflower', 'maize', 'peanuts', 'chickpeas'])


# Apply the new crop recommendation rules to the dataset
crops = [assign_crop(N[i], P[i], K[i], temperature[i], humidity[i],
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
data.to_csv('dataset/synthetic_dataset_with_enhanced_crops.csv', index=False)
# print(data.head(20))  # Display the first 20 rows of the dataset
df = pd.read_csv('dataset/synthetic_dataset_with_enhanced_crops.csv')

print("\033[32mClean the data/remove duplicates\033[0m")
clean_df = df.drop_duplicates()
clean_df.to_csv(
    'dataset/synthetic_dataset_with_enhanced_crops.csv', index=False)
print("✅")
