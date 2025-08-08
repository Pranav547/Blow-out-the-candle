import io
import numpy as np
import soundfile as sf
import librosa

SR = 22050

def wav_bytes_to_mfcc(wav_bytes, n_mfcc=13):
    data, sr = sf.read(io.BytesIO(wav_bytes))
    if data.ndim > 1:
        data = data[:, 0]
    if sr != SR:
        data = librosa.resample(data.astype(float), orig_sr=sr, target_sr=SR)
    if len(data) < SR//2:
        data = np.pad(data, (0, SR//2 - len(data)))
    mfcc = librosa.feature.mfcc(y=data, sr=SR, n_mfcc=n_mfcc)
    feat = np.mean(mfcc.T, axis=0)
    return feat
