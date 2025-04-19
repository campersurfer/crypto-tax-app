import React, { useState } from "react";
import anime from "animejs";

interface NftClassificationResult {
  action: string;
  collection: string;
  type: string;
  explanation: string;
  error?: string;
  raw?: string;
}

export const NftClassifier: React.FC = () => {
  const [transactions, setTransactions] = useState<any[]>([]);
  const [results, setResults] = useState<NftClassificationResult[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    setError(null);
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      setIsLoading(true);
      anime({ targets: "#nft-ai-loader", rotate: 360, loop: true, duration: 1200 });
      const text = await file.text();
      const txs = JSON.parse(text);
      setTransactions(txs);
      await classifyNfts(txs);
    } catch (err: any) {
      setError("Failed to classify NFT transactions. Please check your file format.");
    } finally {
      setIsLoading(false);
      anime.remove("#nft-ai-loader");
    }
  };

  const classifyNfts = async (txs: any[]) => {
    try {
      const response = await fetch("/api/ai/classify_nft_transactions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transactions: txs, task_complexity: "simple" }),
      });
      const data = await response.json();
      setResults(data.results || []);
    } catch (err: any) {
      setError("Failed to classify NFT transactions with AI.");
    }
  };

  return (
    <div className="p-4 bg-base-200 rounded shadow mt-8">
      <h2 className="text-xl font-bold mb-2">AI NFT Transaction Classifier</h2>
      <input
        type="file"
        accept="application/json"
        className="file-input file-input-bordered mb-4"
        onChange={handleFileUpload}
      />
      {isLoading && (
        <div id="nft-ai-loader" className="w-8 h-8 mx-auto my-4 border-4 border-accent border-t-transparent rounded-full animate-spin"></div>
      )}
      {error && <div className="text-error mb-2">{error}</div>}
      {results.length > 0 && (
        <div className="overflow-x-auto">
          <table className="table w-full">
            <thead>
              <tr>
                <th>#</th>
                <th>Action</th>
                <th>Collection</th>
                <th>Type</th>
                <th>Explanation</th>
              </tr>
            </thead>
            <tbody>
              {results.map((r, i) => (
                <tr key={i}>
                  <td>{i + 1}</td>
                  <td>{r.action}</td>
                  <td>{r.collection}</td>
                  <td>{r.type}</td>
                  <td>{r.explanation || r.error || r.raw}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
