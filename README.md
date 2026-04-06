# nemo-file-type-icons

A [Nemo](https://github.com/linuxmint/nemo) Python extension that displays correct custom icons for Google Drive files, PDFs, and videos — fixing the generic white-page icon that appears for 0-byte rclone-mounted Google Workspace files.

## The Problem

When mounting Google Drive with **rclone**, Google Workspace files appear as `.docx`/`.xlsx`/`.pptx` with **0 bytes**. GIO identifies them as `application/x-zerosize`, so Nemo falls back to a generic icon.

The native **GVFS Google Drive mount** (mounted via the Nemo sidebar) shows these files without extensions — only the MIME type is available for identification.

This extension solves both cases transparently with a single lightweight Nemo Python plugin — no manual icon assignment needed.

## Requirements

- Linux Mint or any Cinnamon desktop with **Nemo**
- `nemo-python` package:
  ```bash
  sudo apt install nemo-python
  ```

> **rclone users:** Your mount must support extended attributes (the default).
> If you use `--no-xattrs` or a read-only mount, custom icons cannot be written.

## Installation

```bash
git clone https://github.com/AndiWitt/nemo-file-type-icons.git
cd nemo-file-type-icons
bash install.sh
nemo -q && nemo &
```

The install script copies:
- `file-type-icons.py` → `~/.local/share/nemo-python/extensions/`
- `icons/*.png` → `~/.local/share/nemo-file-type-icons/icons/`

## Uninstallation

```bash
cd nemo-file-type-icons
bash uninstall.sh
nemo -q && nemo &
```

> **Note:** Custom icon assignments are stored in GIO metadata (`~/.local/share/gvfs-metadata/`).
> These entries are harmless and will simply be ignored once the extension is removed.
> Nemo will fall back to its default icons automatically.

## Supported file types

| Type | Extensions | MIME type |
|------|-----------|-----------|
| Google Docs | `.doc`, `.docx` | `application/vnd.google-apps.document` |
| Google Sheets | `.xls`, `.xlsx` | `application/vnd.google-apps.spreadsheet` |
| Google Slides | `.ppt`, `.pptx` | `application/vnd.google-apps.presentation` |
| PDF | `.pdf` | `application/pdf` |
| Video | `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm`, `.mpeg`, `.mpg`, `.m4v`, `.3gp`, `.ts`, `.mts` | `video/*` |

## Adding new file types

Open `~/.local/share/nemo-python/extensions/file-type-icons.py` in a text editor.

**Files with extensions** (local files, rclone mount) → add to `EXT_MAP`:
```python
".xyz": f"file://{ICON_DIR}/my-icon.png",
```

**GVFS/native files without extension** → find the MIME type, then add to `MIME_MAP`:
```python
"application/something": f"file://{ICON_DIR}/my-icon.png",
```

Find a file's MIME type:
```bash
gio info "/path/to/file" | grep content-type
```

Place the icon PNG in `~/.local/share/nemo-file-type-icons/icons/`, then restart Nemo:
```bash
nemo -q && nemo &
```

## How it works

```
Nemo opens a folder
  → calls update_file_info() for each file
  → extension checks MIME type first  (catches GVFS files without extension)
  → then checks file extension        (catches rclone mount and local files)
  → sets metadata::custom-icon = "file:///home/username/.local/share/nemo-file-type-icons/icons/..."
  → Nemo renders the custom icon instead of the generic one
  → on subsequent opens: value already set → skipped (no performance cost)
```

The `metadata::custom-icon` attribute is the same mechanism Nemo uses when you
manually assign an icon via right-click → Properties → Icon.

## Why other approaches didn't work

| Approach | Reason it failed |
|----------|-----------------|
| MIME XML overrides | GIO ignores MIME mappings for 0-byte files |
| Icon theme name as `custom-icon` | Nemo requires a `file://` URI, not a theme name |
| Thumbnail cache | Thumbnailer is never called for 0-byte files |
| Registering a thumbnailer | GIO reports `standard::icon = x-zerosize` regardless of actual type |

## License

[MIT](LICENSE)
