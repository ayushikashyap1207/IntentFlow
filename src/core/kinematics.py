import numpy as np

def calculate_joint_angle(p1, p2, p3):
    """
    Calculates the 3D angle at vertex p2 formed by lines p1-p2 and p3-p2.
    Inputs are arrays/lists of [x, y, z]. Returns angle in degrees.
    """
    # Convert incoming points to numpy arrays
    p1 = np.array(p1) # e.g., Hip
    p2 = np.array(p2) # e.g., Knee (Vertex)
    p3 = np.array(p3) # e.g., Ankle

    # Construct vectors meeting at the vertex p2
    v1 = p1 - p2
    v2 = p3 - p2

    # Calculate dot product and vector magnitudes
    dot_product = np.dot(v1, v2)
    mag_v1 = np.linalg.norm(v1)
    mag_v2 = np.linalg.norm(v2)

    # Avoid division-by-zero errors on edge tracking drops
    if mag_v1 == 0 or mag_v2 == 0:
        return 0.0

    # Calculate cosine angle and clip to valid trigonometric bounds
    cos_angle = dot_product / (mag_v1 * mag_v2)
    cos_angle = np.clip(cos_angle, -1.0, 1.0)

    # Convert radians to degrees
    angle = np.arccos(cos_angle)
    return float(np.degrees(angle))

def extract_clinical_angles(frame_landmarks):
    """
    Extracts key orthopedic angles from a single MediaPipe landmarks dictionary frame.
    Assumes landmarks is a dict mapping index integers to [x, y, z, visibility].
    """
    # MediaPipe standard landmark indices mapping
    L_SHOULDER, R_SHOULDER = 11, 12
    L_ELBOW, R_ELBOW       = 13, 14
    L_HIP, R_HIP           = 23, 24
    L_KNEE, R_KNEE         = 25, 26
    L_ANKLE, R_ANKLE       = 27, 28

    angles = {}

    try:
        # 1. Knee Flexion Angles (Hip -> Knee -> Ankle)
        angles['left_knee'] = calculate_joint_angle(frame_landmarks[L_HIP][:3], frame_landmarks[L_KNEE][:3], frame_landmarks[L_ANKLE][:3])
        angles['right_knee'] = calculate_joint_angle(frame_landmarks[R_HIP][:3], frame_landmarks[R_KNEE][:3], frame_landmarks[R_ANKLE][:3])

        # 2. Shoulder Abduction/Flexion Angles (Elbow -> Shoulder -> Hip)
        angles['left_shoulder'] = calculate_joint_angle(frame_landmarks[L_ELBOW][:3], frame_landmarks[L_SHOULDER][:3], frame_landmarks[L_HIP][:3])
        angles['right_shoulder'] = calculate_joint_angle(frame_landmarks[R_ELBOW][:3], frame_landmarks[R_SHOULDER][:3], frame_landmarks[R_HIP][:3])
        
    except KeyError:
        # Return fallback zero values if tracking drops on a frame
        return {'left_knee': 0.0, 'right_knee': 0.0, 'left_shoulder': 0.0, 'right_shoulder': 0.0}

    return angles