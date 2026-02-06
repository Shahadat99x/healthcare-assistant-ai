"use client";

import { useState } from "react";

interface ChatResponse {
  assistant_message: string;
  urgency: "self_care" | "gp" | "urgent" | "emergency";
  safety_flags: string[];
  recommendations: string[];
}

export default function ChatPage() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<
    { role: "user" | "assistant"; content: string; meta?: ChatResponse }[]
  >([]);
  const [loading, setLoading] = useState(false);



  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = input;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);

    const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
    try {
      const res = await fetch(`${apiBase}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg }),
      });
      if (!res.ok) {
        throw new Error(`API Error: ${res.status}`);
      }
      const data: ChatResponse = await res.json();
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.assistant_message,
          meta: data,
        },
      ]);
    } catch (e: any) {
      console.error(e);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `⚠️ Error: ${e.message || "Could not connect to assistant."}` },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const getUrgencyColor = (u?: string) => {
    if (u === "high") return "bg-red-100 text-red-700";
    if (u === "medium") return "bg-yellow-100 text-yellow-700";
    return "bg-green-100 text-green-700";
  };

  return (
    <div className="flex h-screen flex-col bg-white">
      <header className="border-b p-4 flex justify-between items-center bg-gray-50">
        <h1 className="text-xl font-bold text-gray-800">Healthcare Assistant</h1>
        <div className="text-sm text-gray-500">Phase 0 Stub</div>
      </header>

      <main className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`flex flex-col ${
              m.role === "user" ? "items-end" : "items-start"
            }`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-3 ${
                m.role === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-100 text-gray-900"
              }`}
            >
              {m.content}
            </div>

            {m.role === "assistant" && m.meta && (
              <div className="mt-2 text-xs text-gray-500 max-w-[80%] space-y-2">
                {/* Emergency Banner */}
                {m.meta.urgency === "emergency" && (
                    <div className="p-3 bg-red-50 border border-red-200 rounded-md">
                        <p className="text-red-700 font-bold text-sm flex items-center gap-2">
                             🚨 EMERGENCY: Call 112 or go to ER now.
                        </p>
                    </div>
                )}
                
                <div className="flex flex-wrap gap-2">
                   <span className={`px-2 py-0.5 rounded-full font-medium ${getUrgencyColor(m.meta.urgency)}`}>
                    Urgency: {m.meta.urgency}
                  </span>
                  {m.meta.safety_flags?.map((flag, idx) => (
                      <span key={idx} className="px-2 py-0.5 rounded-full font-medium bg-gray-200 text-gray-700">
                          {flag}
                      </span>
                  ))}
                </div>
                {m.meta.recommendations.length > 0 && (
                  <div>
                    <strong>Recommendations:</strong>
                    <ul className="list-disc list-inside">
                      {m.meta.recommendations.map((r, idx) => (
                        <li key={idx}>{r}</li>
                      ))}
                    </ul>
                  </div>
                )}
                <div className="border-t pt-1 mt-1 border-gray-200">
                  <em>Sources (Placeholder for RAG)</em>
                </div>
              </div>
            )}
          </div>
        ))}
        {loading && <div className="text-gray-400 text-sm">Assistant is thinking...</div>}
      </main>

      <footer className="p-4 border-t bg-gray-50">
        <div className="flex gap-2">
          <input
            className="flex-1 rounded-md border border-gray-300 p-2 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Describe your symptoms..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button
            className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
            onClick={sendMessage}
            disabled={loading}
          >
            Send
          </button>
        </div>
      </footer>
    </div>
  );
}
