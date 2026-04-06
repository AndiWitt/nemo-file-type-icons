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
echo "Note: This extension stored custom icon paths in GIO metadata"
echo "(~/.local/share/gvfs-metadata/). These entries are harmless —"
echo "Nemo will fall back to default icons automatically."
echo "To manually clear a custom icon from a specific file:"
echo "  gio set -t unset '/path/to/file' metadata::custom-icon"
