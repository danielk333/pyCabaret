import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from modele import modele
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from config.input import rad_list , altitude_list , mach_list
"""not needed"""

"""Le but de ce fichier va être d'ouvrir les données de data_mat_input afin de former une liste qui va contenir les inputs de notre modèle ML

Donc créer une liste de la forme 
data = [[[R0; v0; a0]; h0]; [[R1; v1; a1]; h1];[[R2; v2; a2]; h2];...]

qui vont former l'entrée de notre modèle de machine learning. 

Ensuite on va faire notre modèle

PT RENOMER CE FICHIER PCQ JE PENSE QUE LE MIEUX C'EST DE FAIRE L'EXTRACTION ET LE MODELE DANS LE MEME DOSSSSS

IL FAUDRA AUSSI MATCH MAT_DATA ET GRAPH ETC POUR AVOIR QQC DE COHERENT JE PENSE QU'IL EST PT TEMPS DE FAIRE UN DOSSIER INPUT.

"""

data_list = []

#fichier rad, colonne c'est mach et ligne c'est altitude.
for i,rad in enumerate(rad_list):
    print(i)
    #f_rad = open("/Users/jeannelonglune/Desktop/memoire/pyCabaret/src/data_mat_input/rad_"+str(i)+".csv","w")
    for j,altitude in enumerate(altitude_list):
        #density, pressure, temperature = atmosphere.Atmosphere(altitude)
        for k,mach in enumerate(mach_list):
            output = modele(altitude, mach, rad)
            data_list.append([[rad, altitude, mach], output])
            
print(data_list)

"""ici à la place de regénérer les données, ça serait mieux de les lires du fichier. """


#%%

# Modif format datalist
x = np.array([item[0] for item in data_list])  # Entrées : altitude, Mach, taille du déchet
y = np.array([item[1] for item in data_list])  # Sortie : flux de chaleur

print('x check ', x)
print('y check ', y)

# entraînement (70%)  validation (30%)
X_train, X_val, y_train, y_val = train_test_split(x, y, test_size=0.3, random_state=42) 
#spécifier une graine (seed) pour le générateur de nombres aléatoires. L'utilisation d'une graine garantit que la séparation des donnée

# modèle
#model = tf.keras.Sequential([
    #tf.keras.layers.Dense(64, activation='relu', input_shape=(3,)),  # 3 features en entrée
    #tf.keras.layers.Dense(1)  # 1 output
#])

# Build a simple linear regression model
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(1, input_dim=3))

#history = model.fit(X_train, y_train, epochs=10, validation_data=(X_val, y_val), validation_split=0.3)


# Normaliser 
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)

# Compilation
model.compile(optimizer='adam', loss='mean_squared_error')

print('x train', X_train)
print('y_train', y_train)

print('x_val ', X_val)
print('y_val', y_val)

# Entraînement
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_val, y_val))

# Évaluation
predictions = model.predict(X_val)
mse = mean_squared_error(y_val, predictions)
print(f'Mean Squared Error on Validation Set: {mse}')

# Visualisation
#plt.figure(figsize=(10, 6))

#données réelles
#plt.scatter(X_val[:, 1], y_val, label='Données réelles', color='blue', alpha=0.7)

# prédictions du modèle
#predictions = model.predict(X_val)
#plt.scatter(X_val[:, 1], predictions, label='Prédictions du modèle', color='red', alpha=0.7)

# Tracer la ligne reliant les prédictions et les données réelles
#plt.plot(X_val[:, 1], predictions, color='red', linestyle='dashed', linewidth=2, alpha=0.7)

#plt.xlabel('Altitude')
#plt.ylabel('Flux de chaleur')
#plt.title('Comparaison entre les données réelles et les prédictions du modèle')
#plt.legend()
#plt.grid(True)
#plt.show()

# Évaluation des performances 
predictions = model.predict(X_val)
mse = mean_squared_error(y_val, predictions)
print(f'Mean Squared Error on Validation Set: {mse}')

# test
new_data = np.array([[0.1, 50, 18]])
prediction = model.predict(new_data)
#prediction = modele(60, 23, 0.5)
print(f'Prédiction pour de nouvelles données : {prediction}')
