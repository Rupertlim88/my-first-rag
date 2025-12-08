"use client";

import { useState, useCallback } from "react";
import Chatbox, { Message } from "./chatbox";

interface RAGProps {
  apiUrl?: string;
  topN?: number;
  initialMessages?: Message[];
}

export default function RAG({
  apiUrl = "https://firstragapp.rupertlim.com",
  topN = 3,
  initialMessages = [],
}: RAGProps) {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const formatTimestamp = () => {
    const now = new Date();
    return `${now.getHours().toString().padStart(2, "0")}:${now.getMinutes().toString().padStart(2, "0")}:${now.getSeconds().toString().padStart(2, "0")}`;
  };

  const handleSubmit = useCallback(async () => {
    const query = inputValue.trim();
    if (!query || isLoading) return;

    // Add user message immediately
    const userMessage: Message = {
      role: "user",
      content: query,
      timestamp: formatTimestamp(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);
    setError(null);

    try {
      // Call the backend /ask endpoint
      const response = await fetch(`${apiUrl}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: query,
          top_n: topN,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail || `HTTP error! status: ${response.status}`
        );
      }

      const data = await response.json();

      // Add agent response
      const agentMessage: Message = {
        role: "agent",
        content: data.answer || "No response received.",
        timestamp: formatTimestamp(),
      };

      setMessages((prev) => [...prev, agentMessage]);
    } catch (err) {
      const errorMessage =
        err instanceof Error
          ? err.message
          : "An error occurred while generating an answer.";

      setError(errorMessage);

      // Add error message as agent response
      const errorAgentMessage: Message = {
        role: "agent",
        content: `ERROR: ${errorMessage}`,
        timestamp: formatTimestamp(),
      };

      setMessages((prev) => [...prev, errorAgentMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [inputValue, isLoading, apiUrl, topN]);

  const handleInputChange = useCallback((value: string) => {
    setInputValue(value);
    setError(null);
  }, []);

  return (
    <Chatbox
      messages={messages}
      showTypingIndicator={isLoading}
      inputValue={inputValue}
      onInputChange={handleInputChange}
      onSubmit={handleSubmit}
      disabled={isLoading}
    />
  );
}

