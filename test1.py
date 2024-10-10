import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Generate synthetic data for environmental factors and crop choices
np.random.seed(60)

# Define crops and their preferred conditions
crops = ['maize', 'wheat', 'rice', 'tomatoes']
data_size = 1_000_000

# Randomly generate data
soil_ph = np.random.uniform(5.0, 8.5, data_size)  # Soil pH between 5.0 and 8.5
temperature = np.random.uniform(15, 40, data_size)  # Temperature in Celsius (15-40)
rainfall = np.random.uniform(300, 1200, data_size)  # Rainfall in mm (300-1200)
sunlight_hours = np.random.uniform(6, 14, data_size)  # Sunlight exposure in hours (6-14)
soil_type = np.random.randint(0, 3, data_size)  # 0 = Clay, 1 = Loam, 2 = Sand

# Crop preferences for each factor (these are simplified and random for the sake of the example)
crop_choice = np.random.choice(crops, data_size)

# Create DataFrame
df = pd.DataFrame({
    'soil_ph': soil_ph,
    'temperature': temperature,
    'rainfall': rainfall,
    'sunlight_hours': sunlight_hours,
    'soil_type': soil_type,
    'crop_choice': crop_choice
})

# Prepare data for training
X = df[['soil_ph', 'temperature', 'rainfall', 'sunlight_hours', 'soil_type']]
y = df['crop_choice']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a Decision Tree Classifier
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Predict on test data
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

# Output accuracy and sample data for review
accuracy, df.head(), model.feature_importances_
print(accuracy)
print(df.head())
print(model.feature_importances_)
