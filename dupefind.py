#!/usr/bin/env python3
"""dupefind – locate duplicate files by content hash.

Usage:
    python3 dupefind.py [options] <target_directory>

Options:
    -d, --max-depth N   Limit recursion depth (default: unlimited).
    -v, --verbose       Show progress while scanning.
    -h, --help          Show this help message.
"""

import argparse
import hashlib
import os
import sys
from collections import defaultdict
from typing import Dict, List, Tuple

def compute_hash(path: str, chunk_size: int = 8192) -> str:
    """Return SHA‑256 hex digest of the file at *path*.
    Reads the file in chunks to avoid loading large files into memory.
    """
    sha256 = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                sha256.update(data)
    except (OSError, PermissionError) as e:
        print(f"[WARN] Cannot read '{path}': {e}", file=sys.stderr)
        return ""
    return sha256.hexdigest()

def walk_dir(root: str, max_depth: int = None, verbose: bool = False) -> List[str]:
    """Return a list of file paths under *root* respecting *max_depth*.
    *max_depth* = None means unlimited depth.
    """
    files: List[str] = []
    root = os.path.abspath(root)
    for dirpath, dirnames, filenames in os.walk(root):
        # Calculate current depth relative to root
        depth = dirpath.count(os.sep) - root.count(os.sep)
        if max_depth is not None and depth > max_depth:
            # Prune deeper directories
            dirnames.clear()
            continue
        for name in filenames:
            full_path = os.path.join(dirpath, name)
            files.append(full_path)
            if verbose:
                print(f"[INFO] Found file: {full_path}")
    return files

def find_duplicates(files: List[str], verbose: bool = False) -> Dict[str, List[str]]:
    """Group files by their SHA‑256 hash.
    Returns a dict mapping hash → list of file paths (length >= 1).
    """
    hash_map: Dict[str, List[str]] = defaultdict(list)
    total = len(files)
    for idx, path in enumerate(files, 1):
        if verbose:
            print(f"[PROGRESS] ({idx}/{total}) hashing {path}")
        file_hash = compute_hash(path)
        if file_hash:
            hash_map[file_hash].append(path)
    # Keep only groups with more than one file
    duplicates = {h: lst for h, lst in hash_map.items() if len(lst) > 1}
    return duplicates

def print_duplicates(duplicates: Dict[str, List[str]]) -> None:
    if not duplicates:
        print("No duplicate files detected.")
        return
    for h, paths in duplicates.items():
        print(f"Duplicate group (hash: {h[:8]}…):")
        for p in paths:
            print(f"    {p}")
        print()

def parse_args() -> Tuple[argparse.Namespace, List[str]]:
    parser = argparse.ArgumentParser(description="Find duplicate files by content hash.")
    parser.add_argument("directory", help="Target directory to scan")
    parser.add_argument("-d", "--max-depth", type=int, default=None,
                        help="Maximum recursion depth (default: unlimited)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show progress information while scanning")
    args = parser.parse_args()
    return args, sys.argv[1:]

def main() -> int:
    args, _ = parse_args()
    if not os.path.isdir(args.directory):
        print(f"[ERROR] '{args.directory}' is not a directory or does not exist.", file=sys.stderr)
        return 1
    file_list = walk_dir(args.directory, max_depth=args.max_depth, verbose=args.verbose)
    duplicates = find_duplicates(file_list, verbose=args.verbose)
    print_duplicates(duplicates)
    return 0

if __name__ == "__main__":
    sys.exit(main())
