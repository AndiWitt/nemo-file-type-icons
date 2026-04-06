# nemo-file-type-icons

A [Nemo](https://github.com/linuxmint/nemo) Python extension that sets correct custom icons for Google Drive files, PDFs, and videos — even when the file manager would otherwise show a generic white-page icon.

## The Problem

When using an **rclone mount** for Google Drive, Google Workspace files appear as `.docx`/`.xlsx`/`.pptx` with **0 bytes**. GIO reports them as `application/x-zerosize`, so Nemo shows a generic icon instead of the correct one.

The native **GVFS Google Drive mount** shows Google files without extensions — identifiable only by MIME type.

## The Solution

A Nemo Python extension sets the `metadata::custom-icon` attribute for each affected file. This is the same mechanism Nemo uses when you manually assign an icon via right-click → Properties → Icon.

The extension runs automatically when Nemo opens any folder. It works **system-wide** — for local files, rclone mounts, and GVFS Google Drive mounts alike.

## Requirements

- Linux Mint / Cinnamon with **Nemo** file manager
- `nemo-python` package installed
- Python 3 with `gi.repository` (GObject, Gio, Nemo)

## Installation

### 1. Provide icon files

Place PNG icon files in `~/Bilder/Icons/` (or `~/Pictures/Icons/` — adjust `ICON_DIR` in the script).

| Filename | Used for |
|----------|----------|
| `google-docs.png` | .doc, .docx, Google Docs |
| `google-sheets.png` | .xls, .xlsx, Google Sheets |
| `google-slides.png` | .ppt, .pptx, Google Slides |
| `pdf-icon.png` | .pdf |
| `video_datei_logo.png` | All video formats |

Recommended size: 96×96 px or larger, sRGB PNG.

### 2. Install the extension

```bash
bash install.sh
```

Or manually:

```bash
mkdir -p ~/.local/share/nemo-python/extensions/
cp file-type-icons.py ~/.local/share/nemo-python/extensions/
```

### 3. Restart Nemo

```bash
nemo -q && nemo &
```

## Adding new file types

**Files with extensions** (local files, rclone mount) — add to `EXT_MAP`:
```python
".xyz": f"file://{ICON_DIR}/my-icon.png",
```

**GVFS/native files without extension** — find the MIME type and add to `MIME_MAP`:
```python
"application/something": f"file://{ICON_DIR}/my-icon.png",
```

Find a file's MIME type:
```bash
gio info "/path/to/file" | grep content-type
```

Then restart Nemo.

## Supported file types

| Type | Extensions / MIME type |
|------|------------------------|
| Google Docs | `.doc`, `.docx` / `application/vnd.google-apps.document` |
| Google Sheets | `.xls`, `.xlsx` / `application/vnd.google-apps.spreadsheet` |
| Google Slides | `.ppt`, `.pptx` / `application/vnd.google-apps.presentation` |
| PDF | `.pdf` / `application/pdf` |
| Video | `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm`, `.mpeg`, `.mpg`, `.m4v`, `.3gp`, `.ts`, `.mts` / all `video/*` MIME types |

## How it works

```
Nemo opens a folder
  → calls update_file_info() for each file
  → extension checks MIME type first  (catches GVFS files without extension)
  → then checks file extension        (catches rclone mount and local files)
  → sets metadata::custom-icon = "file:///home/user/Pictures/Icons/..."
  → Nemo shows this icon instead of the generic one
  → on second open: value already set → nothing to do (performance)
```

## What didn't work (and why)

| Approach | Why it failed |
|----------|--------------|
| MIME XML overrides | GIO ignores MIME mappings for 0-byte files |
| Icon theme name as `custom-icon` | Nemo expects a `file://` URI, not a theme name |
| Thumbnail cache | Thumbnailer is not called for 0-byte files |
| Registering a thumbnailer | GIO internally reports `standard::icon = x-zerosize` regardless |

## License

MIT
