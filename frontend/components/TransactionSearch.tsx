import React, { useState } from "react";
import anime from "animejs";

export const TransactionSearch: React.FC = () => {
  const [transactions, setTransactions] = useState<any[]>([]);
  const [query, setQuery] = useState<string>("");
  const [results, setResults] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    setError(null);
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      setIsLoading(true);
      anime({ targets: "#tx-search-loader", rotate: 360, loop: true, duration: 1200 });
      const text = await file.text();
      const txs = JSON.parse(text);
      setTransactions(txs);
    } catch (err: any) {
      setError("Failed to load transactions. Please check your file format.");
    } finally {
      setIsLoading(false);
      anime.remove("#tx-search-loader");
    }
  };

  const handleSearch = async () => {
    setError(null);
    setIsLoading(true);
    anime({ targets: "#tx-search-loader", rotate: 360, loop: true, duration: 1200 });
    try {
      const response = await fetch("/api/ai/search_transactions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transactions, query }),
      });
      const data = await response.json();
      setResults(data.results || []);
    } catch (err: any) {
      setError("Failed to search transactions with AI.");
    } finally {
      setIsLoading(false);
      anime.remove("#tx-search-loader");
    }
  };

  return (
    <div className="p-4 bg-base-200 rounded shadow mt-8">
      <h2 className="text-xl font-bold mb-2">AI Transaction Search</h2>
      <input
        type="file"
        accept="application/json"
        className="file-input file-input-bordered mb-2"
        onChange={handleFileUpload}
      />
      <input
        type="text"
        className="input input-bordered w-full mb-2"
        placeholder="Search (e.g. show all swaps in 2024)"
        value={query}
        onChange={e => setQuery(e.target.value)}
        disabled={transactions.length === 0}
      />
      <button
        className="btn btn-primary w-full"
        onClick={handleSearch}
        disabled={isLoading || !query || transactions.length === 0}
      >
        Search
      </button>
      {isLoading && (
        <div id="tx-search-loader" className="w-8 h-8 mx-auto my-4 border-4 border-info border-t-transparent rounded-full animate-spin"></div>
      )}
      {error && <div className="text-error mb-2">{error}</div>}
      {results.length > 0 && (
        <div className="bg-base-100 p-4 rounded shadow text-base-content whitespace-pre-line mt-4">
          <h3 className="font-semibold mb-2">Results</h3>
          <ul className="list-disc ml-6">
            {results.map((item, idx) => (
              <li key={idx} className="mb-2">
                <div className="font-mono text-xs">{JSON.stringify(item, null, 2)}</div>
                {item.explanation && <div className="text-sm text-info mt-1">{item.explanation}</div>}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
