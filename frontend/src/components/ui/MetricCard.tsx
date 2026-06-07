type MetricCardProps = {
  label: string;
  value: string | number;
  delta?: string;
  color?: 'slate' | 'blue' | 'green' | 'amber' | 'red';
};

const valueColors = {
  slate: 'text-slate-900',
  blue: 'text-blue-600',
  green: 'text-green-600',
  amber: 'text-amber-600',
  red: 'text-red-600',
};

export default function MetricCard({ label, value, delta, color = 'slate' }: MetricCardProps) {
  const deltaColor = delta?.trim().startsWith('-') ? 'text-red-600' : 'text-emerald-600';

  return (
    <div className="rounded-lg bg-slate-50 p-4">
      <p className="text-sm text-slate-500">{label}</p>
      <div className="mt-2 flex items-end justify-between gap-3">
        <div className={`text-2xl font-medium ${valueColors[color]}`}>{value}</div>
        {delta ? <div className={`text-sm font-medium ${deltaColor}`}>{delta}</div> : null}
      </div>
    </div>
  );
}