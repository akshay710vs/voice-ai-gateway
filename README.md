# Voice AI Gateway

A voice AI system built around an LLM gateway with automatic failover, full observability, and a carrier-free browser voice interface. Built as a hands-on exploration of the infrastructure patterns behind 
production voice AI — model routing, fallback behavior, streaming, and monitoring — ahead of a move into Forward Deployed Engineering.

## What this demonstrates

- **LLM gateway with multi-provider routing and automatic fallback** (LiteLLM), so a single provider outage doesn't break a live conversation
- **Full observability**: Prometheus + Grafana dashboards tracking request volume, p95 latency, and fallback events per model, with a captured live-failure screenshot
- **Streaming responses**: LLM output is chunked by sentence and sent to TTS incrementally, so the system starts speaking before the full reply is generated
- **A real voice interface**: push-to-talk in the browser (mic capture → STT → LLM → TTS → playback), with no telephony carrier, account, or verification required to run or demo it

## Architecture
<img width="735" height="423" alt="image" src="https://github.com/user-attachments/assets/c6a452b4-335d-4a7e-b109-7d1408336fb9" />


## Why a gateway, not a direct API call

A voice call can't tolerate a stalled or down LLM provider — even a few seconds of silence reads as broken. The gateway sits between the app and the model providers and:

- Routes every request through a single nickname (`voice-primary`) regardless of which real provider sits behind it
- Automatically retries against a fallback model if the primary times out, rate-limits, or errors
- Tracks per-request latency and failures, broken out by model, so "healthy" is a measured baseline, not a guess

This mirrors signaling-layer failover patterns (e.g., DRA/PCRF routing and node failover in telecom networks) applied to AI model traffic instead of network nodes.

## What the dashboard shows

A captured live-failure test: the primary model's API key was deliberately broken, traffic and request volume shifted to the fallback model, and the configured 4-second timeout showed up directly in the measured latency increase during the incident.

**[Insert Grafana screenshot here]**

## Design decisions worth noting

- **Fallback trigger is a timeout, not just an error.** Voice has a much lower tolerance for a slow primary than a batch job would — a model that's merely slow needs to be treated the same as one that's down.
- **Sentence-level streaming, not word-level.** Sending single tokens to TTS would sound broken; buffering to sentence boundaries is the right granularity for natural-sounding speech while still starting playback early.
- **A local model (Ollama) is included as a third tier**, representing the "sovereign"/offline routing option relevant to EU data-residency requirements (GDPR, EU AI Act) — a call can be forced onto a fully local model with nothing leaving the network.
- **Browser-based audio instead of telephony.** PSTN testing from India hit real-world blockers (Telnyx has no India numbers for individual developer accounts; Twilio/other CPaaS trials require phone verification and carry per-minute cost). Rather than work around a carrier, the voice interface uses browser microphone capture over plain HTTP — this proves the same STT → gateway → TTS pipeline without needing any telephony account, and the webhook layer (`telnyx_server.py` drafts in this repo) shows the intended shape of a Telnyx Call Control integration for production use.

## What I'd do differently for production

- The Prometheus `/metrics` endpoint currently runs without authentication (`require_auth_for_metrics_endpoint: false`) — fine for local development, but a real deployment needs this locked down since it exposes request volume and cost data.
- Fallback overlap: TTS generation for a sentence currently waits for that sentence's full text before starting; a production system would pipeline TTS generation for sentence N+1 while sentence N is still playing.
- Real telephony integration (Telnyx Call Control, streaming media over WebSocket) is the natural next step once network/account access allows it — the core pipeline here is already provider-agnostic and ready to plug in.

## Project structure

record.py — microphone capture (local testing) \
transcribe.py — Groq Whisper speech-to-text \
ask.py — streaming LLM calls through the LiteLLM gateway \
stream_utils.py — buffers streamed tokens into complete sentences \
speak.py — Deepgram text-to-speech \
voice_loop.py — local mic-to-speaker demo (non-streaming) \
voice_loop_streaming.py — local mic-to-speaker demo (streaming) \
web_server.py — FastAPI server for the browser voice interface \
static/index.html — push-to-talk browser UI \
config.yaml — LiteLLM gateway configuration (models, fallback, routing) \
monitoring/ — Prometheus + Grafana docker-compose setup \


## Running it

**Prerequisites:** Python 3.10+, Docker Desktop, API keys for Groq, Anthropic (or another fallback provider), and Deepgram.

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables
$env:GROQ_API_KEY="..."
$env:ANTHROPIC_API_KEY="..."
$env:DEEPGRAM_API_KEY="..."

# 3. Start the LiteLLM gateway
litellm --config config.yaml --port 4000

# 4. Start monitoring (separate terminal)
cd monitoring
docker compose up -d

# 5. Start the voice server (separate terminal)
uvicorn web_server:app --reload --port 8000
```

Open `http://localhost:8000`, allow microphone access, hold the button, speak, release.

Grafana dashboard: `http://localhost:3000` (default login `admin`/`admin`).

