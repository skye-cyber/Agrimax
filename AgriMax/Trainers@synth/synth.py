import random

import pandas as pd

# Define parameters
days = 1_000  # Number of days of data
crop_types = ["wheat", "maize", "rice", "soybean", "sugarcane", "barley", "potato", "coffee", "tea", "peas", "cotton", "tomato", "onion", "banana", "pepper", "cassava", "spinach", "kale", "millet", "sorghum",
              "greengram", "cowpea", "sunflower", "yam", "oats", "garlic", "lettuce", "cucumber", "chickpea", "blackgram", "pomegrana", "grapes", "watermelon", "apple", "orange", "lemon", "mango", "pawpaw", "coconut", "pigeonpeas"]
activities = ['Watering', 'Fertilizing', 'Pest Control', 'Harvesting']

print("\033[32mGenerating entries ...\033[0m")
# Generate random weather and activity data
data = []
for day in range(days):
    # Random temperature between 15°C and 35°C
    temperature = random.randint(15, 35)
    rainfall = random.choice([0, 5, 10, 15, 20])  # Random rainfall amount
    humidity = random.randint(40, 90)  # Random humidity
    crop_type = random.choice(crop_types)

    # Calculate rolling rain sum for the last 3 days
    if day >= 3:
        rain_last_3_days = sum(data[i]['rainfall']
                               for i in range(day-3, day))
    else:
        rain_last_3_days = rainfall

    # Determine soil dryness score based on recent weather
    if rain_last_3_days < 10 and temperature > 25 and humidity < 60:
        soil_dryness = 'High'
    elif 10 <= rain_last_3_days <= 20:
        soil_dryness = 'Moderate'
    else:
        soil_dryness = 'Low'

    # Suggested activity based on weather and soil dryness
    if soil_dryness == 'High':
        recommended_activity = 'Watering'
    elif soil_dryness == 'Moderate' and temperature < 25:
        recommended_activity = 'Fertilizing'
    else:
        recommended_activity = random.choice(activities)

    # Append to data list
    data.append({
        'date': f'2024-10-{str(day+1).zfill(2)}',
        'crop': crop_type,
        'temperature': temperature,
        'rainfall': rainfall,
        'humidity': humidity,
        'rain_last_3': rain_last_3_days,
        'dryness_score': soil_dryness,
        'activity': recommended_activity
    })

# Create DataFrame
df = pd.DataFrame(data)
print(df.head())

print("\033[32mClean the data/remove duplicates\033[0m")
clean_df = df.drop_duplicates()
# Save to CSV for model training later
df.to_csv('activity_dataset.csv', index=False)
print("✅")
