import numpy as np

# Instead of generating random data, save it to a file using memory-mapping
data_size = 2000000  # Larger dataset size to showcase memory mapping
filename = 'large_dataset.npy'

# Create a memory-mapped array for large data
# Using 'w+' mode to allow writing and reading
mmapped_array = np.memmap(filename, dtype='float32', mode='w+', shape=(data_size, 5))

# Generate synthetic data for environmental factors directly in memory-mapped array
mmapped_array[:, 0] = np.random.uniform(5.0, 8.5, data_size)  # Soil pH
mmapped_array[:, 1] = np.random.uniform(15, 40, data_size)  # Temperature in Celsius
mmapped_array[:, 2] = np.random.uniform(300, 1200, data_size)  # Rainfall in mm
mmapped_array[:, 3] = np.random.uniform(6, 14, data_size)  # Sunlight hours
mmapped_array[:, 4] = np.random.randint(0, 3, data_size)  # Soil type (0=Clay, 1=Loam, 2=Sand)

# Ensure data is written to disk
mmapped_array.flush()

# Later you can read it back without loading the entire dataset into memory
loaded_array = np.memmap(filename, dtype='float32', mode='r', shape=(data_size, 5))

# Use loaded_array as X in training models
