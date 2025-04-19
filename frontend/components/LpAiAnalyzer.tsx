import React, { useState } from "react";
import anime from "animejs";

interface LpTransaction {
  id: string;
  [key: string]: unknown;
}

interface LpAiResult {
  action: string;
  tokens: string[];
  tax_summary: string;
}

export const LpAiAnalyzer: React.FC = () => {
  const [walletAddress, setWalletAddress] = useState<string>("");
  const [lpTransactions, setLpTransactions] = useState<LpTransaction[]>([]);
  const [results, setResults] = useState<LpAiResult[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    setError(null);
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      setIsLoading(true);
      anime({ targets: "#lp-ai-loader", rotate: 360, loop: true, duration: 1200 });
      const text = await file.text();
      const txs = JSON.parse(text);
      setLpTransactions(txs);
      await analyzeAndSetResults(txs);
    } catch (err: any) {
      setError("Failed to analyze LP transactions. Please check your file format.");
    } finally {
      setIsLoading(false);
      anime.remove("#lp-ai-loader");
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
      anime({ targets: "#lp-ai-loader", rotate: 360, loop: true, duration: 1200 });
      // Fetch transactions for the address
      const resp = await fetch("/api/wallet/fetch_transactions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ address: walletAddress, chain: "eth" }),
      });
      const data = await resp.json();
      if (!data.transactions) throw new Error("No transactions found for this address.");
      setLpTransactions(data.transactions);
      await analyzeAndSetResults(data.transactions);
    } catch (err: any) {
      setError("Failed to fetch or analyze LP transactions for this address.");
    } finally {
      setIsLoading(false);
      anime.remove("#lp-ai-loader");
    }
  };

  const analyzeAndSetResults = async (txs: LpTransaction[]) => {
    const response = await fetch("/api/lp/ai/analyze_lp", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ lp_transactions: txs, task_complexity: "simple" }),
    });
    const data = await response.json();
    setResults(data.results || []);
  };

  return (
    <div className="p-4 bg-base-200 rounded shadow mt-8">
      <h2 className="text-xl font-bold mb-2">AI LP Transaction Analyzer</h2>
      <form className="mb-4 flex items-center gap-2" onSubmit={handleAddressSubmit}>
        <input
          type="text"
          placeholder="Paste wallet address (ETH, etc)"
          className="input input-bordered w-72"
          value={walletAddress}
          onChange={e => setWalletAddress(e.target.value)}
        />
        <button type="submit" className="btn btn-secondary">Analyze</button>
      </form>
      <div className="mb-2 text-center text-xs text-base-content">or upload an LP transaction JSON file:</div>
      <input
        type="file"
        accept="application/json"
        className="file-input file-input-bordered mb-4"
        onChange={handleFileUpload}
      />
      {isLoading && (
        <div id="lp-ai-loader" className="w-8 h-8 mx-auto my-4 border-4 border-secondary border-t-transparent rounded-full animate-spin"></div>
      )}
      {error && <div className="text-error mb-2">{error}</div>}
      {results.length > 0 && (
        <div className="overflow-x-auto">
          <table className="table w-full">
            <thead>
              <tr>
                <th>#</th>
                <th>Action</th>
                <th>Tokens</th>
                <th>Tax Summary</th>
              </tr>
            </thead>
            <tbody>
              {results.map((r, i) => (
                <tr key={i}>
                  <td>{i + 1}</td>
                  <td>{r.action}</td>
                  <td>{r.tokens.join(", ")}</td>
                  <td>{r.tax_summary}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
