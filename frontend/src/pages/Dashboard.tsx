import React, { useEffect, useState } from "react";
import { Scale, FolderOpen, Save, BookOpen, AlertTriangle, FileText, CheckCircle } from "lucide-react";
import { api } from "../services/api";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";

interface DashboardProps {
  userRole: string;
  onNavigate: (view: string, arg?: any) => void;
}

export default function Dashboard({ userRole, onNavigate }: DashboardProps) {
  const [cases, setCases] = useState<any[]>([]);
  const [savedCases, setSavedCases] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  
  // Chart and analytical state
  const [analytics, setAnalytics] = useState<any>({
    summary: { total_cases_analyzed: 0, total_judgments: 0, total_acts: 0, total_sections: 0, total_users: 0 },
    charts: { cases_by_category: [], outcome_distribution: [] }
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const caseList = await api.cases.list();
        setCases(caseList);
        
        const savedList = await api.legal.listSavedCases();
        setSavedCases(savedList);
        
        // Load admin/lawyer style analytics dynamically
        const stats = await api.admin.getAnalytics();
        setAnalytics(stats);
      } catch (err: any) {
        setError("Failed to load dashboard data. Check backend connectivity.");
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, []);

  const COLORS = ["#102c57", "#b48c28", "#3b82f6", "#10b981", "#8b5cf6", "#ec4899"];

  return (
    <div className="space-y-8 font-sans p-6 max-w-7xl mx-auto">
      {/* Top Welcome Title */}
      <div className="flex justify-between items-center border-b border-slate-200 pb-4">
        <div>
          <h1 className="text-3xl font-bold text-primary-500">NyayaAI Workbench</h1>
          <p className="text-slate-500 text-sm mt-1">Role: <span className="font-semibold text-gold-500">{userRole}</span></p>
        </div>
        <button
          onClick={() => onNavigate("new-case")}
          className="bg-gold-500 hover:bg-gold-600 text-white font-bold px-6 py-2.5 rounded-xl text-sm transition-all shadow-md transform hover:-translate-y-0.5"
        >
          Submit Legal Problem
        </button>
      </div>

      {/* Warning safety disclaimers banner */}
      <div className="bg-amber-50 border-l-4 border-amber-500 p-4 rounded-r-xl text-amber-800 text-xs flex items-center space-x-3">
        <AlertTriangle className="h-5 w-5 text-amber-600 flex-shrink-0" />
        <span>
          <strong>Grounded Research Tool:</strong> NyayaAI offers informational outcome simulations. It is NOT an replacement for physical consultation and does NOT guarantee case success.
        </span>
      </div>

      {/* Statistics Cards Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        <div className="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 flex items-center space-x-4 hover:shadow-md transition-shadow">
          <div className="p-3.5 bg-primary-50 text-primary-500 rounded-xl">
            <Scale className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Submitted Cases</p>
            <p className="text-2xl font-bold text-slate-800">{cases.length}</p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 flex items-center space-x-4 hover:shadow-md transition-shadow">
          <div className="p-3.5 bg-gold-50 text-gold-500 rounded-xl">
            <BookOpen className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Legal Library</p>
            <p className="text-2xl font-bold text-slate-800">{analytics.summary.total_sections}</p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 flex items-center space-x-4 hover:shadow-md transition-shadow">
          <div className="p-3.5 bg-indigo-50 text-indigo-500 rounded-xl">
            <FolderOpen className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Precedents Index</p>
            <p className="text-2xl font-bold text-slate-800">{analytics.summary.total_judgments}</p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 flex items-center space-x-4 hover:shadow-md transition-shadow">
          <div className="p-3.5 bg-emerald-50 text-emerald-500 rounded-xl">
            <Save className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Saved Judgments</p>
            <p className="text-2xl font-bold text-slate-800">{savedCases.length}</p>
          </div>
        </div>
      </div>

      {/* Analytics Charts Grid */}
      <div className="grid md:grid-cols-2 gap-8">
        {/* Category breakdown bar chart */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
          <h3 className="text-lg font-bold text-slate-800 mb-4">Submitted Case Categories</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={analytics.charts.cases_by_category}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" tick={{ fontSize: 10 }} />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="value" fill="#102c57" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Outcome distribution pie chart */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
          <h3 className="text-lg font-bold text-slate-800 mb-4">Historical Precedent Outcomes</h3>
          <div className="h-64 flex flex-col justify-center items-center">
            {analytics.charts.outcome_distribution.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={analytics.charts.outcome_distribution}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={3}
                    dataKey="count"
                    nameKey="outcome"
                    label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                  >
                    {analytics.charts.outcome_distribution.map((entry: any, index: number) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-xs text-slate-400">Loading outcome statistics...</p>
            )}
          </div>
        </div>
      </div>

      {/* Cases List & Saved Cases Grid */}
      <div className="grid md:grid-cols-3 gap-8">
        {/* Submitted Cases List */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 md:col-span-2 space-y-4">
          <h3 className="text-xl font-bold text-slate-800 border-b border-slate-100 pb-3">Your Cases Queue</h3>
          {loading ? (
            <p className="text-sm text-slate-400">Loading cases...</p>
          ) : cases.length === 0 ? (
            <div className="text-center py-12 text-slate-400 text-sm">
              <Scale className="h-12 w-12 mx-auto mb-3 opacity-30" />
              <span>No legal problems submitted yet. Click "Submit Legal Problem" to start research.</span>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead>
                  <tr className="bg-slate-50 text-slate-500 uppercase text-xs tracking-wider">
                    <th className="p-4 rounded-l-lg">Title</th>
                    <th className="p-4">Jurisdiction</th>
                    <th className="p-4">Category</th>
                    <th className="p-4">Status</th>
                    <th className="p-4 rounded-r-lg text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {cases.map((c) => (
                    <tr key={c.id} className="hover:bg-slate-50/50 transition-colors">
                      <td className="p-4 font-semibold text-slate-800">{c.title}</td>
                      <td className="p-4 text-slate-600">{c.location || "Not Specified"}</td>
                      <td className="p-4 text-xs font-medium text-primary-500">{c.case_type || "Calculating..."}</td>
                      <td className="p-4">
                        <span className="bg-green-50 text-green-700 px-2 py-0.5 rounded-full text-xs font-semibold border border-green-200">
                          {c.status}
                        </span>
                      </td>
                      <td className="p-4 text-right space-x-2">
                        <button
                          onClick={() => onNavigate("analysis", c.id)}
                          className="bg-primary-500 hover:bg-primary-600 text-white text-xs font-semibold px-3 py-1.5 rounded-lg shadow-sm"
                        >
                          View AI Analysis
                        </button>
                        <a
                          href={api.cases.getReportUrl(c.id)}
                          target="_blank"
                          rel="noreferrer"
                          className="bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold px-3 py-1.5 rounded-lg inline-flex items-center space-x-1"
                        >
                          <FileText className="h-3.5 w-3.5" />
                          <span>PDF</span>
                        </a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Saved Saved Bookmarks Cases */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 space-y-4">
          <h3 className="text-xl font-bold text-slate-800 border-b border-slate-100 pb-3">Bookmarked Judgments</h3>
          {savedCases.length === 0 ? (
            <p className="text-xs text-slate-400 text-center py-12">No saved judgments. Bookmark relevant precedents during analysis.</p>
          ) : (
            <div className="space-y-3">
              {savedCases.map((sc) => (
                <div key={sc.id} className="p-3 bg-slate-50 rounded-xl border border-slate-100 flex justify-between items-start">
                  <div className="space-y-1">
                    <p className="text-xs font-bold text-slate-800 leading-snug">{sc.judgment?.case_name}</p>
                    <p className="text-[10px] text-slate-400">{sc.judgment?.court} • {sc.judgment?.judgment_date}</p>
                    <span className="inline-block bg-primary-100 text-primary-800 text-[9px] font-semibold px-2 py-0.5 rounded mt-1">
                      {sc.judgment?.outcome}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
