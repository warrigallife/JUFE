#!/bin/bash
cd "$(dirname "$0")"
echo "Starting JUFE..."
echo

if [ -x /usr/local/bin/python3 ]; then
    PYTHON="/usr/local/bin/python3"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON="$(command -v python3)"
else
    echo "ERROR: Python 3 could not be found."
    read -n 1 -s -r -p "Press any key to close..."
    exit 1
fi

"$PYTHON" "jufe_original_launcher.py"
STATUS=$?

if [ $STATUS -ne 0 ]; then
    echo
    echo "JUFE stopped with error code $STATUS."
    echo "Read the error above."
    read -n 1 -s -r -p "Press any key to close..."
fi
