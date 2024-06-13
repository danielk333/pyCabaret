import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler  # Normaliser 

#creating our data list. (form : [[[input11, input12, input13], [output1]], [[input21, input22, input23], [output2], [input31...]]])
read_file = open('/Users/jeannelonglune/Desktop/memoire/pyCabaret/src/storage_MLdata/ML1000.csv', 'r')

data_list = []
for line in read_file:
    data = line.split(', ')
    data_list.append([[float(data[0]), float(data[1]), float(data[2])], [float(data[3])]])

#print(data_list)

# creation of the array
x = np.array([item[0] for item in data_list])  # Entrées : altitude, Mach, taille du déchet
y = np.array([item[1] for item in data_list])  # Sortie : flux de chaleur

#print('x check ', x)
#print('y check ', y)

# training data (70%)  validation data (15%) and test data (15%)
# 1st split
X_train, X_val, y_train, y_val = train_test_split(
    x, y, test_size=0.3, random_state=42)
# 2nd split
X_val, X_test, y_val, y_test = train_test_split(
    X_val, y_val, test_size=0.5, random_state=42)

#scaling - Standardize features
x_scaler = StandardScaler()
X_train_scaled = x_scaler.fit_transform(X_train)
X_val_scaled = x_scaler.transform(X_val)
X_test_scaled = x_scaler.transform(X_test)

y_scaler = StandardScaler()
y_train_scaled = y_scaler.fit_transform(y_train)
y_val_scaled = y_scaler.transform(y_val)
y_test_scaled = y_scaler.transform(y_test)


#%%

# model, creation of the hidden layers.
#API keras
input_layer = tf.keras.layers.Input(shape=(3,))
dense_layer1 = tf.keras.layers.Dense(64, activation='relu')(input_layer)
dense_layer2 = tf.keras.layers.Dense(32, activation='relu')(dense_layer1)
output_layer = tf.keras.layers.Dense(1, activation='linear')(dense_layer2)
model = tf.keras.models.Model(inputs=input_layer, outputs=output_layer)
model.summary()

def train_and_evaluate_model(learning_rate):

    # Compile model
    optimizer = tf.keras.optimizers.Adam(
        learning_rate=learning_rate)  
    model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['accuracy'])

    # Train model
    history = model.fit(X_train_scaled, y_train_scaled, epochs=200,
                        batch_size=32, validation_data=(X_val_scaled, y_val_scaled))

    # Plot training and validation loss
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss')
    plt.legend()

    # Plot training and validation accuracy
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.legend()

    plt.show()

    # Evaluate model on test set with Root Mean Squared Error
    predictions = model.predict(X_test_scaled)
    rmse = np.sqrt(mean_squared_error(y_scaler.inverse_transform(
        y_test_scaled), y_scaler.inverse_transform(predictions)))

    # Evaluate accuracy on test set
    _, accuracy = model.evaluate(X_test_scaled, y_test_scaled)
    
    print(f'Root Mean Squared Error on Test Set: {rmse}')
    print(f'Accuracy on Test Set: {accuracy}')

    return rmse, accuracy

learning_rates = [0.006]
#[0.0005, 0.001, 0.004, 0.005, 0.006, 0.007, 0.008, 0.01, 0.011, 0.1 , 0.0065, 0.0055]
#is the learning rate linear? how to find the best learning rate? 

best_result = (1000000000000000000, 0)  # Initialize as a tuple with RMSE and accuracy
best_learning_rate = None
for l in learning_rates:
    result = train_and_evaluate_model(l)
    if result[0] < best_result[0]:  # Compare RMSE values
        best_result = result
        best_learning_rate = l

print(f"The best result obtained was a RMSE of {best_result[0]} and accuracy of {best_result[1]} with a learning rate of {best_learning_rate}")