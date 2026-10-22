# Complete the account setup and final evidence

The code is prepared. Do not submit until `python3 -m policy_assistant check` has no pending requirements and the live links and screenshot have been reviewed.

## 1. Gemini API access

1. Open https://aistudio.google.com/apikey and sign in. Complete any terms or project-creation steps yourself.
2. Create a key for coursework. Check available free quota; enabling billing is not required by this project. If no free access is available, stop and choose another permitted provider rather than silently enabling paid usage.
3. Copy `.env.example` to `.env` and paste the key after `GEMINI_API_KEY=` in that local file. Do not paste it into chat, upload it, or commit it.
4. Confirm the text and embedding model names are available in your account. The suggested text model can be changed in `.env`.
5. Run `python3 -m policy_assistant ask 'How many days may I work remotely?' --method full`.
6. Run `python3 -m policy_assistant index` to embed all 98 policies once. Then run `python3 -m policy_assistant benchmark`. Requests are paced; quota errors are recorded as errors, not invented answers. If quota is exhausted, preserve the run and rerun when quota allows.

## 2. Review measured answers

Open the local site with `python3 -m policy_assistant serve`. Review each LLM answer against the original database and expected answer, not just whether its quote exists. Record decisions in `evaluation/reviews.json` using the exact `result_sha256` shown in `docs/data/results.json`:

```json
[
  {
    "question_id": "q01",
    "method": "full",
    "result_sha256": "COPY_THE_EXACT_HASH_FROM_RESULTS",
    "unsupported": false,
    "answer_correct": true,
    "reviewer": "Simon Svenning Raff",
    "note": "Preserves the three-day limit and manager approval."
  }
]
```

There must be one entry per successful LLM result. Never copy this example as a claim about an unreviewed answer. `unsupported=true` means at least one substantive claim is not supported by the supplied database. A wrong or incomplete answer can still contain no unsupported claim, so assess correctness separately. Change COMPARISON.md to the final evidence-based conclusion, keeping **exactly two paragraphs** and at most two tables (the site uses one). Run `python3 -m policy_assistant export` and publish the updated files.

## 3. Dedicated Slack workspace and channel

1. Create a separate workspace at https://slack.com/get-started named **Simon Svenning Raff — Policies**. Complete sign-in, any verification, and terms yourself.
2. Create the public testing channel **simon-raff-policy-test**.
3. At https://api.slack.com/apps choose **Create New App → From an app manifest**. Select the new workspace and paste `slack-manifest.json`.
4. In **Basic Information → App-Level Tokens**, generate an app-level token with `connections:write`; save it locally as `SLACK_APP_TOKEN` in `.env`.
5. Install the app into the workspace. Review the two bot scopes: `app_mentions:read` and `chat:write`. Save its Bot User OAuth Token as `SLACK_BOT_TOKEN` in `.env`.
6. Open the testing channel details and copy the channel ID into `SLACK_CHANNEL_ID` in `.env`. Invite **Simon Raff Policies** to the channel.
7. Run `python3 -m pip install -r requirements.txt`, then `python3 -m policy_assistant slack`. Keep the process running during the demonstration; permanent hosting is not required.
8. In the testing channel type **@Simon Raff Policies How many days per week may I work remotely?** Open the bot's thread and verify that it identifies **Remote Work Policy**, says **up to three days per week**, and preserves **manager approval**.
9. Capture a real screenshot showing the student-identifiable workspace/channel, the mention question and the bot reply with its policy source. Save it to `evidence/slack-demo.png`. Do not use a mock-up.
10. Invite **raz@sdu.dk** to the workspace and include the testing channel in the invitation. Verify the invitation is shown as sent/pending; acceptance is not required. Record the timestamp and channel URL in `submission-status.json`.

If the bot is unavailable, keep the error and fix setup; do not replace the screenshot with a fabricated conversation. A Slack connector can help manage a workspace but does not replace creating and installing this bot app.

## 4. Publish on GitHub Pages

This repository is separate from the coursework reference folder. Configure the required student identity before commits:

```sh
git config user.name 'Simon Svenning Raff'
git config user.email 'siraf22@student.sdu.dk'
```

Keep it public. In repository **Settings → Pages**, deploy from **main**, folder **/docs**. Verify https://simo150g.github.io/policies-assistant/ without signing in. Updates to recorded results require committing the changed `docs/data/results.json` and any source changes.

## 5. Submission

Record verified links, the Slack screenshot path, the lecturer invitation timestamp, actual student hours, and actual costs in `submission-status.json`. Run `python3 -m policy_assistant check`. The four deliverables are the deployed website link, exactly two comparison paragraphs, the public source repository link, and the Slack screenshot. Read the MitSDU programme's AI-use declaration rules before hand-in.
