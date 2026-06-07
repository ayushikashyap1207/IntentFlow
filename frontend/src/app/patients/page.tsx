'use client';

import { ChevronRight, Plus, Search } from 'lucide-react';
import Link from 'next/link';
import { useMemo, useState } from 'react';
import AppShell from '../../components/layout/AppShell';
import Badge from '../../components/ui/Badge';
import Button from '../../components/ui/Button';
import Card from '../../components/ui/Card';
import { formatDateTime, getLatestSessionForPatient, mockPatients } from '../../lib/mockData';

export default function PatientsPage() {
  const [query, setQuery] = useState('');

  const filteredPatients = useMemo(() => {
    const normalized = query.trim().toLowerCase();

    return mockPatients.filter((patient) => {
      if (!normalized) {
        return true;
      }

      return [patient.name, patient.condition, patient.gender, patient.riskLevel]
        .join(' ')
        .toLowerCase()
        .includes(normalized);
    });
  }, [query]);

  return (
    <AppShell>
      <div className="space-y-6">
        <section className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="text-sm font-medium text-slate-500">Patient registry</p>
            <h1 className="mt-1 text-2xl font-semibold text-slate-900">Patients</h1>
          </div>
          <div className="flex items-center gap-3">
            <div className="rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-600">{mockPatients.length} patients</div>
            <Button variant="secondary" size="sm" disabled leftIcon={<Plus className="h-4 w-4" />}>
              Add patient
            </Button>
          </div>
        </section>

        <Card title="Search patients">
          <div className="flex items-center gap-3 rounded-lg border border-slate-200 bg-white px-3">
            <Search className="h-4 w-4 text-slate-400" />
            <input
              type="search"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search by name, condition, gender, or risk level"
              className="h-11 w-full border-0 bg-transparent text-sm text-slate-900 outline-none placeholder:text-slate-400"
            />
          </div>
        </Card>

        <Card title="All patients">
          <div className="space-y-2">
            {filteredPatients.map((patient) => {
              const latestSession = getLatestSessionForPatient(patient.id);

              return (
                <Link
                  key={patient.id}
                  href={`/patients/${patient.id}`}
                  className="flex items-center gap-4 rounded-lg border border-transparent px-3 py-3 transition-colors hover:border-slate-200 hover:bg-slate-50"
                >
                  <div className={`flex h-12 w-12 items-center justify-center rounded-full text-sm font-semibold ${patient.avatarColor}`}>
                    {patient.initials}
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="font-medium text-slate-900">{patient.name}</span>
                      <Badge riskLevel={patient.riskLevel} />
                    </div>
                    <p className="truncate text-sm text-slate-500">
                      {patient.condition} • {patient.age} years • {patient.gender}
                    </p>
                  </div>
                  <div className="text-right text-sm text-slate-500">
                    <p>Last session</p>
                    <p className="font-medium text-slate-700">{latestSession ? formatDateTime(latestSession.date) : 'No session yet'}</p>
                  </div>
                  <ChevronRight className="h-4 w-4 text-slate-400" />
                </Link>
              );
            })}
          </div>
        </Card>
      </div>
    </AppShell>
  );
}