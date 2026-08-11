import React from "react";
import { Scale, Brain, ShieldAlert, ArrowRight, MessageSquare, Search, FileText } from "lucide-react";

interface LandingProps {
  onNavigate: (view: string) => void;
}

export default function Landing({ onNavigate }: LandingProps) {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      {/* Navbar */}
      <header className="bg-primary-500 text-white shadow-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => onNavigate("landing")}>
            <Scale className="h-8 w-8 text-gold-400" />
            <span className="text-2xl font-bold tracking-wide">Nyaya<span className="text-gold-400">AI</span></span>
          </div>
          <nav className="flex space-x-6 items-center">
            <a href="#features" className="hover:text-gold-100 transition-colors text-sm font-medium">Features</a>
            <a href="#disclaimer" className="hover:text-gold-100 transition-colors text-sm font-medium">Disclaimer</a>
            <button 
              onClick={() => onNavigate("login")} 
              className="bg-gold-500 hover:bg-gold-600 text-white font-semibold px-5 py-2 rounded-lg text-sm transition-all shadow-md transform hover:-translate-y-0.5"
            >
              Access System
            </button>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden bg-primary-500 text-white py-24 md:py-32">
        {/* Background Gradients */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_30%,rgba(180,140,40,0.1),transparent)]" />
        <div className="absolute -bottom-16 -right-16 w-96 h-96 bg-primary-600 rounded-full blur-3xl opacity-50" />
        
        <div className="max-w-7xl mx-auto px-6 relative z-10 grid md:grid-cols-2 gap-12 items-center">
          <div className="space-y-6">
            <div className="inline-flex items-center space-x-2 bg-primary-600 border border-primary-400/20 px-3.5 py-1.5 rounded-full text-xs font-semibold tracking-wide text-gold-400">
              <Brain className="h-4 w-4" />
              <span>AI-Powered Legal Research for India</span>
            </div>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
              Understand Your Legal Case With <span className="text-gold-400">AI-Powered</span> Research
            </h1>
            <p className="text-slate-300 text-lg leading-relaxed">
              Analyze legal problems in natural language, discover relevant acts and sections, search similar judgments, and simulate historical case outcomes with grounded reasoning.
            </p>
            <div className="flex flex-wrap gap-4 pt-4">
              <button 
                onClick={() => onNavigate("login")} 
                className="bg-gold-500 hover:bg-gold-600 text-white font-bold px-8 py-3.5 rounded-xl transition-all shadow-lg flex items-center space-x-2 transform hover:-translate-y-0.5"
              >
                <span>Get Started Now</span>
                <ArrowRight className="h-5 w-5" />
              </button>
              <button 
                onClick={() => {
                  const el = document.getElementById("features");
                  el?.scrollIntoView({ behavior: "smooth" });
                }} 
                className="bg-transparent border border-white/20 hover:bg-white/10 font-bold px-8 py-3.5 rounded-xl transition-all"
              >
                Learn More
              </button>
            </div>
          </div>
          
          <div className="relative flex justify-center">
            {/* Visual Dashboard Card Mock */}
            <div className="w-full max-w-md bg-slate-900/40 border border-white/10 rounded-2xl p-6 shadow-2xl backdrop-blur-xl">
              <div className="flex justify-between items-center mb-6 border-b border-white/10 pb-4">
                <div className="flex items-center space-x-2">
                  <div className="h-3 w-3 bg-red-400 rounded-full" />
                  <div className="h-3 w-3 bg-yellow-400 rounded-full" />
                  <div className="h-3 w-3 bg-green-400 rounded-full" />
                </div>
                <span className="text-xs text-slate-400">NyayaAI Simulator v1.2</span>
              </div>
              <div className="space-y-4">
                <div className="bg-white/5 rounded-lg p-3 border border-white/5">
                  <p className="text-xs text-gold-400 font-semibold mb-1">USER PROBLEM</p>
                  <p className="text-xs text-slate-300">"My landlord won't return my security deposit..."</p>
                </div>
                <div className="bg-white/5 rounded-lg p-3 border border-white/5">
                  <p className="text-xs text-gold-400 font-semibold mb-1">IDENTIFIED DOMAIN</p>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-200">Property / Rent Law</span>
                    <span className="text-xs text-green-400">94.8% Conf.</span>
                  </div>
                </div>
                <div className="bg-white/5 rounded-lg p-3 border border-white/5">
                  <p className="text-xs text-gold-400 font-semibold mb-1">PREDICTED HISTORICAL PATTERN</p>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-200">Allowed (Refund ordered)</span>
                    <span className="text-xs text-yellow-400">78% Favorable</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-20 max-w-7xl mx-auto px-6">
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
          <h2 className="text-3xl font-bold text-primary-500">Core Intelligent Modules</h2>
          <p className="text-slate-600">
            NyayaAI is powered by structured NLP pipelines, semantic vector search, and analytical models, custom-built for the Indian constitutional framework.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white p-8 rounded-2xl shadow-md border border-slate-100 hover:shadow-lg transition-shadow space-y-4">
            <div className="p-3 bg-primary-50 text-primary-500 rounded-xl inline-block">
              <FileText className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-bold text-primary-500">AI Case Extraction</h3>
            <p className="text-slate-600 text-sm leading-relaxed">
              Extracts parties, timeline dates, disputed amounts, locations, and cited provisions from natural language inputs without manual jargon lookup.
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-md border border-slate-100 hover:shadow-lg transition-shadow space-y-4">
            <div className="p-3 bg-primary-50 text-primary-500 rounded-xl inline-block">
              <Search className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-bold text-primary-500">Semantic Case Similarity</h3>
            <p className="text-slate-600 text-sm leading-relaxed">
              Performs high-speed semantic matching across historic judgments. Indexes courts, states, outcomes, and tells you exactly "Why this case matches".
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-md border border-slate-100 hover:shadow-lg transition-shadow space-y-4">
            <div className="p-3 bg-primary-50 text-primary-500 rounded-xl inline-block">
              <Brain className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-bold text-primary-500">Outcome & Counterfactuals</h3>
            <p className="text-slate-600 text-sm leading-relaxed">
              Calculates likelihood of historical outcome patterns and allows "What if?" simulations to see how changing specific facts affects probability.
            </p>
          </div>
        </div>
      </section>

      {/* Legal Safety & Disclaimer Section */}
      <section id="disclaimer" className="bg-slate-100 py-16">
        <div className="max-w-5xl mx-auto px-6">
          <div className="bg-white border-l-4 border-gold-500 p-8 rounded-r-2xl shadow-md flex flex-col md:flex-row items-start md:items-center space-y-6 md:space-y-0 md:space-x-8">
            <div className="p-4 bg-gold-50 text-gold-500 rounded-2xl flex-shrink-0">
              <ShieldAlert className="h-10 w-10" />
            </div>
            <div className="space-y-3">
              <h3 className="text-xl font-bold text-primary-500">Legal Safety & Research Intent</h3>
              <p className="text-slate-600 text-sm leading-relaxed">
                NyayaAI provides AI-assisted legal research and educational information only. It is not a substitute for professional legal advice and does not guarantee any legal outcome. Users should verify information with current official legal sources and consult a qualified legal professional.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-primary-500 text-white/70 py-8 border-t border-white/10 mt-auto">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center text-xs space-y-4 md:space-y-0">
          <div>
            <span className="font-bold text-white">NyayaAI</span> - MCA Final Year Project (2026).
          </div>
          <div className="flex space-x-6">
            <a href="#features" className="hover:text-white transition-colors">Features</a>
            <a href="#disclaimer" className="hover:text-white transition-colors">Safety Disclaimer</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
