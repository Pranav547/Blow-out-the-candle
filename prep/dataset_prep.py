import os
import librosa
import numpy as np
import joblib

DATA_DIR = "../data"
OUT_NPZ = "../data/features.npz"

def extract_mfcc(path, sr=22050, n_mfcc=13):
    y, sr = librosa.load(path, sr=sr)
    if len(y) < sr//2:
        y = np.pad(y, (0, sr//2 - len(y)))
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return np.mean(mfcc.T, axis=0)

if __name__ == "__main__":
    X = []
    y = []
    for label, folder in enumerate(["blowing", "not_blowing"]):
        folder_path = os.path.join(DATA_DIR, folder)
        for fname in os.listdir(folder_path):
            if not fname.lower().endswith((".wav", ".mp3", ".flac")):
                continue
            path = os.path.join(folder_path, fname)
            try:
                feat = extract_mfcc(path)
                X.append(feat)
                y.append(label)
            except Exception as e:
                print("skip", path, e)
    X = np.array(X)
    y = np.array(y)
    np.savez(OUT_NPZ, X=X, y=y)
    print("Saved features to", OUT_NPZ)
