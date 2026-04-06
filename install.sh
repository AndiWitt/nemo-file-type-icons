#!/bin/bash
set -e

EXT_DEST="$HOME/.local/share/nemo-python/extensions/"
ICON_DEST="$HOME/.local/share/nemo-file-type-icons/icons/"

mkdir -p "$EXT_DEST"
mkdir -p "$ICON_DEST"

cp file-type-icons.py "$EXT_DEST"
cp icons/*.png "$ICON_DEST"

echo "Extension installed to $EXT_DEST"
echo "Icons installed to $ICON_DEST"
echo ""
echo "Restart Nemo to activate: nemo -q && nemo &"
