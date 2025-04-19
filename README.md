# Crypto Tax Software App

This project is a US-compliant crypto tax software platform supporting all blockchains, NFTs, and ordinals.

## Tech Stack
- Backend: FastAPI (Python 3.10+ recommended)
- Frontend: Next.js (TypeScript), Tailwind CSS, DaisyUI, anime.js

## One-Click Local Setup (Recommended)

1. **Set your API keys as environment variables:**
   - `ALCHEMY_API_KEY` (Ethereum, Base, Arbitrum)
   - `HELIUS_API_KEY` (Solana)
   - `OPENROUTER_API_KEY` (AI features)

2. **Run the automation script:**
   ```sh
   bash dev_setup.sh
   ```
   This will:
   - Create a Python virtual environment (if not present)
   - Install all backend dependencies (`uvicorn`, `fastapi`, `pytest`, etc.)
   - Install all frontend dependencies (`npm install`)
   - Lint, build, and type-check the frontend
   - Run backend tests with pytest

3. **Start the backend:**
   ```sh
   source .venv/bin/activate
   uvicorn main:app --reload
   ```

4. **Start the frontend:**
   ```sh
   cd frontend
   npm run dev
   ```

5. **Visit your app:**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend (API): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Troubleshooting (Mac)
- If you see errors about PEP 668 or 'externally-managed-environment', always use the Python venv provided by `dev_setup.sh`.
- If you add new Python dependencies, activate your venv first: `source .venv/bin/activate`
- For persistent API keys, add them to your `~/.zshrc` and run `source ~/.zshrc`.

---
See `global_rules.md` for architecture, features, and workflow documentation.
