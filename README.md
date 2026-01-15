# AgnoTest — AI Contract Review System (Streamlit + Telegram + WhatsApp)

Multi-agent contract review project built on **Agno AgentOS**.

It ships with:
- a **Streamlit** UI to upload a contract and generate a structured review
- a **FastAPI** app that can receive **Telegram webhooks** (including document uploads)
- an (optional) **WhatsApp** interface (depends on provider setup)

## What it does

The main team is `review_contract`, which combines 3 agents:
- **Structure agent**: assesses/improves contract structure
- **Legal agent**: legal framework checks
- **Negotiation agent**: negotiation opportunities

The team outputs a **decision-ready report** with traceability (quotes clauses).

## Requirements

- **Python**: 3.11+
- Package manager:
  - recommended: **Poetry**
  - or: regular `pip` (advanced users)

## Setup

### 1) Install dependencies

With Poetry:

```bash
poetry install
```

If Poetry isn’t installed:

```bash
pip install poetry
poetry install
```

### 2) Create `.env`

Copy `env.example` to `.env` (project root) and fill in values.

```bash
copy env.example .env
```

Minimum required for Streamlit:
- `OPENAI_API_KEY`

Minimum required for Telegram:
- `TELEGRAM_BOT_TOKEN`

Optional:
- `TELEGRAM_CHAT_ID` (fallback chat id if incoming update doesn’t contain one)
- `DEFAULT_MODEL_PROVIDER` (default: `openai`)
- `DEFAULT_MODEL_ID` (default: `gpt-4o-mini`)

## Run — Streamlit UI (recommended)

Runs a local UI to upload a contract (`pdf`, `docx`, `txt`) and get a report.

```bash
poetry run streamlit run app_streamlit.py
```

Notes:
- The UI reads `OPENAI_API_KEY` from `.env` (or you can paste it in the sidebar).

## Run — Telegram webhook (FastAPI)

### 1) Start the FastAPI server

```bash
poetry run uvicorn app_telegram:app --reload --port 8000
```

Your webhook route is:
- `POST /telegram/webhook`

### 2) Expose localhost with ngrok

In another terminal:

```bash
ngrok http 8000
```

ngrok dashboard:
- `http://127.0.0.1:4040`

### 3) Set the Telegram webhook URL

Once ngrok shows a public forwarding URL (example: `https://xxxx.ngrok-free.dev`),
set Telegram webhook to:

`https://<YOUR_NGROK_HOST>/telegram/webhook`

You can set it via Telegram Bot API:

`https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://<YOUR_NGROK_HOST>/telegram/webhook`

Verify:

`https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo`

### 4) Test

- Send a message (or a document) to your bot in Telegram
- In ngrok dashboard (`127.0.0.1:4040`) you should see a request to `/telegram/webhook`

## Run — WhatsApp (optional)

There is a starter entrypoint:

```bash
poetry run python app_whatsapp.py
```

This relies on `agno.os.interfaces.whatsapp.Whatsapp` and typically requires additional
provider credentials/config (Meta / WhatsApp Cloud). If you want, tell me which WhatsApp
provider you’re using and I’ll document the exact env vars + webhook steps.

## Project structure

Key files:
- `app_streamlit.py`: Streamlit UI entrypoint
- `app_telegram.py`: FastAPI/AgentOS entrypoint + Telegram interface
- `src/AgnoTest/interfaces/telegram.py`: Telegram webhook handler (`/telegram/webhook`)
- `src/AgnoTest/teams/review_contract.py`: team orchestration + report format
- `src/AgnoTest/agents/*`: individual agents
- `src/AgnoTest/tools/get_document.py`: extracts text from PDFs

## Troubleshooting

- **No Telegram requests arriving**:
  - confirm webhook is set to `https://<ngrok-host>/telegram/webhook`
  - check ngrok dashboard (`127.0.0.1:4040`) for incoming requests
  - run `getWebhookInfo` and inspect `last_error_message`
- **“poetry not recognized” (Windows)**:
  - install with `pip install poetry` then re-run `poetry install`