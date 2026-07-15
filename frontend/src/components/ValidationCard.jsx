import React from 'react';
import { ShieldCheck, ShieldAlert, Check, X, ShieldQuestion } from 'lucide-react';

export default function ValidationCard({ validation }) {
  if (!validation) return null;

  const { is_valid, hallucination_risk, details, category, issue } = validation;

  const getRiskStyles = (risk) => {
    switch (risk?.toLowerCase()) {
      case 'low':
        return {
          bg: 'bg-emerald-950/20 border-emerald-500/25',
          badge: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
          text: 'text-emerald-400',
          ring: 'border-emerald-500/35 bg-emerald-500/10'
        };
      case 'medium':
        return {
          bg: 'bg-amber-950/20 border-amber-500/25',
          badge: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
          text: 'text-amber-400',
          ring: 'border-amber-500/35 bg-amber-500/10'
        };
      case 'high':
      default:
        return {
          bg: 'bg-rose-950/20 border-rose-500/25',
          badge: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
          text: 'text-rose-400',
          ring: 'border-rose-500/35 bg-rose-500/10'
        };
    }
  };

  const riskStyles = getRiskStyles(hallucination_risk || 'low');

  return (
    <div className={`glass-panel rounded-2xl p-6 relative overflow-hidden transition-all duration-300 ${riskStyles.bg}`}>
      <div className="flex items-center justify-between border-b border-slate-800/80 pb-4 mb-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <span className="text-[10px] uppercase font-bold tracking-widest text-slate-500">
              Agent Guardrails
            </span>
            <h3 className="text-lg font-serif font-semibold text-slate-100">
              Validator Verdict
            </h3>
          </div>
        </div>

        {/* Validation Status Indicator */}
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400">Status:</span>
          {is_valid ? (
            <span className="flex items-center gap-1 text-xs px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-medium">
              <Check className="w-3.5 h-3.5" />
              Verified
            </span>
          ) : (
            <span className="flex items-center gap-1 text-xs px-2.5 py-1 rounded-full bg-rose-500/10 border border-rose-500/20 text-rose-400 font-medium">
              <X className="w-3.5 h-3.5" />
              Flagged
            </span>
          )}
        </div>
      </div>

      <div className="space-y-4">
        {/* Category & Issue detail */}
        {(category || issue) && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-slate-950/40 p-4 rounded-xl border border-slate-850/60 text-xs">
            {category && (
              <div>
                <span className="text-slate-500 uppercase tracking-wide block mb-1">Identified Category</span>
                <span className="text-slate-200 font-medium">{category}</span>
              </div>
            )}
            {issue && (
              <div>
                <span className="text-slate-500 uppercase tracking-wide block mb-1">Extracted Legal Issue</span>
                <span className="text-slate-200 font-medium">{issue}</span>
              </div>
            )}
          </div>
        )}

        {/* Hallucination Risk Metric */}
        <div className="flex items-center justify-between p-4 rounded-xl bg-slate-950/40 border border-slate-850/60">
          <div className="flex items-center gap-3">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center border ${riskStyles.ring}`}>
              {hallucination_risk?.toLowerCase() === 'low' ? (
                <ShieldCheck className={`w-4 h-4 ${riskStyles.text}`} />
              ) : (
                <ShieldAlert className={`w-4 h-4 ${riskStyles.text}`} />
              )}
            </div>
            <div>
              <p className="text-xs text-slate-400">Hallucination Risk</p>
              <p className={`text-sm font-semibold capitalize ${riskStyles.text}`}>
                {hallucination_risk || 'Low'}
              </p>
            </div>
          </div>
          <span className="text-[10px] text-slate-500 max-w-[150px] leading-tight text-right">
            Cross-referenced with source constitutional collection.
          </span>
        </div>

        {/* Fact-check checks */}
        {details && (
          <div>
            <span className="text-slate-500 text-xs uppercase tracking-wide block mb-2">
              Verification Check details
            </span>
            <div className="text-xs text-slate-400 bg-slate-950/20 p-4 rounded-xl border border-slate-850/40 leading-relaxed max-h-36 overflow-y-auto">
              <p className="whitespace-pre-line">{details}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
