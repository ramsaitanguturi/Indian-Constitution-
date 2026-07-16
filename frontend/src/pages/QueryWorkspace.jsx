import React, { useState, useEffect } from 'react';
import ChatInput from '../components/ChatInput';
import AgentTimeline from '../components/AgentTimeline';
import ArticleCard from '../components/ArticleCard';
import CaseCard from '../components/CaseCard';
import VerdictCard from '../components/VerdictCard';
import ValidationCard from '../components/ValidationCard';
import ReasoningPanel from '../components/ReasoningPanel';
import { queryConstitutionStream } from '../services/api';
import { AlertCircle, RefreshCw, Scale, BookMarked, HelpCircle, Activity, LayoutDashboard, FileText, Printer } from 'lucide-react';

export default function QueryWorkspace({ preloadedQuery, setPreloadedQuery }) {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState('router');
  const [viewMode, setViewMode] = useState('dashboard');
  const [streamingStatus, setStreamingStatus] = useState('Initiating legal query...');
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

  const handleSearch = async (queryText) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setQuery(queryText);
    setLoadingStep('router');
    setStreamingStatus('Router running...');

    try {
      const onProgress = (statusEvent) => {
        const { node, message } = statusEvent;
        setStreamingStatus(message);
        
        // Map LangGraph node names to timeline steps
        const nodeMap = {
          'router': 'router',
          'constitution_agent': 'research',
          'case_law_agent': 'research',
          'reasoning_agent': 'reasoning',
          'validation_agent': 'validation',
          'verdict_agent': 'verdict',
          'verdict': 'verdict'
        };
        
        if (nodeMap[node]) {
          setLoadingStep(nodeMap[node]);
        }
      };

      const data = await queryConstitutionStream(queryText, 5, onProgress);
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
                {streamingStatus}
              </p>
              <p className="text-[11px] text-slate-500 mt-1 uppercase tracking-widest font-mono">
                Active Node: {loadingStep} agent
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
      {/* Results Workspace dashboard */}
      {result && !loading && (
        <div className="space-y-8 animate-fade-in">
          
          {/* Agent execution log for success */}
          <AgentTimeline 
            currentStep="completed" 
            validationResult={result.validation_result} 
          />

          {/* View Toggle and Actions Toolbar */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 bg-slate-900/35 border border-slate-800 p-4 rounded-xl no-print">
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-450 uppercase tracking-widest mr-2 font-bold font-sans">Select View:</span>
              <button
                onClick={() => setViewMode('dashboard')}
                className={`flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-semibold transition-all duration-150 cursor-pointer ${
                  viewMode === 'dashboard'
                    ? 'bg-amber-500 text-slate-950 shadow-md shadow-amber-500/10'
                    : 'text-slate-400 hover:text-slate-250 hover:bg-slate-800/60'
                }`}
              >
                <LayoutDashboard className="w-3.5 h-3.5" />
                <span>Interactive Dashboard</span>
              </button>
              <button
                onClick={() => setViewMode('report')}
                className={`flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-semibold transition-all duration-150 cursor-pointer ${
                  viewMode === 'report'
                    ? 'bg-amber-500 text-slate-950 shadow-md shadow-amber-500/10'
                    : 'text-slate-400 hover:text-slate-250 hover:bg-slate-800/60'
                }`}
              >
                <FileText className="w-3.5 h-3.5" />
                <span>Formal Legal Brief</span>
              </button>
            </div>
            
            <button
              onClick={() => window.print()}
              className="w-full sm:w-auto flex items-center justify-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-slate-600 rounded-xl text-xs font-medium text-slate-250 transition-all duration-150 cursor-pointer active:scale-[0.98]"
            >
              <Printer className="w-4 h-4 text-amber-500" />
              <span>Print / Save as PDF</span>
            </button>
          </div>

          {/* Quick Query Re-cap Info Card */}
          <div className="glass-panel rounded-xl p-4 bg-slate-900/40 text-xs flex items-center justify-between border-slate-800/80 no-print">
            <span className="text-slate-450 font-light truncate max-w-xl font-sans">
              <strong>Query:</strong> "{result.question}"
            </span>
            <span className="text-[10px] text-amber-500 uppercase tracking-widest font-bold font-sans">
              Analysis Resolved
            </span>
          </div>

          {/* Interactive Dashboard View */}
          {viewMode === 'dashboard' && (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start no-print">
              
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
          )}

          {/* Formal Legal Brief Report View (Always visible in print media via CSS overrides) */}
          <div className={viewMode === 'report' ? 'block animate-fade-in' : 'hidden md:print:block'}>
            <div id="print-area" className="printable-brief bg-slate-900/35 border border-slate-850 rounded-2xl p-8 max-w-4xl mx-auto shadow-inner space-y-8 font-serif leading-relaxed text-slate-200">
              {/* Header */}
              <div className="print-header-details border-b-2 border-slate-800 pb-6 text-left space-y-4">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div>
                    <h1 className="text-2xl font-bold uppercase tracking-wider text-amber-500 font-serif">ConstituAI</h1>
                    <p className="text-[10px] uppercase tracking-widest text-slate-500 font-sans mt-0.5">Indian Constitution Legal Assistant</p>
                  </div>
                  <div className="md:text-right text-xs text-slate-450 font-sans space-y-1">
                    <p><strong>Ref ID:</strong> CONSTITUAI-2026-{(result.question || 'query').substring(0, 10).toUpperCase().replace(/[^A-Z0-9]/g, '') || 'SCENARIO'}</p>
                    <p><strong>Date:</strong> {new Date().toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' })}</p>
                    <p><strong>Status:</strong> Validated Legal Assessment</p>
                  </div>
                </div>
                <div className="pt-4 border-t border-slate-850/50 text-center">
                  <h2 className="text-xl font-bold uppercase tracking-wider text-slate-100 font-serif">Constitutional Analysis Brief</h2>
                </div>
              </div>

              {/* 1. Legal Issue */}
              <div className="space-y-3 print-legal-section">
                <h3 className="text-sm font-bold uppercase tracking-wider text-amber-500 font-serif border-b border-slate-850 pb-2">I. Legal Issue Under Evaluation</h3>
                <div className="pl-4 border-l-2 border-amber-500/40 text-sm leading-relaxed italic text-slate-350">
                  "{result.question}"
                </div>
                {result.validation_result?.issue && (
                  <p className="text-xs text-slate-450 font-sans mt-2">
                    <strong>Core Case Conflict:</strong> {result.validation_result.issue}
                  </p>
                )}
              </div>

              {/* 2. Applicable Articles */}
              <div className="space-y-3 print-legal-section">
                <h3 className="text-sm font-bold uppercase tracking-wider text-amber-500 font-serif border-b border-slate-850 pb-2">II. Applicable Constitutional Provisions</h3>
                <div className="space-y-4">
                  {result.articles && result.articles.length > 0 ? (
                    result.articles.map((art, idx) => (
                      <div key={idx} className="pl-4 space-y-1.5 text-sm">
                        <h4 className="font-semibold text-slate-200">
                          Article {art.article_number} {art.clause ? `(Clause ${art.clause})` : ''} — {art.title}
                        </h4>
                        <p className="text-slate-350 font-sans font-light leading-relaxed text-xs pl-3 border-l border-slate-800">
                          {art.content}
                        </p>
                      </div>
                    ))
                  ) : (
                    <p className="text-xs text-slate-500 italic pl-4 font-sans">No direct constitutional articles retrieved for this case.</p>
                  )}
                </div>
              </div>

              {/* 3. Judgments */}
              <div className="space-y-3 print-legal-section">
                <h3 className="text-sm font-bold uppercase tracking-wider text-amber-500 font-serif border-b border-slate-850 pb-2">III. Landmark Supreme Court Judgments</h3>
                <div className="space-y-4">
                  {result.cases && result.cases.length > 0 ? (
                    result.cases.map((cs, idx) => (
                      <div key={idx} className="pl-4 space-y-1.5 text-sm">
                        <h4 className="font-semibold text-slate-200">
                          {cs.case_name} <span className="font-mono text-xs text-indigo-400">[{cs.citation}]</span>
                        </h4>
                        <p className="text-slate-350 font-sans font-light leading-relaxed text-xs pl-3 border-l border-slate-800">
                          {cs.summary}
                        </p>
                      </div>
                    ))
                  ) : (
                    <p className="text-xs text-slate-500 italic pl-4 font-sans">No citing landmark court judgments retrieved.</p>
                  )}
                </div>
              </div>

              {/* 4. Reasoning */}
              <div className="space-y-3 print-legal-section">
                <h3 className="text-sm font-bold uppercase tracking-wider text-amber-500 font-serif border-b border-slate-850 pb-2">IV. Synthesized Legal Reasoning</h3>
                <div className="pl-4 text-xs text-slate-300 font-sans font-light leading-relaxed space-y-3">
                  {result.reasoning ? (
                    result.reasoning.split('\n').filter(p => p.trim()).map((para, idx) => (
                      <p key={idx} className="whitespace-pre-line">
                        {para.replace(/\*\*/g, '')}
                      </p>
                    ))
                  ) : (
                    <p className="italic text-slate-550 pl-4 font-sans">No reasoning details provided.</p>
                  )}
                </div>
              </div>

              {/* 5. Validation */}
              <div className="space-y-3 print-legal-section">
                <h3 className="text-sm font-bold uppercase tracking-wider text-amber-500 font-serif border-b border-slate-850 pb-2">V. Orchestrator Validation Details</h3>
                <div className="pl-4 text-xs text-slate-350 space-y-2">
                  <div className="flex items-center gap-4 font-sans text-slate-400">
                    <span><strong>Validation Check:</strong> {result.validation_result?.is_valid ? <span className="text-emerald-400">PASSED</span> : <span className="text-rose-400">FLAGGED</span>}</span>
                    <span>•</span>
                    <span><strong>Hallucination Risk:</strong> <span className="capitalize text-amber-400">{result.validation_result?.hallucination_risk || 'Low'}</span></span>
                  </div>
                  {result.validation_result?.details && (
                    <p className="font-sans font-light leading-relaxed text-xs bg-slate-950/40 p-4 rounded-xl border border-slate-850 mt-2">
                      {result.validation_result.details}
                    </p>
                  )}
                </div>
              </div>

              {/* 6. Possible Verdict */}
              <div className="space-y-3 print-legal-section bg-slate-950/40 p-6 rounded-xl border border-slate-850/80">
                <h3 className="text-sm font-bold uppercase tracking-wider text-amber-500 font-serif border-b border-slate-850 pb-2">VI. Predicted Verdict & Outcome</h3>
                <div className="pl-2 space-y-3">
                  <p className="text-sm italic font-semibold text-slate-200">
                    "{result.verdict || 'No verdict predicted.'}"
                  </p>
                  <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between text-xs text-slate-500 font-sans gap-2 pt-3 border-t border-slate-850/60">
                    <span><strong>Confidence Score:</strong> <span className="text-amber-500 font-bold">{result.confidence || 'High'}</span></span>
                    <span>Disclaimer: AI-generated guidance. Consultation with counsel advised.</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      )}

    </div>
  );
}
