const API_BASE = "http://localhost:8000/api";

// Helper to get token
const getAuthHeaders = () => {
  const token = localStorage.getItem("nyaya_token");
  return token ? { "Authorization": `Bearer ${token}` } : {};
};

export const api = {
  // Authentication
  auth: {
    async register(payload: any) {
      const resp = await fetch(`${API_BASE}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!resp.ok) throw new Error((await resp.json()).detail || "Registration failed");
      return resp.json();
    },
    
    async login(payload: any) {
      const resp = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!resp.ok) throw new Error((await resp.json()).detail || "Login failed");
      const data = await resp.json();
      localStorage.setItem("nyaya_token", data.access_token);
      localStorage.setItem("nyaya_role", data.role);
      localStorage.setItem("nyaya_username", data.username);
      return data;
    },
    
    logout() {
      localStorage.removeItem("nyaya_token");
      localStorage.removeItem("nyaya_role");
      localStorage.removeItem("nyaya_username");
    },
    
    async me() {
      const resp = await fetch(`${API_BASE}/auth/me`, {
        headers: { ...getAuthHeaders() }
      });
      if (!resp.ok) throw new Error("Auth verification failed");
      return resp.json();
    }
  },
  
  // Client Cases
  cases: {
    async list() {
      const resp = await fetch(`${API_BASE}/cases`, {
        headers: { ...getAuthHeaders() }
      });
      if (!resp.ok) throw new Error("Failed to fetch cases");
      return resp.json();
    },
    
    async get(id: number) {
      const resp = await fetch(`${API_BASE}/cases/${id}`, {
        headers: { ...getAuthHeaders() }
      });
      if (!resp.ok) throw new Error("Failed to fetch case details");
      return resp.json();
    },
    
    async create(payload: any) {
      const resp = await fetch(`${API_BASE}/cases`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...getAuthHeaders()
        },
        body: JSON.stringify(payload)
      });
      if (!resp.ok) throw new Error("Failed to submit case");
      return resp.json();
    },
    
    async analyze(id: number) {
      const resp = await fetch(`${API_BASE}/cases/${id}/analyze`, {
        method: "POST",
        headers: { ...getAuthHeaders() }
      });
      if (!resp.ok) throw new Error("AI Case Analysis pipeline execution failed");
      return resp.json();
    },
    
    async counterfactual(payload: any) {
      const resp = await fetch(`${API_BASE}/cases/counterfactual`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!resp.ok) throw new Error("Factual simulation recalculation failed");
      return resp.json();
    },
    
    getReportUrl(id: number) {
      const token = localStorage.getItem("nyaya_token") || "";
      return `${API_BASE}/cases/${id}/report?token=${encodeURIComponent(token)}`;
    }
  },
  
  // Legal Database
  legal: {
    async listActs() {
      const resp = await fetch(`${API_BASE}/legal/acts`, {
        headers: { ...getAuthHeaders() }
      });
      return resp.json();
    },
    
    async listSections(domain?: string) {
      const url = domain ? `${API_BASE}/legal/sections?domain=${encodeURIComponent(domain)}` : `${API_BASE}/legal/sections`;
      const resp = await fetch(url, {
        headers: { ...getAuthHeaders() }
      });
      return resp.json();
    },
    
    async searchJudgments(filters: any = {}) {
      const params = new URLSearchParams();
      if (filters.court) params.append("court", filters.court);
      if (filters.state) params.append("state", filters.state);
      if (filters.outcome) params.append("outcome", filters.outcome);
      if (filters.case_type) params.append("case_type", filters.case_type);
      if (filters.q) params.append("q", filters.q);
      
      const resp = await fetch(`${API_BASE}/legal/judgments?${params.toString()}`, {
        headers: { ...getAuthHeaders() }
      });
      return resp.json();
    },
    
    async getJudgment(id: number) {
      const resp = await fetch(`${API_BASE}/legal/judgments/${id}`, {
        headers: { ...getAuthHeaders() }
      });
      return resp.json();
    },
    
    async listSavedCases() {
      const resp = await fetch(`${API_BASE}/legal/saved-cases`, {
        headers: { ...getAuthHeaders() }
      });
      return resp.json();
    },
    
    async saveCase(judgmentId: number) {
      const resp = await fetch(`${API_BASE}/legal/saved-cases`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...getAuthHeaders()
        },
        body: JSON.stringify({ judgment_id: judgmentId })
      });
      return resp.json();
    },
    
    async unsaveCase(id: number) {
      const resp = await fetch(`${API_BASE}/legal/saved-cases/${id}`, {
        method: "DELETE",
        headers: { ...getAuthHeaders() }
      });
      return resp.json();
    }
  },
  
  // Chat Bot
  chat: {
    async ask(message: string) {
      const resp = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...getAuthHeaders()
        },
        body: JSON.stringify({ message })
      });
      if (!resp.ok) throw new Error("Chatbot failed to respond");
      return resp.json();
    },
    
    async getHistory() {
      const resp = await fetch(`${API_BASE}/chat/history`, {
        headers: { ...getAuthHeaders() }
      });
      return resp.json();
    }
  },
  
  // Administrator Dashboard
  admin: {
    async getAnalytics() {
      const resp = await fetch(`${API_BASE}/admin/analytics`, {
        headers: { ...getAuthHeaders() }
      });
      if (!resp.ok) throw new Error("Failed to fetch admin stats");
      return resp.json();
    },
    
    async retrain() {
      const resp = await fetch(`${API_BASE}/admin/retrain`, {
        method: "POST",
        headers: { ...getAuthHeaders() }
      });
      return resp.json();
    },
    
    async getModelMetrics() {
      const resp = await fetch(`${API_BASE}/admin/model-metrics`, {
        headers: { ...getAuthHeaders() }
      });
      return resp.json();
    },
    
    async listUsers() {
      const resp = await fetch(`${API_BASE}/admin/users`, {
        headers: { ...getAuthHeaders() }
      });
      return resp.json();
    },
    
    async ingestDocument(payload: any) {
      const resp = await fetch(`${API_BASE}/admin/documents`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...getAuthHeaders()
        },
        body: JSON.stringify(payload)
      });
      return resp.json();
    }
  }
};
