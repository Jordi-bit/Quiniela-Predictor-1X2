import pandas as pd
import numpy as np
import json
import os

# Dataset
file_path = "todas_divisiones_2024_2025.csv"
if not os.path.exists(file_path):
    print("Error: Dataset no encontrado.")
    exit()

df = pd.read_csv(file_path)

def extract_features(df):
    X, y = [], []
    stats = {}
    for _, row in df.iterrows():
        l, v = row['Equipo_Local'], row['Equipo_Visitante']
        if l not in stats: stats[l] = {'g': [], 'r': []}
        if v not in stats: stats[v] = {'g': [], 'r': []}
        hL, hV = stats[l], stats[v]
        gLp = np.mean(hL['g']) if hL['g'] else 0
        gVp = np.mean(hV['g']) if hV['g'] else 0
        X.append([gLp, gVp, gLp-gVp, hL['r'].count(1), hL['r'].count(0), hL['r'].count(-1), 0, hL['r'][-1] if hL['r'] else 0, 1])
        res = row['Resultado']
        if res == 1: y.append([1, 0, 0])
        elif res == 0: y.append([0, 1, 0])
        else: y.append([0, 0, 1])
        stats[l]['g'].append(row['Goles_Local']); stats[l]['r'].append(row['Resultado'])
        stats[v]['g'].append(row['Goles_Visitante']); stats[v]['r'].append(-row['Resultado'])
    return np.array(X), np.array(y)

X_train, y_train = extract_features(df)

# Estandarización básica
X_mean = X_train.mean(axis=0)
X_std = X_train.std(axis=0) + 1e-8
X_train = (X_train - X_mean) / X_std

# Parámetros red
input_size = 9
h1_size = 16
h2_size = 8
output_size = 3

# Inicialización Xavier
W1 = np.random.randn(input_size, h1_size) * np.sqrt(2./input_size)
b1 = np.zeros(h1_size)
W2 = np.random.randn(h1_size, h2_size) * np.sqrt(2./h1_size)
b2 = np.zeros(h2_size)
W3 = np.random.randn(h2_size, output_size) * np.sqrt(2./h2_size)
b3 = np.zeros(output_size)

def relu(x): return np.maximum(0, x)
def relu_deriv(x): return (x > 0).astype(float)
def softmax(x):
    e = np.exp(x - np.max(x, axis=1, keepdims=True))
    return e / np.sum(e, axis=1, keepdims=True)

# Entrenamiento
lr = 0.01
epochs = 200
for epoch in range(epochs):
    # Forward
    z1 = X_train @ W1 + b1
    a1 = relu(z1)
    z2 = a1 @ W2 + b2
    a2 = relu(z2)
    z3 = a2 @ W3 + b3
    a3 = softmax(z3)
    
    # Loss (Cross Entropy)
    if epoch % 50 == 0:
        loss = -np.mean(np.sum(y_train * np.log(a3 + 1e-8), axis=1))
        print(f"Epoch {epoch}, Loss: {loss:.4f}")
        
    # Backward
    dz3 = a3 - y_train
    dW3 = a2.T @ dz3 / len(X_train)
    db3 = np.sum(dz3, axis=0) / len(X_train)
    
    da2 = dz3 @ W3.T
    dz2 = da2 * relu_deriv(z2)
    dW2 = a1.T @ dz2 / len(X_train)
    db2 = np.sum(dz2, axis=0) / len(X_train)
    
    da1 = dz2 @ W2.T
    dz1 = da1 * relu_deriv(z1)
    dW1 = X_train.T @ dz1 / len(X_train)
    db1 = np.sum(dz1, axis=0) / len(X_train)
    
    # Update
    W3 -= lr * dW3; b3 -= lr * db3
    W2 -= lr * dW2; b2 -= lr * db2
    W1 -= lr * dW1; b1 -= lr * db1

print("Exportando manualmente a web_model...")
os.makedirs("web_model", exist_ok=True)

# Los pesos deben estar en Float32
weights = [W1, b1, W2, b2, W3, b3]
weight_names = ["dense/kernel", "dense/bias", "dense_1/kernel", "dense_1/bias", "dense_2/kernel", "dense_2/bias"]
weights_list = []
weight_specs = []

for i, w_data in enumerate(weights):
    data = w_data.astype('float32')
    bytes_data = data.tobytes()
    weights_list.append(bytes_data)
    weight_specs.append({
        "name": weight_names[i],
        "shape": list(data.shape),
        "dtype": "float32"
    })

with open("web_model/group1-shard1of1.bin", "wb") as f:
    for w in weights_list: f.write(w)

model_json = {
    "format": "layers-model",
    "generatedBy": "Antigravity-Numpy-Exporter",
    "modelTopology": {
        "class_name": "Sequential",
        "config": {
            "name": "sequential",
            "layers": [
                {"class_name": "Dense", "config": {"name": "dense", "trainable": True, "batch_input_shape": [None, 9], "dtype": "float32", "units": 16, "activation": "relu", "use_bias": True}},
                {"class_name": "Dense", "config": {"name": "dense_1", "trainable": True, "dtype": "float32", "units": 8, "activation": "relu", "use_bias": True}},
                {"class_name": "Dense", "config": {"name": "dense_2", "trainable": True, "dtype": "float32", "units": 3, "activation": "softmax", "use_bias": True}}
            ]
        },
        "keras_version": "2.15.0", "backend": "tensorflow"
    },
    "weightsManifest": [{"paths": ["group1-shard1of1.bin"], "weights": weight_specs}]
}

with open("web_model/model.json", "w") as f:
    json.dump(model_json, f, indent=2)

print("¡Hecho! web_model generado sin usar TensorFlow/Keras.")
