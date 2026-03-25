"use client";
import { useState } from "react";

export default function Chat() {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: input }),
      });

      const data = await res.json();

      setMessages([
        ...newMessages,
        { role: "assistant", content: data.reply },
      ]);
    } catch {
      setMessages([
        ...newMessages,
        { role: "assistant", content: "Error 😢" },
      ]);
    }

    setInput("");
    setLoading(false);
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-gray-900 to-black text-white">
      
      {/* Header */}
      <div className="p-4 text-xl font-bold border-b border-gray-700">
        🎓 AI Career Counselor
      </div>

      {/* Chat */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`max-w-xl p-4 rounded-2xl shadow ${
              msg.role === "user"
                ? "bg-blue-600 ml-auto"
                : "bg-gray-800"
            }`}
          >
            {msg.content}
          </div>
        ))}

        {loading && (
          <div className="bg-gray-700 p-3 rounded-xl w-fit">
            Thinking...
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 flex border-t border-gray-700">
        <input
          className="flex-1 p-3 rounded-xl bg-gray-800 outline-none"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about your career..."
        />
        <button
          onClick={sendMessage}
          className="ml-3 px-6 bg-blue-600 rounded-xl hover:bg-blue-700"
        >
          Send
        </button>
      </div>
    </div>
  );
}