import React, { useState, useEffect } from 'react';
import ChatInput from '../components/ChatInput';
import AgentTimeline from '../components/AgentTimeline';
import ArticleCard from '../components/ArticleCard';
import CaseCard from '../components/CaseCard';
import VerdictCard from '../components/VerdictCard';
import ValidationCard from '../components/ValidationCard';
import ReasoningPanel from '../components/ReasoningPanel';
import { queryConstitution } from '../services/api';
import { AlertCircle, RefreshCw, Scale, BookMarked, HelpCircle, Activity } from 'lucide-react';

export default function QueryWorkspace({ preloadedQuery, setPreloadedQuery }) {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState('router');
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  // Sync with preloaded queries from Landing Page presets
  useEffect(() => {
    if (preloadedQuery) {
      setQuery(preloadedQuery);
      handleSearch(preloadedQuery);
      // Reset preload after firing
      setPreloadedQuery('');
    }
  }, [preloadedQuery]);

  // Simulate active agent steps for loading progress
  useEffect(() => {
    if (!loading) return;

    const steps = ['router', 'research', 'reasoning', 'validation', 'verdict'];
    let currentIdx = 0;
    setLoadingStep(steps[0]);

    const interval = setInterval(() => {
      if (currentIdx < steps.length - 1) {
        currentIdx++;
        setLoadingStep(steps[currentIdx]);
      }
    }, 1800); // Shift agent nodes every 1.8s

    return () => clearInterval(interval);
  }, [loading]);

  const handleSearch = async (queryText) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setQuery(queryText);

    try {
      const data = await queryConstitution(queryText);
      setResult(data);
    } catch (err) {
      console.error(err);
      setError(err.message || 'An unexpected error occurred while querying the legal agents.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      
      {/* Workspace Header */}
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <h2 className="text-2xl md:text-3xl font-serif font-semibold text-slate-100">
          Constitutional Analysis Workspace
        </h2>
        <p className="text-xs text-slate-400 font-light">
          Input a scenario describing a potential constitutional dispute. Our multi-agent system will perform child-clause matching and cross-reference cases.
        </p>
      </div>

      {/* Input Section */}
      <ChatInput 
        onSubmit={handleSearch} 
        isLoading={loading} 
        initialQuery={query} 
      />

      {/* Loading & Agent Pipeline state */}
      {loading && (
        <div className="space-y-6 max-w-5xl mx-auto">
          <AgentTimeline currentStep={loadingStep} />
          
          <div className="glass-panel rounded-2xl p-10 flex flex-col items-center justify-center text-center space-y-4">
            <div className="relative">
              <div className="w-12 h-12 rounded-full border-4 border-amber-500/20 border-t-amber-500 animate-spin" />
              <Scale className="w-5 h-5 text-amber-500 absolute top-3.5 left-3.5 animate-pulse" />
            </div>
            <div>
              <p className="text-sm font-medium text-slate-300">
                Orchestrating AI Legal Experts...
              </p>
              <p className="text-[11px] text-slate-500 mt-1 capitalize animate-pulse">
                Current Active: {loadingStep} Agent
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Error state */}
      {error && (
        <div className="max-w-3xl mx-auto p-4 rounded-xl bg-rose-950/20 border border-rose-500/30 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-rose-500 shrink-0 mt-0.5" />
          <div className="flex-1 space-y-1">
            <h5 className="text-sm font-semibold text-rose-400">Analysis Request Failed</h5>
            <p className="text-xs text-slate-450 leading-relaxed">{error}</p>
            <button
              onClick={() => handleSearch(query)}
              className="mt-2 text-xs flex items-center gap-1.5 font-semibold text-amber-500 hover:text-amber-400 transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Retry Search</span>
            </button>
          </div>
        </div>
      )}

      {/* Results Workspace dashboard */}
      {result && !loading && (
        <div className="space-y-8 animate-fade-in">
          
          {/* Agent execution log for success */}
          <AgentTimeline 
            currentStep="completed" 
            validationResult={result.validation_result} 
          />

          {/* Quick Query Re-cap Info Card */}
          <div className="glass-panel rounded-xl p-4 bg-slate-900/40 text-xs flex items-center justify-between border-slate-800/80">
            <span className="text-slate-400 font-light truncate max-w-xl">
              <strong>Query:</strong> "{result.question}"
            </span>
            <span className="text-[10px] text-amber-500 uppercase tracking-widest font-bold">
              Analysis Resolved
            </span>
          </div>

          {/* Grid Layout of results */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            
            {/* Left Column (5/12 width) - Legal Category, Issue & Articles */}
            <div className="lg:col-span-5 space-y-6">
              
              {/* Legal Issue summary card */}
              <div className="glass-panel rounded-2xl p-5 border-l-4 border-amber-500">
                <span className="text-[9px] uppercase font-bold tracking-widest text-slate-500 block mb-1">
                  Router Assessment
                </span>
                <h4 className="text-base font-serif font-semibold text-slate-200">
                  {result.validation_result?.issue || 'Identified Legal Issue'}
                </h4>
                <div className="mt-3 flex items-center justify-between text-xs text-slate-450 border-t border-slate-850 pt-2.5">
                  <span>Category: <strong>{result.validation_result?.category || 'General'}</strong></span>
                  <span className="text-slate-500">Articles Found: {result.articles?.length || 0}</span>
                </div>
              </div>

              {/* Constitutional Articles List */}
              <div className="space-y-4">
                <div className="flex items-center gap-2 mb-2">
                  <BookMarked className="w-4 h-4 text-amber-500" />
                  <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 font-serif">
                    Constitutional Authority
                  </h3>
                </div>

                {result.articles && result.articles.length > 0 ? (
                  result.articles.map((art, idx) => (
                    <ArticleCard key={idx} article={art} />
                  ))
                ) : (
                  <div className="p-6 rounded-xl border border-dashed border-slate-800 text-center text-xs text-slate-550 italic">
                    No matching constitutional articles found for this scenario.
                  </div>
                )}
              </div>

            </div>

            {/* Right Column (7/12 width) - Verdict, Validator, Cases, Reasoning */}
            <div className="lg:col-span-7 space-y-6">
              
              {/* Verdict Card */}
              <VerdictCard 
                verdict={result.verdict} 
                confidence={result.confidence} 
              />

              {/* Validator Card */}
              {result.validation_result && (
                <ValidationCard validation={result.validation_result} />
              )}

              {/* Landmark Cases Timeline */}
              <div className="space-y-4">
                <div className="flex items-center gap-2 mb-2">
                  <Scale className="w-4 h-4 text-indigo-400" />
                  <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 font-serif">
                    Supreme Court Judgments
                  </h3>
                </div>

                {result.cases && result.cases.length > 0 ? (
                  result.cases.map((cs, idx) => (
                    <CaseCard key={idx} caseItem={cs} />
                  ))
                ) : (
                  <div className="p-6 rounded-xl border border-dashed border-slate-800 text-center text-xs text-slate-550 italic">
                    No citing landmark court judgments retrieved.
                  </div>
                )}
              </div>

              {/* Reasoning Panel */}
              <ReasoningPanel reasoning={result.reasoning} />

            </div>

          </div>

        </div>
      )}

    </div>
  );
}
