import { Clock3, Users } from 'lucide-react';
import Link from 'next/link';
import AppShell from '../../components/layout/AppShell';
import Badge from '../../components/ui/Badge';
import Card from '../../components/ui/Card';
import MetricCard from '../../components/ui/MetricCard';
import { formatDateTime, getLatestSessionForPatient, getRecentPatients, mockActivityFeed, mockPatients, mockSessions } from '../../lib/mockData';

const todayLabel = new Intl.DateTimeFormat('en-US', {
  weekday: 'long',
  month: 'short',
  day: 'numeric',
}).format(new Date('2026-06-07T09:00:00Z'));

export default function DashboardPage() {
  const recentPatients = getRecentPatients(4);
  const sessionsThisWeek = mockSessions.length;
  const highRiskFlags = mockSessions.filter((session) => session.riskLevel === 'HIGH').length;
  const averageFormScore = Math.round(mockSessions.reduce((sum, session) => sum + session.formScore, 0) / mockSessions.length);

  return (
    <AppShell>
      <div className="space-y-6">
        <section className="flex flex-col gap-4 rounded-xl border border-slate-200 bg-white p-5">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="text-sm font-medium text-slate-500">Good morning, Dr. Sharma</p>
              <h1 className="mt-1 text-2xl font-semibold text-slate-900">Clinical overview</h1>
            </div>
            <div className="flex items-center gap-3 text-sm text-slate-500">
              <Clock3 className="h-4 w-4" />
              <span>{todayLabel}</span>
              <span>•</span>
              <span>{sessionsThisWeek} sessions recorded</span>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
            <MetricCard label="Total patients" value={mockPatients.length} delta="+2 this month" color="blue" />
            <MetricCard label="Sessions this week" value={sessionsThisWeek} delta="+5 vs last week" color="green" />
            <MetricCard label="High risk flags" value={highRiskFlags} delta="Needs review" color="red" />
            <MetricCard label="Avg form score" value={`${averageFormScore}%`} delta="+6% vs baseline" color="slate" />
          </div>
        </section>

        <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          <Card title="Recent patients">
            <div className="space-y-2">
              {recentPatients.map((patient) => {
                const latestSession = getLatestSessionForPatient(patient.id);

                return (
                  <Link
                    key={patient.id}
                    href={`/patients/${patient.id}`}
                    className="flex items-center gap-4 rounded-lg border border-transparent px-3 py-3 transition-colors hover:border-slate-200 hover:bg-slate-50"
                  >
                    <div className={`flex h-11 w-11 items-center justify-center rounded-full text-sm font-semibold ${patient.avatarColor}`}>
                      {patient.initials}
                    </div>
                    <div className="min-w-0 flex-1">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="font-medium text-slate-900">{patient.name}</span>
                        <Badge riskLevel={patient.riskLevel} />
                      </div>
                      <p className="truncate text-sm text-slate-500">
                        {patient.condition} • Last session {latestSession ? formatDateTime(latestSession.date) : 'No session yet'}
                      </p>
                    </div>
                    <Users className="h-4 w-4 text-slate-400" />
                  </Link>
                );
              })}
            </div>
          </Card>

          <Card title="Recent activity">
            <div className="space-y-4">
              {mockActivityFeed.map((item) => {
                const toneClasses = {
                  blue: 'bg-blue-500',
                  green: 'bg-green-500',
                  amber: 'bg-amber-500',
                  red: 'bg-red-500',
                }[item.tone];

                return (
                  <div key={`${item.text}-${item.time}`} className="flex items-start gap-3">
                    <span className={`mt-1 h-2.5 w-2.5 rounded-full ${toneClasses}`} />
                    <div className="min-w-0 flex-1">
                      <p className="text-sm text-slate-700">{item.text}</p>
                      <p className="mt-1 text-xs text-slate-400">{item.time}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}