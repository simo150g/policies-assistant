# Verification — 22 October 2026

- 16 automated checks passed, including source integrity, exact citations, invalid-answer suppression, vector retrieval, shared generation settings, missing token metadata, timeout handling, and resuming without repeating successful answers.
- Real Gemini 3.5 Flash-Lite generation verified using the saved local key. Gemini Embedding 001 produced 98 stored 3,072-dimensional vectors. The key and index are excluded from Git.
- All 90 benchmark pairs attempted: rules 30 successes, full context 21 successes/9 errors, vector 21 successes/9 errors. All 72 successful outputs have substantive AI-assisted reviews bound to their hashes. Student verification is pending.
- Successful outputs survive retries unchanged. Archived failures and interruptions remain visible. Mixed request concurrency and timeouts prevent a controlled latency ranking. Different successful subsets prevent a direct accuracy-equivalence claim.
- Exactly two comparison paragraphs and one comparison table. Unknown embedding/failed-request token usage and billed cost are not reported as zero.
- Implementation commits use Simon Svenning Raff <siraf22@student.sdu.dk>. GitHub generated the initial repository README commit.
- Slack has NOT been connected or demonstrated. No lecturer invitation or real Slack screenshot has been recorded. Student hours and final AI-use declaration still need completion.
