import numpy as np
from tensorflow.keras import models, layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

DATA_NPZ = "../data/features.npz"
OUT_MODEL = "../models/blowing_detector.h5"
OUT_SCALER = "../models/scaler.pkl"

if __name__ == '__main__':
    data = np.load(DATA_NPZ)
    X, y = data['X'], data['y']

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    joblib.dump(scaler, OUT_SCALER)

    X_train, X_test, y_train, y_test = train_test_split(Xs, y, test_size=0.2, random_state=42)

    model = models.Sequential([
        layers.Input(shape=(X.shape[1],)),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(64, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=30, batch_size=16)
    model.save(OUT_MODEL)
    print('Model saved to', OUT_MODEL)
