'use client';

import { Cog, FileText, LayoutDashboard, Plus, Users } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const items = [
  { label: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { label: 'Patients', href: '/patients', icon: Users },
  { label: 'New Analysis', href: '/analysis', icon: Plus },
  { label: 'Reports', href: '/reports/session-001', icon: FileText },
  { label: 'Settings', icon: Cog },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden w-[220px] shrink-0 border-r border-slate-200 bg-white lg:flex lg:flex-col">
      <div className="px-4 py-5">
        <div className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-400">Navigation</div>
        <div className="space-y-1">
          {items.map((item) => {
            const Icon = item.icon;
            const isActive = item.href
              ? item.href.startsWith('/reports')
                ? pathname.startsWith('/reports')
                : pathname.startsWith(item.href)
              : false;
            const baseClass =
              'flex items-center gap-3 rounded-lg border-l-2 px-3 py-2 text-sm font-medium transition-colors';

            if (!item.href) {
              return (
                <div key={item.label} className={`${baseClass} border-l-transparent text-slate-400`}>
                  <Icon className="h-4 w-4" />
                  <span>{item.label}</span>
                </div>
              );
            }

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`${baseClass} ${
                  isActive
                    ? 'border-blue-600 bg-blue-50 text-blue-600'
                    : 'border-l-transparent text-slate-500 hover:bg-slate-50 hover:text-slate-700'
                }`}
              >
                <Icon className="h-4 w-4" />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </div>
      </div>

      <div className="mt-auto border-t border-slate-200 p-4 text-xs text-slate-400">
        AI-assisted rehab insights for physiotherapy workflows.
      </div>
    </aside>
  );
}