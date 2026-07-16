import React from 'react';
import { Scale, Info, LayoutDashboard, Home, Activity } from 'lucide-react';

export default function Header({ currentPage, setCurrentPage, backendHealthy }) {
  const navItems = [
    { id: 'landing', label: 'Home', icon: Home },
    { id: 'query', label: 'Workbench', icon: LayoutDashboard },
    { id: 'about', label: 'About Architecture', icon: Info }
  ];

  return (
    <header className="sticky top-0 z-50 w-full bg-slate-950/80 backdrop-blur-md border-b border-slate-900 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        {/* Brand Logo */}
        <div 
          onClick={() => setCurrentPage('landing')} 
          className="flex items-center gap-2.5 cursor-pointer group"
        >
          <div className="p-2 rounded-xl bg-amber-500/10 text-amber-500 border border-amber-500/25 group-hover:bg-amber-500/20 group-hover:scale-105 transition-all duration-200">
            <Scale className="w-5.5 h-5.5" />
          </div>
          <div>
            <span className="text-lg font-serif font-bold tracking-wide text-slate-100 uppercase">
              Constitu<span className="text-amber-500">AI</span>
            </span>
            <span className="block text-[9px] uppercase tracking-widest text-slate-500 font-sans leading-none">
              Constitution RAG Assistant
            </span>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center gap-1 bg-slate-900/60 p-1 rounded-xl border border-slate-800/80">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentPage === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentPage(item.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-medium transition-all duration-200 ${
                  isActive
                    ? 'bg-amber-500 text-slate-950 font-semibold shadow-md shadow-amber-500/10'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* API connection indicator */}
        <div className="flex items-center gap-2 text-xs bg-slate-900 border border-slate-850 px-3 py-1.5 rounded-full">
          <Activity className={`w-3.5 h-3.5 ${backendHealthy ? 'text-emerald-500 animate-pulse' : 'text-rose-500'}`} />
          <span className="text-slate-400 font-medium">
            Backend: {backendHealthy ? (
              <span className="text-emerald-400">Online</span>
            ) : (
              <span className="text-rose-400">Offline</span>
            )}
          </span>
        </div>

      </div>
    </header>
  );
}
