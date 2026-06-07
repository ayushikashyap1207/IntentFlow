import type { ReactNode } from 'react';

type CardProps = {
  title?: string;
  children: ReactNode;
  className?: string;
};

export default function Card({ title, children, className = '' }: CardProps) {
  return (
    <section className={`rounded-xl border border-slate-200 bg-white p-5 shadow-none ${className}`.trim()}>
      {title ? <h3 className="mb-4 text-base font-semibold text-slate-900">{title}</h3> : null}
      {children}
    </section>
  );
}