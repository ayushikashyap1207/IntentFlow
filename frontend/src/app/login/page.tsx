'use client';

import { HeartPulse, Mail, Lock } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import Button from '../../components/ui/Button';
import Card from '../../components/ui/Card';

export default function LoginPage() {
  const router = useRouter();
  const [rememberMe, setRememberMe] = useState(true);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    router.push('/dashboard');
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-10">
      <Card className="w-full max-w-[380px] p-6">
        <div className="flex flex-col items-center text-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-50 text-blue-600">
            <HeartPulse className="h-6 w-6" />
          </div>
          <h1 className="mt-4 text-2xl font-semibold text-slate-900">IntentFlow</h1>
          <p className="mt-1 text-sm text-slate-500">Clinical rehabilitation AI for physiotherapists.</p>
        </div>

        <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
          <label className="block">
            <span className="mb-2 block text-sm font-medium text-slate-700">Email</span>
            <div className="flex items-center gap-3 rounded-lg border border-slate-200 bg-white px-3">
              <Mail className="h-4 w-4 text-slate-400" />
              <input
                type="email"
                placeholder="doctor@clinic.com"
                className="h-11 w-full border-0 bg-transparent text-sm text-slate-900 outline-none placeholder:text-slate-400"
              />
            </div>
          </label>

          <label className="block">
            <span className="mb-2 block text-sm font-medium text-slate-700">Password</span>
            <div className="flex items-center gap-3 rounded-lg border border-slate-200 bg-white px-3">
              <Lock className="h-4 w-4 text-slate-400" />
              <input
                type="password"
                placeholder="••••••••"
                className="h-11 w-full border-0 bg-transparent text-sm text-slate-900 outline-none placeholder:text-slate-400"
              />
            </div>
          </label>

          <div className="flex items-center justify-between gap-3 text-sm">
            <label className="flex items-center gap-2 text-slate-600">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(event) => setRememberMe(event.target.checked)}
                className="h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
              />
              Remember me
            </label>
            <a href="#" className="font-medium text-blue-600 hover:text-blue-700">
              Forgot password?
            </a>
          </div>

          <Button type="submit" variant="primary" className="w-full">
            Sign in
          </Button>
        </form>

        <p className="mt-6 text-center text-xs text-slate-500">Powered by MediaPipe + Groq</p>
      </Card>
    </main>
  );
}