# Contributing

Contributions are welcome — bug fixes, new file type support, improved icons, or better documentation.

## How to contribute

1. **Fork** the repository
2. **Create a branch** for your change:
   ```bash
   git checkout -b feature/add-odt-support
   ```
3. **Make your changes** and commit with a clear message:
   ```bash
   git commit -m "Add support for .odt / LibreOffice Writer files"
   ```
4. **Open a Pull Request** — describe what you changed and why

## Adding support for a new file type

1. Place a PNG icon (96×96 px or larger, sRGB) in the `icons/` folder
2. Add the file extension to `EXT_MAP` in `file-type-icons.py`
3. Add the MIME type to `MIME_MAP` (find it with `gio info "/path/to/file" | grep content-type`)
4. Update the supported file types table in both `README.md` and `README-de.md`

## Reporting issues

Please open a [GitHub Issue](https://github.com/AndiWitt/nemo-file-type-icons/issues) and include:
- Your Linux Mint / Nemo version
- How you mount Google Drive (rclone or GVFS)
- What you expected vs. what you saw
