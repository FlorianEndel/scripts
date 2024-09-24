#!/usr/bin/env python3

import os
import sys
import re
import argparse

# Define the replacement list
replacements = {
    "Ungek?rzt": "Ungekürzt",
    # Add more replacements here
}

# Dictionary to store user-provided replacements
user_replacements = {}

def extract_words(name):
    # Regular expression to match words containing '?', excluding parentheses
    word_pattern = r'[^\s\._\-()]*\?[^\s\._\-()]*'
    return re.findall(word_pattern, name)

def rename_item(path, dry_run=False):
    dir_path, old_name = os.path.split(path)
    new_name = old_name

    if '?' in new_name:
        # Check if we have a predefined replacement
        for key, value in replacements.items():
            if key in new_name:
                new_name = new_name.replace(key, value)

        # If there are still question marks, process each one
        words = extract_words(new_name)
        for word in words:
            print(f"Current name: {new_name}")
            print(f"Word to process: {word}")

            if word in user_replacements:
                replacement = user_replacements[word]
                print(f"Using previous replacement: '{replacement}'")
            else:
                replacement = input(f"Enter replacement character for '?' in '{word}': ")
                user_replacements[word] = replacement

            new_word = word.replace('?', replacement, 1)
            new_name = new_name.replace(word, new_word, 1)

        # Rename the item
        if new_name != old_name:
            old_path = os.path.join(dir_path, old_name)
            new_path = os.path.join(dir_path, new_name)
            if dry_run:
                print(f"Would rename: {old_path} -> {new_path}")
            else:
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")

def process_directory(directory, dry_run=False):
    # Walk through the directory tree
    for root, dirs, files in os.walk(directory, topdown=False):
        # Process directories
        for name in dirs:
            rename_item(os.path.join(root, name), dry_run)

        # Process files
        for name in files:
            rename_item(os.path.join(root, name), dry_run)

def print_user_replacements():
    print("\nUser-provided replacements:")
    print("replacements = {")
    for key, value in user_replacements.items():
        print(f"    \"{key}\": \"{key.replace('?', value)}\",")
    print("}")
    print("\nYou can add these entries to the 'replacements' dictionary in the script for future use.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rename files and directories by replacing '?' characters.",
        epilog="""
This script walks through the specified directory (or the current directory if not specified)
and renames files and folders containing '?' characters. It uses a predefined list of replacements
and interactively asks for replacements when encountering new patterns.

To add your own predefined replacements, edit the 'replacements' dictionary at the beginning of
the script. After running the script, it will output a list of user-provided replacements that
you can add to the 'replacements' dictionary for future use.

Example usage:
  %(prog)s                             # Process current directory
  %(prog)s /path/to/directory          # Process specific directory
  %(prog)s --dry-run                   # Show what would be renamed without making changes
  %(prog)s /path/to/directory --dry-run  # Dry run on specific directory
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("directory", nargs="?", default=".", help="Directory to process (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be renamed without making any changes")
    args = parser.parse_args()

    process_directory(args.directory, args.dry_run)
    print_user_replacements()
