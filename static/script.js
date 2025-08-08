const startBtn = document.getElementById('startBtn');
const statusP = document.getElementById('status');
const flame = document.getElementById('flame');

let audioContext;
let analyser;
let microphone;
let javascriptNode;
let running = false;

startBtn.onclick = () => {
  if (running) {
    stop();
  } else {
    start();
  }
}

async function start() {
  startBtn.textContent = 'Stop';
  running = true;
  statusP.textContent = 'Status: listening...';

  // Create audio context and get microphone input
  audioContext = new (window.AudioContext || window.webkitAudioContext)();
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  
  microphone = audioContext.createMediaStreamSource(stream);
  analyser = audioContext.createAnalyser();
  analyser.fftSize = 256;

  javascriptNode = audioContext.createScriptProcessor(256, 1, 1);
  microphone.connect(analyser);
  analyser.connect(javascriptNode);
  javascriptNode.connect(audioContext.destination);

  const dataArray = new Uint8Array(analyser.frequencyBinCount);

  javascriptNode.onaudioprocess = () => {
    analyser.getByteTimeDomainData(dataArray);
    let sum = 0;
    for (let i = 0; i < dataArray.length; i++) {
      let val = (dataArray[i] - 128) / 128;
      sum += val * val;
    }
    const rms = Math.sqrt(sum / dataArray.length);

    // If RMS volume crosses threshold → blow detected
    if (rms > 0.25) { // adjust if too sensitive or not enough
      statusP.textContent = 'Status: blow detected!';
      blowOut();
      stop();
    }
  };
}

function stop() {
  startBtn.textContent = 'Start';
  running = false;
  statusP.textContent = 'Status: stopped';
  if (audioContext) {
    audioContext.close();
    audioContext = null;
  }
}

function blowOut() {
  flame.classList.add('off');
}
