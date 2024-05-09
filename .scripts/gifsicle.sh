#!/usr/bin/env bash
set -uo pipefail

_=$(command -v gifsicle > /dev/null)
EXIT="$?"
set -e

if [[ "$EXIT" == "0" ]]; then
  gifsicle -O3 -i --batch "${@:1}"
else
  echo "Skipping gifsicle as it is not installed"
fi
