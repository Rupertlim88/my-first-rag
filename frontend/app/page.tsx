import RAG from "@/components/rag";

export default function Home() {
  // Optional: You can pass initial messages, API URL, and topN here
  // For a fresh start, we'll use empty initial messages
  // Normalize API URL by removing trailing slashes to prevent double slashes
  const apiUrl = (process.env.NEXT_PUBLIC_API_URL || "https://firstragapp.rupertlim.com").replace(/\/+$/, "");
  
  return (
    <div className="min-h-screen bg-white">
      <RAG
        apiUrl={apiUrl}
        topN={3}
        initialMessages={[]}
      />
    </div>
  );
}
