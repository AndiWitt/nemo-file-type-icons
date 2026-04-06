#!/usr/bin/env bash
set -euo pipefail

EXT_FILE="$HOME/.local/share/nemo-python/extensions/file-type-icons.py"
ICON_DIR="$HOME/.local/share/nemo-file-type-icons"

echo "Uninstalling nemo-file-type-icons..."

if [ -f "$EXT_FILE" ]; then
    rm "$EXT_FILE"
    echo "  Removed: $EXT_FILE"
else
    echo "  Not found (skipping): $EXT_FILE"
fi

if [ -d "$ICON_DIR" ]; then
    rm -rf "$ICON_DIR"
    echo "  Removed: $ICON_DIR"
else
    echo "  Not found (skipping): $ICON_DIR"
fi

echo ""
echo "Done. Restart Nemo to apply:"
echo "  nemo -q && nemo &"
echo ""
echo "Note: Custom icon assignments stored in GIO metadata"
echo "(~/.local/share/gvfs-metadata/) are not removed."
echo "They are harmless and will simply be ignored once"
echo "the extension is no longer active."
