import React from "react";
import Link from "next/link";
import { TransactionClassifier } from "../components/TransactionClassifier";
import { LpAiAnalyzer } from "../components/LpAiAnalyzer";
import { NftClassifier } from "../components/NftClassifier";
import { TaxReportSummary } from "../components/TaxReportSummary";
import { DashboardWidgets } from "../components/DashboardWidgets";
import { TransactionSearch } from "../components/TransactionSearch";
import { DefiProtocolClassifier } from "../components/DefiProtocolClassifier";

/**
 * Main dashboard landing page for Crypto Tax App
 */
export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-base-100">
      <h1 className="text-4xl font-bold mb-8 text-primary">Crypto Tax App</h1>
      <main className="max-w-3xl mx-auto py-8">
        <DashboardWidgets />
        <TransactionSearch />
        <DefiProtocolClassifier />
        <TransactionClassifier />
        <LpAiAnalyzer />
        <NftClassifier />
        <TaxReportSummary />
      </main>
      <footer className="w-full flex justify-center mt-8 mb-4">
        <Link
          href="/disclaimer"
          className="text-xs text-base-content opacity-70 hover:underline hover:text-warning"
          aria-label="Legal Disclaimer"
        >
          Legal Disclaimer
        </Link>
      </footer>
    </div>
  );
}
