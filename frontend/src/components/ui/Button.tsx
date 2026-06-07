import Link from 'next/link';
import type { ReactNode } from 'react';

type ButtonProps = {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md';
  children: ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  href?: string;
  leftIcon?: ReactNode;
  className?: string;
  type?: 'button' | 'submit' | 'reset';
};

const variantClasses = {
  primary: 'bg-blue-600 text-white hover:bg-blue-700 border border-blue-600',
  secondary: 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-50',
  danger: 'bg-red-600 text-white hover:bg-red-700 border border-red-600',
};

const sizeClasses = {
  sm: 'h-9 px-3 text-sm',
  md: 'h-10 px-4 text-sm',
};

export default function Button({
  variant = 'primary',
  size = 'md',
  children,
  onClick,
  disabled = false,
  href,
  leftIcon,
  className = '',
  type = 'button',
}: ButtonProps) {
  const classes = [
    'inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-colors',
    'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
    variantClasses[variant],
    sizeClasses[size],
    disabled ? 'cursor-not-allowed opacity-60 hover:bg-inherit' : '',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  const content = (
    <>
      {leftIcon ? <span className="shrink-0">{leftIcon}</span> : null}
      <span>{children}</span>
    </>
  );

  if (href && !disabled) {
    return (
      <Link href={href} className={classes}>
        {content}
      </Link>
    );
  }

  return (
    <button type={type} onClick={onClick} disabled={disabled} className={classes}>
      {content}
    </button>
  );
}