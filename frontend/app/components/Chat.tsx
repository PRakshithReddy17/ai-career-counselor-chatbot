"use client";

import { useState } from "react";

type Message = {
  role: "user" | "bot";
  content: string;
};

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userInput = input;
    setInput("");

    // Add user message
    setMessages((prev) => [...prev, { role: "user", content: userInput }]);

    setLoading(true);

    try {
      const res = await fetch(
        "https://ai-career-counselor-chatbot.onrender.com/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message: userInput }),
        }
      );

      const data = await res.json();

      // Add bot reply
      setMessages((prev) => [
        ...prev,
        { role: "bot", content: data.reply || "No response" },
      ]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { role: "bot", content: "Error connecting to server." },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="flex flex-col h-screen bg-black text-white">
      {/* Header */}
      <div className="p-4 border-b border-gray-700 text-lg font-semibold">
        🤖 AI Career Counselor
      </div>

      {/* Chat messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`max-w-[70%] p-3 rounded-lg ${
              msg.role === "user"
                ? "bg-blue-600 ml-auto text-right"
                : "bg-gray-800 mr-auto"
            }`}
          >
            {msg.content}
          </div>
        ))}

        {loading && (
          <div className="text-gray-400 text-sm">AI is typing...</div>
        )}
      </div>

      {/* Input box */}
      <div className="p-4 border-t border-gray-700 flex gap-2">
        <input
          type="text"
          className="flex-1 p-2 rounded bg-gray-800 outline-none"
          placeholder="Ask about your career..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button
          onClick={sendMessage}
          className="bg-blue-600 px-4 py-2 rounded hover:bg-blue-700"
        >
          Send
        </button>
      </div>
    </div>
  );
}