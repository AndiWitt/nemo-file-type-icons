#!/usr/bin/env bash
set -euo pipefail

EXT_NAME="file-type-icons.py"
EXT_DEST="$HOME/.local/share/nemo-python/extensions"
ICON_DEST="$HOME/.local/share/nemo-file-type-icons/icons"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing nemo-file-type-icons..."

# Check that nemo-python is installed
if ! dpkg -s nemo-python &>/dev/null; then
    echo ""
    echo "Error: nemo-python is not installed."
    echo "Install it first with:"
    echo "  sudo apt install nemo-python"
    echo ""
    exit 1
fi

# Install extension
mkdir -p "$EXT_DEST"
cp "$SCRIPT_DIR/$EXT_NAME" "$EXT_DEST/$EXT_NAME"
echo "  Extension → $EXT_DEST/$EXT_NAME"

# Install icons
mkdir -p "$ICON_DEST"
cp "$SCRIPT_DIR"/icons/*.png "$ICON_DEST/"
echo "  Icons     → $ICON_DEST/"

echo ""
echo "Done. Restart Nemo to activate:"
echo "  nemo -q && nemo &"
