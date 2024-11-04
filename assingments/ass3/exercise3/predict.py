import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder


loaded_model = tf.keras.models.load_model('my_model.keras')

new_data = pd.DataFrame({
    'Model Year': [2022],
    'Make': ['Tesla'],
    'Model': ['Model 3'],
    'E.V_Type': ['Battery Electric Vehicle (BEV)'],
    'Base MSRP': [39990]
})

new_data['Make'] = LabelEncoder().fit_transform(new_data['Make'])
new_data['Model'] = LabelEncoder().fit_transform(new_data['Model'])
new_data['E.V_Type'] = LabelEncoder().fit_transform(new_data['E.V_Type'])

scaler = StandardScaler()
new_data_scaled = scaler.fit_transform(new_data)

prediction = loaded_model.predict(new_data_scaled)
print(f"Predicted Electric Range: {prediction[0][0]}")
