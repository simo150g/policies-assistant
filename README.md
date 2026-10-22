# Policy Lab — Company Policy Assistant

Simon Svenning Raff · SDU, AI in Accounting and Business · Autumn 2026

Compares deterministic keyword search, a full-context LLM without a vector index, and the same LLM with vector retrieval over the 98 supplied company policies. Includes a local Slack bot.

**Current status: implementation prepared; submission incomplete.** The rules method has real measurements. Live Gemini runs, substantive LLM answer review, Slack workspace/channel, lecturer invitation and a real Slack screenshot still require account setup. The comparison is explicitly provisional. No simulated results are presented as evidence.

- Website: https://simo150g.github.io/policies-assistant/ (deployment status in `submission-status.json`)
- Source: https://github.com/simo150g/policies-assistant
- Required exactly two-paragraph comparison: [COMPARISON.md](COMPARISON.md)
- Setup and completion steps: [SETUP.md](SETUP.md)
- Requirement-by-requirement mapping: [REQUIREMENTS.md](REQUIREMENTS.md)
- Evaluation definitions: [evaluation/PROTOCOL.md](evaluation/PROTOCOL.md)

## Run locally

Python 3.9+ is sufficient for search, the web app, evaluation, and direct Gemini REST calls. Only Slack requires an additional dependency.

```sh
python3 -m unittest discover -s tests -v
python3 -m policy_assistant serve
```

Open http://127.0.0.1:8765. The local page can call all three methods once the API key and index are configured. GitHub Pages displays recorded benchmark answers and offers browser-local keyword search; it cannot host a Python backend. Secrets are never put into the static page.

```sh
cp .env.example .env
# Edit .env locally; never commit it.
python3 -m policy_assistant index
python3 -m policy_assistant benchmark
python3 -m pip install -r requirements.txt
python3 -m policy_assistant slack
```

The Slack bot defaults to the full-context LLM provisionally. Set `SLACK_METHOD=rules` or `vector` to switch. It responds only to mentions in the explicitly configured coursework channel, and sends only the question and synthetic policy records to the LLM, not user IDs or channel history. Do not submit personal or sensitive information in questions.

## Structure

- `policy_assistant/`: shared answer methods, index, evaluation, local server and Slack bot.
- `docs/`: public GitHub Pages site and recorded results.
- `evaluation/questions.json`: 30 fixed questions and expected evidence, including six development questions.
- `evaluation/runs/`: immutable raw run outputs with timestamps and hashes.
- `evaluation/reviews.json`: substantive reviewer decisions bound to each exact answer hash.
- `slack-manifest.json`: minimal bot permissions and mention event subscription.
- `local/` and `.env`: private setup and embedding index, ignored by Git.

## Time, cost and AI use

AI assistance was used for implementation, test design, documentation and website design. Exact Codex token counts and per-task subscription cost are not available. Student time is not yet recorded and must not be described as zero. Provider-reported policy-answer tokens are recorded in each run; one-time embedding preparation is separate. Unknown token counts remain null. Do not claim a free tier or zero API cost without checking the actual account. Course-specific declaration rules must be checked on MitSDU before submission.

## Technical references

- [Gemini text generation REST API](https://ai.google.dev/api/generate-content)
- [Gemini embeddings API](https://ai.google.dev/api/embeddings)
- [Gemini models](https://ai.google.dev/gemini-api/docs/models)
- [Slack Socket Mode for Python](https://docs.slack.dev/tools/bolt-python/concepts/socket-mode/)

Model availability and free quotas depend on the account. The configured model is explicit and can be changed; both LLM methods must use the same model for a fair run. Live provider compatibility is unverified until the first real call succeeds.
