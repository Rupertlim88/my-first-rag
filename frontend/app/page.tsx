import RAG from "@/components/rag";

export default function Home() {
  // Optional: You can pass initial messages, API URL, and topN here
  // For a fresh start, we'll use empty initial messages
  return (
    <div className="min-h-screen bg-white">
      <RAG
        apiUrl={process.env.NEXT_PUBLIC_API_URL || "https://firstragapp.rupertlim.com"}
        topN={3}
        initialMessages={[]}
      />
    </div>
  );
}
