import React, { useState, useEffect, useRef } from "react";
import { Send, Scale, AlertTriangle, Sparkles, MessageCircle, RefreshCw } from "lucide-react";
import { api } from "../services/api";

export default function ChatAssistant() {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    // Load historical conversations from DB
    const loadHistory = async () => {
      try {
        const history = await api.chat.getHistory();
        if (history.length > 0) {
          setMessages(history);
        } else {
          // Add default welcome message
          setMessages([
            {
              id: 0,
              role: "assistant",
              message: "Welcome to NyayaAI Legal Research Chatbot. I can assist in researching Indian statutory codes, acts, and precedent outcomes. Ask your legal query below.\n\n*Example:* 'What are the consequences of Section 138 cheque dishonour?'",
              timestamp: new Date().toISOString()
            }
          ]);
        }
      } catch (err) {
        console.error("Failed to load chat logs history:", err);
      }
    };
    loadHistory();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    
    const userMsg = {
      id: Date.now(),
      role: "user",
      message: input,
      timestamp: new Date().toISOString()
    };
    
    setMessages((prev) => [...prev, userMsg]);
    const currentInput = input;
    setInput("");
    setLoading(true);
    setError("");

    try {
      const res = await api.chat.ask(currentInput);
      const assistantMsg = {
        id: Date.now() + 1,
        role: "assistant",
        message: res.response,
        source: res.source,
        timestamp: new Date().toISOString()
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      setError("Failed to fetch response. Check backend connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 font-sans space-y-6 flex flex-col h-[85vh]">
      {/* Title */}
      <div className="border-b border-slate-200 pb-3 flex justify-between items-center flex-shrink-0">
        <div>
          <h1 className="text-2xl font-bold text-primary-500 flex items-center space-x-2">
            <MessageCircle className="h-6 w-6 text-gold-500" />
            <span>AI Legal Research Chatbot</span>
          </h1>
          <p className="text-slate-500 text-xs mt-0.5">Explore Indian statutes and judgments interactively</p>
        </div>
      </div>

      {/* Safety Disclaimer Banner */}
      <div className="bg-amber-50 border-l-4 border-amber-500 p-3.5 rounded-r-xl text-[10px] text-amber-800 flex items-center space-x-2 flex-shrink-0">
        <AlertTriangle className="h-4 w-4 text-amber-600 flex-shrink-0" />
        <span>
          Disclaimer: AI research assistant only. Frame queries informatively. Does not replace professional advocate counsel.
        </span>
      </div>

      {/* Conversation Thread */}
      <div className="flex-1 bg-white border border-slate-100 rounded-2xl shadow-inner p-6 overflow-y-auto space-y-4 min-h-[250px]">
        {messages.map((msg, index) => {
          const isUser = msg.role === "user";
          return (
            <div 
              key={msg.id || index} 
              className={`flex ${isUser ? "justify-end" : "justify-start"}`}
            >
              <div 
                className={`max-w-[80%] p-4 rounded-2xl text-sm leading-relaxed border ${
                  isUser 
                    ? "bg-primary-500 text-white border-primary-600 rounded-br-none" 
                    : "bg-slate-50 text-slate-800 border-slate-200/60 rounded-bl-none"
                }`}
              >
                {/* Parse newline to list formatting in basic markdown */}
                <div className="whitespace-pre-line space-y-1">
                  {msg.message}
                </div>
                
                {/* Sources badge */}
                {!isUser && msg.source && (
                  <div className="mt-3 pt-2 border-t border-slate-200/50 flex justify-between items-center text-[9px] text-slate-400 font-bold uppercase tracking-wider">
                    <span>Engine: {msg.source}</span>
                    <span className="text-primary-500">Grounded Source ✅</span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-slate-50 text-slate-400 border border-slate-200 p-4 rounded-2xl rounded-bl-none flex items-center space-x-2 text-xs">
              <RefreshCw className="h-4 w-4 animate-spin text-primary-500" />
              <span>NyayaAI is retrieving context and verifying laws...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Form Submission input */}
      <form onSubmit={handleSend} className="flex items-center space-x-3 flex-shrink-0">
        <input
          type="text"
          disabled={loading}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a legal question... (e.g., 'What is Section 10 of Contract Act?')"
          className="flex-1 px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-primary-500 transition-colors shadow-sm disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="bg-primary-500 hover:bg-primary-600 disabled:opacity-50 text-white font-bold p-3.5 rounded-xl transition-all shadow-md flex-shrink-0"
        >
          <Send className="h-4 w-4" />
        </button>
      </form>
    </div>
  );
}
