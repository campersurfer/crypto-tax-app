# Crypto Tax Software App: Project Rules & Steps

## Project Overview
- Build a US crypto tax software app, copying and improving all features from Koinly and Awaken.
- Must handle all blockchains, NFTs, and Bitcoin ordinals.
- Compliance with US tax law is required.

## Feature Requirements: Koinly & Awaken
- Automatic wallet and exchange sync (API, CSV, xPub, etc.)
- Support for all major blockchains, tokens, NFTs, ordinals
- NFT, DeFi, and LP (liquidity pool) transaction parsing (staking, farming, lending, borrowing)
- Cost basis methods: FIFO, LIFO, HIFO, Spec ID
- Realized/unrealized gains, income, margin, and derivatives tracking
- IRS Form 8949, Schedule D, TurboTax export, international forms
- Tax-loss harvesting tools
- Wash sale, airdrop, mining, staking, rewards, and fork handling
- Portfolio tracking dashboard
- Multi-year tax reporting and carryover
- Transaction classification and manual editing
- Audit trail and downloadable reports (PDF, CSV)
- Alerts for missing/incomplete data
- Multi-user and accountant access
- Comprehensive error handling and input validation
- Privacy, security, and GDPR/CCPA compliance

## Architecture & Tech Stack
- Backend: FastAPI (Python 3.10 recommended for compatibility)
- Frontend: Next.js (TypeScript), Tailwind CSS, DaisyUI, anime.js for UI/UX
- Use requirements.txt (no version pinning) for Python dependencies
- Use package.json for JS dependencies
- Modular, extensible, and secure codebase

## Security & Compliance
- All sensitive data handled securely (env vars, HTTPS, input validation)
- US-specific tax logic and reporting
- User data privacy and auditability

## UI/UX
- Responsive, modern UI (Tailwind, DaisyUI)
- Loading animations for API calls (anime.js)
- Accessible and easy to use

## Deployment & Hosting
- Frontend deployed to Netlify with continuous deployment
  - Netlify internal ID: 01JS88PMHJH2HV7HYNCX0KM9DA
  - Live URL: https://crypto-tax-app.netlify.app
  - GitHub Repo: campersurfer/crypto-tax-app (branch main)

## Workflow & Documentation
- Update this file after every user request/step
- All new features, architectural changes, or design decisions must be reflected here
- Follow all coding, security, and documentation best practices as outlined in global rules

## AI Usage Policy
- Use AI for all feasible features (transaction classification, LP analysis, error explanations, report summaries, etc.)
- When an API key is required, always prefer the OpenRouter API key
- Prioritize free models (such as DeepSeek, Gemini) and shuffle models as needed
- Paid models should only be used when a task requires more advanced, up-to-date, or complex responses

### Implementation Details
- Backend AI service (`app/services/ai_service.py`) uses OpenRouter API, selects free models by default, and shuffles between DeepSeek and Gemini for simple tasks.
- Complex or advanced tasks use paid models (e.g., GPT-4o, Claude 3 Opus) only when necessary.
- FastAPI endpoint `/ai/classify_transactions` (in `app/routes/ai.py`) provides AI-powered transaction classification, returning type and explanation for each transaction.
- API key is always loaded from environment variables via `os.getenv`.
- All AI calls and errors are logged with `termcolor`.
- AI router is registered in `main.py` with `/ai` prefix.
- Blockchain transaction fetching is performed in `app/utils/fetch_wallet_transactions.py` with multi-chain support:
  - **Ethereum, Base, Arbitrum**: Alchemy API (`ALCHEMY_API_KEY` env var)
  - **Solana**: Helius API (`HELIUS_API_KEY` env var)
  - **Bitcoin**: Blockstream API (no key required)
  - If the required API key is missing or the API fails, the system falls back to mock data. The code is easily extensible for additional chains.
- NFT Classification: The backend provides an AI-powered NFT classification endpoint at `/ai/classify_nft_transactions` (see `app/routes/ai_nft.py`). This uses OpenRouter API and a dedicated service (`app/services/ai_nft_service.py`) to classify transactions as NFT-related (mint, transfer, sale, etc.), identify collection and type, and generate explanations. Output is a list of objects with keys: action, collection, type, explanation.
- Tax Report Summary: The backend provides an AI-powered tax summary endpoint at `/ai/tax_report_summary` (see `app/routes/ai_tax.py`). This uses OpenRouter API and a dedicated service (`app/services/ai_tax_service.py`) to generate a plain-English summary of the user's tax position, including total gains/losses, taxable events, and key actions. The frontend component (`TaxReportSummary.tsx`) allows users to upload transactions and view the generated summary.
- Transaction Search: The backend provides an AI-powered transaction search endpoint at `/ai/search_transactions` (see `app/routes/ai_search.py`). This uses OpenRouter API and a dedicated service (`app/services/ai_search_service.py`) to find and explain transactions matching a natural language query. The frontend component (`TransactionSearch.tsx`) allows users to upload transactions, enter a query, and view AI-selected matches with explanations.
- DeFi Protocol Classification: The backend provides an AI-powered DeFi protocol classification endpoint at `/ai/classify_defi_protocols` (see `app/routes/ai_defi.py`). This uses OpenRouter API and a dedicated service (`app/services/ai_defi_service.py`) to classify each transaction by protocol (e.g., Uniswap, Aave), action, and explanation. The frontend component (`DefiProtocolClassifier.tsx`) allows users to upload transactions and view protocol/action breakdowns.
- TransactionSearch.tsx: Frontend component for AI-powered transaction search. Users upload transactions and enter a natural language query. Results are displayed with AI explanations. Integrated into the dashboard after DashboardWidgets.
- DefiProtocolClassifier.tsx: Frontend component for DeFi protocol classification. Users upload transactions and view protocol/action breakdowns. Integrated into the dashboard after TransactionSearch.

## Legal Disclaimer

This application and its AI-powered features are provided for informational purposes only and do not constitute legal, tax, or financial advice. Users should consult a qualified tax professional or legal advisor for guidance specific to their situation. The app's outputs, including all AI-generated summaries and classifications, are not guaranteed to be accurate or sufficient for compliance purposes.

## Development Roadmap

### Phase 1: Core Infrastructure
- [x] Backend directory structure created (`app/routes`, `app/utils`)
- [x] Modular FastAPI routing implemented (health, auth endpoints)
- [x] Health check endpoint (`/health`) and placeholder auth endpoints (`/auth/login`, `/auth/register`)
- [x] Utility for environment variable access (`app/utils/env.py`)
- [x] termcolor used for informative prints at each step
- [x] Next.js frontend scaffolding (directory, package.json, Tailwind CSS, DaisyUI, anime.js, initial pages/styles)
- [ ] CI/CD setup (pending)
- [ ] Implement real user authentication (pending)
- [ ] Secure API key & environment variable management (pending)

### Phase 2: Data Ingestion & Wallet Sync
- [x] `/wallet/import` endpoint for all major chains (placeholder logic)
- [x] `/exchange/import` endpoint for API, CSV, xPub (placeholder logic, utf-8 file read)
- [x] `/transactions/import` endpoint for NFT, DeFi, ordinals (placeholder logic, utf-8 file read)
- [ ] Transaction deduplication and normalization (pending)
- [ ] Error handling for missing/invalid data (pending)

### Phase 3: Transaction Parsing & Classification
- [x] `/transactions/classify` endpoint for parsing/classification (placeholder logic)
- [x] `/transactions/manual_edit` endpoint for manual editing (placeholder logic)
- [x] `/audit/trail` endpoint for audit trail (placeholder logic)
- [ ] NFT, DeFi, and LP (liquidity pool) transaction logic (pending)
- [ ] Full classification logic (pending)

### Phase 4: Tax Calculation Engine
- [x] `/tax/calculate` endpoint for tax calculation (placeholder logic)
- [ ] Cost basis methods (pending)
- [ ] Realized/unrealized gains, income, margin, derivatives (pending)
- [ ] Multi-year/carryover logic (pending)
- [ ] Wash sale, loss harvesting, compliance (pending)

### Phase 5: Reporting & Export
- [x] `/report/generate` endpoint for report generation (placeholder logic)
- [ ] IRS Form 8949, Schedule D, TurboTax, CSV/PDF export (pending)
- [ ] Portfolio dashboard (pending)
- [ ] Alerts for missing/incomplete data (pending)

### Phase 6: Advanced Features & Integrations
- Multi-user and accountant access
- International tax forms (if desired)
- Privacy controls, GDPR/CCPA compliance
- Automated test suite and monitoring

### Phase 7: UI/UX Polish
- Responsive, modern UI (Tailwind, DaisyUI)
- Loading animations (anime.js)
- Accessibility improvements
- Comprehensive documentation and onboarding

---
_Last updated: 2025-04-19_

## Architecture & Tech Stack
- Backend: FastAPI (Python 3.10 recommended for compatibility)
- Frontend: Next.js (TypeScript), Tailwind CSS, DaisyUI, anime.js for UI/UX
- Use requirements.txt (no version pinning) for Python dependencies
- Use package.json for JS dependencies
- Modular, extensible, and secure codebase

## Core Features (MVP)
- User authentication (OAuth, email/password)
- Secure API for uploading wallet addresses, CSVs, API keys
- Auto-import transactions from all major chains (ETH, BTC, Solana, Polygon, etc.)
- NFT, DeFi, and ordinals transaction support
- Cost basis calculation (FIFO, LIFO, Specific ID)
- Realized/unrealized gain/loss reports
- IRS Form 8949 and Schedule D generation
- Wash sale, airdrop, staking, mining, and fork handling
- Tax-loss harvesting suggestions
- Multi-year tax history
- Audit trail and exportable reports (PDF, CSV)
- Comprehensive error handling and input validation

## Security & Compliance
- All sensitive data handled securely (env vars, HTTPS, input validation)
- US-specific tax logic and reporting
- User data privacy and auditability

## UI/UX
- Responsive, modern UI (Tailwind, DaisyUI)
- Loading animations for API calls (anime.js)
- Accessible and easy to use

## Workflow & Documentation
- Update this file after every user request/step
- All new features, architectural changes, or design decisions must be reflected here
- Follow all coding, security, and documentation best practices as outlined in global rules

## AI Usage Policy
- Use AI for all feasible features (transaction classification, LP analysis, error explanations, report summaries, etc.)
- When an API key is required, always prefer the OpenRouter API key
- Prioritize free models (such as DeepSeek, Gemini) and shuffle models as needed
- Paid models should only be used when a task requires more advanced, up-to-date, or complex responses

### Implementation Details
- Backend AI service (`app/services/ai_service.py`) uses OpenRouter API, selects free models by default, and shuffles between DeepSeek and Gemini for simple tasks.
- Complex or advanced tasks use paid models (e.g., GPT-4o, Claude 3 Opus) only when necessary.
- FastAPI endpoint `/ai/classify_transactions` (in `app/routes/ai.py`) provides AI-powered transaction classification, returning type and explanation for each transaction.
- API key is always loaded from environment variables via `os.getenv`.
- All AI calls and errors are logged with `termcolor`.
- AI router is registered in `main.py` with `/ai` prefix.
- Blockchain transaction fetching is performed in `app/utils/fetch_wallet_transactions.py` with multi-chain support:
  - **Ethereum, Base, Arbitrum**: Alchemy API (`ALCHEMY_API_KEY` env var)
  - **Solana**: Helius API (`HELIUS_API_KEY` env var)
  - **Bitcoin**: Blockstream API (no key required)
  - If the required API key is missing or the API fails, the system falls back to mock data. The code is easily extensible for additional chains.

## Development Roadmap

### Phase 1: Core Infrastructure
- [x] Backend directory structure created (`app/routes`, `app/utils`)
- [x] Modular FastAPI routing implemented (health, auth endpoints)
- [x] Health check endpoint (`/health`) and placeholder auth endpoints (`/auth/login`, `/auth/register`)
- [x] Utility for environment variable access (`app/utils/env.py`)
- [x] termcolor used for informative prints at each step
- [x] Next.js frontend scaffolding (directory, package.json, Tailwind CSS, DaisyUI, anime.js, initial pages/styles)
- [ ] CI/CD setup (pending)
- [ ] Implement real user authentication (pending)
- [ ] Secure API key & environment variable management (pending)

### Phase 2: Data Ingestion & Wallet Sync
- [x] `/wallet/import` endpoint for all major chains (placeholder logic)
- [x] `/exchange/import` endpoint for API, CSV, xPub (placeholder logic, utf-8 file read)
- [x] `/transactions/import` endpoint for NFT, DeFi, ordinals (placeholder logic, utf-8 file read)
- [ ] Transaction deduplication and normalization (pending)
- [ ] Error handling for missing/invalid data (pending)

### Phase 3: Transaction Parsing & Classification
- [x] `/transactions/classify` endpoint for parsing/classification (placeholder logic)
- [x] `/transactions/manual_edit` endpoint for manual editing (placeholder logic)
- [x] `/audit/trail` endpoint for audit trail (placeholder logic)
- [ ] NFT, DeFi, and LP (liquidity pool) transaction logic (pending)
- [ ] Full classification logic (pending)

### Phase 4: Tax Calculation Engine
- [x] `/tax/calculate` endpoint for tax calculation (placeholder logic)
- [ ] Cost basis methods (pending)
- [ ] Realized/unrealized gains, income, margin, derivatives (pending)
- [ ] Multi-year/carryover logic (pending)
- [ ] Wash sale, loss harvesting, compliance (pending)

### Phase 5: Reporting & Export
- [x] `/report/generate` endpoint for report generation (placeholder logic)
- [ ] IRS Form 8949, Schedule D, TurboTax, CSV/PDF export (pending)
- [ ] Portfolio dashboard (pending)
- [ ] Alerts for missing/incomplete data (pending)

### Phase 6: Advanced Features & Integrations
- Multi-user and accountant access
- International tax forms (if desired)
- Privacy controls, GDPR/CCPA compliance
- Automated test suite and monitoring

### Phase 7: UI/UX Polish
- Responsive, modern UI (Tailwind, DaisyUI)
- Loading animations (anime.js)
- Accessibility improvements
- Comprehensive documentation and onboarding

---
_Last updated: 2025-04-19_
