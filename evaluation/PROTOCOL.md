# Evaluation protocol

The fixed test set contains 30 questions over the original 98 policy records. The first six are development examples; the remaining 24 are evaluation questions. The full table is a descriptive comparison across all 30, explicitly including development items, not a pristine held-out performance claim. Questions and expectations were AI-assisted, not independently authored by the lecturer. Review expectations before final submission and disclose changes.

## Controls

Both LLM methods use the same provider, model, system instruction, temperature and structured answer format. Full-context sends all policy records. Vector retrieval uses learned embeddings for each whole policy (title, text, category and department metadata), stored as a reusable flat vector index; cosine similarity selects five policies. A flat exact index is appropriate to 98 documents and avoids an unnecessary database service. It is a genuine embedding index, not a keyword-vector proxy. Title hashes identify policies independently of row order; the index additionally checks the database hash and record order.

The keyword baseline uses deterministic BM25-style scoring over title (weighted twice) and policy text, up to three matches above 45% of the best score. It returns exact extracts and does not generate a synthesized answer. No hand-coded answer for a benchmark question is used. Hyperparameters are fixed before LLM evaluation. Every benchmark run writes a new timestamped directory; method order rotates across questions. There are no silent fallbacks from a failed LLM to rules.

## Measures

- Response time: wall-clock duration around retrieval, API calls and answer validation; excludes database loading and one-time index construction. Network delay is included. One measured run per question; do not interpret tiny differences as statistically meaningful.
- Token use: provider-reported prompt, output, thinking and total generation tokens. Query embedding tokens are separate. Index preparation time and embedding tokens are separate. `null` means the API did not report usage, not zero. These are token counts, not billed cost.
- Policy recall: fraction of expected policies present in the answer citations. Average over questions with expected sources and successful results; report errors separately. Retrieval of distractors or a high recall does not prove answer correctness.
- Unsupported answers: fraction of reviewed successful answers containing at least one substantive statement not supported by the full policy database. Missing conditions and wrong statements count as errors in correctness; unsupported invented conditions, numbers and permissions count as unsupported claims. Justified abstention does not.
- Correctness: substantive review against the expected answer, including relevant source, key conditions and appropriate acknowledgement of missing information. Store separately from unsupported claims.
- Citation check: policy ID exists in supplied context and quote is an exact substring of its text. This flags malformed evidence but is NOT a hallucination detector. The benchmark keeps invalid answers visible and flagged; Slack suppresses an answer whose citation check fails.

Rules-only extracts receive a deterministic source-integrity check (all returned statements are exact database text); the baseline's zero unsupported additions does not imply it answers the question correctly. Generated answers need a human/substantive review. Reviews identify the exact answer hash, so a review of an older output cannot silently apply to a new run. Failed requests are reported separately and never counted as correct abstentions or zero-token successful answers.

Do not generalize a zero count from 30 questions to a zero population hallucination rate. Before deciding the preferred approach, examine missed policies, wrong synthesis, unsupported details, ambiguous questions and total cost/latency. For this small database, full context is a provisional design preference only.
