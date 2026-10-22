# Assignment compliance map

The original brief is preserved in ASSIGNMENT.md. This checklist is implementation status, not a claim that pending account-dependent tasks are complete.

| Required outcome | Implementation / evidence | Status |
|---|---|---|
| Deployed comparison website | `docs/`, GitHub Pages | Published and verified 22 October 2026 |
| Rules-based search | `core.py:rules_answer`, 30 recorded benchmark answers | Measured |
| LLM without vector index | `core.py:llm_answer` full-context mode | 21 successful live answers; 9 service errors disclosed |
| LLM with vector index | Learned policy embeddings, persisted vectors, cosine retrieval, same LLM | Real 98-policy index; 21 successful live answers; 9 service errors disclosed |
| Each answer and relevant policy | Three side-by-side cards with source quotes | 72 successful results measured; 18 service errors disclosed |
| Response time and token use | Actual elapsed timers, API usage metadata, separate embedding usage | 72 successful results measured; 18 service errors disclosed |
| Tendency to provide unsupported answers | Hash-bound answer reviews and per-method rate | All 72 successful answers reviewed with hashes; student verification pending |
| Exactly two comparison paragraphs, maximum two tables | `COMPARISON.md`; website interpretation section; one website table | Exactly two evidence-based paragraphs; one website table |
| Slack bot answers and identifies policy | `slack_bot.py` and app manifest | Implemented; real connection pending |
| Separate identifiable workspace and channel | Setup names in `SETUP.md` | User setup pending |
| Invitation to raz@sdu.dk | Record sent invitation and timestamp | Pending |
| Website and source-code links | `submission-status.json` | Both public links verified |
| Screenshot of bot call and response in channel | `evidence/slack-demo.png` must be real | Pending |

Course workspace rules additionally require a public GitHub repo and GitHub Pages, correct student commit identity, time/cost records and an AI-use declaration. No paid service or permanent bot hosting is necessary in the design.
