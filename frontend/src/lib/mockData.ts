export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH';

export interface Session {
  id: string;
  patientId: string;
  patientName: string;
  exercise: string;
  date: string;
  riskLevel: RiskLevel;
  formScore: number;
  repsAnalysed: number;
  avgKneeAngle: number;
  confidence: number;
  diagnosis: string;
  prescription: string;
  kinematics: string;
  detectedIssues: string[];
  references: string[];
  chartData: { rep: number; knee: number; hip: number; ankle: number }[];
}

export interface Patient {
  id: string;
  name: string;
  initials: string;
  age: number;
  gender: string;
  condition: string;
  riskLevel: RiskLevel;
  since: string;
  avatarColor: string;
  sessions: Session[];
  progress: { label: string; value: number }[];
}

export interface ActivityItem {
  tone: 'blue' | 'green' | 'amber' | 'red';
  text: string;
  time: string;
}

export const exerciseOptions = [
  'Push-ups',
  'Tai Chi',
  'Squats Rehab',
  'Shoulder Abduction',
  'Knee Extension',
  'Hip Abduction',
  'Lunges',
  'Ankle Dorsiflexion',
] as const;

const coreReferences = [
  'Magee DJ. Orthopedic Physical Assessment. 7th ed.',
  'Kisner C, Colby LA. Therapeutic Exercise: Foundations and Techniques. 8th ed.',
  'Neumann DA. Kinesiology of the Musculoskeletal System. 4th ed.',
];

const shoulderReferences = [
  'Brukner P, Khan K. Clinical Sports Medicine. 5th ed.',
  'Sahrmann SA. Diagnosis and Treatment of Movement Impairment Syndromes.',
  'Neumann DA. Kinesiology of the Musculoskeletal System. 4th ed.',
];

const balanceReferences = [
  'Shumway-Cook A, Woollacott M. Motor Control: Translating Research into Clinical Practice.',
  'Kisner C, Colby LA. Therapeutic Exercise: Foundations and Techniques. 8th ed.',
  'Norkin CC, Levangie PK. Joint Structure and Function.',
];

const buildChartData = (knee: number[], hip: number[], ankle: number[]) =>
  knee.map((value, index) => ({
    rep: index + 1,
    knee: value,
    hip: hip[index],
    ankle: ankle[index],
  }));

export const mockPatients: Patient[] = [
  {
    id: 'p001',
    name: 'Priya Sharma',
    initials: 'PS',
    age: 42,
    gender: 'Female',
    condition: 'Post-ACL reconstruction',
    riskLevel: 'MEDIUM',
    since: '2025-12-18T00:00:00Z',
    avatarColor: 'bg-blue-100 text-blue-700',
    progress: [
      { label: 'Strength recovery', value: 72 },
      { label: 'Knee control', value: 64 },
      { label: 'Confidence on load', value: 58 },
      { label: 'Home program adherence', value: 91 },
    ],
    sessions: [
      {
        id: 'session-001',
        patientId: 'p001',
        patientName: 'Priya Sharma',
        exercise: 'Squats Rehab',
        date: '2026-06-07T08:40:00Z',
        riskLevel: 'MEDIUM',
        formScore: 68,
        repsAnalysed: 24,
        avgKneeAngle: 56,
        confidence: 0.92,
        diagnosis: 'Mild dynamic valgus appears during mid-descent, with a delayed hip hinge.',
        prescription: 'Reduce squat depth to 70 degrees, cue knees over toes, and reinforce posterior chain loading.',
        kinematics: 'Knee flexion stays controlled, but hip excursion is insufficient and trunk angle rises early.',
        detectedIssues: ['Dynamic valgus', 'Trunk compensation', 'Uneven weight shift'],
        references: [...coreReferences],
        chartData: buildChartData([58, 56, 55, 57, 59], [42, 43, 44, 43, 42], [16, 17, 18, 17, 16]),
      },
      {
        id: 'session-002',
        patientId: 'p001',
        patientName: 'Priya Sharma',
        exercise: 'Knee Extension',
        date: '2026-06-05T09:10:00Z',
        riskLevel: 'LOW',
        formScore: 81,
        repsAnalysed: 20,
        avgKneeAngle: 18,
        confidence: 0.95,
        diagnosis: 'Terminal knee extension is consistent with only mild quadriceps lag.',
        prescription: 'Maintain slow tempo, add a 2-second pause at terminal extension, and progress resistance gradually.',
        kinematics: 'Extension path is smooth with a small loss of end-range control in the final repetitions.',
        detectedIssues: ['Mild quadriceps lag', 'Slight end-range drift'],
        references: [...coreReferences],
        chartData: buildChartData([17, 18, 18, 19, 18], [11, 11, 12, 11, 10], [6, 6, 5, 6, 6]),
      },
      {
        id: 'session-003',
        patientId: 'p001',
        patientName: 'Priya Sharma',
        exercise: 'Lunges',
        date: '2026-06-01T07:45:00Z',
        riskLevel: 'MEDIUM',
        formScore: 74,
        repsAnalysed: 18,
        avgKneeAngle: 61,
        confidence: 0.89,
        diagnosis: 'Forward step length is improving, though the pelvis still drops on the trailing side.',
        prescription: 'Use mirror feedback, shorten the stride slightly, and cue pelvic level during the lowering phase.',
        kinematics: 'Sagittal plane motion is controlled, but frontal plane stability needs more work.',
        detectedIssues: ['Pelvic drop', 'Short stance control', 'Frontal plane instability'],
        references: [...coreReferences],
        chartData: buildChartData([60, 61, 62, 61, 60], [44, 43, 44, 43, 42], [18, 18, 17, 18, 19]),
      },
    ],
  },
  {
    id: 'p002',
    name: 'Daniel Cruz',
    initials: 'DC',
    age: 58,
    gender: 'Male',
    condition: 'Rotator cuff rehabilitation',
    riskLevel: 'HIGH',
    since: '2025-11-04T00:00:00Z',
    avatarColor: 'bg-rose-100 text-rose-700',
    progress: [
      { label: 'Shoulder elevation', value: 49 },
      { label: 'Pain-free range', value: 42 },
      { label: 'Scapular control', value: 37 },
      { label: 'Session adherence', value: 78 },
    ],
    sessions: [
      {
        id: 'session-004',
        patientId: 'p002',
        patientName: 'Daniel Cruz',
        exercise: 'Shoulder Abduction',
        date: '2026-06-06T10:25:00Z',
        riskLevel: 'HIGH',
        formScore: 46,
        repsAnalysed: 16,
        avgKneeAngle: 14,
        confidence: 0.87,
        diagnosis: 'Marked scapular hiking and early trunk lean appear once the arm passes 80 degrees.',
        prescription: 'Lower the load, cap abduction at pain-free range, and reinforce serratus activation before progression.',
        kinematics: 'Movement quality deteriorates late in the set, with compensation increasing on the dominant side.',
        detectedIssues: ['Scapular hiking', 'Trunk lean', 'Limited pain-free range'],
        references: [...shoulderReferences],
        chartData: buildChartData([73, 76, 79, 82, 85], [21, 22, 23, 24, 25], [12, 12, 13, 13, 14]),
      },
      {
        id: 'session-005',
        patientId: 'p002',
        patientName: 'Daniel Cruz',
        exercise: 'Push-ups',
        date: '2026-06-03T11:00:00Z',
        riskLevel: 'HIGH',
        formScore: 42,
        repsAnalysed: 12,
        avgKneeAngle: 52,
        confidence: 0.88,
        diagnosis: 'Lumbar extension increases with fatigue and the shoulder girdle collapses late in each rep.',
        prescription: 'Switch to incline push-ups, tighten the trunk brace, and keep elbows at a 45-degree angle.',
        kinematics: 'The kinetic chain loses stiffness at the bottom of the movement, making the rep pattern unstable.',
        detectedIssues: ['Lumbar extension', 'Scapular collapse', 'Fatigue compensation'],
        references: [...shoulderReferences],
        chartData: buildChartData([49, 51, 52, 54, 56], [28, 29, 29, 30, 31], [18, 18, 19, 19, 20]),
      },
      {
        id: 'session-006',
        patientId: 'p002',
        patientName: 'Daniel Cruz',
        exercise: 'Hip Abduction',
        date: '2026-05-30T09:50:00Z',
        riskLevel: 'MEDIUM',
        formScore: 59,
        repsAnalysed: 18,
        avgKneeAngle: 13,
        confidence: 0.91,
        diagnosis: 'Hip lift is adequate, but trunk stability drops on the last several repetitions.',
        prescription: 'Add an isometric core hold and reduce range slightly until pelvic control improves.',
        kinematics: 'Coronal plane alignment is acceptable early, then the trunk begins to rotate to compensate.',
        detectedIssues: ['Trunk rotation', 'Core fatigue', 'Late-rep compensation'],
        references: [...coreReferences],
        chartData: buildChartData([11, 12, 12, 13, 14], [17, 17, 18, 18, 18], [8, 8, 9, 9, 10]),
      },
    ],
  },
  {
    id: 'p003',
    name: 'Meera Patel',
    initials: 'MP',
    age: 67,
    gender: 'Female',
    condition: 'Post-stroke balance retraining',
    riskLevel: 'MEDIUM',
    since: '2025-09-22T00:00:00Z',
    avatarColor: 'bg-emerald-100 text-emerald-700',
    progress: [
      { label: 'Balance control', value: 79 },
      { label: 'Weight shift symmetry', value: 63 },
      { label: 'Ankle mobility', value: 71 },
      { label: 'Walking confidence', value: 66 },
    ],
    sessions: [
      {
        id: 'session-007',
        patientId: 'p003',
        patientName: 'Meera Patel',
        exercise: 'Tai Chi',
        date: '2026-06-07T06:30:00Z',
        riskLevel: 'LOW',
        formScore: 87,
        repsAnalysed: 30,
        avgKneeAngle: 19,
        confidence: 0.96,
        diagnosis: 'Weight transfer is fluid with improved symmetry across the stance phases.',
        prescription: 'Keep the same cadence and introduce longer single-leg holds to challenge proprioception.',
        kinematics: 'Movement is smooth, with only a small loss of ankle strategy during slower transitions.',
        detectedIssues: ['Mild ankle strategy loss', 'Low-amplitude sway'],
        references: [...balanceReferences],
        chartData: buildChartData([18, 19, 19, 20, 19], [12, 12, 13, 12, 12], [8, 8, 9, 8, 8]),
      },
      {
        id: 'session-008',
        patientId: 'p003',
        patientName: 'Meera Patel',
        exercise: 'Ankle Dorsiflexion',
        date: '2026-06-04T08:20:00Z',
        riskLevel: 'MEDIUM',
        formScore: 72,
        repsAnalysed: 22,
        avgKneeAngle: 11,
        confidence: 0.93,
        diagnosis: 'Dorsiflexion range is improving, although the toe clearance window remains narrow.',
        prescription: 'Add seated dorsiflexion holds, then progress to standing repetitions with a slower eccentric return.',
        kinematics: 'Tibial translation is adequate, but the foot clears the floor by a small margin only.',
        detectedIssues: ['Narrow toe clearance', 'Limited dorsiflexion'],
        references: [...balanceReferences],
        chartData: buildChartData([12, 11, 12, 11, 10], [8, 8, 8, 9, 9], [4, 4, 4, 5, 5]),
      },
      {
        id: 'session-009',
        patientId: 'p003',
        patientName: 'Meera Patel',
        exercise: 'Squats Rehab',
        date: '2026-05-28T07:40:00Z',
        riskLevel: 'MEDIUM',
        formScore: 65,
        repsAnalysed: 20,
        avgKneeAngle: 53,
        confidence: 0.9,
        diagnosis: 'Squat depth is limited by balance, not pain, but trunk control still needs reinforcement.',
        prescription: 'Use a support bar, keep repetitions slower, and preserve the mid-foot pressure line.',
        kinematics: 'Posterior sway appears when the descent speed increases, especially in the final reps.',
        detectedIssues: ['Posterior sway', 'Balance-limited depth', 'Slow trunk recovery'],
        references: [...coreReferences],
        chartData: buildChartData([55, 54, 53, 54, 55], [39, 39, 40, 39, 38], [15, 15, 16, 15, 15]),
      },
    ],
  },
  {
    id: 'p004',
    name: 'Omar Hassan',
    initials: 'OH',
    age: 31,
    gender: 'Male',
    condition: 'Patellofemoral pain syndrome',
    riskLevel: 'LOW',
    since: '2026-01-10T00:00:00Z',
    avatarColor: 'bg-amber-100 text-amber-700',
    progress: [
      { label: 'Pain reduction', value: 88 },
      { label: 'Quad endurance', value: 81 },
      { label: 'Single-leg balance', value: 74 },
      { label: 'Return-to-run readiness', value: 67 },
    ],
    sessions: [
      {
        id: 'session-010',
        patientId: 'p004',
        patientName: 'Omar Hassan',
        exercise: 'Lunges',
        date: '2026-06-06T13:15:00Z',
        riskLevel: 'LOW',
        formScore: 84,
        repsAnalysed: 28,
        avgKneeAngle: 58,
        confidence: 0.97,
        diagnosis: 'Lunge mechanics are stable with strong hip-knee coordination and minimal valgus drift.',
        prescription: 'Progress depth gradually and add tempo variation to continue building eccentric control.',
        kinematics: 'Frontal plane control remains centered throughout the movement cycle.',
        detectedIssues: ['Mild stride asymmetry'],
        references: [...coreReferences],
        chartData: buildChartData([57, 58, 59, 58, 57], [40, 41, 41, 42, 41], [16, 16, 17, 16, 16]),
      },
      {
        id: 'session-011',
        patientId: 'p004',
        patientName: 'Omar Hassan',
        exercise: 'Knee Extension',
        date: '2026-06-02T10:05:00Z',
        riskLevel: 'LOW',
        formScore: 88,
        repsAnalysed: 24,
        avgKneeAngle: 16,
        confidence: 0.96,
        diagnosis: 'Terminal extension is clean and pain-free, with excellent control across all repetitions.',
        prescription: 'Maintain current loading and add a short isometric hold at the top of the movement.',
        kinematics: 'The knee path is steady and the pelvis remains quiet during the extension phase.',
        detectedIssues: ['None significant'],
        references: [...coreReferences],
        chartData: buildChartData([16, 16, 17, 17, 16], [10, 10, 10, 11, 10], [4, 4, 5, 4, 4]),
      },
      {
        id: 'session-012',
        patientId: 'p004',
        patientName: 'Omar Hassan',
        exercise: 'Push-ups',
        date: '2026-05-29T12:20:00Z',
        riskLevel: 'LOW',
        formScore: 79,
        repsAnalysed: 18,
        avgKneeAngle: 49,
        confidence: 0.95,
        diagnosis: 'Trunk control is adequate, though speed consistency varies slightly between sets.',
        prescription: 'Keep current level and add a metronome to stabilize tempo across all reps.',
        kinematics: 'The body line stays aligned with only a small loss of rigidity on the final two reps.',
        detectedIssues: ['Tempo drift', 'Late-set fatigue'],
        references: [...coreReferences],
        chartData: buildChartData([48, 49, 50, 50, 49], [27, 28, 28, 29, 28], [17, 17, 18, 18, 17]),
      },
    ],
  },
  {
    id: 'p005',
    name: 'Hannah Lee',
    initials: 'HL',
    age: 49,
    gender: 'Female',
    condition: 'Shoulder mobility and postural control',
    riskLevel: 'MEDIUM',
    since: '2025-10-07T00:00:00Z',
    avatarColor: 'bg-cyan-100 text-cyan-700',
    progress: [
      { label: 'Shoulder range', value: 68 },
      { label: 'Postural endurance', value: 61 },
      { label: 'Scapular control', value: 76 },
      { label: 'Workout consistency', value: 84 },
    ],
    sessions: [
      {
        id: 'session-013',
        patientId: 'p005',
        patientName: 'Hannah Lee',
        exercise: 'Shoulder Abduction',
        date: '2026-06-05T15:45:00Z',
        riskLevel: 'MEDIUM',
        formScore: 63,
        repsAnalysed: 20,
        avgKneeAngle: 8,
        confidence: 0.9,
        diagnosis: 'Shoulder elevation is improving, but the scapula still elevates sooner than expected.',
        prescription: 'Pause at 60 degrees, cue the shoulder blade to stay anchored, and reduce speed slightly.',
        kinematics: 'Abduction path is smooth until the upper third where scapular substitution becomes visible.',
        detectedIssues: ['Scapular elevation', 'Early substitution', 'Speed compensation'],
        references: [...shoulderReferences],
        chartData: buildChartData([32, 34, 36, 38, 39], [24, 24, 25, 25, 26], [9, 9, 10, 10, 10]),
      },
      {
        id: 'session-014',
        patientId: 'p005',
        patientName: 'Hannah Lee',
        exercise: 'Tai Chi',
        date: '2026-06-01T14:10:00Z',
        riskLevel: 'LOW',
        formScore: 85,
        repsAnalysed: 26,
        avgKneeAngle: 20,
        confidence: 0.94,
        diagnosis: 'Weight transfer and breathing cadence are synchronized with a clean center-of-mass path.',
        prescription: 'Continue the current sequence and add longer pauses during transitions to increase control demand.',
        kinematics: 'The trunk stays tall and the lower limbs move in a coordinated, low-compensation pattern.',
        detectedIssues: ['Minor cadence drift'],
        references: [...balanceReferences],
        chartData: buildChartData([21, 20, 20, 19, 20], [13, 13, 14, 13, 13], [9, 9, 9, 8, 8]),
      },
      {
        id: 'session-015',
        patientId: 'p005',
        patientName: 'Hannah Lee',
        exercise: 'Ankle Dorsiflexion',
        date: '2026-05-27T09:35:00Z',
        riskLevel: 'MEDIUM',
        formScore: 70,
        repsAnalysed: 18,
        avgKneeAngle: 10,
        confidence: 0.91,
        diagnosis: 'Dorsiflexion improves with a small medial shift at the end of each set.',
        prescription: 'Add a wall-supported range drill and keep the heel grounded through each hold.',
        kinematics: 'Ankle motion is smooth with a mild compensatory inversion pattern near the top end.',
        detectedIssues: ['Mild inversion bias', 'End-range compensation'],
        references: [...balanceReferences],
        chartData: buildChartData([10, 10, 11, 10, 10], [7, 7, 8, 7, 7], [3, 4, 4, 4, 3]),
      },
    ],
  },
];

export const mockSessions: Session[] = mockPatients.flatMap((patient) => patient.sessions);

export const mockActivityFeed: ActivityItem[] = [
  {
    tone: 'green',
    text: 'Priya Sharma completed Squats Rehab with improved valgus control.',
    time: '8 min ago',
  },
  {
    tone: 'red',
    text: 'Daniel Cruz triggered a high-risk alert during Shoulder Abduction.',
    time: '21 min ago',
  },
  {
    tone: 'blue',
    text: 'Meera Patel started a Tai Chi balance session in the clinic room.',
    time: '39 min ago',
  },
  {
    tone: 'amber',
    text: 'Omar Hassan progressed to deeper lunges with stable knee alignment.',
    time: '1 hr ago',
  },
  {
    tone: 'green',
    text: 'Hannah Lee reviewed the latest report and prescribed home exercises.',
    time: 'Today',
  },
];

export const getPatientById = (id: string) => mockPatients.find((patient) => patient.id === id);

export const getSessionById = (id: string) => mockSessions.find((session) => session.id === id);

export const getLatestSessionForPatient = (patientId: string) => {
  const patient = getPatientById(patientId);
  return patient?.sessions[0];
};

export const getRecentPatients = (limit = 4) =>
  [...mockPatients]
    .sort((left, right) => {
      const leftDate = new Date(getLatestSessionForPatient(left.id)?.date ?? left.since).getTime();
      const rightDate = new Date(getLatestSessionForPatient(right.id)?.date ?? right.since).getTime();
      return rightDate - leftDate;
    })
    .slice(0, limit);

export const formatDate = (value: string) =>
  new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  }).format(new Date(value));

export const formatDateTime = (value: string) =>
  new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  }).format(new Date(value));