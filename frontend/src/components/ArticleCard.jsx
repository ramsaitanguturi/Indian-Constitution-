import React, { useState } from 'react';
import { BookOpen, ChevronDown, ChevronUp, Star } from 'lucide-react';

export default function ArticleCard({ article }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const { article_number, title, clause, content, source_document, similarity_score } = article;

  const scorePercentage = Math.round(similarity_score * 100);

  return (
    <div className="glass-panel glass-panel-hover rounded-xl p-5 mb-4 relative overflow-hidden">
      {/* Decorative Gold Side Strip */}
      <div className="absolute left-0 top-0 bottom-0 w-1 bg-amber-500/80" />

      <div className="flex items-start justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-amber-500/10 text-amber-500 border border-amber-500/20">
            <BookOpen className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-amber-500">
                Article {article_number}
              </span>
              {clause && (
                <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300 font-mono">
                  Clause {clause}
                </span>
              )}
            </div>
            <h4 className="text-base font-serif font-semibold text-slate-200 mt-1">
              {title}
            </h4>
          </div>
        </div>

        {/* Score Badge */}
        <div className="flex items-center gap-1.5 text-xs text-slate-400 bg-slate-950 px-2.5 py-1 rounded-full border border-slate-850">
          <Star className="w-3.5 h-3.5 text-amber-500 fill-amber-500/35" />
          <span>Match: {scorePercentage}%</span>
        </div>
      </div>

      {/* Excerpt / Full Content */}
      <div className="mt-4 text-sm text-slate-300 leading-relaxed font-sans font-light">
        {isExpanded ? (
          <p className="whitespace-pre-line">{content}</p>
        ) : (
          <p className="line-clamp-3">
            {content}
          </p>
        )}
      </div>

      <div className="flex items-center justify-between mt-4 pt-3 border-t border-slate-850 text-xs text-slate-500">
        <span>Source: {source_document || 'Constitution of India'}</span>
        
        {content.length > 180 && (
          <button
            type="button"
            onClick={() => setIsExpanded(!isExpanded)}
            className="flex items-center gap-1 text-amber-500 hover:text-amber-400 font-medium transition-colors duration-150"
          >
            <span>{isExpanded ? 'Collapse' : 'Read Full Text'}</span>
            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        )}
      </div>
    </div>
  );
}
