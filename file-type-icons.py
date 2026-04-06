"""
Nemo extension: Sets custom-icon for Google Workspace, PDF, and video files.

Works for:
  - rclone mount (files have extensions like .docx/.xlsx)
  - GVFS Google Drive mount (native Google files without extension, identified by MIME type)

Installation:
  cp file-type-icons.py ~/.local/share/nemo-python/extensions/
  nemo -q && nemo &

Icon directory: adjust ICON_DIR below if your Pictures folder has a different name.
"""

import os
from gi.repository import GObject, Gio, Nemo

ICON_DIR = os.path.expanduser("~/Bilder/Icons")  # Change to ~/Pictures/Icons if needed

# Extension mapping (for rclone mount and local files)
EXT_MAP = {
    ".docx": f"file://{ICON_DIR}/google-docs.png",
    ".doc":  f"file://{ICON_DIR}/google-docs.png",
    ".xlsx": f"file://{ICON_DIR}/google-sheets.png",
    ".xls":  f"file://{ICON_DIR}/google-sheets.png",
    ".pptx": f"file://{ICON_DIR}/google-slides.png",
    ".ppt":  f"file://{ICON_DIR}/google-slides.png",
    ".pdf":  f"file://{ICON_DIR}/pdf-icon.png",
    ".mp4":  f"file://{ICON_DIR}/video_datei_logo.png",
    ".mkv":  f"file://{ICON_DIR}/video_datei_logo.png",
    ".avi":  f"file://{ICON_DIR}/video_datei_logo.png",
    ".mov":  f"file://{ICON_DIR}/video_datei_logo.png",
    ".wmv":  f"file://{ICON_DIR}/video_datei_logo.png",
    ".flv":  f"file://{ICON_DIR}/video_datei_logo.png",
    ".webm": f"file://{ICON_DIR}/video_datei_logo.png",
    ".mpeg": f"file://{ICON_DIR}/video_datei_logo.png",
    ".mpg":  f"file://{ICON_DIR}/video_datei_logo.png",
    ".m4v":  f"file://{ICON_DIR}/video_datei_logo.png",
    ".3gp":  f"file://{ICON_DIR}/video_datei_logo.png",
    ".ts":   f"file://{ICON_DIR}/video_datei_logo.png",
    ".mts":  f"file://{ICON_DIR}/video_datei_logo.png",
}

# MIME type mapping (for GVFS Google Drive mount and system-wide)
MIME_MAP = {
    "application/vnd.google-apps.document":     f"file://{ICON_DIR}/google-docs.png",
    "application/vnd.google-apps.spreadsheet":  f"file://{ICON_DIR}/google-sheets.png",
    "application/vnd.google-apps.presentation": f"file://{ICON_DIR}/google-slides.png",
    "application/pdf":                           f"file://{ICON_DIR}/pdf-icon.png",
    "video/mp4":          f"file://{ICON_DIR}/video_datei_logo.png",
    "video/x-matroska":   f"file://{ICON_DIR}/video_datei_logo.png",
    "video/x-msvideo":    f"file://{ICON_DIR}/video_datei_logo.png",
    "video/quicktime":    f"file://{ICON_DIR}/video_datei_logo.png",
    "video/x-ms-wmv":     f"file://{ICON_DIR}/video_datei_logo.png",
    "video/x-flv":        f"file://{ICON_DIR}/video_datei_logo.png",
    "video/webm":         f"file://{ICON_DIR}/video_datei_logo.png",
    "video/mpeg":         f"file://{ICON_DIR}/video_datei_logo.png",
    "video/x-m4v":        f"file://{ICON_DIR}/video_datei_logo.png",
    "video/3gpp":         f"file://{ICON_DIR}/video_datei_logo.png",
    "video/mp2t":         f"file://{ICON_DIR}/video_datei_logo.png",
}

class FileTypeIconProvider(GObject.GObject, Nemo.InfoProvider):

    def update_file_info(self, file):
        icon_uri = None

        # 1. Check MIME type first (handles GVFS files without extension)
        mime = file.get_mime_type()
        if mime:
            icon_uri = MIME_MAP.get(mime)

        # 2. Check file extension as fallback (rclone mount)
        if not icon_uri:
            name = file.get_name()
            display = file.get_string_attribute("standard::display-name")
            if display and '.' in display:
                name = display
            ext = os.path.splitext(name.lower())[1]
            icon_uri = EXT_MAP.get(ext)

        if not icon_uri:
            return Nemo.OperationResult.COMPLETE

        # Already set correctly? → do nothing (performance)
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
