import React, { useState } from "react";
import anime from "animejs";

export const DefiProtocolClassifier: React.FC = () => {
  const [transactions, setTransactions] = useState<any[]>([]);
  const [results, setResults] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    setError(null);
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      setIsLoading(true);
      anime({ targets: "#defi-classifier-loader", rotate: 360, loop: true, duration: 1200 });
      const text = await file.text();
      const txs = JSON.parse(text);
      setTransactions(txs);
      await classifyDefiProtocols(txs);
    } catch (err: any) {
      setError("Failed to load transactions. Please check your file format.");
    } finally {
      setIsLoading(false);
      anime.remove("#defi-classifier-loader");
    }
  };

  const classifyDefiProtocols = async (txs: any[]) => {
    try {
      const response = await fetch("/api/ai/classify_defi_protocols", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transactions: txs }),
      });
      const data = await response.json();
      setResults(data.results || []);
    } catch (err: any) {
      setError("Failed to classify DeFi protocols with AI.");
    }
  };

  return (
    <div className="p-4 bg-base-200 rounded shadow mt-8">
      <h2 className="text-xl font-bold mb-2">AI DeFi Protocol Classifier</h2>
      <input
        type="file"
        accept="application/json"
        className="file-input file-input-bordered mb-4"
        onChange={handleFileUpload}
      />
      {isLoading && (
        <div id="defi-classifier-loader" className="w-8 h-8 mx-auto my-4 border-4 border-info border-t-transparent rounded-full animate-spin"></div>
      )}
      {error && <div className="text-error mb-2">{error}</div>}
      {results.length > 0 && (
        <div className="bg-base-100 p-4 rounded shadow text-base-content whitespace-pre-line mt-4">
          <h3 className="font-semibold mb-2">Protocol Breakdown</h3>
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
