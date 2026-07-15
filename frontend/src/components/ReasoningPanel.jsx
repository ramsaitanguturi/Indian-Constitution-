import React from 'react';
import { BrainCircuit, Info, AlertTriangle } from 'lucide-react';

export default function ReasoningPanel({ reasoning }) {
  // A lightweight parser to convert simple Markdown symbols into structured HTML
  const formatMarkdown = (text) => {
    if (!text) return null;

    // Split text by lines to construct paragraphs and lists
    const lines = text.split('\n');
    let insideList = false;
    const elements = [];

    lines.forEach((line, idx) => {
      const trimmed = line.trim();

      // Handle empty lines (paragraph breaks)
      if (!trimmed) {
        if (insideList) {
          insideList = false;
        }
        return;
      }

      // Parse headers (e.g., ### Subheader)
      const headerMatch = trimmed.match(/^(#{1,6})\s+(.*)$/);
      if (headerMatch) {
        if (insideList) {
          insideList = false;
        }
        const level = headerMatch[1].length;
        const content = parseInlineFormatting(headerMatch[2]);
        
        if (level <= 3) {
          elements.push(
            <h4 key={`h-${idx}`} className="text-base font-serif font-semibold text-amber-500 mt-5 mb-2">
              {content}
            </h4>
          );
        } else {
          elements.push(
            <h5 key={`h-${idx}`} className="text-sm font-serif font-bold text-slate-300 mt-4 mb-2">
              {content}
            </h5>
          );
        }
        return;
      }

      // Parse bullet lists (e.g., - item or * item)
      if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
        const itemContent = parseInlineFormatting(trimmed.substring(2));
        elements.push(
          <li key={`li-${idx}`} className="ml-5 list-disc text-sm text-slate-350 leading-relaxed mb-1.5 font-light">
            {itemContent}
          </li>
        );
        return;
      }

      // Regular paragraphs
      const pContent = parseInlineFormatting(trimmed);
      elements.push(
        <p key={`p-${idx}`} className="text-sm text-slate-300 leading-relaxed font-sans font-light mb-4">
          {pContent}
        </p>
      );
    });

    return elements;
  };

  // Helper to parse bold (**text**) and italic (*text* or _text_) inline formatting
  const parseInlineFormatting = (text) => {
    const parts = [];
    let currentText = text;
    let keyIdx = 0;

    // Match bold formatting (**bold**)
    while (currentText.includes('**')) {
      const startIdx = currentText.indexOf('**');
      const endIdx = currentText.indexOf('**', startIdx + 2);
      
      if (endIdx === -1) break;

      // Add text before bold
      if (startIdx > 0) {
        parts.push(currentText.substring(0, startIdx));
      }

      // Add bold text
      parts.push(
        <strong key={`b-${keyIdx++}`} className="font-bold text-amber-400/90 font-serif">
          {currentText.substring(startIdx + 2, endIdx)}
        </strong>
      );

      currentText = currentText.substring(endIdx + 2);
    }

    // Add any remaining text
    if (currentText) {
      parts.push(currentText);
    }

    return parts.length > 0 ? parts : text;
  };

  return (
    <div className="glass-panel rounded-2xl p-6 mb-8 relative">
      <div className="flex items-center justify-between border-b border-slate-800/80 pb-4 mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
            <BrainCircuit className="w-6 h-6" />
          </div>
          <div>
            <span className="text-[10px] uppercase font-bold tracking-widest text-slate-500">
              Precedent & Clause Synthesis
            </span>
            <h3 className="text-lg font-serif font-semibold text-slate-100">
              Legal Reasoning Chain
            </h3>
          </div>
        </div>
      </div>

      <div className="font-sans px-2">
        {reasoning ? (
          formatMarkdown(reasoning)
        ) : (
          <div className="flex items-center gap-2.5 text-sm text-slate-500 italic py-4">
            <Info className="w-4 h-4 text-slate-600" />
            <span>Submit a query to generate legal reasoning connections.</span>
          </div>
        )}
      </div>
    </div>
  );
}
