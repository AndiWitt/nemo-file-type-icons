#!/bin/bash
set -e

DEST="$HOME/.local/share/nemo-python/extensions/"

mkdir -p "$DEST"
cp file-type-icons.py "$DEST"

echo "Extension installed to $DEST"
echo "Now restart Nemo: nemo -q && nemo &"
