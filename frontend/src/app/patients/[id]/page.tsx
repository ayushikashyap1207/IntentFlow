import { ArrowLeft, ChevronRight } from 'lucide-react';
import { notFound } from 'next/navigation';
import AppShell from '../../../components/layout/AppShell';
import Badge from '../../../components/ui/Badge';
import Button from '../../../components/ui/Button';
import Card from '../../../components/ui/Card';
import { formatDate, formatDateTime, getLatestSessionForPatient, getPatientById } from '../../../lib/mockData';

type PatientDetailPageProps = {
  params: {
    id: string;
  };
};

export default function PatientDetailPage({ params }: PatientDetailPageProps) {
  const patient = getPatientById(params.id);

  if (!patient) {
    notFound();
  }

  const latestSession = getLatestSessionForPatient(patient.id) ?? patient.sessions[0];

  return (
    <AppShell>
      <div className="space-y-6">
        <div className="flex items-center justify-between gap-4">
          <Button href="/patients" variant="secondary" size="sm" leftIcon={<ArrowLeft className="h-4 w-4" />}>
            Back
          </Button>
          <div className="text-sm text-slate-500">Patient profile</div>
        </div>

        <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          <Card>
            <div className="space-y-5">
              <div className="flex items-start gap-4">
                <div className={`flex h-16 w-16 items-center justify-center rounded-full text-lg font-semibold ${patient.avatarColor}`}>
                  {patient.initials}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <h1 className="text-2xl font-semibold text-slate-900">{patient.name}</h1>
                    <Badge riskLevel={patient.riskLevel} />
                  </div>
                  <p className="mt-1 text-sm text-slate-500">Patient ID {patient.id}</p>
                </div>
              </div>

              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Age</p>
                  <p className="mt-1 text-sm text-slate-900">{patient.age} years</p>
                </div>
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Gender</p>
                  <p className="mt-1 text-sm text-slate-900">{patient.gender}</p>
                </div>
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Condition</p>
                  <p className="mt-1 text-sm text-slate-900">{patient.condition}</p>
                </div>
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Under care since</p>
                  <p className="mt-1 text-sm text-slate-900">{formatDate(patient.since)}</p>
                </div>
              </div>

              <div className="flex flex-wrap gap-3">
                <Button href="/analysis" variant="primary" leftIcon={<ChevronRight className="h-4 w-4" />}>
                  New session
                </Button>
                {latestSession ? (
                  <Button href={`/reports/${latestSession.id}`} variant="secondary">
                    View report
                  </Button>
                ) : null}
              </div>
            </div>
          </Card>

          <Card title="Recovery progress">
            <div className="space-y-4">
              {patient.progress.map((item) => (
                <div key={item.label}>
                  <div className="flex items-center justify-between gap-3 text-sm">
                    <span className="font-medium text-slate-700">{item.label}</span>
                    <span className="text-slate-500">{item.value}%</span>
                  </div>
                  <div className="mt-2 h-2 rounded-full bg-slate-100">
                    <div className="h-2 rounded-full bg-blue-600" style={{ width: `${item.value}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        <Card title="Session history">
          <div className="overflow-hidden rounded-lg border border-slate-200">
            <table className="min-w-full divide-y divide-slate-200">
              <thead className="bg-slate-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">Exercise</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">Date</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">Risk</th>
                  <th className="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wide text-slate-500">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 bg-white">
                {patient.sessions.map((session) => (
                  <tr key={session.id}>
                    <td className="px-4 py-4 text-sm font-medium text-slate-900">{session.exercise}</td>
                    <td className="px-4 py-4 text-sm text-slate-500">{formatDateTime(session.date)}</td>
                    <td className="px-4 py-4">
                      <Badge riskLevel={session.riskLevel} />
                    </td>
                    <td className="px-4 py-4 text-right">
                      <Button href={`/reports/${session.id}`} variant="secondary" size="sm">
                        View
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </AppShell>
  );
}