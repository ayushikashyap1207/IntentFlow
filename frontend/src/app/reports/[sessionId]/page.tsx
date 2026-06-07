'use client';

import { ArrowLeft, BookOpen, Download } from 'lucide-react';
import { useMemo, useState } from 'react';
import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import AppShell from '../../../components/layout/AppShell';
import Badge from '../../../components/ui/Badge';
import Button from '../../../components/ui/Button';
import Card from '../../../components/ui/Card';
import MetricCard from '../../../components/ui/MetricCard';
import RiskBanner from '../../../components/ui/RiskBanner';
import { formatDateTime, getSessionById, mockSessions } from '../../../lib/mockData';

type ReportPageProps = {
  params: {
    sessionId: string;
  };
};

type ChartMode = 'knee' | 'hip' | 'ankle';
type MetricColor = 'slate' | 'blue' | 'green' | 'amber' | 'red';

export default function ReportPage({ params }: ReportPageProps) {
  const session = getSessionById(params.sessionId) ?? mockSessions[0];
  const [chartMode, setChartMode] = useState<ChartMode>('knee');

  const chartData = useMemo(
    () =>
      session.chartData.map((point) => ({
        rep: point.rep,
        value: point[chartMode],
      })),
    [chartMode, session.chartData],
  );

  const metricCards: Array<{ label: string; value: string | number; color: MetricColor }> = [
    { label: 'Form score', value: `${session.formScore}%`, color: session.formScore < 50 ? 'red' : 'blue' },
    { label: 'Reps analysed', value: session.repsAnalysed, color: 'slate' },
    { label: 'Avg knee angle', value: `${session.avgKneeAngle}°`, color: 'blue' },
    { label: 'Confidence', value: `${Math.round(session.confidence * 100)}%`, color: 'green' },
  ];

  return (
    <AppShell>
      <div className="space-y-6">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="space-y-3">
            <Button href="/dashboard" variant="secondary" size="sm" leftIcon={<ArrowLeft className="h-4 w-4" />}>
              Back
            </Button>
            <div>
              <p className="text-sm font-medium text-slate-500">Session report</p>
              <h1 className="mt-1 text-2xl font-semibold text-slate-900">{session.patientName}</h1>
              <p className="mt-2 text-sm text-slate-500">
                {session.exercise} • {formatDateTime(session.date)}
              </p>
            </div>
          </div>

          <Button variant="secondary" leftIcon={<Download className="h-4 w-4" />}>
            Export PDF
          </Button>
        </div>

        <RiskBanner riskLevel={session.riskLevel} />

        <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          <div className="space-y-6">
            <Card title="Clinical details">
              <div className="space-y-5">
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Assessment type</p>
                  <div className="mt-2">
                    <Badge variant="blue">{session.exercise}</Badge>
                  </div>
                </div>

                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Diagnosed flaw</p>
                  <p className="mt-2 text-sm leading-6 text-slate-700">{session.diagnosis}</p>
                </div>

                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Prescribed solution</p>
                  <p className="mt-2 text-sm leading-6 text-slate-700">{session.prescription}</p>
                </div>

                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Biomechanical description</p>
                  <p className="mt-2 text-sm leading-6 text-slate-700">{session.kinematics}</p>
                </div>
              </div>
            </Card>

            <Card title="References">
              <div className="space-y-3">
                {session.references.map((reference) => (
                  <div key={reference} className="flex items-start gap-3 rounded-lg border border-slate-200 bg-slate-50 p-3">
                    <BookOpen className="mt-0.5 h-4 w-4 text-blue-600" />
                    <p className="text-sm text-slate-700">{reference}</p>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          <div className="space-y-6">
            <Card title="Joint angle chart">
              <div className="mb-4 flex items-center gap-2 rounded-lg bg-slate-100 p-1">
                {(['knee', 'hip', 'ankle'] as ChartMode[]).map((mode) => {
                  const active = chartMode === mode;
                  return (
                    <button
                      key={mode}
                      type="button"
                      onClick={() => setChartMode(mode)}
                      className={`rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                        active ? 'bg-white text-blue-600 shadow-none' : 'text-slate-500 hover:text-slate-700'
                      }`}
                    >
                      {mode.charAt(0).toUpperCase() + mode.slice(1)}
                    </button>
                  );
                })}
              </div>

              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartData}>
                    <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" />
                    <XAxis dataKey="rep" tick={{ fill: '#64748b', fontSize: 12 }} axisLine={{ stroke: '#cbd5e1' }} tickLine={false} />
                    <YAxis tick={{ fill: '#64748b', fontSize: 12 }} axisLine={{ stroke: '#cbd5e1' }} tickLine={false} />
                    <Tooltip
                      contentStyle={{
                        border: '1px solid #e2e8f0',
                        borderRadius: '12px',
                        backgroundColor: '#ffffff',
                        boxShadow: 'none',
                      }}
                    />
                    <Line type="monotone" dataKey="value" stroke="#1a56db" strokeWidth={2} dot={{ r: 3 }} activeDot={{ r: 5 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </Card>

            <Card title="Session metrics">
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                {metricCards.map((metric) => (
                  <MetricCard key={metric.label} label={metric.label} value={metric.value} color={metric.color} />
                ))}
              </div>
            </Card>

            <Card title="Detected issues">
              <div className="flex flex-wrap gap-2">
                {session.detectedIssues.map((issue) => (
                  <span key={issue} className="rounded-md border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-600">
                    {issue}
                  </span>
                ))}
              </div>
            </Card>
          </div>
        </div>
      </div>
    </AppShell>
  );
}