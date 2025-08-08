let ws;
let mediaRecorder;
let chunks = [];
const startBtn = document.getElementById('startBtn');
const statusP = document.getElementById('status');
const flame = document.getElementById('flame');

startBtn.onclick = async () => {
  if (startBtn.dataset.running === '1') {
    stop();
  } else {
    await start();
  }
}

async function start(){
  startBtn.textContent = 'Stop';
  startBtn.dataset.running = '1';
  statusP.textContent = 'Status: connecting...';

  ws = new WebSocket('ws://localhost:8000/ws');
  ws.onopen = () => { statusP.textContent = 'Status: connected to server'; };
  ws.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.event === 'blow') {
      statusP.textContent = `Status: blow detected (p=${msg.prob.toFixed(2)})`;
      blowOut();
    }
  }

  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  mediaRecorder.ondataavailable = e => {
    if (e.data.size > 0) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64data = reader.result;
        if (ws && ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({audio: base64data}));
        }
      };
      reader.readAsDataURL(e.data);
    }
  };
  mediaRecorder.start(600);
}

function stop(){
  startBtn.textContent = 'Start';
  startBtn.dataset.running = '0';
  statusP.textContent = 'Status: stopped';
  if (mediaRecorder && mediaRecorder.state !== 'inactive') mediaRecorder.stop();
  if (ws) ws.close();
}

function blowOut(){
  flame.classList.add('off');
}
