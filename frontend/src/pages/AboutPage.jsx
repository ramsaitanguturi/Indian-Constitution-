import React from 'react';
import { 
  GitMerge, 
  Cpu, 
  Layers, 
  Search, 
  BrainCircuit, 
  ShieldAlert, 
  Database,
  Terminal,
  Bookmark,
  Scale
} from 'lucide-react';

export default function AboutPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-16">
      
      {/* Page Header */}
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <h2 className="text-2xl md:text-3xl font-serif font-semibold text-slate-100">
          RAG & Multi-Agent Architecture
        </h2>
        <p className="text-xs text-slate-400 font-light">
          Understanding the semantic indexing and agentic orchestration driving ConstituAI.
        </p>
      </div>

      {/* 1. Parent-Child RAG Flow */}
      <section className="glass-panel rounded-2xl p-8 space-y-6">
        <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
          <div className="p-2.5 rounded-xl bg-amber-500/10 text-amber-500 border border-amber-500/20">
            <Layers className="w-6 h-6" />
          </div>
          <div>
            <span className="text-[10px] uppercase font-bold tracking-widest text-slate-500">
              Information Retrieval
            </span>
            <h3 className="text-lg font-serif font-semibold text-slate-200">
              Hierarchical Parent-Child RAG
            </h3>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          <div className="space-y-4 text-sm text-slate-350 font-light leading-relaxed">
            <p>
              Constitutional articles (e.g., <strong>Article 21</strong>: <em>"Protection of life and personal liberty"</em>) are highly abstract and concise. A direct semantic embedding search for a query like "unauthorized tapping of cell phone data" often fails because it has low text similarity to the abstract term "life and personal liberty".
            </p>
            <p>
              To solve this, our system implements <strong>Hierarchical Retrieval</strong>:
            </p>
            <ul className="space-y-2">
              <li className="flex items-start gap-2">
                <span className="text-amber-500 font-bold mt-0.5">•</span>
                <span><strong>Child Chunk Indexing:</strong> We segment parent articles into specific child chunks containing detailed clauses, explanations, landmark ratio summaries, and search keywords.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-amber-500 font-bold mt-0.5">•</span>
                <span><strong>Reverse Mapping:</strong> The vector database searches the detail-rich child collections. When a match is found, the system uses metadata links to pull the full, original parent article to present to the LLM.</span>
              </li>
            </ul>
          </div>

          {/* Visual Schematic Diagram */}
          <div className="p-6 rounded-xl bg-slate-950/80 border border-slate-850 space-y-4 font-mono text-xs text-slate-400">
            <div className="text-amber-500 font-bold">// Retrieval Flow Diagram</div>
            
            <div className="space-y-3 pl-2">
              <div className="p-2 rounded bg-slate-900 border border-slate-800">
                User Query: "warrantless search of device"
              </div>
              <div className="text-center">↓</div>
              <div className="p-2 rounded bg-indigo-950/30 border border-indigo-900/40 text-indigo-300">
                1. Vector Match on Child: "clause 21(1) digital privacy"
              </div>
              <div className="text-center">↓</div>
              <div className="p-2 rounded bg-emerald-950/30 border border-emerald-900/40 text-emerald-300">
                2. Map back to Parent ID: "art_21"
              </div>
              <div className="text-center">↓</div>
              <div className="p-2 rounded bg-amber-950/30 border border-amber-900/40 text-amber-300">
                3. Load Article 21 full text for LLM Context
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 2. Multi-Agent System Graph */}
      <section className="glass-panel rounded-2xl p-8 space-y-6">
        <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
          <div className="p-2.5 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <GitMerge className="w-6 h-6" />
          </div>
          <div>
            <span className="text-[10px] uppercase font-bold tracking-widest text-slate-500">
              Stateful Orchestration
            </span>
            <h3 className="text-lg font-serif font-semibold text-slate-200">
              Multi-Agent LangGraph System
            </h3>
          </div>
        </div>

        <p className="text-sm text-slate-350 font-light leading-relaxed">
          Instead of relying on a single prompt, ConstituAI routes queries through a sequence of autonomous agent nodes managed in a stateful LangGraph graph structure:
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          
          <div className="p-5 rounded-xl bg-slate-950/40 border border-slate-850 space-y-2">
            <div className="flex items-center gap-2 text-indigo-400">
              <Cpu className="w-4 h-4" />
              <h4 className="text-xs uppercase font-bold tracking-wider font-serif">1. Router Agent</h4>
            </div>
            <p className="text-[11px] text-slate-450 leading-relaxed">
              Analyzes the user scenario's intent. Classifies categories (e.g. personal liberty, freedom of expression, equality) and triggers target sub-agents.
            </p>
          </div>

          <div className="p-5 rounded-xl bg-slate-950/40 border border-slate-850 space-y-2">
            <div className="flex items-center gap-2 text-indigo-400">
              <Search className="w-4 h-4" />
              <h4 className="text-xs uppercase font-bold tracking-wider font-serif">2. Research Agents</h4>
            </div>
            <p className="text-[11px] text-slate-450 leading-relaxed">
              Retrieves statutory sections from the constitution collection and corresponding Supreme Court landmark precedents from the Case Law collection.
            </p>
          </div>

          <div className="p-5 rounded-xl bg-slate-950/40 border border-slate-850 space-y-2">
            <div className="flex items-center gap-2 text-indigo-400">
              <BrainCircuit className="w-4 h-4" />
              <h4 className="text-xs uppercase font-bold tracking-wider font-serif">3. Reasoning Agent</h4>
            </div>
            <p className="text-[11px] text-slate-450 leading-relaxed">
              Acts as the central synthesiser, linking user facts, matching constitutional clauses, and landmark ratio decidendi to map logical pathways.
            </p>
          </div>

          <div className="p-5 rounded-xl bg-slate-950/40 border border-slate-850 space-y-2">
            <div className="flex items-center gap-2 text-indigo-400">
              <ShieldAlert className="w-4 h-4" />
              <h4 className="text-xs uppercase font-bold tracking-wider font-serif">4. Validator Agent</h4>
            </div>
            <p className="text-[11px] text-slate-450 leading-relaxed">
              A guardrail step checking the reasoning chain against original sources to verify citations and evaluate hallucination metrics.
            </p>
          </div>

          <div className="p-5 rounded-xl bg-slate-950/40 border border-slate-850 space-y-2">
            <div className="flex items-center gap-2 text-indigo-400">
              <Scale className="w-4 h-4" />
              <h4 className="text-xs uppercase font-bold tracking-wider font-serif">5. Verdict Agent</h4>
            </div>
            <p className="text-[11px] text-slate-450 leading-relaxed">
              Concludes the analysis, predicting the potential outcome of the constitutional dispute and assigning confidence ratings.
            </p>
          </div>

          <div className="p-5 rounded-xl bg-slate-950/40 border border-slate-850 flex flex-col justify-center text-center items-center">
            <span className="text-[9px] uppercase font-bold text-amber-500 tracking-wider">Design Goal</span>
            <p className="text-[10px] text-slate-500 mt-1 max-w-[155px]">
              Modularity ensures individual nodes can be modified or tested independently.
            </p>
          </div>

        </div>
      </section>

      {/* 3. Tech Stack details */}
      <section className="glass-panel rounded-2xl p-8 space-y-6">
        <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
          <div className="p-2.5 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
            <Terminal className="w-6 h-6" />
          </div>
          <div>
            <span className="text-[10px] uppercase font-bold tracking-widest text-slate-500">
              System Engineering
            </span>
            <h3 className="text-lg font-serif font-semibold text-slate-200">
              Technology Stack
            </h3>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs font-light">
          
          <div className="space-y-1">
            <span className="text-slate-400 block font-semibold">Backend Engine</span>
            <span className="text-slate-500 block">FastAPI / Python 3.12</span>
            <span className="text-slate-500 block font-mono">Uvicorn server hosting</span>
          </div>

          <div className="space-y-1">
            <span className="text-slate-400 block font-semibold">Graph Framework</span>
            <span className="text-slate-500 block">LangGraph / LangChain</span>
            <span className="text-slate-500 block font-mono">Stateful agent transitions</span>
          </div>

          <div className="space-y-1">
            <span className="text-slate-400 block font-semibold">Vector Database</span>
            <span className="text-slate-500 block">ChromaDB (Persistent)</span>
            <span className="text-slate-500 block font-mono">Semantic & Keyword Fusion</span>
          </div>

          <div className="space-y-1">
            <span className="text-slate-400 block font-semibold">UI Presentation</span>
            <span className="text-slate-500 block">React 19 / Vite / Tailwind</span>
            <span className="text-slate-500 block font-mono">Lucide icons / CSS v4</span>
          </div>

        </div>
      </section>

    </div>
  );
}
