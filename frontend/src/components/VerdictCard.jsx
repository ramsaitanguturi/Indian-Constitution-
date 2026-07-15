import React from 'react';
import { Scale, CheckCircle, ShieldAlert, Award } from 'lucide-react';

export default function VerdictCard({ verdict, confidence = 'High' }) {
  // Determine style colors based on confidence
  const getConfidenceStyles = (lvl) => {
    switch (lvl?.toLowerCase()) {
      case 'high':
        return {
          bg: 'bg-emerald-950/35 border-emerald-500/30',
          text: 'text-emerald-400',
          badge: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
          fill: 'fill-emerald-400/20'
        };
      case 'medium':
        return {
          bg: 'bg-amber-950/35 border-amber-500/30',
          text: 'text-amber-400',
          badge: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
          fill: 'fill-amber-400/20'
        };
      case 'low':
      default:
        return {
          bg: 'bg-rose-950/35 border-rose-500/30',
          text: 'text-rose-400',
          badge: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
          fill: 'fill-rose-400/20'
        };
    }
  };

  const styles = getConfidenceStyles(confidence);

  return (
    <div className={`glass-panel border-2 rounded-2xl p-6 relative overflow-hidden transition-all duration-300 ${styles.bg}`}>
      {/* Decorative background visual of scales */}
      <div className="absolute right-[-20px] bottom-[-20px] opacity-[0.03] text-white">
        <Scale className="w-56 h-56" />
      </div>

      <div className="flex items-center justify-between border-b border-slate-800/80 pb-4 mb-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-amber-500/10 text-amber-500 border border-amber-500/20">
            <Scale className="w-6 h-6" />
          </div>
          <div>
            <span className="text-[10px] uppercase font-bold tracking-widest text-slate-500">
              Constitutional Evaluation
            </span>
            <h3 className="text-lg font-serif font-semibold text-slate-100">
              Predicted Verdict
            </h3>
          </div>
        </div>

        {/* Confidence Badge */}
        <div className={`flex items-center gap-1 px-3 py-1 rounded-full border text-xs font-medium font-sans ${styles.badge}`}>
          <Award className="w-4 h-4" />
          <span>Confidence: {confidence}</span>
        </div>
      </div>

      {/* Predicted Ruling Box */}
      <div className="relative z-10">
        <div className="p-5 rounded-xl bg-slate-950/60 border border-slate-850/80 shadow-inner">
          <p className="text-base text-slate-200 font-serif leading-relaxed italic">
            "{verdict || 'Awaiting evaluation. Provide a query scenario above to begin analysis.'}"
          </p>
        </div>

        {/* Confidence scale weights illustration */}
        <div className="mt-5 flex items-center justify-between text-xs text-slate-500">
          <span className="flex items-center gap-1.5">
            <ShieldAlert className="w-4 h-4 text-slate-600" />
            Disclaimer: Non-binding legal AI advice.
          </span>
          
          <div className="flex items-center gap-1">
            <div className="w-2 h-2 rounded-full bg-emerald-500" />
            <span className="text-slate-400">Validated Precedents Integrated</span>
          </div>
        </div>
      </div>
    </div>
  );
}
