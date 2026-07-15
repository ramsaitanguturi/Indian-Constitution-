import React from 'react';
import { 
  Shuffle, 
  Search, 
  Brain, 
  ShieldCheck, 
  Scale, 
  CheckCircle2, 
  Loader2 
} from 'lucide-react';

export default function AgentTimeline({ currentStep = 'completed', validationResult = null }) {
  // Define the agent execution steps
  const steps = [
    {
      id: 'router',
      name: 'Router Agent',
      description: 'Analyzing legal scenario category',
      icon: Shuffle,
      details: validationResult?.category ? `Category: ${validationResult.category}` : 'Deciding agent workflows'
    },
    {
      id: 'research',
      name: 'Research Agents',
      description: 'Retrieving Articles & Case Laws',
      icon: Search,
      details: 'ChromaDB Parent-Child search'
    },
    {
      id: 'reasoning',
      name: 'Reasoning Agent',
      description: 'Synthesizing arguments & precedents',
      icon: Brain,
      details: 'Connecting facts to constitution'
    },
    {
      id: 'validation',
      name: 'Validation Agent',
      description: 'Verifying hallucination & accuracy',
      icon: ShieldCheck,
      details: validationResult?.hallucination_risk ? `Hallucination Risk: ${validationResult.hallucination_risk}` : 'Executing fact checks'
    },
    {
      id: 'verdict',
      name: 'Verdict Agent',
      description: 'Formulating legal prediction',
      icon: Scale,
      details: 'Determining final outcome'
    }
  ];

  // Helper to get step status index
  const getStepStatus = (stepId) => {
    if (currentStep === 'loading') {
      // Simulate active flow for loading states
      return 'active'; 
    }
    
    const statusMap = {
      'router': 0,
      'research': 1,
      'reasoning': 2,
      'validation': 3,
      'verdict': 4
    };

    const currentIdx = statusMap[currentStep] ?? 4; // default to all complete if success
    const stepIdx = statusMap[stepId];

    if (stepIdx < currentIdx) return 'completed';
    if (stepIdx === currentIdx) return 'active';
    return 'pending';
  };

  return (
    <div className="glass-panel rounded-2xl p-6 mb-8">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold tracking-wide text-amber-500 font-serif">
          Agentic Workflow Timeline
        </h3>
        <span className="text-xs px-2.5 py-1 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
          LangGraph StateGraph
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 relative">
        {steps.map((step, idx) => {
          const status = getStepStatus(step.id);
          const Icon = step.icon;
          
          let statusBg = 'bg-slate-900 border-slate-800 text-slate-500';
          let borderLine = 'border-slate-850';
          let nameColor = 'text-slate-400';
          let pulseClass = '';

          if (status === 'completed') {
            statusBg = 'bg-emerald-950/40 border-emerald-500/50 text-emerald-400';
            borderLine = 'border-emerald-500/40';
            nameColor = 'text-slate-200';
          } else if (status === 'active') {
            statusBg = 'bg-indigo-950/60 border-indigo-500 text-indigo-300';
            borderLine = 'border-slate-800';
            nameColor = 'text-indigo-200 font-semibold';
            pulseClass = 'pulse-active-node';
          }

          return (
            <div key={step.id} className="flex flex-col items-center text-center relative group">
              {/* Connector line for large screens */}
              {idx < steps.length - 1 && (
                <div className={`hidden md:block absolute top-7 left-[60%] right-[-40%] h-[2px] border-t-2 border-dashed ${borderLine} z-0 transition-colors duration-500`} />
              )}

              {/* Node Circle */}
              <div className={`w-14 h-14 rounded-full flex items-center justify-center border-2 z-10 transition-all duration-500 ${statusBg} ${pulseClass}`}>
                {status === 'completed' ? (
                  <CheckCircle2 className="w-6 h-6" />
                ) : status === 'active' && currentStep === 'loading' ? (
                  <Loader2 className="w-6 h-6 animate-spin" />
                ) : (
                  <Icon className="w-6 h-6" />
                )}
              </div>

              {/* Description */}
              <div className="mt-3 z-10">
                <p className={`text-sm ${nameColor}`}>{step.name}</p>
                <p className="text-[11px] text-slate-500 mt-1 max-w-[150px] leading-tight mx-auto">
                  {step.description}
                </p>
                {step.details && (status === 'completed' || status === 'active') && (
                  <span className="inline-block mt-1.5 text-[9px] px-2 py-0.5 rounded bg-slate-900 border border-slate-800/80 text-amber-500/85">
                    {step.details}
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
