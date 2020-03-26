#!/usr/bin/env bash
# A convenience script to call images.py
# -------------------------------------------------------
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 username password collection"
  exit 1
fi

SECONDS=0
pythonFile="/opt/images.py"
python3.6 "$pythonFile" "$@"
exit_code="$?"
ELAPSED="$(($SECONDS / 3600))hrs $(($SECONDS / 60 % 60))min $(($SECONDS % 60))sec"

if [ "$exit_code" -eq 0 ]; then
  echo "Done. $ELAPSED"
else
  NORMAL="\\033[0;39m"
  RED="\\033[1;31m"
  printf "${RED}Something went wrong.${NORMAL}\n"
fi
