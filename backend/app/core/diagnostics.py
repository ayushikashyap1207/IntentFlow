from __future__ import annotations

from typing import Any


_REFERENCES = {
    'PushUps': [
        'Escamilla, R. F., et al. (2002). Biomechanical analysis of the push-up and bench press exercises. Journal of Applied Biomechanics.',
        'Lehman, G. J., et al. (2005). Shoulder muscle activity during push-up variations. Journal of Strength and Conditioning Research.',
        'Kisner, C., Colby, L. A. Therapeutic Exercise: Foundations and Techniques. 8th ed.',
    ],
    'TaiChi': [
        'Li, F., et al. (2005). Tai Chi and postural stability in older adults. Journal of Gerontology.',
        'Shumway-Cook, A., Woollacott, M. Motor Control: Translating Research into Clinical Practice.',
        'Norkin, C. C., Levangie, P. K. Joint Structure and Function.',
    ],
    'Squats_Rehab': [
        'Schoenfeld, B. J. (2010). Squatting mechanics: kinematics, kinetics, and muscle recruitment. The Journal of Strength & Conditioning Research.',
        'Neumann, D. A. Kinesiology of the Musculoskeletal System. 4th ed.',
        'Kisner, C., Colby, L. A. Therapeutic Exercise: Foundations and Techniques. 8th ed.',
    ],
    'Shoulder_Abduction': [
        'Wilk, K. E., et al. (2009). Rehabilitation of shoulder compressive pathologies. JOSPT.',
        'Magee, D. J. Orthopedic Physical Assessment. 7th ed.',
        'Sahrmann, S. A. Diagnosis and Treatment of Movement Impairment Syndromes.',
    ],
    'Knee_Extension': [
        'Perry, J., Burnfield, J. M. Gait Analysis: Normal and Pathological Function.',
        'Neumann, D. A. Kinesiology of the Musculoskeletal System. 4th ed.',
        'Magee, D. J. Orthopedic Physical Assessment. 7th ed.',
    ],
    'Hip_Abduction': [
        'Bolgla, L. A., Uhl, T. L. Electromyographic analysis of hip abductor exercises. Journal of Orthopaedic & Sports Physical Therapy.',
        'Neumann, D. A. Kinesiology of the Musculoskeletal System. 4th ed.',
        'Kisner, C., Colby, L. A. Therapeutic Exercise: Foundations and Techniques. 8th ed.',
    ],
    'Lunges': [
        'McCurdy, K., et al. (2010). Kinematic analysis of the lunge and step-up. Journal of Strength and Conditioning Research.',
        'Neumann, D. A. Kinesiology of the Musculoskeletal System. 4th ed.',
        'Magee, D. J. Orthopedic Physical Assessment. 7th ed.',
    ],
    'Ankle_Dorsiflexion': [
        'Norkin, C. C., Levangie, P. K. Joint Structure and Function.',
        'Kisner, C., Colby, L. A. Therapeutic Exercise: Foundations and Techniques. 8th ed.',
        'Perry, J., Burnfield, J. M. Gait Analysis: Normal and Pathological Function.',
    ],
}


def _base_report(exercise: str) -> dict[str, Any]:
    return {
        'diagnosis': 'Movement pattern is clinically acceptable with no major compensations detected.',
        'prescription': 'Maintain the current program and progress load or range gradually while preserving form quality.',
        'kinematics': 'Joint motion remains symmetrical and within expected rehabilitation thresholds.',
        'risk_level': 'LOW',
        'detected_issues': ['None significant'],
        'references': _REFERENCES.get(exercise, _REFERENCES['Squats_Rehab']),
        'form_score': 82,
    }


def get_fallback_report(exercise: str) -> dict[str, Any]:
    key = exercise.replace(' ', '_').replace('-', '_')
    report = _base_report(key)

    overrides: dict[str, dict[str, Any]] = {
        'PushUps': {
            'diagnosis': 'Trunk stiffness is acceptable, but shoulder and elbow control degrade when depth increases. Mild scapular compensation appears near the bottom of the rep.',
            'prescription': 'Use incline push-ups, cue a rigid trunk brace, and keep elbows near a 45-degree angle. Progress only when chest depth and scapular control remain stable across all repetitions.',
            'kinematics': 'Elbow flexion is present with some late-rep loss of posterior chain stiffness and minor scapular protraction.',
            'risk_level': 'MEDIUM',
            'detected_issues': ['Scapular control loss', 'Trunk extension drift', 'Depth inconsistency'],
            'form_score': 61,
        },
        'TaiChi': {
            'diagnosis': 'Weight transfer is smooth, but the center of mass drifts slightly during slower transitions. Balance recovery is generally good.',
            'prescription': 'Increase hold times in single-leg transitions and emphasize quiet trunk control. Add proprioceptive feedback to keep the pelvis centered over the stance leg.',
            'kinematics': 'The lower limb chain shows coordinated sagittal and frontal plane control with mild sway under tempo changes.',
            'risk_level': 'LOW',
            'detected_issues': ['Mild sway', 'Cadence drift'],
            'form_score': 86,
        },
        'Squats_Rehab': {
            'diagnosis': 'Squat depth is limited by balance and motor control rather than pain alone. Mild valgus collapse appears in the last third of the descent.',
            'prescription': 'Use a box target or support bar, cue knees over toes, and slow the eccentric phase. Build depth gradually while maintaining a stable foot tripod.',
            'kinematics': 'Hip and knee flexion are coordinated, but frontal plane stability decreases as depth increases.',
            'risk_level': 'MEDIUM',
            'detected_issues': ['Dynamic valgus', 'Posterior sway', 'Asymmetrical loading'],
            'form_score': 67,
        },
        'Shoulder_Abduction': {
            'diagnosis': 'Scapular substitution appears before full overhead range is achieved, suggesting compensatory elevation. Range tolerance is reduced late in the set.',
            'prescription': 'Reduce the load, stay in a pain-free arc, and reinforce serratus and lower trapezius activation. Progress only after the scapula remains stable through the upper third of the movement.',
            'kinematics': 'Glenohumeral abduction is truncated by trunk lean and early scapular hiking.',
            'risk_level': 'HIGH',
            'detected_issues': ['Scapular hiking', 'Trunk lean', 'Limited range'],
            'form_score': 48,
        },
        'Knee_Extension': {
            'diagnosis': 'Terminal knee extension is mostly controlled, with a small quadriceps lag at the end of the set. End-range tracking is otherwise satisfactory.',
            'prescription': 'Use a slower concentric tempo with a brief end-range pause. Increase resistance only if the knee remains aligned and the pelvis stays quiet.',
            'kinematics': 'Tibiofemoral motion is clean, with modest reduction in terminal extension control under fatigue.',
            'risk_level': 'LOW',
            'detected_issues': ['Mild quadriceps lag', 'End-range drift'],
            'form_score': 79,
        },
        'Hip_Abduction': {
            'diagnosis': 'Hip abduction is achieved, but trunk rotation and pelvic drift emerge toward the end of the set. Coronal plane control needs reinforcement.',
            'prescription': 'Reduce range slightly, add an isometric core brace, and cue the pelvis to stay stacked. Progress once the trunk remains quiet for all repetitions.',
            'kinematics': 'The lateral hip chain is active, but pelvic stability drops when fatigue accumulates.',
            'risk_level': 'MEDIUM',
            'detected_issues': ['Pelvic drift', 'Trunk rotation', 'Core fatigue'],
            'form_score': 63,
        },
        'Lunges': {
            'diagnosis': 'Lunge mechanics are functional with mild asymmetry between stance and swing phases. The trailing pelvis dips slightly during the lowering phase.',
            'prescription': 'Shorten the step slightly, keep the torso tall, and mirror-check pelvic level during each repetition. Add slower eccentrics before increasing depth.',
            'kinematics': 'Sagittal plane motion is smooth, but frontal plane control weakens when the patient descends quickly.',
            'risk_level': 'LOW',
            'detected_issues': ['Pelvic drop', 'Stride asymmetry', 'Tempo drift'],
            'form_score': 74,
        },
        'Ankle_Dorsiflexion': {
            'diagnosis': 'Dorsiflexion range is improving, though the final degrees of motion remain slightly limited. Toe clearance is present but narrow.',
            'prescription': 'Use wall-supported dorsiflexion holds, then progress to standing repeats with a slow eccentric return. Keep the heel grounded and avoid compensatory inversion.',
            'kinematics': 'Tibial translation is present with mild inversion bias at the top end of the available range.',
            'risk_level': 'MEDIUM',
            'detected_issues': ['Limited dorsiflexion', 'Narrow toe clearance', 'Inversion bias'],
            'form_score': 70,
        },
    }

    if key in overrides:
        report.update(overrides[key])
    return report
