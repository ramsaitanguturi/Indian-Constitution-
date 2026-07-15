import React, { useState } from 'react';
import { Gavel, ChevronDown, ChevronUp, Calendar } from 'lucide-react';

export default function CaseCard({ caseItem }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const { case_name, citation, summary, similarity_score } = caseItem;

  // Extract year from citation if possible, or default to general landmark
  const extractYear = (cite) => {
    const match = cite.match(/\b(19|20)\d{2}\b/);
    return match ? match[0] : 'Landmark Decision';
  };

  const year = extractYear(citation);

  return (
    <div className="glass-panel glass-panel-hover rounded-xl p-5 mb-4 relative overflow-hidden">
      {/* Decorative Indigo Side Strip */}
      <div className="absolute left-0 top-0 bottom-0 w-1 bg-indigo-500/80" />

      <div className="flex items-start justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <Gavel className="w-5 h-5" />
          </div>
          <div>
            <h4 className="text-base font-serif font-semibold text-slate-200">
              {case_name}
            </h4>
            <div className="flex items-center gap-2 mt-1">
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-950 border border-slate-850 text-indigo-300">
                {citation}
              </span>
              <span className="text-[10px] text-slate-500 flex items-center gap-1 font-sans">
                <Calendar className="w-3 h-3" />
                {year}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Judgment Holding / Ratio Decidendi */}
      <div className="mt-4 text-sm text-slate-300 leading-relaxed font-sans font-light">
        {isExpanded ? (
          <p className="whitespace-pre-line">{summary}</p>
        ) : (
          <p className="line-clamp-3">
            {summary}
          </p>
        )}
      </div>

      <div className="flex items-center justify-end mt-4 pt-3 border-t border-slate-850 text-xs text-slate-500">
        {summary.length > 180 && (
          <button
            type="button"
            onClick={() => setIsExpanded(!isExpanded)}
            className="flex items-center gap-1 text-indigo-400 hover:text-indigo-300 font-medium transition-colors duration-150"
          >
            <span>{isExpanded ? 'Collapse Summary' : 'Read Full Decision Summary'}</span>
            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        )}
      </div>
    </div>
  );
}
