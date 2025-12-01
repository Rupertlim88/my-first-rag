"use client";

import { Send, Plane } from "lucide-react";
import { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";

export interface Message {
  role: "user" | "agent";
  content: string;
  timestamp?: string;
}

interface ChatboxProps {
  messages: Message[];
  showTypingIndicator?: boolean;
  inputValue: string;
  onInputChange: (value: string) => void;
  onSubmit: () => void;
  disabled?: boolean;
}

export default function Chatbox({
  messages,
  showTypingIndicator = false,
  inputValue,
  onInputChange,
  onSubmit,
  disabled = false,
}: ChatboxProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, showTypingIndicator]);

  const formatTimestamp = (timestamp?: string) => {
    if (!timestamp) {
      const now = new Date();
      return `${now.getHours().toString().padStart(2, "0")}:${now.getMinutes().toString().padStart(2, "0")}:${now.getSeconds().toString().padStart(2, "0")}`;
    }
    return timestamp;
  };

  return (
    <div className="min-h-screen bg-[#FAFAFA] relative overflow-hidden">
    <section className="py-20 px-6 bg-white border-b-8 border-black">
      <div className="max-w-5xl mx-auto">
        

        {/* Chat interface */}
        <div className="border-8 border-black bg-[#E0E0E0] shadow-[16px_16px_0_rgba(0,0,0,1)] relative">
          {/* Header */}
          <div className="bg-black text-white p-4 flex items-center justify-between border-b-4 border-white">
            <div className="flex items-center gap-2"><Plane className="w-6 h-6" /> <div className="font-bold text-sm">TRIP PLANNER</div></div> 
            <div className="flex gap-2">
              <div className="w-4 h-4 bg-[#D32F2F] border-2 border-white"></div>
              <div className="w-4 h-4 bg-[#FBC02D] border-2 border-white"></div>
              <div className="w-4 h-4 bg-white border-2 border-white"></div>
            </div>
          </div>

          {/* Messages - Scrollable */}
          <div className="p-6 space-y-6 min-h-[400px] max-h-[600px] overflow-y-auto">
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-[400px] text-[#616161] font-bold text-sm">
                NO MESSAGES YET. START A CONVERSATION.
              </div>
            ) : (
              <>
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
                  >
                    <div
                      className={`border-4 border-black p-5 max-w-md shadow-[4px_4px_0_rgba(0,0,0,1)] ${
                        message.role === "user"
                          ? "bg-white"
                          : "bg-[#D32F2F] text-white"
                      }`}
                    >
                      <div
                        className={`text-xs font-bold mb-2 ${
                          message.role === "user"
                            ? "text-[#616161]"
                            : "opacity-90"
                        }`}
                      >
                        {message.role === "user" ? "USER_INPUT" : "SYSTEM_OUTPUT"} //{" "}
                        {formatTimestamp(message.timestamp)}
                      </div>
                      {message.role === "agent" ? (
                        <div className="font-bold text-sm leading-relaxed">
                          <ReactMarkdown
                            components={{
                              p: ({ children }) => <p className="mb-5 last:mb-0 text-white/95">{children}</p>,
                              ul: ({ children }) => <ul className="list-none mb-5 space-y-3 ml-0">{children}</ul>,
                              ol: ({ children }) => <ol className="list-none mb-5 space-y-3 ml-0">{children}</ol>,
                              li: ({ children }) => {
                                // Convert children to string to check content
                                const content = typeof children === 'string' 
                                  ? children 
                                  : Array.isArray(children) 
                                    ? children.map(c => typeof c === 'string' ? c : '').join('')
                                    : String(children);
                                
                                // Check if this is a bullet with practical info (contains "Hours:" or "Location:")
                                const isPracticalInfo = content.includes("Hours:") || content.includes("Location:");
                                
                                return (
                                  <li className={`leading-relaxed mb-2 pl-0 ${isPracticalInfo ? 'text-white/85 text-xs font-normal' : 'text-white/95 font-bold'}`}>
                                    <span className="text-white/70 font-bold mr-2">•</span>
                                    {children}
                                  </li>
                                );
                              },
                              strong: ({ children }) => (
                                <strong className="font-bold text-base text-white block mb-3 mt-5 first:mt-0 leading-tight">
                                  {children}
                                </strong>
                              ),
                              em: ({ children }) => <em className="italic text-white/90">{children}</em>,
                              code: ({ children }) => (
                                <code className="bg-white/20 px-1.5 py-0.5 rounded text-xs font-mono border border-white/30 text-white/90">
                                  {children}
                                </code>
                              ),
                              h1: ({ children }) => (
                                <h1 className="text-base font-bold mb-3 mt-6 first:mt-0 text-white">
                                  {children}
                                </h1>
                              ),
                              h2: ({ children }) => (
                                <h2 className="text-sm font-bold mb-2 mt-5 first:mt-0 text-white">
                                  {children}
                                </h2>
                              ),
                              h3: ({ children }) => (
                                <h3 className="text-sm font-bold mb-1 mt-4 first:mt-0 text-white">
                                  {children}
                                </h3>
                              ),
                              blockquote: ({ children }) => (
                                <blockquote className="border-l-4 border-white/40 pl-3 italic my-3 bg-white/10 py-2 text-white/90">
                                  {children}
                                </blockquote>
                              ),
                              hr: () => <hr className="border-white/20 my-5" />,
                              br: () => <br className="mb-1" />,
                            }}
                          >
                            {message.content}
                          </ReactMarkdown>
                        </div>
                      ) : (
                        <div className="font-bold text-sm whitespace-pre-wrap">
                          {message.content}
                        </div>
                      )}
                    </div>
                  </div>
                ))}

                {/* Typing indicator with wave animation */}
                {showTypingIndicator && (
                  <div className="flex gap-2 items-center text-xs font-bold text-[#616161]">
                    <div className="flex gap-1.5 items-center">
                      <div className="w-2 h-2 bg-[#D32F2F] animate-wave" style={{ animationDelay: "0s" }}></div>
                      <div className="w-2 h-2 bg-[#D32F2F] animate-wave" style={{ animationDelay: "0.2s" }}></div>
                      <div className="w-2 h-2 bg-[#D32F2F] animate-wave" style={{ animationDelay: "0.4s" }}></div>
                    </div>
                    <span>PROCESSING...</span>
                  </div>
                )}

                {/* Scroll anchor */}
                <div ref={messagesEndRef} />
              </>
            )}
          </div>

          {/* Input bar */}
          <div className="border-t-4 border-black bg-white p-4 flex gap-4">
            <input
              type="text"
              placeholder="ENTER YOUR QUERY..."
              value={inputValue}
              onChange={(e) => onInputChange(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !disabled && inputValue.trim()) {
                  onSubmit();
                }
              }}
              disabled={disabled}
              className="flex-1 bg-[#E0E0E0] border-4 border-black px-4 py-3 font-bold text-sm placeholder:text-[#616161] focus:outline-none focus:ring-4 focus:ring-[#D32F2F] disabled:opacity-50 disabled:cursor-not-allowed"
            />
            <button
              onClick={onSubmit}
              disabled={disabled || !inputValue.trim()}
              className="bg-[#D32F2F] text-white p-4 border-4 border-black shadow-[4px_4px_0_rgba(0,0,0,1)] hover:shadow-[6px_6px_0_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:shadow-[4px_4px_0_rgba(0,0,0,1)] disabled:hover:translate-x-0 disabled:hover:translate-y-0"
            >
              <Send className="w-6 h-6" strokeWidth={3} />
            </button>
          </div>
        </div>
      </div>
    </section>
    </div>
  );
}
