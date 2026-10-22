# Verification — 22 October 2026

- 14 automated checks passed: data integrity, required approval conditions, abstention on zero keyword overlap, exact extracts across all 30 questions, invalid input, invalid citation suppression, separation of citation checks from factual review, vector ranking and stale-index rejection, shared model settings, incomplete API response handling, unknown token accounting, two-paragraph format, and safe configuration parsing.
- Website JavaScript syntax check passed.
- Local browser verified recorded results, live keyword search, explicit missing-key errors, and database filtering.
- GitHub Pages reported a successful build and the live public page loaded. Public keyword search returned Password Policy with the 90-day condition.
- Implementation commits use Simon Svenning Raff <siraf22@student.sdu.dk>. GitHub generated the repository's initial README commit before the local implementation commits.
- Live Gemini requests and learned vector-index creation have NOT been verified: no API key is configured. Automated tests use isolated fakes only to verify code behavior; these are not published as measured LLM results.
- Slack has NOT been connected or demonstrated. No invitation has been sent and no Slack screenshot exists.

Baseline: 30 successful rules runs; median measured Python response 0.6455 ms; mean expected-policy recall 85.19%; 0 LLM tokens. All extracts match the database exactly, but that does not establish answer correctness.
