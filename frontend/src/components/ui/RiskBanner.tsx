import { AlertTriangle, BadgeCheck, ShieldAlert } from 'lucide-react';
import type { RiskLevel } from '../../lib/mockData';

type RiskBannerProps = {
  riskLevel: RiskLevel;
};

const config = {
  LOW: {
    className: 'bg-green-50 text-green-800 border-green-200',
    icon: BadgeCheck,
    message: 'Low risk. Movement quality is within expected rehab thresholds.',
  },
  MEDIUM: {
    className: 'bg-amber-50 text-amber-800 border-amber-200',
    icon: AlertTriangle,
    message: 'Medium risk. Compensations are present and should be monitored closely.',
  },
  HIGH: {
    className: 'bg-red-50 text-red-800 border-red-200',
    icon: ShieldAlert,
    message: 'High risk. Pause progression and review the movement pattern immediately.',
  },
} as const;

export default function RiskBanner({ riskLevel }: RiskBannerProps) {
  const banner = config[riskLevel];
  const Icon = banner.icon;

  return (
    <div className={`flex items-start gap-3 rounded-xl border px-4 py-4 ${banner.className}`}>
      <div className="mt-0.5 rounded-full bg-white/70 p-2">
        <Icon className="h-4 w-4" />
      </div>
      <div>
        <div className="text-sm font-semibold uppercase tracking-wide">{riskLevel} risk</div>
        <p className="mt-1 text-sm">{banner.message}</p>
      </div>
    </div>
  );
}