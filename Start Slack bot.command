#!/bin/zsh
cd "$(dirname "$0")" || exit 1
if [[ -x .venv/bin/python ]]; then
  .venv/bin/python -m policy_assistant slack
else
  print 'The local Slack environment is not installed yet. See SETUP.md.'
fi
read '?Press Return to close this window.'
