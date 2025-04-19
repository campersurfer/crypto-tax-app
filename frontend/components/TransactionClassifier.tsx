import React, { useState } from "react";
import anime from "animejs";

interface Transaction {
  id: string;
  [key: string]: unknown;
}

interface ClassificationResult {
  type: string;
  explanation: string;
}

export const TransactionClassifier: React.FC = () => {
  const [walletAddress, setWalletAddress] = useState<string>("");
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [results, setResults] = useState<ClassificationResult[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    setError(null);
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      setIsLoading(true);
      anime({ targets: "#ai-loader", rotate: 360, loop: true, duration: 1200 });
      const text = await file.text();
      const txs = JSON.parse(text);
      setTransactions(txs);
      await classifyAndSetResults(txs);
    } catch (err: any) {
      setError("Failed to classify transactions. Please check your file format.");
    } finally {
      setIsLoading(false);
      anime.remove("#ai-loader");
    }
  };

  const handleAddressSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!walletAddress) {
      setError("Please enter a wallet address.");
      return;
    }
    try {
      setIsLoading(true);
      anime({ targets: "#ai-loader", rotate: 360, loop: true, duration: 1200 });
      // Fetch transactions for the address
      const resp = await fetch("/api/wallet/fetch_transactions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ address: walletAddress, chain: "eth" }),
      });
      const data = await resp.json();
      if (!data.transactions) throw new Error("No transactions found for this address.");
      setTransactions(data.transactions);
      await classifyAndSetResults(data.transactions);
    } catch (err: any) {
      setError("Failed to fetch or classify transactions for this address.");
    } finally {
      setIsLoading(false);
      anime.remove("#ai-loader");
    }
  };

  const classifyAndSetResults = async (txs: Transaction[]) => {
    const response = await fetch("/api/ai/classify_transactions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ transactions: txs, task_complexity: "simple" }),
    });
    const data = await response.json();
    setResults(data.results || []);
  };

  return (
    <div className="p-4 bg-base-200 rounded shadow">
      <h2 className="text-xl font-bold mb-2">AI Transaction Classifier</h2>
      <form className="mb-4 flex items-center gap-2" onSubmit={handleAddressSubmit}>
        <input
          type="text"
          placeholder="Paste wallet address (ETH, etc)"
          className="input input-bordered w-72"
          value={walletAddress}
          onChange={e => setWalletAddress(e.target.value)}
        />
        <button type="submit" className="btn btn-primary">Analyze</button>
      </form>
      <div className="mb-2 text-center text-xs text-base-content">or upload a transaction JSON file:</div>
      <input
        type="file"
        accept="application/json"
        className="file-input file-input-bordered mb-4"
        onChange={handleFileUpload}
      />
      {isLoading && (
        <div id="ai-loader" className="w-8 h-8 mx-auto my-4 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
      )}
      {error && <div className="text-error mb-2">{error}</div>}
      {results.length > 0 && (
        <div className="overflow-x-auto">
          <table className="table w-full">
            <thead>
              <tr>
                <th>#</th>
                <th>Type</th>
                <th>Explanation</th>
              </tr>
            </thead>
            <tbody>
              {results.map((r, i) => (
                <tr key={i}>
                  <td>{i + 1}</td>
                  <td>{r.type}</td>
                  <td>{r.explanation}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
