import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pandas as pd

# Load the dataset
data = pd.read_csv('./data.csv')

# Preprocessing the data
features = data[['Model Year', 'Make', 'Model', 'E.V_Type', 'Base MSRP']]
target = data['Electric Range']

# Handle categorical data
features['Make'] = LabelEncoder().fit_transform(features['Make'])
features['Model'] = LabelEncoder().fit_transform(features['Model'])
features['E.V_Type'] = LabelEncoder().fit_transform(features['E.V_Type'])

# Handle missing values
features.fillna(features.mean(), inplace=True)
target.fillna(target.mean(), inplace=True)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Normalize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create a TensorFlow model
def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

# Train the model
model = create_model()
model.fit(X_train, y_train, epochs=1, validation_data=(X_test, y_test))
model.export('./')
# model.export('./', format="tf_saved_model", verbose=True)