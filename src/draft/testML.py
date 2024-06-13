import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
 
# Load your data from a CSV file
f_read = open("/Users/jeannelonglune/Desktop/memoire/pyCabaret/src/data_ML/ML.csv","r") 
#df = pd.read_csv("ML.csv")
 
# Assuming the columns are named 'feature1', 'feature2', 'feature3', and 'output'
read_file = open('file_name', 'r')

list = []

for line in read_file:
    data = line.split(', ')
    list.append([float(data[0]), float(data[1]), float(data[2]]), [float(data[3])])
close(read_file)

list = np.array(list)
 
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
 
# Standardize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
 
# Build a simple linear regression model
model = Sequential()
model.add(Dense(1, input_dim=3))
 
# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
 
# Train the model
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1)
 
# Evaluate the model on the test set
loss, mae = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss:.4f}, Test MAE: {mae:.4f}')
 
# Make predictions on new data
new_data = scaler.transform(np.array([[your_feature1_value, your_feature2_value, your_feature3_value]]))
predictions = model.predict(new_data)
print(f'Predicted Output: {predictions[0][0]:.4f}')
 
# Plot training history
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Mean Squared Error')
plt.legend()
plt.show()