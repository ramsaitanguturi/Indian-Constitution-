import React from 'react';
import { ShieldAlert, BookOpen } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="w-full bg-slate-950/40 border-t border-slate-900 mt-auto py-8 px-6 text-center text-xs text-slate-500">
      <div className="max-w-4xl mx-auto space-y-4">
        
        {/* Legal Disclaimer Box */}
        <div className="flex items-start gap-2.5 text-left p-3.5 rounded-lg bg-rose-950/15 border border-rose-950/30 max-w-2xl mx-auto">
          <ShieldAlert className="w-4 h-4 text-rose-500/70 shrink-0 mt-0.5" />
          <p className="text-slate-500 leading-normal text-[11px]">
            <strong>Legal Notice & Disclaimer:</strong> Vidhi.AI is an AI-powered legal assistant designed for research and educational purposes only. The verdict predictions and analyses do not constitute binding legal counsel or judicial opinions. Users must consult qualified legal practitioners for statutory case advisories.
          </p>
        </div>

        <div className="flex items-center justify-center gap-6 text-slate-600">
          <span className="flex items-center gap-1.5">
            <BookOpen className="w-3.5 h-3.5" />
            Indian Constitutional Law RAG
          </span>
          <span>•</span>
          <span>Powered by LangGraph & FastAPI</span>
        </div>

        <p className="text-slate-700">
          © {new Date().getFullYear()} Vidhi.AI. Licensed under MIT patterns.
        </p>
      </div>
    </footer>
  );
}
