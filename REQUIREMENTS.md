# Assignment compliance map

The original brief is preserved in ASSIGNMENT.md. This checklist is implementation status, not a claim that pending account-dependent tasks are complete.

| Required outcome | Implementation / evidence | Status |
|---|---|---|
| Deployed comparison website | `docs/`, GitHub Pages | Deployment to be verified |
| Rules-based search | `core.py:rules_answer`, 30 recorded benchmark answers | Measured |
| LLM without vector index | `core.py:llm_answer` full-context mode | Implemented; API run pending |
| LLM with vector index | Learned policy embeddings, persisted vectors, cosine retrieval, same LLM | Implemented; real index and API run pending |
| Each answer and relevant policy | Three side-by-side cards with source quotes | Rules measured; LLM pending |
| Response time and token use | Actual elapsed timers, API usage metadata, separate embedding usage | Rules measured; LLM pending |
| Tendency to provide unsupported answers | Hash-bound answer reviews and per-method rate | Source-only baseline verified; LLM review pending |
| Exactly two comparison paragraphs, maximum two tables | `COMPARISON.md`; website interpretation section; one website table | Two paragraphs prepared; conclusion provisional |
| Slack bot answers and identifies policy | `slack_bot.py` and app manifest | Implemented; real connection pending |
| Separate identifiable workspace and channel | Setup names in `SETUP.md` | User setup pending |
| Invitation to raz@sdu.dk | Record sent invitation and timestamp | Pending |
| Website and source-code links | `submission-status.json` | Repository created; website pending |
| Screenshot of bot call and response in channel | `evidence/slack-demo.png` must be real | Pending |

Course workspace rules additionally require a public GitHub repo and GitHub Pages, correct student commit identity, time/cost records and an AI-use declaration. No paid service or permanent bot hosting is necessary in the design.
