import React, { useState } from "react";
import { Scale, ArrowLeft, Send, Sparkles } from "lucide-react";
import { api } from "../services/api";

interface NewCaseProps {
  onNavigate: (view: string, arg?: any) => void;
}

export default function NewCase({ onNavigate }: NewCaseProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [incidentDate, setIncidentDate] = useState("");
  const [location, setLocation] = useState("");
  const [parties, setParties] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !description) {
      setError("Please fill in the title and description fields.");
      return;
    }
    setError("");
    setLoading(true);

    try {
      const newCase = await api.cases.create({
        title,
        description,
        incident_date: incidentDate || null,
        location: location || null,
        parties: parties || null
      });
      // Redirect to the analysis page for this case
      onNavigate("analysis", newCase.id);
    } catch (err: any) {
      setError(err.message || "Failed to submit case.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6 font-sans space-y-6">
      {/* Back Header */}
      <div className="flex items-center space-x-3 border-b border-slate-200 pb-4">
        <button
          onClick={() => onNavigate("dashboard")}
          className="p-2 hover:bg-slate-100 rounded-lg text-slate-500 transition-colors"
        >
          <ArrowLeft className="h-5 w-5" />
        </button>
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Submit New Legal Case</h1>
          <p className="text-slate-500 text-xs mt-0.5">Describe your problem in plain language. AI will extract parameters.</p>
        </div>
      </div>

      <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100">
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-50 text-red-600 text-xs p-3 rounded-lg border border-red-200">
              {error}
            </div>
          )}

          {/* Title */}
          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Case Title / Reference</label>
            <input
              type="text"
              required
              placeholder="e.g., Landlord Withholding Refund Deposit Dispute"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-primary-500 transition-colors"
            />
          </div>

          {/* Description */}
          <div className="space-y-1">
            <div className="flex justify-between items-center">
              <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Describe your problem in your own words</label>
              <span className="text-[10px] text-primary-500 font-semibold flex items-center space-x-1">
                <Sparkles className="h-3 w-3 text-gold-500" />
                <span>No legal jargon needed</span>
              </span>
            </div>
            <textarea
              required
              rows={6}
              placeholder="Provide a detailed description. (e.g., 'I signed a 1-year rent contract on 2023-01-01 and vacated the premises on 2024-01-01. I gave a deposit of Rs. 50,000. However, the landlord is refusing to return my deposit claiming damage that didn't happen...')"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-primary-500 transition-colors resize-y leading-relaxed"
            />
          </div>

          {/* Advanced details toggles */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-1">
              <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Incident Date (Optional)</label>
              <input
                type="date"
                value={incidentDate}
                onChange={(e) => setIncidentDate(e.target.value)}
                className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-primary-500 transition-colors"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">State / Jurisdiction (Optional)</label>
              <select
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-primary-500 transition-colors"
              >
                <option value="">Select State</option>
                <option value="Karnataka">Karnataka</option>
                <option value="Delhi">Delhi</option>
                <option value="Maharashtra">Maharashtra</option>
                <option value="Tamil Nadu">Tamil Nadu</option>
                <option value="Uttar Pradesh">Uttar Pradesh</option>
                <option value="West Bengal">West Bengal</option>
              </select>
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Parties Involved (Optional)</label>
            <input
              type="text"
              placeholder="e.g., Ramesh Sharma (Tenant) vs Amit Patel (Landlord)"
              value={parties}
              onChange={(e) => setParties(e.target.value)}
              className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-primary-500 transition-colors"
            />
          </div>

          {/* Submit */}
          <div className="flex justify-end pt-4 border-t border-slate-100">
            <button
              type="submit"
              disabled={loading}
              className="bg-primary-500 hover:bg-primary-600 text-white font-bold px-8 py-3 rounded-xl text-sm transition-all shadow-md flex items-center space-x-2 disabled:opacity-50"
            >
              <span>{loading ? "Analyzing..." : "Submit for AI Analysis"}</span>
              <Send className="h-4 w-4" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
