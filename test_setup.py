import os
import sys

print("=" * 60)
print("IntentFlow - Local Stack Verification Suite")
print("=" * 60)

print(f"Active Python Path: {sys.executable}")
print(f"Platform Machine: {sys.platform} - {os.uname().machine}\n")

checks = []

def verify_module(name, import_statement):
    try:
        mod = import_statement()
        version = getattr(mod, '__version__', 'Installed (OK)')
        checks.append((name, version, True))
    except Exception as e:
        checks.append((name, str(e)[:40], False))

# Core Modules Tracking
try:
    import mediapipe as mp
    checks.append(("MediaPipe", "Installed (OK)", True))
except Exception as e:
    checks.append(("MediaPipe", str(e)[:40], False))

try:
    import tensorflow as tf
    checks.append(("TensorFlow", tf.__version__, True))
except Exception as e:
    checks.append(("TensorFlow", str(e)[:40], False))

try:
    import cv2
    checks.append(("OpenCV", cv2.__version__, True))
except Exception as e:
    checks.append(("OpenCV", str(e)[:40], False))

try:
    import chromadb
    checks.append(("ChromaDB", chromadb.__version__, True))
except Exception as e:
    checks.append(("ChromaDB", str(e)[:40], False))

try:
    import sentence_transformers
    checks.append(("Sentence-Transformers", sentence_transformers.__version__, True))
except Exception as e:
    checks.append(("Sentence-Transformers", str(e)[:40], False))

try:
    import fastapi
    checks.append(("FastAPI", fastapi.__version__, True))
except Exception as e:
    checks.append(("FastAPI", str(e)[:40], False))

try:
    import streamlit
    checks.append(("Streamlit", streamlit.__version__, True))
except Exception as e:
    checks.append(("Streamlit", str(e)[:40], False))

try:
    import groq
    checks.append(("Groq Cloud SDK", "Installed (OK)", True))
except Exception as e:
    checks.append(("Groq Cloud SDK", str(e)[:40], False))

try:
    import supabase
    import psycopg2
    checks.append(("Supabase/Postgres", "Drivers Linked (OK)", True))
except Exception as e:
    checks.append(("Supabase/Postgres", str(e)[:40], False))

all_passed = True
for name, version, passed in checks:
    status = "[OK]" if passed else "[FAIL]"
    print(f"  {status:<7} {name:<25}: {version}")
    if not passed:
        all_passed = False

print("-" * 60)
if all_passed:
    print("STATUS: Configuration verified! Ready for Phase 2 processing.")
else:
    print("STATUS: Error detected. Re-verify your conda installation mappings.")
print("=" * 60)