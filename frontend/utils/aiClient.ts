/**
 * AI API Client for Crypto Tax App
 * Uses fetch to call backend /ai endpoints
 */

export interface ClassifyRequest {
  transactions: unknown[];
  task_complexity?: string;
}

export interface ClassificationResult {
  type: string;
  explanation: string;
}

export async function classifyTransactions(
  req: ClassifyRequest
): Promise<ClassificationResult[]> {
  const response = await fetch("/api/ai/classify_transactions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!response.ok) {
    throw new Error("AI classification failed");
  }
  const data = await response.json();
  return data.results || [];
}
