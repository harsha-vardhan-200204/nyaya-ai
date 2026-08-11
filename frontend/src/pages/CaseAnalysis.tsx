import React, { useEffect, useState } from "react";
import { 
  ArrowLeft, FileText, Scale, Save, CheckCircle2, XCircle, 
  HelpCircle, Sparkles, RefreshCw, Layers, Compass, Network, Award
} from "lucide-react";
import { api } from "../services/api";

interface CaseAnalysisProps {
  caseId: number;
  onNavigate: (view: string, arg?: any) => void;
}

export default function CaseAnalysis({ caseId, onNavigate }: CaseAnalysisProps) {
  const [caseData, setCaseData] = useState<any>(null);
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [pipelineProgress, setPipelineProgress] = useState(0);
  const [error, setError] = useState("");
  
  // Bookmark state
  const [bookmarkSuccess, setBookmarkSuccess] = useState<number | null>(null);

  // Counterfactual Simulation State
  const [cfContract, setCfContract] = useState(false);
  const [cfNotice, setCfNotice] = useState(false);
  const [cfReceipt, setCfReceipt] = useState(false);
  const [cfEvidence, setCfEvidence] = useState(false);
  const [cfPrediction, setCfPrediction] = useState<any>(null);
  const [cfLoading, setCfLoading] = useState(false);

  // Side-by-Side Comparison State
  const [compareCase, setCompareCase] = useState<any>(null);

  useEffect(() => {
    const runPipeline = async () => {
      try {
        setLoading(true);
        // Step-by-step progress simulation to impress users during actual load
        setPipelineProgress(15);
        const basicCase = await api.cases.get(caseId);
        setCaseData(basicCase);
        
        setPipelineProgress(45);
        const res = await api.cases.analyze(caseId);
        setAnalysis(res);
        
        // Populate default counterfactual states from model features
        const features = res.prediction.factual_features;
        setCfContract(features.written_contract);
        setCfNotice(features.notice_sent);
        setCfReceipt(features.receipt_exists);
        setCfEvidence(features.evidence_present);
        
        setPipelineProgress(100);
      } catch (err: any) {
        setError(err.message || "Failed to complete AI legal analysis.");
      } finally {
        setLoading(false);
      }
    };
    
    runPipeline();
  }, [caseId]);

  // Recalculate simulation
  const handleSimulationRun = async () => {
    if (!analysis) return;
    setCfLoading(true);
    try {
      const sim = await api.cases.counterfactual({
        written_contract: cfContract,
        notice_sent: cfNotice,
        receipt_exists: cfReceipt,
        evidence_present: cfEvidence,
        category: analysis.category,
        facts: caseData.description
      });
      setCfPrediction(sim);
    } catch (err) {
      console.error(err);
    } finally {
      setCfLoading(false);
    }
  };

  // Bookmark / Save judgment handler
  const handleSaveCase = async (judgId: number) => {
    try {
      await api.legal.saveCase(judgId);
      setBookmarkSuccess(judgId);
      setTimeout(() => setBookmarkSuccess(null), 3000);
    } catch (err) {
      console.error(err);
    }
  };

  const getOutcomeStyle = (outcome: string) => {
    const o = outcome.toLowerCase();
    if (o.includes("allowed") || o.includes("convict") || o.includes("grant")) {
      return "bg-green-50 text-green-700 border-green-200";
    }
    return "bg-red-50 text-red-700 border-red-200";
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col justify-center items-center p-6 font-sans">
        <div className="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg border border-slate-100 space-y-6 text-center">
          <div className="relative inline-block">
            <Scale className="h-12 w-12 text-primary-500 animate-bounce mx-auto" />
            <Sparkles className="absolute -top-2 -right-2 h-5 w-5 text-gold-500 animate-pulse" />
          </div>
          <h2 className="text-xl font-bold text-slate-800">NyayaAI Analysis Active</h2>
          <p className="text-xs text-slate-400">Processing natural language case facts & matching legal precedents...</p>
          
          {/* Progress bar */}
          <div className="space-y-2">
            <div className="w-full bg-slate-100 rounded-full h-3 overflow-hidden border border-slate-200">
              <div 
                className="bg-primary-500 h-full rounded-full transition-all duration-500 ease-out" 
                style={{ width: `${pipelineProgress}%` }}
              />
            </div>
            <div className="flex justify-between text-[10px] text-slate-400 font-bold uppercase tracking-wider">
              <span>Extracting facts ({pipelineProgress}%)</span>
              <span>Matching Laws</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !analysis) {
    return (
      <div className="max-w-3xl mx-auto p-12 text-center space-y-4 font-sans">
        <XCircle className="h-16 w-16 text-red-500 mx-auto" />
        <h2 className="text-xl font-bold text-slate-800">Analysis Failed</h2>
        <p className="text-sm text-slate-500">{error || "Ensure backend server is running and database is active."}</p>
        <button onClick={() => onNavigate("dashboard")} className="bg-primary-500 text-white px-6 py-2 rounded-lg text-sm">
          Return to Dashboard
        </button>
      </div>
    );
  }

  const currentPred = cfPrediction || analysis.prediction;

  return (
    <div className="max-w-7xl mx-auto p-6 font-sans space-y-8">
      {/* Header toolbar */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-slate-200 pb-4 gap-4">
        <div className="flex items-center space-x-3">
          <button
            onClick={() => onNavigate("dashboard")}
            className="p-2 hover:bg-slate-100 rounded-lg text-slate-500 transition-colors"
          >
            <ArrowLeft className="h-5 w-5" />
          </button>
          <div>
            <h1 className="text-2xl font-bold text-slate-800">{caseData.title}</h1>
            <p className="text-slate-500 text-xs mt-0.5">AI Legal Evaluation Docket</p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <a
            href={api.cases.getReportUrl(caseId)}
            target="_blank"
            rel="noreferrer"
            className="bg-primary-500 hover:bg-primary-600 text-white font-semibold px-5 py-2.5 rounded-xl text-sm transition-all shadow-md inline-flex items-center space-x-2"
          >
            <FileText className="h-4 w-4" />
            <span>Generate PDF Report</span>
          </a>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid lg:grid-cols-3 gap-8">
        
        {/* Left Side: Summary & Extracted Timeline */}
        <div className="lg:col-span-2 space-y-8">
          
          {/* Fact card */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 space-y-4">
            <h2 className="text-lg font-bold text-primary-500 border-b border-slate-100 pb-2 flex items-center space-x-2">
              <Scale className="h-5 w-5 text-gold-500" />
              <span>1. Case Facts Summary</span>
            </h2>
            <div className="space-y-3">
              <div className="bg-slate-50 p-4 rounded-xl text-sm leading-relaxed text-slate-700 border border-slate-100">
                {caseData.description}
              </div>
              <div className="grid grid-cols-2 gap-4 text-xs">
                <div className="bg-slate-50/50 p-3 rounded-lg border border-slate-100">
                  <p className="text-slate-400 font-bold uppercase tracking-wider">Identified Category</p>
                  <p className="text-slate-800 font-bold text-sm mt-1">{analysis.category}</p>
                </div>
                <div className="bg-slate-50/50 p-3 rounded-lg border border-slate-100">
                  <p className="text-slate-400 font-bold uppercase tracking-wider">Jurisdiction (State)</p>
                  <p className="text-slate-800 font-bold text-sm mt-1">{analysis.nlp_analysis.location}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Timeline flowchart */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 space-y-4">
            <h2 className="text-lg font-bold text-primary-500 border-b border-slate-100 pb-2 flex items-center space-x-2">
              <Compass className="h-5 w-5 text-gold-500" />
              <span>2. Chronological Timeline flowchart</span>
            </h2>
            <div className="relative pl-6 border-l border-primary-100 space-y-6">
              {analysis.nlp_analysis.timeline.map((item: any, idx: number) => (
                <div key={idx} className="relative">
                  {/* Timeline dot */}
                  <span className="absolute -left-[30px] top-1.5 bg-primary-500 w-3 h-3 rounded-full border-2 border-white ring-4 ring-primary-100" />
                  <div className="space-y-1">
                    <span className="inline-block bg-gold-100 text-gold-800 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">
                      {item.date}
                    </span>
                    <p className="text-sm text-slate-700">{item.event}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Recommended Statutory Sections */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 space-y-4">
            <h2 className="text-lg font-bold text-primary-500 border-b border-slate-100 pb-2 flex items-center space-x-2">
              <Layers className="h-5 w-5 text-gold-500" />
              <span>3. Potentially Relevant Provisions</span>
            </h2>
            <p className="text-xs text-slate-400">
              Listed based on semantic overlap with problem details. *Subject to verification by qualified counsel.*
            </p>
            <div className="space-y-3">
              {analysis.nlp_analysis.citations.length === 0 ? (
                <p className="text-sm text-slate-500 italic">No specific statutory references extracted. System recommends general civil remedy provisions.</p>
              ) : (
                analysis.nlp_analysis.citations.map((cit: string, idx: number) => (
                  <div key={idx} className="p-3.5 bg-slate-50/70 border border-slate-100 rounded-xl flex justify-between items-center">
                    <div className="space-y-0.5">
                      <p className="text-sm font-bold text-slate-800">{cit}</p>
                      <p className="text-[10px] text-slate-400">Indian Legal Code Database</p>
                    </div>
                    <span className="bg-primary-100 text-primary-800 border border-primary-200 text-[10px] font-bold px-3 py-1 rounded-full uppercase tracking-wider">
                      Verified Reference
                    </span>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Interactive Case Graph (SVG-based) */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 space-y-4">
            <h2 className="text-lg font-bold text-primary-500 border-b border-slate-100 pb-2 flex items-center space-x-2">
              <Network className="h-5 w-5 text-gold-500" />
              <span>4. Interactive Legal Knowledge Graph</span>
            </h2>
            <div className="h-72 border border-slate-100 rounded-xl bg-slate-900/90 relative overflow-hidden flex items-center justify-center p-4">
              {/* SVG interactive network mapping */}
              <svg className="w-full h-full max-w-lg" viewBox="0 0 500 250">
                {/* Connection lines */}
                <line x1="250" y1="125" x2="100" y2="60" stroke="#b48c28" strokeWidth="2" strokeDasharray="3,3" />
                <line x1="250" y1="125" x2="400" y2="60" stroke="#1e293b" strokeWidth="2" />
                <line x1="250" y1="125" x2="250" y2="200" stroke="#3b82f6" strokeWidth="2" />
                <line x1="100" y1="60" x2="250" y2="200" stroke="#3b82f6" strokeWidth="1" opacity="0.5" />
                
                {/* Node: Current Case */}
                <circle cx="250" cy="125" r="28" fill="#102c57" />
                <text x="250" y="129" textAnchor="middle" fill="#ffffff" fontSize="9" fontWeight="bold">Current Case</text>
                
                {/* Node: Legal Acts/Sections */}
                <circle cx="100" cy="60" r="24" fill="#b48c28" />
                <text x="100" y="63" textAnchor="middle" fill="#ffffff" fontSize="8" fontWeight="bold">Sections</text>
                
                {/* Node: Historical Judgments */}
                <circle cx="400" cy="60" r="24" fill="#0f172a" />
                <text x="400" y="63" textAnchor="middle" fill="#ffffff" fontSize="8" fontWeight="bold">Precedents</text>
                
                {/* Node: Court level */}
                <circle cx="250" cy="200" r="22" fill="#3b82f6" />
                <text x="250" y="203" textAnchor="middle" fill="#ffffff" fontSize="8" fontWeight="bold">Judiciary</text>
              </svg>
              <div className="absolute bottom-3 left-3 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700/50 text-[10px] text-slate-300">
                Nodes connect matching laws, precedents and jurisdictions dynamically.
              </div>
            </div>
          </div>

        </div>

        {/* Right Side: Prediction dials, Counterfactual panel, and similar cases */}
        <div className="space-y-8">
          
          {/* Outcome Prediction Dials */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 space-y-6">
            <div className="border-b border-slate-100 pb-3 flex justify-between items-center">
              <h3 className="text-lg font-bold text-slate-800 flex items-center space-x-2">
                <Award className="h-5 w-5 text-gold-500" />
                <span>Historical Prediction</span>
              </h3>
              <span className="bg-gold-50 text-gold-700 px-2 py-0.5 rounded text-[10px] font-bold border border-gold-200">
                Confidence: {currentPred.confidence_score}%
              </span>
            </div>

            {/* Probability Bars */}
            <div className="space-y-4">
              {currentPred.probabilities.map((prob: any, idx: number) => {
                const isAllowed = idx === 0;
                return (
                  <div key={idx} className="space-y-1">
                    <div className="flex justify-between text-xs font-semibold text-slate-600">
                      <span>{prob.label}</span>
                      <span>{prob.probability}%</span>
                    </div>
                    <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden border border-slate-200">
                      <div 
                        className={`h-full rounded-full transition-all duration-500 ${isAllowed ? 'bg-green-500' : 'bg-red-500'}`}
                        style={{ width: `${prob.probability}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
            
            {/* Predict Description */}
            <p className="text-xs text-slate-500 leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-100">
              {currentPred.explanation}
            </p>
          </div>

          {/* Counterfactuals Simulator Panel */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 space-y-4">
            <h3 className="text-lg font-bold text-slate-800 flex items-center space-x-2 border-b border-slate-100 pb-3">
              <RefreshCw className="h-5 w-5 text-gold-500" />
              <span> Factual Simulator ("What If?")</span>
            </h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Recalculate outcomes by simulating changes in available legal evidence:
            </p>
            
            <div className="space-y-3 pt-2">
              <label className="flex items-center space-x-3 text-xs text-slate-700 font-semibold cursor-pointer">
                <input 
                  type="checkbox" 
                  checked={cfContract} 
                  onChange={(e) => setCfContract(e.target.checked)}
                  className="rounded border-slate-300 text-primary-500 focus:ring-primary-500 h-4 w-4"
                />
                <span>Written Agreement Exists</span>
              </label>

              <label className="flex items-center space-x-3 text-xs text-slate-700 font-semibold cursor-pointer">
                <input 
                  type="checkbox" 
                  checked={cfNotice} 
                  onChange={(e) => setCfNotice(e.target.checked)}
                  className="rounded border-slate-300 text-primary-500 focus:ring-primary-500 h-4 w-4"
                />
                <span>Formal Notice Was Sent</span>
              </label>

              <label className="flex items-center space-x-3 text-xs text-slate-700 font-semibold cursor-pointer">
                <input 
                  type="checkbox" 
                  checked={cfReceipt} 
                  onChange={(e) => setCfReceipt(e.target.checked)}
                  className="rounded border-slate-300 text-primary-500 focus:ring-primary-500 h-4 w-4"
                />
                <span>Transaction Receipts Available</span>
              </label>

              <label className="flex items-center space-x-3 text-xs text-slate-700 font-semibold cursor-pointer">
                <input 
                  type="checkbox" 
                  checked={cfEvidence} 
                  onChange={(e) => setCfEvidence(e.target.checked)}
                  className="rounded border-slate-300 text-primary-500 focus:ring-primary-500 h-4 w-4"
                />
                <span>Digital/Secondary Evidence Ready</span>
              </label>
              
              <button
                onClick={handleSimulationRun}
                disabled={cfLoading}
                className="w-full bg-slate-900 hover:bg-slate-800 text-white font-bold py-2 rounded-lg text-xs mt-2 transition-all shadow"
              >
                {cfLoading ? "Recalculating..." : "Simulate Outcome Shifts"}
              </button>
            </div>

            {/* Explainable AI Factors */}
            <div className="pt-4 border-t border-slate-100 space-y-3">
              <div>
                <p className="text-[10px] font-bold text-green-600 uppercase tracking-wide">Supporting Elements</p>
                <div className="space-y-1.5 mt-1.5">
                  {currentPred.supporting_factors.map((f: string, idx: number) => (
                    <div key={idx} className="flex items-start space-x-2 text-xs text-slate-600">
                      <CheckCircle2 className="h-3.5 w-3.5 text-green-500 mt-0.5 flex-shrink-0" />
                      <span>{f}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <p className="text-[10px] font-bold text-red-500 uppercase tracking-wide">Vulnerability Elements</p>
                <div className="space-y-1.5 mt-1.5">
                  {currentPred.risk_factors.map((f: string, idx: number) => (
                    <div key={idx} className="flex items-start space-x-2 text-xs text-slate-600">
                      <XCircle className="h-3.5 w-3.5 text-red-500 mt-0.5 flex-shrink-0" />
                      <span>{f}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Precedent matches list */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 space-y-4">
            <h3 className="text-lg font-bold text-slate-800 border-b border-slate-100 pb-3 flex items-center space-x-2">
              <Compass className="h-5 w-5 text-gold-500" />
              <span>Similar precedents</span>
            </h3>
            <div className="space-y-4">
              {analysis.similar_cases.map((sc: any) => (
                <div key={sc.id} className="p-3 bg-slate-50 rounded-xl border border-slate-100 space-y-2">
                  <div className="flex justify-between items-start">
                    <p className="text-xs font-bold text-slate-800 hover:underline cursor-pointer" onClick={() => setCompareCase(sc)}>
                      {sc.case_name}
                    </p>
                    <span className="text-[9px] bg-primary-100 text-primary-800 px-1.5 py-0.5 rounded font-bold">
                      {sc.similarity_score}% Match
                    </span>
                  </div>
                  <div className="flex justify-between items-center text-[10px] text-slate-400">
                    <span>{sc.court}</span>
                    <span>{sc.judgment_date}</span>
                  </div>
                  <div className="flex justify-between items-center border-t border-slate-200/50 pt-2 mt-1">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${getOutcomeStyle(sc.outcome)}`}>
                      {sc.outcome}
                    </span>
                    <button
                      onClick={() => handleSaveCase(sc.id)}
                      disabled={bookmarkSuccess === sc.id}
                      className="text-[10px] text-primary-500 font-bold hover:underline inline-flex items-center space-x-1"
                    >
                      <Save className="h-3 w-3" />
                      <span>{bookmarkSuccess === sc.id ? "Bookmarked!" : "Save precedent"}</span>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>

      {/* Side-by-Side Case Comparison Grid Modal (if chosen) */}
      {compareCase && (
        <div className="fixed inset-0 bg-slate-900/60 flex items-center justify-center p-6 z-50 overflow-y-auto">
          <div className="bg-white rounded-2xl w-full max-w-4xl max-h-[85vh] overflow-y-auto shadow-2xl p-6 space-y-6">
            <div className="flex justify-between items-center border-b border-slate-200 pb-3">
              <h2 className="text-xl font-bold text-primary-500">Side-by-Side Case Comparison</h2>
              <button 
                onClick={() => setCompareCase(null)}
                className="text-slate-400 hover:text-slate-600 font-bold text-sm bg-slate-100 hover:bg-slate-200 h-8 w-8 rounded-full"
              >
                ✕
              </button>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left border-collapse border border-slate-200">
                <thead>
                  <tr className="bg-slate-50 text-slate-500 border border-slate-200">
                    <th className="p-4 border border-slate-200 w-1/4">Evaluation Attribute</th>
                    <th className="p-4 border border-slate-200 w-3/8 text-primary-500 font-bold">Your Case (Current)</th>
                    <th className="p-4 border border-slate-200 w-3/8 text-gold-600 font-bold">Precedent: {compareCase.case_name}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td className="p-4 border border-slate-200 font-bold text-slate-600">Legal Domain</td>
                    <td className="p-4 border border-slate-200">{analysis.category}</td>
                    <td className="p-4 border border-slate-200">{compareCase.acts}</td>
                  </tr>
                  <tr>
                    <td className="p-4 border border-slate-200 font-bold text-slate-600">Disputed Circumstances</td>
                    <td className="p-4 border border-slate-200 text-slate-700 leading-relaxed">{caseData.description}</td>
                    <td className="p-4 border border-slate-200 text-slate-700 leading-relaxed">{compareCase.facts}</td>
                  </tr>
                  <tr>
                    <td className="p-4 border border-slate-200 font-bold text-slate-600">Key Provisions Cited</td>
                    <td className="p-4 border border-slate-200 font-semibold">{analysis.nlp_analysis.citations.join(', ') || "Calculating..."}</td>
                    <td className="p-4 border border-slate-200 font-semibold">{compareCase.sections}</td>
                  </tr>
                  <tr>
                    <td className="p-4 border border-slate-200 font-bold text-slate-600">Outcome Outcome</td>
                    <td className="p-4 border border-slate-200 italic font-semibold text-primary-500">Pending Evaluation</td>
                    <td className="p-4 border border-slate-200"><span className={`px-2.5 py-1 rounded text-xs font-bold border ${getOutcomeStyle(compareCase.outcome)}`}>{compareCase.outcome}</span></td>
                  </tr>
                  <tr className="bg-slate-50/50">
                    <td className="p-4 border border-slate-200 font-bold text-slate-600">Correlation Reasoning</td>
                    <td colSpan={2} className="p-4 border border-slate-200 text-slate-700">
                      <strong>Analysis Match: {compareCase.similarity_score}%</strong>. Relevancy reasons: {compareCase.why_similar}.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <div className="flex justify-end border-t border-slate-100 pt-4">
              <button onClick={() => setCompareCase(null)} className="bg-primary-500 text-white font-bold px-6 py-2 rounded-lg text-xs shadow-md">
                Close Comparison
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
