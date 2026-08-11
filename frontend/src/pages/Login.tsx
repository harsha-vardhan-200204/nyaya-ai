import React, { useState } from "react";
import { Scale, Lock, User, Mail, ShieldAlert } from "lucide-react";
import { api } from "../services/api";

interface LoginProps {
  onLoginSuccess: (role: string, username: string) => void;
  onNavigate: (view: string) => void;
}

export default function Login({ onLoginSuccess, onNavigate }: LoginProps) {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("Client");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      if (isRegister) {
        await api.auth.register({ username, email, password, role });
        setSuccess("Registration successful! You can now log in.");
        setIsRegister(false);
        setPassword("");
      } else {
        const data = await api.auth.login({ username, password });
        onLoginSuccess(data.role, data.username);
      }
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center p-6 font-sans">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl border border-slate-100 overflow-hidden">
        {/* Banner header */}
        <div className="bg-primary-500 text-white p-8 text-center relative">
          <div className="flex justify-center mb-2">
            <Scale className="h-10 w-10 text-gold-400" />
          </div>
          <h2 className="text-2xl font-bold">NyayaAI Legal System</h2>
          <p className="text-slate-300 text-xs mt-1">AI-Powered Legal Case Analysis & Decision Support</p>
        </div>

        {/* Form area */}
        <div className="p-8">
          <form onSubmit={handleSubmit} className="space-y-5">
            {error && (
              <div className="bg-red-50 text-red-600 text-xs p-3 rounded-lg border border-red-200 flex items-start space-x-2">
                <ShieldAlert className="h-4 w-4 mt-0.5 flex-shrink-0" />
                <span>{error}</span>
              </div>
            )}
            
            {success && (
              <div className="bg-green-50 text-green-700 text-xs p-3 rounded-lg border border-green-200">
                {success}
              </div>
            )}

            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-500">Username</label>
              <div className="relative">
                <User className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                <input
                  type="text"
                  required
                  placeholder="Enter username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:border-primary-500 transition-colors"
                />
              </div>
            </div>

            {isRegister && (
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-500">Email Address</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                  <input
                    type="email"
                    required
                    placeholder="Enter email address"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:border-primary-500 transition-colors"
                  />
                </div>
              </div>
            )}

            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-500">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                <input
                  type="password"
                  required
                  placeholder="Enter password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:border-primary-500 transition-colors"
                />
              </div>
            </div>

            {isRegister && (
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-500">Role Assign</label>
                <select
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:border-primary-500 transition-colors"
                >
                  <option value="Client">Client (Submit disputes & reports)</option>
                  <option value="Lawyer">Lawyer / Researcher (Case Search & Analysis)</option>
                  <option value="Admin">Administrator (Manage models & users)</option>
                </select>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-primary-500 hover:bg-primary-600 text-white font-bold py-2.5 rounded-lg text-sm shadow-md transition-all disabled:opacity-50"
            >
              {loading ? "Processing..." : isRegister ? "Register Account" : "Sign In"}
            </button>
          </form>

          {/* Toggle register */}
          <div className="mt-6 text-center text-xs text-slate-500">
            {isRegister ? (
              <span>
                Already have an account?{" "}
                <button
                  onClick={() => {
                    setIsRegister(false);
                    setError("");
                  }}
                  className="text-primary-500 font-bold hover:underline"
                >
                  Sign In
                </button>
              </span>
            ) : (
              <span>
                Don't have an account?{" "}
                <button
                  onClick={() => {
                    setIsRegister(true);
                    setError("");
                  }}
                  className="text-primary-500 font-bold hover:underline"
                >
                  Register Here
                </button>
              </span>
            )}
            <div className="mt-3">
              <button onClick={() => onNavigate("landing")} className="text-slate-400 hover:underline">
                Back to Home Page
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
