#!/bin/zsh
cd "$(dirname "$0")" || exit 1
if [[ -x .venv/bin/python ]]; then
  .venv/bin/python -m policy_assistant serve
else
  python3 -m policy_assistant serve
fi
