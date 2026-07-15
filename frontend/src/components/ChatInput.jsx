import React, { useState, useEffect } from 'react';
import { Scale, Search, CornerDownLeft, AlertCircle } from 'lucide-react';

export default function ChatInput({ onSubmit, isLoading, initialQuery = '' }) {
  const [query, setQuery] = useState(initialQuery);

  useEffect(() => {
    setQuery(initialQuery);
  }, [initialQuery]);

  const exampleScenarios = [
    {
      title: "Peaceful Protest",
      text: "Can the government stop a peaceful protest assembly?"
    },
    {
      title: "Warrantless Search",
      text: "Can police search my personal mobile phone without a judicial warrant?"
    },
    {
      title: "Freedom of Speech",
      text: "Can the police arrest someone for posting critical political commentary online?"
    }
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;
    onSubmit(query.trim());
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto mb-8">
      <form onSubmit={handleSubmit} className="relative">
        <div className="glass-panel rounded-2xl p-4 focus-within:border-amber-500/50 focus-within:shadow-2xl focus-within:shadow-amber-500/5 transition-all duration-300">
          <div className="flex items-start gap-3">
            <div className="mt-2.5 p-2 rounded-lg bg-slate-950 border border-slate-800 text-amber-500">
              <Scale className="w-5 h-5" />
            </div>
            
            <div className="flex-1">
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Describe your legal scenario or question in detail (e.g., 'Police searched my house without a search warrant and confiscated my files...')"
                disabled={isLoading}
                rows={3}
                className="w-full bg-transparent border-0 text-slate-100 placeholder-slate-500 focus:ring-0 text-base resize-none outline-none pr-12 pt-2"
              />
            </div>
          </div>

          <div className="flex items-center justify-between mt-3 pt-3 border-t border-slate-800/80">
            <div className="text-[11px] text-slate-500 flex items-center gap-1.5">
              <AlertCircle className="w-3.5 h-3.5 text-slate-500" />
              <span>Shift+Enter for new line. Provide detailed facts for better agent reasoning.</span>
            </div>
            
            <div className="flex items-center gap-3">
              <span className="text-xs text-slate-500">
                {query.length} chars
              </span>
              <button
                type="submit"
                disabled={isLoading || !query.trim()}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-medium text-sm transition-all duration-200 ${
                  isLoading || !query.trim()
                    ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
                    : 'bg-amber-500 hover:bg-amber-600 text-slate-950 shadow-lg shadow-amber-500/10 active:scale-[0.98]'
                }`}
              >
                {isLoading ? (
                  <>
                    <span className="animate-spin w-4 h-4 border-2 border-slate-950 border-t-transparent rounded-full" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <span>Submit Query</span>
                    <CornerDownLeft className="w-3.5 h-3.5" />
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </form>

      {/* Example pills */}
      <div className="mt-4 flex flex-wrap items-center gap-2 justify-center">
        <span className="text-xs text-slate-500 mr-1">Try example scenarios:</span>
        {exampleScenarios.map((item, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => !isLoading && setQuery(item.text)}
            className="text-xs bg-slate-900/50 hover:bg-slate-900 border border-slate-850 hover:border-slate-700 rounded-full px-3 py-1.5 text-slate-400 hover:text-amber-500 transition-all duration-200"
          >
            {item.title}
          </button>
        ))}
      </div>
    </div>
  );
}
