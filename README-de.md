# nemo-file-type-icons

Eine [Nemo](https://github.com/linuxmint/nemo) Python-Extension, die korrekte benutzerdefinierte Icons für Google Drive-Dateien, PDFs und Videos anzeigt — und damit das generische weiße Seiten-Icon behebt, das bei 0-Byte-Dateien aus rclone-gemounteten Google Workspace-Ordnern erscheint.

## Das Problem

Beim Einbinden von Google Drive über **rclone** erscheinen Google Workspace-Dateien als `.docx`/`.xlsx`/`.pptx` mit **0 Bytes**. GIO identifiziert sie als `application/x-zerosize`, weshalb Nemo auf ein generisches Icon zurückfällt.

Der native **GVFS Google Drive-Mount** (eingehängtes Laufwerk in der Nemo-Seitenleiste) zeigt diese Dateien ohne Dateiendung — nur der MIME-Typ ist zur Erkennung verfügbar.

Diese Extension löst beide Fälle transparent mit einem einzigen schlanken Nemo Python-Plugin — ohne manuelle Icon-Zuweisung.

## Voraussetzungen

- Linux Mint oder ein beliebiger Cinnamon-Desktop mit **Nemo**
- Paket `nemo-python`:
  ```bash
  sudo apt install nemo-python
  ```

> **rclone-Nutzer:** Der Mount muss Extended Attributes unterstützen (Standard).
> Bei `--no-xattrs` oder Read-only-Mounts können keine Icons gesetzt werden.

## Installation

```bash
git clone https://github.com/AndiWitt/nemo-file-type-icons.git
cd nemo-file-type-icons
bash install.sh
nemo -q && nemo &
```

Das Installationsskript kopiert:
- `file-type-icons.py` → `~/.local/share/nemo-python/extensions/`
- `icons/*.png` → `~/.local/share/nemo-file-type-icons/icons/`

## Deinstallation

```bash
cd nemo-file-type-icons
bash uninstall.sh
nemo -q && nemo &
```

> **Hinweis:** Benutzerdefinierte Icon-Zuweisungen werden in GIO-Metadaten gespeichert
> (`~/.local/share/gvfs-metadata/`). Diese Einträge sind harmlos und werden nach dem
> Entfernen der Extension einfach ignoriert. Nemo fällt automatisch auf seine
> Standard-Icons zurück.

## Unterstützte Dateitypen

| Typ | Dateiendungen | MIME-Typ |
|-----|--------------|----------|
| Google Docs | `.doc`, `.docx` | `application/vnd.google-apps.document` |
| Google Sheets | `.xls`, `.xlsx` | `application/vnd.google-apps.spreadsheet` |
| Google Slides | `.ppt`, `.pptx` | `application/vnd.google-apps.presentation` |
| PDF | `.pdf` | `application/pdf` |
| Video | `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm`, `.mpeg`, `.mpg`, `.m4v`, `.3gp`, `.ts`, `.mts` | `video/*` |

## Neuen Dateityp hinzufügen

Datei öffnen: `~/.local/share/nemo-python/extensions/file-type-icons.py`

**Dateien mit Endung** (lokale Dateien, rclone-Mount) → in `EXT_MAP` eintragen:
```python
".xyz": f"file://{ICON_DIR}/mein-icon.png",
```

**GVFS-/native Dateien ohne Endung** → MIME-Typ ermitteln und in `MIME_MAP` eintragen:
```python
"application/irgendwas": f"file://{ICON_DIR}/mein-icon.png",
```

MIME-Typ einer Datei herausfinden:
```bash
gio info "/pfad/zur/datei" | grep content-type
```

Icon-PNG in `~/.local/share/nemo-file-type-icons/icons/` ablegen, dann Nemo neu starten:
```bash
nemo -q && nemo &
```

## Funktionsweise

```
Nemo öffnet einen Ordner
  → ruft update_file_info() für jede Datei auf
  → Extension prüft zuerst den MIME-Typ  (trifft GVFS-Dateien ohne Endung)
  → dann die Dateiendung als Fallback    (trifft rclone-Mount und lokale Dateien)
  → setzt metadata::custom-icon = "file:///home/nutzername/.local/share/nemo-file-type-icons/icons/..."
  → Nemo zeigt dieses Icon statt dem generischen
  → beim nächsten Öffnen: Wert bereits gesetzt → wird übersprungen (kein Performance-Aufwand)
```

Das Attribut `metadata::custom-icon` ist derselbe Mechanismus, den Nemo beim manuellen
Setzen eines Icons über Rechtsklick → Eigenschaften → Symbol verwendet.

## Was nicht funktioniert hat (und warum)

| Ansatz | Grund des Scheiterns |
|--------|---------------------|
| MIME-XML-Overrides | GIO ignoriert MIME-Mappings für 0-Byte-Dateien |
| Icon-Theme-Name als `custom-icon` | Nemo erwartet eine `file://`-URI, keinen Theme-Namen |
| Thumbnail-Cache | Thumbnailer wird für 0-Byte-Dateien nie aufgerufen |
| Thumbnailer registrieren | GIO meldet intern `standard::icon = x-zerosize` unabhängig vom tatsächlichen Typ |

## Lizenz

[MIT](LICENSE)
