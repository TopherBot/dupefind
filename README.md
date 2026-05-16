# dupefind

**dupefind** is a lightweight, zero‑dependency Python script that helps you locate duplicate files in a given directory. It works by hashing each file’s contents (SHA‑256) and grouping files that share the same hash.

## Features
- Single‑file, no external libraries required.
- Recursive scan with optional depth limit.
- Human‑readable output (list of duplicate groups).
- Safe: read‑only operation, no files are modified or deleted.

## Installation
```bash
# Clone the repository (or download dupefind.py directly)
git clone https://github.com/yourusername/dupefind.git
cd dupefind
```
Or simply copy the `dupefind.py` file into a directory of your choice and ensure it is executable.

## Usage
```bash
python3 dupefind.py [options] <target_directory>
```
### Options
- `-d, --max-depth N` – Limit recursion depth to *N* levels (default: unlimited).
- `-v, --verbose` – Print progress information while scanning.
- `-h, --help` – Show help message and exit.

### Example
```bash
# Find duplicates under the current folder, showing progress
python3 dupefind.py -v .

# Limit search to 2 directory levels
python3 dupefind.py -d 2 /path/to/data
```

## Output
The script prints groups of duplicate files, each group separated by a blank line:
```
Duplicate group (hash: a3f5…):
    ./photos/img1.jpg
    ./backup/img1_copy.jpg

Duplicate group (hash: f9c2…):
    ./docs/report.pdf
    ./archive/old/report_backup.pdf
```
If no duplicates are found, it prints `No duplicate files detected.`.

## License
This project is released under the MIT License. See the `LICENSE` file for details.

## Contributing
Feel free to open issues or submit pull requests. Keep the project tiny and dependency‑free!
