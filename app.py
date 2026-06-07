import os
import sys
import numpy as np
import tensorflow as tf
import streamlit as st
import pandas as pd
import av
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

# Premium dark mode configuration
st.set_page_config(page_title="IntentFlow Clinical Rehab AI", page_icon="🏥", layout="wide", initial_sidebar_state="collapsed")

# Custom Premium CSS (Glassmorphism, Google Fonts, Vibrant Gradients)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .main {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: #f8fafc;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out;
    }
    .glass-card:hover {
        transform: translateY(-5px);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TFLITE_PATH = os.path.join(ROOT_DIR, "models/tflite/intentflow_lstm.tflite")
sys.path.append(ROOT_DIR)

from src.core.diagnostics import evaluate_patient_kinematics
from src.core.extractor import process_live_frame, options
from mediapipe.tasks.python import vision

st.title("🏥 IntentFlow — Live Orthopedic Assessment")
st.markdown("Real-time Automated Biomechanical Analysis and Rehabilitative Prescriptions.")
st.divider()

class PoseProcessor(VideoProcessorBase):
    def __init__(self):
        self.frame_buffer = []
        self.latest_report = None
        
        # Load TFLite Model inside processor
        if os.path.exists(TFLITE_PATH):
            self.interpreter = tf.lite.Interpreter(model_path=TFLITE_PATH)
            self.interpreter.allocate_tensors()
        else:
            self.interpreter = None
            
        self.landmarker = vision.PoseLandmarker.create_from_options(options)

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        annotated_frame, features = process_live_frame(img, self.landmarker)
        
        self.frame_buffer.append(features)
        if len(self.frame_buffer) > 30:
            self.frame_buffer.pop(0)
            
        if len(self.frame_buffer) == 30 and self.interpreter is not None:
            sample_sequence = np.array([self.frame_buffer]).astype(np.float32)
            self.interpreter.set_tensor(self.interpreter.get_input_details()[0]['index'], sample_sequence)
            self.interpreter.invoke()
            predictions = self.interpreter.get_tensor(self.interpreter.get_output_details()[0]['index'])[0]
            
            classes = ["PushUps", "TaiChi", "Squats_Rehab", "Shoulder_Abduction"]
            predicted_class = classes[np.argmax(predictions)]
            self.latest_report = evaluate_patient_kinematics(predicted_class, sample_sequence[0])
            
        return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🎥 Live Tracking Feed")
    st.write("Ensure your full body is visible in the frame.")
    ctx = webrtc_streamer(key="pose-tracking", video_processor_factory=PoseProcessor,
                          media_stream_constraints={"video": True, "audio": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if ctx and ctx.video_processor and hasattr(ctx.video_processor, 'latest_report') and ctx.video_processor.latest_report:
        rep = ctx.video_processor.latest_report
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📋 Clinical Assessment Report")
        
        if rep["risk_level"] == "LOW":
            st.success(f"### **RISK LEVEL: {rep['risk_level']}**")
        elif rep["risk_level"] == "MEDIUM":
            st.warning(f"### **RISK LEVEL: {rep['risk_level']}**")
        else:
            st.error(f"### **RISK LEVEL: {rep['risk_level']}**")
            
        st.markdown(f"#### Assessment Type\n> <span class='metric-value'>{rep['type'].upper()}</span>", unsafe_allow_html=True)
        st.markdown(f"#### Diagnosed Problem\n* {rep['problem']}")
        st.markdown(f"#### Corrective Solution\n* {rep['solution']}")
        st.markdown(f"#### Kinematics\n{rep['kinematics_description']}")
        
        chart_df = pd.DataFrame(rep["chart_data"])
        st.line_chart(chart_df)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.info("Awaiting live sequence data. Step into the frame and perform your prescribed exercise for 1-2 seconds.")
        st.markdown('</div>', unsafe_allow_html=True)