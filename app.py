import os
import sys
import numpy as np
import tensorflow as tf
import streamlit as st
import pandas as pd

st.set_page_config(page_title="IntentFlow Clinical Rehab AI", page_icon="🏥", layout="wide")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TFLITE_PATH = os.path.join(ROOT_DIR, "models/tflite/intentflow_lstm.tflite")
SEQ_PATH = os.path.join(ROOT_DIR, "data/sequences/X_sequences.npy")

sys.path.append(ROOT_DIR)
from src.core.diagnostics import evaluate_patient_kinematics

st.title("🏥 IntentFlow — Advanced Orthopedic Diagnostics Dashboard")
st.markdown("Automated Biomechanical Analysis, Risk Triage, and Evidence-Based Rehabilitative Prescriptions")
st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Patient Session Control Panel")
    st.write("Execute deep kinematic analysis on raw tracking matrix streams to generate an automated clinical evaluation report.")
    run_btn = st.button("Generate Diagnostic Report", type="primary")

with col2:
    if run_btn:
        if not os.path.exists(TFLITE_PATH) or not os.path.exists(SEQ_PATH):
            st.error("Missing critical backend pipeline model or sequence binary data layers.")
        else:
            # 1. Edge model loading & inference execution
            interpreter = tf.lite.Interpreter(model_path=TFLITE_PATH)
            interpreter.allocate_tensors()
            
            X_data = np.load(SEQ_PATH)
            sample_sequence = X_data[0:1].astype(np.float32)
            
            interpreter.set_tensor(interpreter.get_input_details()[0]['index'], sample_sequence)
            interpreter.invoke()
            predictions = interpreter.get_tensor(interpreter.get_output_details()[0]['index'])[0]
            
            classes = ["PushUps", "TaiChi", "Squats_Rehab", "Shoulder_Abduction"]
            predicted_class = classes[np.argmax(predictions)]
            
            # 2. Extract detailed medical report telemetry dictionary
            rep = evaluate_patient_kinematics(predicted_class, sample_sequence)
            
            # -----------------------------------------------------------------
            # VISUAL RENDERING: THE AUTOMATED CLINICAL REPORT CARD
            # -----------------------------------------------------------------
            st.subheader("📋 Comprehensive Orthopedic Assessment Report")
            
            # Formulating the triage banner based on Risk Levels
            if rep["risk_level"] == "LOW":
                st.success(f"### **RISK LEVEL: {rep['risk_level']}**")
            elif rep["risk_level"] == "MEDIUM":
                st.warning(f"### **RISK LEVEL: {rep['risk_level']}**")
            else:
                st.error(f"### **RISK LEVEL: {rep['risk_level']}**")
                
            # Layout the clinical core metrics inside clean presentation sections
            st.markdown(f"#### **1. Assessment Type**\n> `{rep['type'].upper()}`")
            st.markdown(f"#### **2. Diagnosed Flaw / Problem**\n* {rep['problem']}")
            st.markdown(f"#### **3. Prescribed Corrective Solution**\n* {rep['solution']}")
            st.markdown(f"#### **4. Biomechanical Kinematics Description**\n{rep['kinematics_description']}")
            
            st.markdown("#### **5. Evidence-Based Clinical References**")
            for ref in rep["references"]:
                st.caption(f"📚 {ref}")
                
            st.markdown("---")
            st.markdown("### 📈 Measured Angular Trajectory Logs")
            
            # Pass the dynamically selected joint arrays directly to the UI chart layer
            chart_df = pd.DataFrame(rep["chart_data"])
            st.line_chart(chart_df)
            
    else:
        st.info("Awaiting streaming activation telemetry. Click the button to compile full evidence-based reports from spatial movement data.")