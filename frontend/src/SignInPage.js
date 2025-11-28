import React from 'react';
import { SignIn } from '@clerk/clerk-react';
import { Command } from 'lucide-react';

export default function SignInPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50">
      <div className="mb-8 flex items-center gap-3">
        <div className="w-10 h-10 bg-gradient-to-br from-indigo-600 to-blue-600 rounded-xl flex items-center justify-center text-white shadow-lg">
          <Command size={20} />
        </div>
        <span className="text-2xl font-bold text-slate-900">Merit</span>
      </div>
      
      <SignIn 
        appearance={{
          elements: {
            formButtonPrimary: 'bg-slate-900 hover:bg-black text-sm normal-case',
            card: 'shadow-xl border border-slate-200 rounded-2xl'
          }
        }}
      />
    </div>
  );
}