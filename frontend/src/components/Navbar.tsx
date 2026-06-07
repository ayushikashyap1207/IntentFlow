'use client';

import { HeartPulse } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import Button from './ui/Button';

const navItems = [
  { label: 'Dashboard', href: '/dashboard' },
  { label: 'Patients', href: '/patients' },
  { label: 'Analysis', href: '/analysis' },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <header className="flex h-14 items-center justify-between border-b border-slate-200 bg-white px-6">
      <div className="flex items-center gap-8">
        <Link href="/dashboard" className="flex items-center gap-2 text-base font-semibold text-blue-600">
          <HeartPulse className="h-5 w-5" />
          <span>IntentFlow</span>
        </Link>

        <nav className="hidden items-center gap-1 md:flex">
          {navItems.map((item) => {
            const active = pathname.startsWith(item.href);
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                  active ? 'text-blue-600' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-700'
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="flex items-center gap-3">
        <Button href="/analysis" size="sm" variant="primary">
          New session
        </Button>
        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-blue-100 text-sm font-semibold text-blue-700">
          DS
        </div>
      </div>
    </header>
  );
}