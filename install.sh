#!/usr/bin/env bash
set -euo pipefail

EXT_NAME="file-type-icons.py"
EXT_DEST="$HOME/.local/share/nemo-python/extensions"
ICON_DEST="$HOME/.local/share/nemo-file-type-icons/icons"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing nemo-file-type-icons..."

# Check that Nemo Python bindings are available
# (package is 'nemo-python' on Debian/Ubuntu/Mint, 'python-nemo' on Arch)
if dpkg -s nemo-python &>/dev/null 2>&1; then
    : # found via dpkg
elif python3 -c "from gi.repository import Nemo" &>/dev/null 2>&1; then
    : # found via GI typelib (non-Debian systems)
else
    echo ""
    echo "Error: Nemo Python bindings not found."
    echo "Install with:"
    echo "  Debian/Ubuntu/Mint:  sudo apt install nemo-python"
    echo "  Arch:                sudo pacman -S python-nemo"
    echo ""
    exit 1
fi

# Check that icons are present
if ! ls "$SCRIPT_DIR"/icons/*.png &>/dev/null; then
    echo ""
    echo "Error: No PNG icons found in $SCRIPT_DIR/icons/"
    echo "Please clone the full repository."
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
