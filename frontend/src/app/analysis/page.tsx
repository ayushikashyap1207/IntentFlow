'use client';

import { Camera, CameraOff, Upload, Waves } from 'lucide-react';
import { useState } from 'react';
import AppShell from '../../components/layout/AppShell';
import Button from '../../components/ui/Button';
import Card from '../../components/ui/Card';
import { exerciseOptions, mockPatients } from '../../lib/mockData';

type ExerciseName = (typeof exerciseOptions)[number];

const poseDots = [
  { top: '18%', left: '24%' },
  { top: '29%', left: '42%' },
  { top: '41%', left: '31%' },
  { top: '53%', left: '54%' },
  { top: '68%', left: '40%' },
  { top: '26%', left: '67%' },
  { top: '62%', left: '72%' },
];

export default function AnalysisPage() {
  const [selectedPatient, setSelectedPatient] = useState(mockPatients[0]?.id ?? '');
  const [selectedExercise, setSelectedExercise] = useState<ExerciseName>(exerciseOptions[0]);
  const [inputMethod, setInputMethod] = useState<'webcam' | 'upload'>('webcam');
  const [cameraOn, setCameraOn] = useState(false);

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <p className="text-sm font-medium text-slate-500">Live analysis workflow</p>
          <h1 className="mt-1 text-2xl font-semibold text-slate-900">New analysis session</h1>
        </div>

        <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          <Card title="Session setup">
            <div className="space-y-4">
              <label className="block">
                <span className="mb-2 block text-sm font-medium text-slate-700">Select patient</span>
                <select
                  value={selectedPatient}
                  onChange={(event) => setSelectedPatient(event.target.value)}
                  className="h-11 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm text-slate-900 outline-none focus:border-blue-500"
                >
                  {mockPatients.map((patient) => (
                    <option key={patient.id} value={patient.id}>
                      {patient.name} • {patient.condition}
                    </option>
                  ))}
                </select>
              </label>

              <label className="block">
                <span className="mb-2 block text-sm font-medium text-slate-700">Select exercise</span>
                <select
                  value={selectedExercise}
                  onChange={(event) => setSelectedExercise(event.target.value as ExerciseName)}
                  className="h-11 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm text-slate-900 outline-none focus:border-blue-500"
                >
                  {exerciseOptions.map((exercise) => (
                    <option key={exercise} value={exercise}>
                      {exercise}
                    </option>
                  ))}
                </select>
              </label>

              <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
                <p className="mb-3 text-sm font-medium text-slate-700">Input method</p>
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                  <button
                    type="button"
                    onClick={() => setInputMethod('webcam')}
                    className={`rounded-xl border p-4 text-left transition-colors ${
                      inputMethod === 'webcam' ? 'border-blue-600 bg-blue-50 text-blue-700' : 'border-slate-200 bg-white text-slate-600 hover:bg-slate-50'
                    }`}
                  >
                    <Camera className="h-5 w-5" />
                    <div className="mt-3 text-sm font-semibold">Live webcam</div>
                    <p className="mt-1 text-xs text-slate-500">Best for real-time MediaPipe pose detection.</p>
                  </button>

                  <button
                    type="button"
                    onClick={() => setInputMethod('upload')}
                    className={`rounded-xl border p-4 text-left transition-colors ${
                      inputMethod === 'upload' ? 'border-blue-600 bg-blue-50 text-blue-700' : 'border-slate-200 bg-white text-slate-600 hover:bg-slate-50'
                    }`}
                  >
                    <Upload className="h-5 w-5" />
                    <div className="mt-3 text-sm font-semibold">Upload video</div>
                    <p className="mt-1 text-xs text-slate-500">Analyze an existing session recording.</p>
                  </button>
                </div>
              </div>
            </div>
          </Card>

          <Card title="Session context">
            <div className="space-y-4">
              <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
                <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Selected patient</p>
                <p className="mt-2 text-sm font-medium text-slate-900">
                  {mockPatients.find((patient) => patient.id === selectedPatient)?.name ?? 'No patient selected'}
                </p>
              </div>

              <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
                <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Exercise target</p>
                <p className="mt-2 text-sm font-medium text-slate-900">{selectedExercise}</p>
              </div>

              <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
                <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Input mode</p>
                <p className="mt-2 text-sm font-medium text-slate-900">{inputMethod === 'webcam' ? 'Live webcam' : 'Upload video'}</p>
              </div>
            </div>
          </Card>
        </div>

        <Card title="Webcam feed">
          <div className="space-y-4">
            <div className="relative overflow-hidden rounded-xl border border-slate-800 bg-slate-900">
              <div className="flex h-96 items-center justify-center">
                {cameraOn ? (
                  <>
                    <div className="absolute left-4 top-4 flex items-center gap-2 rounded-full bg-slate-800/90 px-3 py-1.5 text-xs font-medium text-cyan-300">
                      <span className="h-2 w-2 rounded-full bg-cyan-400" />
                      Live - MediaPipe pose detection active
                    </div>
                    {poseDots.map((dot, index) => (
                      <span
                        key={`${dot.top}-${dot.left}-${index}`}
                        className="absolute h-2.5 w-2.5 rounded-full bg-cyan-400 shadow-[0_0_0_6px_rgba(34,211,238,0.14)]"
                        style={{ top: dot.top, left: dot.left }}
                      />
                    ))}
                    <div className="text-center text-slate-200">
                      <Waves className="mx-auto h-10 w-10 text-cyan-300" />
                      <p className="mt-4 text-sm text-slate-300">Tracking body landmarks in real time.</p>
                    </div>
                  </>
                ) : (
                  <div className="text-center text-slate-300">
                    <CameraOff className="mx-auto h-10 w-10 text-slate-400" />
                    <p className="mt-4 text-sm font-medium text-slate-200">Camera not started</p>
                    <p className="mt-1 text-sm text-slate-400">Start the camera to activate pose detection.</p>
                  </div>
                )}
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              <Button variant="primary" onClick={() => setCameraOn(true)}>
                Start camera
              </Button>
              <Button variant="secondary" onClick={() => setCameraOn(false)} disabled={!cameraOn}>
                Stop
              </Button>
            </div>
          </div>
        </Card>

        <div className="flex justify-end">
          <Button href="/reports/session-001" variant="primary" className="px-6">
            Run analysis &amp; generate report →
          </Button>
        </div>
      </div>
    </AppShell>
  );
}