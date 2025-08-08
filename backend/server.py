import base64
import io
import numpy as np
import soundfile as sf
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

BLOW_THRESHOLD = 0.1  # Adjust for sensitivity

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            msg = eval(data)  # simple parse
            if "audio" in msg:
                audio_base64 = msg["audio"].split(",")[1]
                audio_bytes = base64.b64decode(audio_base64)
                
                audio_data, samplerate = sf.read(io.BytesIO(audio_bytes))
                volume = np.abs(audio_data).mean()

                if volume > BLOW_THRESHOLD:
                    await websocket.send_text(
                        '{"event": "blow", "prob": %f}' % volume
                    )
        except Exception as e:
            print("Disconnected:", e)
            break

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)