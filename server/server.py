import base64
import json
import joblib
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
from tensorflow.keras.models import load_model
from utils.audio_utils import wav_bytes_to_mfcc

MODEL_PATH = "../models/blowing_detector.h5"
SCALER_PATH = "../models/scaler.pkl"

app = FastAPI()
model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

@app.get('/')
async def root():
    return {"status": "server up"}

@app.websocket('/ws')
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            obj = json.loads(data)
            b64 = obj.get('audio')
            if not b64:
                continue
            wav_bytes = base64.b64decode(b64.split(',')[-1])
            try:
                feat = wav_bytes_to_mfcc(wav_bytes)
                X = scaler.transform(feat.reshape(1, -1))
                p = float(model.predict(X)[0][0])
                if p > 0.8:
                    await ws.send_text(json.dumps({"event": "blow", "prob": p}))
                else:
                    await ws.send_text(json.dumps({"event": "no_blow", "prob": p}))
            except Exception as e:
                await ws.send_text(json.dumps({"event": "error", "msg": str(e)}))
    except WebSocketDisconnect:
        print('client disconnected')

if __name__ == '__main__':
    uvicorn.run('server:app', host='0.0.0.0', port=8000, reload=False)
