import React, { useState } from "react";
import anime from "animejs";

export const TaxReportSummary: React.FC = () => {
  const [transactions, setTransactions] = useState<any[]>([]);
  const [summary, setSummary] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    setError(null);
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      setIsLoading(true);
      anime({ targets: "#tax-summary-loader", rotate: 360, loop: true, duration: 1200 });
      const text = await file.text();
      const txs = JSON.parse(text);
      setTransactions(txs);
      await generateSummary(txs);
    } catch (err: any) {
      setError("Failed to load transactions. Please check your file format.");
    } finally {
      setIsLoading(false);
      anime.remove("#tax-summary-loader");
    }
  };

  const generateSummary = async (txs: any[]) => {
    try {
      const response = await fetch("/api/ai/tax_report_summary", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transactions: txs }),
      });
      const data = await response.json();
      setSummary(data.summary || data.error || "No summary generated.");
    } catch (err: any) {
      setError("Failed to generate tax summary with AI.");
    }
  };

  return (
    <div className="p-4 bg-base-200 rounded shadow mt-8">
      <h2 className="text-xl font-bold mb-2">AI Tax Report Summary</h2>
      <input
        type="file"
        accept="application/json"
        className="file-input file-input-bordered mb-4"
        onChange={handleFileUpload}
      />
      {isLoading && (
        <div id="tax-summary-loader" className="w-8 h-8 mx-auto my-4 border-4 border-info border-t-transparent rounded-full animate-spin"></div>
      )}
      {error && <div className="text-error mb-2">{error}</div>}
      {summary && (
        <div className="bg-base-100 p-4 rounded shadow text-base-content whitespace-pre-line mt-4">
          {summary}
        </div>
      )}
    </div>
  );
};
