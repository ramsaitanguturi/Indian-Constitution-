import React from 'react';
import { 
  Scale, 
  Cpu, 
  Timeline, 
  ShieldAlert, 
  HelpCircle, 
  ArrowRight, 
  Bookmark, 
  Database,
  Layers,
  FolderOpen
} from 'lucide-react';

export default function LandingPage({ setCurrentPage, setPreloadedQuery }) {
  const features = [
    {
      title: "Hierarchical RAG Flow",
      desc: "Searches semantic child chunks containing specific details first, then retrieves full parent articles to preserve entire constitutional contexts.",
      icon: Layers,
      color: "text-amber-500 bg-amber-500/10 border-amber-500/20"
    },
    {
      title: "Multi-Agent Architecture",
      desc: "Coordinates specialized agents (Router, Constitution, Case Law, Reasoning, Validation, Verdict) in LangGraph to separate tasks.",
      icon: Cpu,
      color: "text-indigo-400 bg-indigo-500/10 border-indigo-500/20"
    },
    {
      title: "Landmark Judgments Database",
      desc: "Integrates landmark Supreme Court rulings (e.g., Puttaswamy, Maneka Gandhi, Shreya Singhal) to tie statutes to judicial precedent.",
      icon: Database,
      color: "text-purple-400 bg-purple-500/10 border-purple-500/20"
    },
    {
      title: "Validator Guardrails",
      desc: "An autonomous agent fact-checks retrieved sources against the generated answer, flagging hallucination risks and calculating confidence.",
      icon: ShieldAlert,
      color: "text-rose-400 bg-rose-500/10 border-rose-500/20"
    }
  ];

  const presets = [
    {
      category: "Privacy & Liberty",
      q: "Can police search my personal mobile phone without a judicial warrant?",
      badge: "Article 21"
    },
    {
      category: "Freedom of Expression",
      q: "Can the government ban peaceful protests in public parks?",
      badge: "Article 19"
    },
    {
      category: "Religious Freedoms",
      q: "Can state institutions mandate a specific dress code overriding religious observances?",
      badge: "Article 25"
    },
    {
      category: "Equality & Representation",
      q: "Does reservation apply to appointments in private joint ventures funded by the state?",
      badge: "Article 16"
    }
  ];

  const handleStartQuery = (queryText) => {
    setPreloadedQuery(queryText);
    setCurrentPage('query');
  };

  return (
    <div className="max-w-6xl mx-auto px-6 py-12 md:py-20 space-y-24">
      
      {/* 1. Hero Section */}
      <section className="text-center space-y-6 max-w-4xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-xs text-amber-500">
          <Bookmark className="w-3.5 h-3.5" />
          <span>Advanced AI Legal Advisor (Indian Constitution)</span>
        </div>

        <h1 className="text-4xl md:text-6xl font-serif font-extrabold tracking-tight text-slate-100 leading-tight">
          Systematic Constitutional analysis <br className="hidden md:inline" />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-amber-500 to-indigo-400">
            Powered by Multi-Agent RAG
          </span>
        </h1>

        <p className="text-base md:text-lg text-slate-400 font-light leading-relaxed max-w-2xl mx-auto">
          Vidhi.AI parses real-world legal problems, identifies fundamental rights implications, references landmark Supreme Court decisions, and outlines logical verdicts.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
          <button
            type="button"
            onClick={() => handleStartQuery("")}
            className="w-full sm:w-auto flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl bg-amber-500 hover:bg-amber-600 text-slate-950 font-medium transition-all duration-200 shadow-lg shadow-amber-500/10 hover:shadow-xl hover:shadow-amber-500/20 active:scale-[0.98]"
          >
            <span>Launch Analysis Workbench</span>
            <ArrowRight className="w-4 h-4" />
          </button>
          
          <button
            type="button"
            onClick={() => setCurrentPage('about')}
            className="w-full sm:w-auto flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 text-slate-300 font-medium transition-all duration-200"
          >
            <span>Explore RAG Architecture</span>
          </button>
        </div>
      </section>

      {/* 2. Presets Grid */}
      <section className="space-y-6">
        <div className="text-center">
          <h2 className="text-2xl md:text-3xl font-serif font-semibold text-slate-200">
            Common Constitutional Queries
          </h2>
          <p className="text-sm text-slate-500 mt-2 max-w-lg mx-auto">
            Select a scenario to witness the routing, retrieval, reasoning, and validation pipeline in action.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-4xl mx-auto">
          {presets.map((item, idx) => (
            <div 
              key={idx}
              onClick={() => handleStartQuery(item.q)}
              className="glass-panel glass-panel-hover rounded-xl p-5 cursor-pointer flex flex-col justify-between text-left group"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] uppercase font-bold tracking-wider text-indigo-400">
                    {item.category}
                  </span>
                  <span className="text-[9px] px-2 py-0.5 rounded bg-slate-950 border border-slate-850 text-amber-500/80 font-mono">
                    {item.badge}
                  </span>
                </div>
                <p className="text-sm text-slate-300 group-hover:text-slate-100 transition-colors">
                  "{item.q}"
                </p>
              </div>
              
              <div className="mt-4 flex items-center gap-1.5 text-xs text-slate-500 group-hover:text-amber-500 transition-colors font-medium">
                <span>Analyze this case</span>
                <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 3. Features Section */}
      <section className="space-y-12">
        <div className="text-center">
          <h2 className="text-2xl md:text-3xl font-serif font-semibold text-slate-200">
            Engineered for Precision, Not Chat
          </h2>
          <p className="text-sm text-slate-500 mt-2 max-w-lg mx-auto">
            Legal research demands factual consistency. Vidhi.AI replaces generic chat loops with specialized pipeline nodes.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto">
          {features.map((feat, idx) => {
            const Icon = feat.icon;
            return (
              <div key={idx} className="glass-panel rounded-xl p-6 flex gap-4 text-left">
                <div className={`p-3 rounded-xl border shrink-0 h-fit ${feat.color}`}>
                  <Icon className="w-6 h-6" />
                </div>
                <div className="space-y-2">
                  <h4 className="text-base font-serif font-semibold text-slate-200">
                    {feat.title}
                  </h4>
                  <p className="text-xs text-slate-400 leading-relaxed font-light">
                    {feat.desc}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* 4. Timeline Workflow */}
      <section className="glass-panel rounded-2xl p-8 max-w-4xl mx-auto space-y-8">
        <div className="text-center max-w-md mx-auto space-y-2">
          <h2 className="text-xl md:text-2xl font-serif font-semibold text-slate-200">
            How the Analysis Pipeline Executes
          </h2>
          <p className="text-xs text-slate-500 leading-relaxed">
            Every submission triggers an orchestration graph to ingest, lookup, validate, and summarize the law.
          </p>
        </div>

        <div className="space-y-6 relative before:absolute before:left-4 before:top-2 before:bottom-2 before:w-[2px] before:bg-slate-800">
          
          <div className="flex gap-4 items-start text-left relative">
            <div className="w-8 h-8 rounded-full bg-slate-900 border border-slate-850 flex items-center justify-center text-xs text-amber-500 font-bold shrink-0 z-10">
              1
            </div>
            <div>
              <h5 className="text-sm font-semibold text-slate-200">Router Intent Analysis</h5>
              <p className="text-xs text-slate-450 mt-1 leading-relaxed">
                The query is parsed to identify categories (e.g. Fundamental Rights, Privacy, Equality, Arrest) and trigger specific workflows.
              </p>
            </div>
          </div>

          <div className="flex gap-4 items-start text-left relative">
            <div className="w-8 h-8 rounded-full bg-slate-900 border border-slate-850 flex items-center justify-center text-xs text-amber-500 font-bold shrink-0 z-10">
              2
            </div>
            <div>
              <h5 className="text-sm font-semibold text-slate-200">Parent-Child Vector Retrieval</h5>
              <p className="text-xs text-slate-450 mt-1 leading-relaxed">
                Matches the query against short, semantic child clauses in ChromaDB, then pulls full parent articles to prevent reading gaps.
              </p>
            </div>
          </div>

          <div className="flex gap-4 items-start text-left relative">
            <div className="w-8 h-8 rounded-full bg-slate-900 border border-slate-850 flex items-center justify-center text-xs text-amber-500 font-bold shrink-0 z-10">
              3
            </div>
            <div>
              <h5 className="text-sm font-semibold text-slate-200">Precedent Reference Mapping</h5>
              <p className="text-xs text-slate-450 mt-1 leading-relaxed">
                The database matches citation keywords to locate landmark judgments in the Case Law collection.
              </p>
            </div>
          </div>

          <div className="flex gap-4 items-start text-left relative">
            <div className="w-8 h-8 rounded-full bg-slate-900 border border-slate-850 flex items-center justify-center text-xs text-amber-500 font-bold shrink-0 z-10">
              4
            </div>
            <div>
              <h5 className="text-sm font-semibold text-slate-200">Verification & Verdict Generation</h5>
              <p className="text-xs text-slate-450 mt-1 leading-relaxed">
                The Validator Agent confirms that findings match retrieved texts before the Verdict Agent outputs a verdict confidence score.
              </p>
            </div>
          </div>

        </div>
      </section>

    </div>
  );
}
