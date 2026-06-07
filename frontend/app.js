const video = document.getElementById('webcam');
const canvas = document.getElementById('snapshot-canvas');
const ctx = canvas.getContext('2d');
const outputFeed = document.getElementById('output-feed');
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const reportContent = document.getElementById('report-content');

let ws;
let isStreaming = false;
let streamInterval;

// Start Webcam & WebSocket
startBtn.addEventListener('click', async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        
        // Wait for video metadata to load to set canvas dimensions
        video.onloadedmetadata = () => {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            video.play();
            
            // Connect WebSocket
            connectWebSocket();
        };
        
        startBtn.disabled = true;
        stopBtn.disabled = false;
        isStreaming = true;
        
    } catch (err) {
        console.error("Error accessing webcam: ", err);
        alert("Please allow webcam access to use IntentFlow.");
    }
});

// Stop Webcam & WebSocket
stopBtn.addEventListener('click', () => {
    isStreaming = false;
    clearInterval(streamInterval);
    
    if (ws) {
        ws.close();
    }
    
    const stream = video.srcObject;
    if (stream) {
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
    }
    video.srcObject = null;
    
    outputFeed.src = "";
    startBtn.disabled = false;
    stopBtn.disabled = true;
});

function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    // If running locally, it defaults to localhost:8000
    const wsUrl = `${protocol}//${window.location.hostname}:${window.location.port || 8000}/ws/video`;
    
    ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
        console.log("WebSocket Connected");
        // Start sending frames
        streamInterval = setInterval(sendFrame, 100); // ~10 FPS to save bandwidth
    };
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        // Update Video Feed
        if (data.image) {
            outputFeed.src = data.image;
        }
        
        // Update Report
        if (data.report) {
            updateReport(data.report);
        }
    };
    
    ws.onerror = (err) => {
        console.error("WebSocket Error: ", err);
    };
    
    ws.onclose = () => {
        console.log("WebSocket Disconnected");
        if (isStreaming) {
            // Attempt reconnect if still supposedly streaming
            setTimeout(connectWebSocket, 1000);
        }
    };
}

function sendFrame() {
    if (!isStreaming || ws.readyState !== WebSocket.OPEN) return;
    
    // Draw current video frame to hidden canvas
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Get base64 string (JPEG compression)
    const base64Img = canvas.toDataURL('image/jpeg', 0.7);
    
    // Send to backend
    ws.send(base64Img);
}

function updateReport(rep) {
    const riskClass = `risk-${rep.risk_level}`;
    
    let html = `
        <div class="risk-banner ${riskClass}">
            RISK LEVEL: ${rep.risk_level}
        </div>
        
        <div class="report-item">
            <h4>Assessment Type</h4>
            <div class="metric-value">${rep.type.toUpperCase()}</div>
        </div>
        
        <div class="report-item">
            <h4>Diagnosed Problem</h4>
            <p>• ${rep.problem}</p>
        </div>
        
        <div class="report-item">
            <h4>Corrective Solution</h4>
            <p>• ${rep.solution}</p>
        </div>
        
        <div class="report-item">
            <h4>Kinematics Description</h4>
            <p>${rep.kinematics_description}</p>
        </div>
    `;
    
    reportContent.innerHTML = html;
    reportContent.classList.remove('empty');
}
