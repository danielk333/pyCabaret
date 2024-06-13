import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler  # Normaliser 


read_file = open('/Users/jeannelonglune/Desktop/memoire/pyCabaret/src/storage_MLdata/ML1000.csv', 'r')

data_list = []
for line in read_file:
    data = line.split(', ')
    data_list.append([[float(data[0]), float(data[1]), float(data[2])], [float(data[3])]])

print(data_list)

# Modif format datalist
x = np.array([item[0] for item in data_list])  # Entrées : altitude, Mach, taille du déchet
y = np.array([item[1] for item in data_list])  # Sortie : flux de chaleur

#print('x check ', x)
#print('y check ', y)

# entraînement data (70%)  validation data (15%) and test data (15%)
# 1st split
X_train, X_val, y_train, y_val = train_test_split(
    x, y, test_size=0.3, random_state=42)

# 2nd split
X_val, X_test, y_val, y_test = train_test_split(
    X_val, y_val, test_size=0.5, random_state=42)
#spécifier une graine (seed) pour le générateur de nombres aléatoires. L'utilisation d'une graine garantit que la séparation des données

#scaling - Standardize features
x_scaler = StandardScaler()
X_train_scaled = x_scaler.fit_transform(X_train)
X_val_scaled = x_scaler.transform(X_val)
X_test_scaled = x_scaler.transform(X_test)

y_scaler = StandardScaler()
y_train_scaled = y_scaler.fit_transform(y_train)
y_val_scaled = y_scaler.transform(y_val)
y_test_scaled = y_scaler.transform(y_test)


# modèle
model = tf.keras.Sequential([
    #tf.keras.layers.Dense(128, activation='relu', input_shape=(3,)),
    tf.keras.layers.Dense(64, activation='relu'),
    #couche 32? plus complexe
    tf.keras.layers.Dense(1, activation='linear')
])

# Build a simple linear regression model
#model = tf.keras.Sequential()
#model.add(tf.keras.layers.Dense(1, input_dim=3))

def train_and_evaluate_model(learning_rate):

    # Compile model
    optimizer = tf.keras.optimizers.Adam(
        learning_rate=learning_rate)  # Try different learning rates
    model.compile(optimizer=optimizer, loss='mean_squared_error')

    # Train model
    history = model.fit(X_train_scaled, y_train_scaled, epochs=500,
                        batch_size=32, validation_data=(X_val_scaled, y_val_scaled))

    # Evaluate model on test set with Root Mean Squared Error (in order to have the same unit as the data)
    predictions = model.predict(X_test_scaled)
    rmse = np.sqrt(mean_squared_error(y_scaler.inverse_transform(
        y_test_scaled), y_scaler.inverse_transform(predictions)))
    print(f'Root Mean Squared Error on Test Set: {rmse}')
    return rmse

learning_rates = [0.006]
#[0.0005, 0.001, 0.004, 0.005, 0.006, 0.007, 0.008, 0.01, 0.011, 0.1 , 0.0065, 0.0055]
#is the learning rate linear? how to find the best learning rate? 

best_result = 1000000000000000000
best_learning_rate = None
for l in learning_rates:
    result = train_and_evaluate_model(l)
    if result < best_result:
        best_result = result
        best_learning_rate = l

print(
    f"The best result obtained was a RMSE of {best_result} with a learning rate of {best_learning_rate}")

model.summary()
#MODEL SAVING 
model.save('saved_model/my_model')

#LOADING MODEL FOR THE TEST
new_model = tf.keras.models.load_model('saved_model/my_model')
# Check its architecture
new_model.summary()
# Evaluate the restored model
loss = new_model.evaluate(X_test_scaled, y_test_scaled, verbose=2)
print('Restored model, accuracy: {:5.2f}%'.format(loss))
print(new_model.predict(X_test).shape)

#TEST
# Example input for prediction
new_data = np.array([[0.4, 70.0, 21.06122448979592]])
# Scale the new data
new_data_scaled = x_scaler.transform(new_data)
# Make a prediction using the trained model
prediction = new_model.predict(new_data_scaled)
# Inverse transform the prediction to get the original scale
original_prediction = y_scaler.inverse_transform(prediction)
print("Predicted output:", original_prediction)

