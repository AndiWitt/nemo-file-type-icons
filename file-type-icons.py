"""
Nemo extension: Sets custom-icon for Google Workspace, PDF, and video files.

Works for:
  - rclone mounts (files have extensions like .docx, .xlsx, .pptx but are 0 bytes)
  - GVFS Google Drive mount (native Google files without extension, identified by MIME type)
  - Local files with matching extensions or MIME types

Icons are read from: ~/.local/share/nemo-file-type-icons/icons/
Install with: bash install.sh
"""

import os
from gi.repository import GObject, Gio, Nemo

ICON_DIR = os.path.expanduser("~/.local/share/nemo-file-type-icons/icons")

# Extension mapping (for rclone mount and local files)
EXT_MAP = {
    ".docx": f"file://{ICON_DIR}/docs_datei_symbol.png",
    ".doc":  f"file://{ICON_DIR}/docs_datei_symbol.png",
    ".xlsx": f"file://{ICON_DIR}/sheets_datei_symbol.png",
    ".xls":  f"file://{ICON_DIR}/sheets_datei_symbol.png",
    ".pptx": f"file://{ICON_DIR}/slides_datei_symbol.png",
    ".ppt":  f"file://{ICON_DIR}/slides_datei_symbol.png",
    ".pdf":  f"file://{ICON_DIR}/pdf_datei_symbol_1.png",
    ".mp4":  f"file://{ICON_DIR}/video_datei_symbol.png",
    ".mkv":  f"file://{ICON_DIR}/video_datei_symbol.png",
    ".avi":  f"file://{ICON_DIR}/video_datei_symbol.png",
    ".mov":  f"file://{ICON_DIR}/video_datei_symbol.png",
    ".wmv":  f"file://{ICON_DIR}/video_datei_symbol.png",
    ".flv":  f"file://{ICON_DIR}/video_datei_symbol.png",
    ".webm": f"file://{ICON_DIR}/video_datei_symbol.png",
    ".mpeg": f"file://{ICON_DIR}/video_datei_symbol.png",
    ".mpg":  f"file://{ICON_DIR}/video_datei_symbol.png",
    ".m4v":  f"file://{ICON_DIR}/video_datei_symbol.png",
    ".3gp":  f"file://{ICON_DIR}/video_datei_symbol.png",
    ".ts":   f"file://{ICON_DIR}/video_datei_symbol.png",
    ".mts":  f"file://{ICON_DIR}/video_datei_symbol.png",
}

# MIME type mapping (for GVFS Google Drive mount and system-wide)
MIME_MAP = {
    "application/vnd.google-apps.document":     f"file://{ICON_DIR}/docs_datei_symbol.png",
    "application/vnd.google-apps.spreadsheet":  f"file://{ICON_DIR}/sheets_datei_symbol.png",
    "application/vnd.google-apps.presentation": f"file://{ICON_DIR}/slides_datei_symbol.png",
    "application/pdf":                           f"file://{ICON_DIR}/pdf_datei_symbol_1.png",
    "video/mp4":        f"file://{ICON_DIR}/video_datei_symbol.png",
    "video/x-matroska": f"file://{ICON_DIR}/video_datei_symbol.png",
    "video/x-msvideo":  f"file://{ICON_DIR}/video_datei_symbol.png",
    "video/quicktime":  f"file://{ICON_DIR}/video_datei_symbol.png",
    "video/x-ms-wmv":   f"file://{ICON_DIR}/video_datei_symbol.png",
    "video/x-flv":      f"file://{ICON_DIR}/video_datei_symbol.png",
    "video/webm":       f"file://{ICON_DIR}/video_datei_symbol.png",
    "video/mpeg":       f"file://{ICON_DIR}/video_datei_symbol.png",
    "video/x-m4v":      f"file://{ICON_DIR}/video_datei_symbol.png",
    "video/3gpp":       f"file://{ICON_DIR}/video_datei_symbol.png",
    "video/mp2t":       f"file://{ICON_DIR}/video_datei_symbol.png",
}


class FileTypeIconProvider(GObject.GObject, Nemo.InfoProvider):

    def update_file_info(self, file):
        icon_uri = None

        # 1. Check MIME type first (handles GVFS files without extension)
        mime = file.get_mime_type()
        if mime:
            icon_uri = MIME_MAP.get(mime)
            # Catch all video/* MIME types not explicitly listed
            if not icon_uri and mime.startswith("video/"):
                icon_uri = f"file://{ICON_DIR}/video_datei_symbol.png"

        # 2. Check file extension as fallback (rclone mount and local files)
        if not icon_uri:
            name = file.get_name()
            display = file.get_string_attribute("standard::display-name")
            if display and "." in display:
                name = display
            ext = os.path.splitext(name.lower())[1]
            icon_uri = EXT_MAP.get(ext)

        if not icon_uri:
            return Nemo.OperationResult.COMPLETE

        # Already set correctly → nothing to do (performance)
        if file.get_string_attribute("metadata::custom-icon") == icon_uri:
            return Nemo.OperationResult.COMPLETE

        try:
            gfile = Gio.File.new_for_uri(file.get_uri())
            info = Gio.FileInfo()
            info.set_attribute_string("metadata::custom-icon", icon_uri)
            gfile.set_attributes_from_info(info, Gio.FileQueryInfoFlags.NONE, None)
            file.invalidate_extension_info()
        except Exception:
            pass

        return Nemo.OperationResult.COMPLETE
