import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from modele import modele
 
altitude_list = np.linspace(50,70,3) #pq 4 ça fonctionne pas?? 
mach_list = np.linspace(18,28,4) #PARLER DE CA, SI JE METS 18 ON A QQC DE NEGATIF POUR CERTAINS POINTS
rad_list = np.linspace(0.1,1,2)

data_list = []


#fichier rad, colonne c'est mach et ligne c'est altitude.
for i,rad in enumerate(rad_list):
    print(i)
    #f_rad = open("/Users/jeannelonglune/Desktop/memoire/pyCabaret/src/data_mat_input/rad_"+str(i)+".csv","w")
    for j,altitude in enumerate(altitude_list):
        #density, pressure, temperature = atmosphere.Atmosphere(altitude)
        for k,mach in enumerate(mach_list):
            #preshock_state = [temperature,pressure,mach]
            #def modele(alt, M_1, reff):
            #forward(preshock_state,residual,throat_area,rad,surface_temp,Prandtl,Lewis,mix,print_info,option)
            #f_rad.write(str(output)+', ')
            #f_ML.write(f"{rad}, {altitude}, {mach}, {output}, ")
            #f_ML.write("\n")
            output = modele(altitude, mach, rad)
            data_list.append([[rad, altitude, mach], output])
        #f_rad.write("\n")
    #f_rad.close()
#f_ML.close()
            
print(data_list)


# Convertir data_list en un format utilisable pour l'entraînement du modèle
X = np.array([item[0] for item in data_list])  # Entrées : altitude, Mach, taille du déchet
y = np.array([item[1] for item in data_list])  # Sortie : flux de chaleur


print(type(X), type(y))

X2 = np.random.rand(1000, 3)  # Exemple avec 3 features

y2 = 2*X2[:, 0] + 3*X2[:, 1] - 1.5*X2[:, 2] + 2*np.random.randn(1000)  # Relation linéaire avec bruit

print(type(X2), type(y2))


# Séparer les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
 
# Normaliser les données (standardisation)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Définir le modèle séquentiel
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(100, input_dim=3, activation='relu'))  # Couche cachée avec activation ReLU
model.add(tf.keras.layers.Dense(1, activation='linear'))  # Couche de sortie avec activation linéaire
 
# Compiler le modèle
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mse'])
 
# Entraîner le modèle
model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_data=(X_test_scaled, y_test))
 
# Évaluer le modèle sur l'ensemble de test



