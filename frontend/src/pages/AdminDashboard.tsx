import React, { useState, useEffect } from "react";
import { Scale, RefreshCw, Database, Users, ShieldAlert, Award, Play } from "lucide-react";
import { api } from "../services/api";

export default function AdminDashboard() {
  const [metrics, setMetrics] = useState<any>(null);
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [retraining, setRetraining] = useState(false);
  const [successMsg, setSuccessMsg] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  // Ingestion form state
  const [docType, setDocType] = useState("judgment");
  const [caseName, setCaseName] = useState("");
  const [court, setCourt] = useState("");
  const [state, setState] = useState("");
  const [facts, setFacts] = useState("");
  const [summary, setSummary] = useState("");
  const [outcome, setOutcome] = useState("Allowed");
  const [acts, setActs] = useState("");
  const [sections, setSections] = useState("");
  const [keywords, setKeywords] = useState("");

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const m = await api.admin.getModelMetrics();
        setMetrics(m);
        const u = await api.admin.listUsers();
        setUsers(u);
      } catch (err) {
        console.error("Failed to load admin stats:", err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  const handleRetrain = async () => {
    setRetraining(true);
    setSuccessMsg("");
    setErrorMsg("");
    try {
      await api.admin.retrain();
      setSuccessMsg("Domain Classifier successfully retrained on current database judgments.");
      // Reload metrics
      const m = await api.admin.getModelMetrics();
      setMetrics(m);
    } catch (err: any) {
      setErrorMsg(err.message || "Model retraining pipeline execution failed.");
    } finally {
      setRetraining(false);
    }
  };

  const handleIngest = async (e: React.FormEvent) => {
    e.preventDefault();
    setSuccessMsg("");
    setErrorMsg("");
    try {
      const payload = {
        type: docType,
        case_name: caseName,
        court,
        state,
        facts,
        judgment_summary: summary,
        outcome,
        acts,
        sections,
        keywords
      };
      await api.admin.ingestDocument(payload);
      setSuccessMsg(`Legal ${docType} successfully ingested into search index and DB.`);
      
      // Clear forms
      setCaseName("");
      setFacts("");
      setSummary("");
      setActs("");
      setSections("");
      setKeywords("");
    } catch (err: any) {
      setErrorMsg(err.message || "Document ingestion failed.");
    }
  };

  if (loading) {
    return <div className="text-center py-12 text-sm text-slate-400 font-sans">Loading administrative metrics...</div>;
  }

  return (
    <div className="max-w-7xl mx-auto p-6 font-sans space-y-8">
      {/* Title */}
      <div className="border-b border-slate-200 pb-3 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-primary-500 flex items-center space-x-2">
            <Database className="h-6 w-6 text-gold-500" />
            <span>Administrator Control Console</span>
          </h1>
          <p className="text-slate-500 text-xs mt-0.5">Manage models, users, and ingest judgments</p>
        </div>
      </div>

      {successMsg && (
        <div className="bg-green-50 text-green-700 p-3 rounded-lg border border-green-200 text-xs">
          {successMsg}
        </div>
      )}
      
      {errorMsg && (
        <div className="bg-red-50 text-red-700 p-3 rounded-lg border border-red-200 text-xs">
          {errorMsg}
        </div>
      )}

      {/* Grid: Model retraining and metrics */}
      <div className="grid md:grid-cols-3 gap-8">
        
        {/* ML model metrics */}
        <div className="md:col-span-2 bg-white p-6 rounded-2xl shadow-sm border border-slate-100 space-y-6">
          <div className="border-b border-slate-100 pb-3 flex justify-between items-center">
            <h3 className="text-lg font-bold text-slate-800 flex items-center space-x-2">
              <Award className="h-5 w-5 text-gold-500" />
              <span>Model Evaluation Dashboard</span>
            </h3>
            <button
              onClick={handleRetrain}
              disabled={retraining}
              className="bg-primary-500 hover:bg-primary-600 text-white text-xs font-bold px-4 py-2 rounded-lg flex items-center space-x-1.5 transition-all shadow disabled:opacity-50"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${retraining ? 'animate-spin' : ''}`} />
              <span>{retraining ? "Retraining..." : "Retrain Domain Classifier"}</span>
            </button>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
              <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Classification Acc</p>
              <p className="text-2xl font-black text-slate-800 mt-1">{metrics?.classifier_metrics.accuracy}%</p>
            </div>
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
              <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">F1-Score Classify</p>
              <p className="text-2xl font-black text-slate-800 mt-1">{metrics?.classifier_metrics.f1_score}%</p>
            </div>
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
              <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Retrieval P@5</p>
              <p className="text-2xl font-black text-slate-800 mt-1">{metrics?.retrieval_metrics.precision_at_k}%</p>
            </div>
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
              <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Model AUC-ROC</p>
              <p className="text-2xl font-black text-slate-800 mt-1">{metrics?.predictions_metrics.auc_roc}</p>
            </div>
          </div>

          {/* User Directory */}
          <div className="space-y-3">
            <h4 className="text-sm font-bold text-slate-700 flex items-center space-x-2">
              <Users className="h-4 w-4 text-primary-500" />
              <span>Registered Accounts ({users.length})</span>
            </h4>
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead>
                  <tr className="bg-slate-50 text-slate-400 uppercase tracking-wider">
                    <th className="p-3 rounded-l-lg">Username</th>
                    <th className="p-3">Email</th>
                    <th className="p-3 rounded-r-lg">Assigned Role</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {users.map((u) => (
                    <tr key={u.id} className="hover:bg-slate-50/50">
                      <td className="p-3 font-semibold text-slate-800">{u.username}</td>
                      <td className="p-3 text-slate-600">{u.email}</td>
                      <td className="p-3">
                        <span className="bg-primary-50 text-primary-800 font-bold px-2.5 py-0.5 rounded-full">
                          {u.role}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Ingest document form */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 space-y-4">
          <h3 className="text-lg font-bold text-slate-800 border-b border-slate-100 pb-3">Ingest Judgment</h3>
          
          <form onSubmit={handleIngest} className="space-y-3">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Case Name</label>
              <input
                type="text"
                required
                placeholder="e.g., Sunil Verma v. K. J. George (2024)"
                value={caseName}
                onChange={(e) => setCaseName(e.target.value)}
                className="w-full px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:outline-none focus:border-primary-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1">
                <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Court</label>
                <input
                  type="text"
                  required
                  placeholder="Supreme Court"
                  value={court}
                  onChange={(e) => setCourt(e.target.value)}
                  className="w-full px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:outline-none focus:border-primary-500"
                />
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">State</label>
                <input
                  type="text"
                  placeholder="Karnataka"
                  value={state}
                  onChange={(e) => setState(e.target.value)}
                  className="w-full px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:outline-none focus:border-primary-500"
                />
              </div>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Acts Involved</label>
              <input
                type="text"
                placeholder="Indian Contract Act"
                value={acts}
                onChange={(e) => setActs(e.target.value)}
                className="w-full px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:outline-none focus:border-primary-500"
              />
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Sections (Semicolon-separated)</label>
              <input
                type="text"
                placeholder="73;10"
                value={sections}
                onChange={(e) => setSections(e.target.value)}
                className="w-full px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:outline-none focus:border-primary-500"
              />
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Facts Description</label>
              <textarea
                required
                rows={3}
                placeholder="Provide case facts..."
                value={facts}
                onChange={(e) => setFacts(e.target.value)}
                className="w-full px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:outline-none focus:border-primary-500 resize-none"
              />
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Outcome Judgment</label>
              <textarea
                required
                rows={3}
                placeholder="Provide judgment summary/reasoning..."
                value={summary}
                onChange={(e) => setSummary(e.target.value)}
                className="w-full px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:outline-none focus:border-primary-500 resize-none"
              />
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Decision Label</label>
              <select
                value={outcome}
                onChange={(e) => setOutcome(e.target.value)}
                className="w-full px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:outline-none focus:border-primary-500"
              >
                <option value="Allowed">Allowed</option>
                <option value="Dismissed">Dismissed</option>
                <option value="Acquitted">Acquitted</option>
                <option value="Convicted">Convicted</option>
                <option value="Bail Granted">Bail Granted</option>
              </select>
            </div>

            <button
              type="submit"
              className="w-full bg-slate-900 hover:bg-slate-800 text-white font-bold py-2 rounded-lg text-xs shadow"
            >
              Add to Legal Precedents
            </button>
          </form>
        </div>

      </div>
    </div>
  );
}
