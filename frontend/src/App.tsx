import React, { useState, useEffect } from "react";
import { Scale, LogOut, User, MessageSquare, Database, LayoutDashboard, FileText, AlertTriangle } from "lucide-react";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import NewCase from "./pages/NewCase";
import CaseAnalysis from "./pages/CaseAnalysis";
import ChatAssistant from "./pages/ChatAssistant";
import AdminDashboard from "./pages/AdminDashboard";
import { api } from "./services/api";

export default function App() {
  const [view, setView] = useState("landing");
  const [userRole, setUserRole] = useState("");
  const [username, setUsername] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [activeCaseId, setActiveCaseId] = useState<number | null>(null);

  // Auto login persistence check
  useEffect(() => {
    const token = localStorage.getItem("nyaya_token");
    const role = localStorage.getItem("nyaya_role");
    const uname = localStorage.getItem("nyaya_username");
    
    if (token && role && uname) {
      setIsLoggedIn(true);
      setUserRole(role);
      setUsername(uname);
      setView("dashboard");
    }
  }, []);

  const handleLoginSuccess = (role: string, name: string) => {
    setIsLoggedIn(true);
    setUserRole(role);
    setUsername(name);
    setView("dashboard");
  };

  const handleLogout = () => {
    api.auth.logout();
    setIsLoggedIn(false);
    setUserRole("");
    setUsername("");
    setView("landing");
  };

  const navigateTo = (newView: string, arg?: any) => {
    if (newView === "analysis" && arg) {
      setActiveCaseId(arg);
    }
    setView(newView);
  };

  // Switch content views
  const renderView = () => {
    switch (view) {
      case "landing":
        return <Landing onNavigate={navigateTo} />;
      case "login":
        return <Login onLoginSuccess={handleLoginSuccess} onNavigate={navigateTo} />;
      case "dashboard":
        return <Dashboard userRole={userRole} onNavigate={navigateTo} />;
      case "new-case":
        return <NewCase onNavigate={navigateTo} />;
      case "analysis":
        return activeCaseId ? (
          <CaseAnalysis caseId={activeCaseId} onNavigate={navigateTo} />
        ) : (
          <Dashboard userRole={userRole} onNavigate={navigateTo} />
        );
      case "chat":
        return <ChatAssistant />;
      case "admin":
        return <AdminDashboard />;
      default:
        return <Landing onNavigate={navigateTo} />;
    }
  };

  if (view === "landing" || view === "login") {
    return renderView();
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      {/* Navigation Top Header */}
      <header className="bg-primary-500 text-white shadow-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setView("dashboard")}>
            <Scale className="h-7 w-7 text-gold-400" />
            <span className="text-xl font-bold tracking-wide">Nyaya<span className="text-gold-400">AI</span></span>
          </div>

          <div className="flex items-center space-x-6 text-sm">
            <button 
              onClick={() => setView("dashboard")} 
              className={`hover:text-gold-100 flex items-center space-x-1.5 transition-colors ${view === "dashboard" ? "text-gold-400 font-bold" : ""}`}
            >
              <LayoutDashboard className="h-4 w-4" />
              <span>Dashboard</span>
            </button>
            <button 
              onClick={() => setView("chat")} 
              className={`hover:text-gold-100 flex items-center space-x-1.5 transition-colors ${view === "chat" ? "text-gold-400 font-bold" : ""}`}
            >
              <MessageSquare className="h-4 w-4" />
              <span>Research Chat</span>
            </button>
            {userRole === "Admin" && (
              <button 
                onClick={() => setView("admin")} 
                className={`hover:text-gold-100 flex items-center space-x-1.5 transition-colors ${view === "admin" ? "text-gold-400 font-bold" : ""}`}
              >
                <Database className="h-4 w-4" />
                <span>Admin Console</span>
              </button>
            )}
            
            {/* Profile Dropdown or simple logout */}
            <div className="flex items-center space-x-3 border-l border-white/20 pl-6">
              <span className="text-slate-200 text-xs hidden md:inline">
                Welcome, <span className="font-semibold text-white">{username}</span>
              </span>
              <button 
                onClick={handleLogout}
                className="bg-red-600 hover:bg-red-700 text-white text-xs font-bold px-3 py-1.5 rounded-lg flex items-center space-x-1 shadow"
              >
                <LogOut className="h-3.5 w-3.5" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Screen Layout Container */}
      <main className="flex-1 bg-slate-50">
        {renderView()}
      </main>

      {/* Global Safety Alert Sticky Disclaimer */}
      <footer className="bg-slate-100 border-t border-slate-200 py-4 flex-shrink-0">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-4 text-[10px] text-slate-500 leading-snug">
          <div className="flex items-start space-x-2.5 max-w-3xl">
            <AlertTriangle className="h-5 w-5 text-gold-500 flex-shrink-0 mt-0.5" />
            <span>
              <strong>NyayaAI Disclaimer:</strong> AI-assisted educational research tool only. It does not provide legal advice, does not replace a qualified lawyer and cannot guarantee the outcome of any legal proceeding. Users must verify details with current official legislative gazettes.
            </span>
          </div>
          <div className="text-right flex-shrink-0 font-semibold text-primary-500">
            NyayaAI Project © 2026
          </div>
        </div>
      </footer>
    </div>
  );
}
