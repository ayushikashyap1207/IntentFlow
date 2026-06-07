import type { ReactNode } from 'react';
import type { RiskLevel } from '../../lib/mockData';

type BadgeProps = {
  riskLevel?: RiskLevel;
  variant?: 'blue' | 'gray';
  className?: string;
  children?: ReactNode;
};

const riskClasses: Record<RiskLevel, string> = {
  LOW: 'bg-green-50 text-green-700 border-green-200',
  MEDIUM: 'bg-amber-50 text-amber-700 border-amber-200',
  HIGH: 'bg-red-50 text-red-700 border-red-200',
};

const variantClasses = {
  blue: 'bg-blue-50 text-blue-700 border-blue-200',
  gray: 'bg-slate-100 text-slate-600 border-slate-200',
};

export default function Badge({ riskLevel, variant = 'gray', className = '', children }: BadgeProps) {
  const label = children ?? riskLevel;
  const classes = riskLevel ? riskClasses[riskLevel] : variantClasses[variant];

  return (
    <span className={`inline-flex items-center rounded-md border px-2.5 py-1 text-xs font-medium ${classes} ${className}`.trim()}>
      {label}
    </span>
  );
}