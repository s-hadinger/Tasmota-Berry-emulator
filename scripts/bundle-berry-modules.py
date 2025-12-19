#!/usr/bin/env python3
"""
Bundle Berry Modules for Browser Virtual Filesystem

This script scans Berry source directories and generates a JavaScript file
that registers all Berry modules in the browser's virtual filesystem.

The generated file (dist/berry-modules.js) should be loaded after virtual-fs.js
and before berry.js to make Berry modules available for import.

Usage:
    python scripts/bundle-berry-modules.py

Output:
    dist/berry-modules.js - JavaScript file with all Berry modules as strings
"""

import os
import json
import sys
from pathlib import Path

# Configuration
ANIMATION_SRC_DIR = "lib/libesp32/berry_animation/src"
TASMOTA_ENV_DIR = "tasmota_env"
OUTPUT_FILE = "dist/berry-modules.js"

# Files to exclude (tests, etc.)
EXCLUDE_PATTERNS = [
    "*_test.be",
    "test_*.be",
    "tests/",
    "solidify/",
    ".DS_Store",
]

# Patterns for tasmota_env files to exclude
TASMOTA_ENV_EXCLUDE_PATTERNS = [
    "*_test.be",      # Test files
    "test_*.be",      # Test files
    "*_orig.be",      # Original/backup files
    "emulator_test.be",  # Emulator test file
]

# Root-level files to include (will also scan for all *.be in project root)
ROOT_FILES = [
    "tasmota.be",  # Main Tasmota emulator entry point
]

# Patterns for root-level files to exclude
ROOT_EXCLUDE_PATTERNS = [
    "test_*.be",      # Test files
    "debug_*.be",     # Debug files
    "compile_*.be",   # Compilation scripts
    "run_*.be",       # Run scripts
    "example_*.be",   # Example files (not needed for runtime)
]


def should_exclude(filepath: str) -> bool:
    """Check if a file should be excluded based on patterns."""
    path = Path(filepath)
    
    for pattern in EXCLUDE_PATTERNS:
        if pattern.endswith("/"):
            # Directory pattern
            if pattern[:-1] in path.parts:
                return True
        elif "*" in pattern:
            # Glob pattern
            if path.match(pattern):
                return True
        else:
            # Exact match
            if path.name == pattern:
                return True
    
    return False


def escape_js_string(content: str) -> str:
    """Escape a string for use in JavaScript template literals."""
    # Use JSON encoding which handles all escaping properly
    # Then strip the surrounding quotes since we'll use template literals
    return json.dumps(content)


def get_module_name(filepath: str, base_dir: str) -> str:
    """
    Get the module name from a file path.
    
    For animation framework files, preserves the directory structure:
        lib/libesp32/berry_animation/src/core/animation_base.be -> core/animation_base.be
        lib/libesp32/berry_animation/src/animation.be -> animation.be
    
    For tasmota_env files:
        tasmota_env/Leds.be -> Leds.be
    """
    rel_path = os.path.relpath(filepath, base_dir)
    return rel_path


def scan_directory(directory: str, base_dir: str = None) -> dict:
    """
    Scan a directory for .be files and return a dict of module_name -> content.
    """
    if base_dir is None:
        base_dir = directory
    
    modules = {}
    
    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]
        
        for filename in files:
            if not filename.endswith(".be"):
                continue
            
            filepath = os.path.join(root, filename)
            
            if should_exclude(filepath):
                continue
            
            module_name = get_module_name(filepath, base_dir)
            
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                modules[module_name] = content
            except Exception as e:
                print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
    
    return modules


def should_exclude_tasmota_env_file(filename: str) -> bool:
    """Check if a tasmota_env file should be excluded."""
    path = Path(filename)
    
    for pattern in TASMOTA_ENV_EXCLUDE_PATTERNS:
        if "*" in pattern:
            # Glob pattern
            if path.match(pattern):
                return True
        else:
            # Exact match
            if path.name == pattern:
                return True
    
    return False


def scan_tasmota_env() -> dict:
    """Scan tasmota_env directory for all .be files.
    
    Files are registered with the tasmota_env/ prefix to match the folder structure.
    For example: tasmota_env/Leds.be -> "tasmota_env/Leds.be"
    """
    modules = {}
    
    # Scan for all *.be files in tasmota_env (non-recursive)
    tasmota_env_path = Path(TASMOTA_ENV_DIR)
    if not tasmota_env_path.exists():
        print(f"Warning: {TASMOTA_ENV_DIR} directory not found", file=sys.stderr)
        return modules
    
    for filepath in tasmota_env_path.glob("*.be"):
        filename = filepath.name
        
        # Skip excluded patterns
        if should_exclude_tasmota_env_file(filename):
            continue
        
        # Use full path with tasmota_env/ prefix
        module_name = f"{TASMOTA_ENV_DIR}/{filename}"
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            modules[module_name] = content
        except Exception as e:
            print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
    
    return modules


def should_exclude_root_file(filename: str) -> bool:
    """Check if a root-level file should be excluded."""
    path = Path(filename)
    
    for pattern in ROOT_EXCLUDE_PATTERNS:
        if "*" in pattern:
            # Glob pattern
            if path.match(pattern):
                return True
        else:
            # Exact match
            if path.name == pattern:
                return True
    
    return False


def scan_root_files() -> dict:
    """Scan root-level .be files in the project root."""
    modules = {}
    
    # First, add explicitly listed files
    for filename in ROOT_FILES:
        if not os.path.exists(filename):
            print(f"Warning: {filename} not found", file=sys.stderr)
            continue
        
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            modules[filename] = content
        except Exception as e:
            print(f"Warning: Could not read {filename}: {e}", file=sys.stderr)
    
    # Then scan for all *.be files in project root (non-recursive)
    for filepath in Path(".").glob("*.be"):
        filename = filepath.name
        
        # Skip if already added from ROOT_FILES
        if filename in modules:
            continue
        
        # Skip excluded patterns
        if should_exclude_root_file(filename):
            continue
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            modules[filename] = content
        except Exception as e:
            print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
    
    return modules


def generate_js_output(modules: dict) -> str:
    """Generate the JavaScript output file content."""
    lines = []
    
    # Header
    lines.append("/**")
    lines.append(" * Berry Modules for Virtual Filesystem")
    lines.append(" * ")
    lines.append(f" * Total modules: {len(modules)}")
    lines.append(" * ")
    lines.append(" * This file registers all Berry animation framework modules")
    lines.append(" * in the browser's virtual filesystem for use with `import`.")
    lines.append(" * ")
    lines.append(" * Load order:")
    lines.append(" *   1. virtual-fs.js (creates window.virtualFS)")
    lines.append(" *   2. berry-modules.js (this file - registers modules)")
    lines.append(" *   3. berry.js (Berry WASM module)")
    lines.append(" */")
    lines.append("")
    lines.append("(function() {")
    lines.append("    'use strict';")
    lines.append("")
    lines.append("    // Ensure virtualFS is available")
    lines.append("    if (typeof window.virtualFS === 'undefined') {")
    lines.append("        console.error('[BerryModules] Error: window.virtualFS not found. Load virtual-fs.js first.');")
    lines.append("        return;")
    lines.append("    }")
    lines.append("")
    lines.append("    const modules = {};")
    lines.append("")
    
    # Add each module
    for module_name in sorted(modules.keys()):
        content = modules[module_name]
        escaped = escape_js_string(content)
        lines.append(f"    modules[{json.dumps(module_name)}] = {escaped};")
    
    lines.append("")
    lines.append("    // Register all modules in the virtual filesystem")
    lines.append("    let count = 0;")
    lines.append("    for (const [name, content] of Object.entries(modules)) {")
    lines.append("        window.virtualFS.registerFile(name, content);")
    lines.append("        count++;")
    lines.append("    }")
    lines.append("")
    lines.append("    console.log(`[BerryModules] Registered ${count} Berry modules`);")
    lines.append("")
    lines.append("    // Export module list for debugging")
    lines.append("    window.berryModuleList = Object.keys(modules);")
    lines.append("")
    lines.append("})();")
    lines.append("")
    
    return "\n".join(lines)


def main():
    """Main entry point."""
    print("Bundling Berry modules for browser virtual filesystem...")
    
    all_modules = {}
    
    # Scan animation framework source
    print(f"Scanning {ANIMATION_SRC_DIR}...")
    animation_modules = scan_directory(ANIMATION_SRC_DIR)
    print(f"  Found {len(animation_modules)} animation modules")
    all_modules.update(animation_modules)
    
    # Scan tasmota_env
    print(f"Scanning {TASMOTA_ENV_DIR}...")
    tasmota_modules = scan_tasmota_env()
    print(f"  Found {len(tasmota_modules)} tasmota_env modules")
    all_modules.update(tasmota_modules)
    
    # Scan root files
    if ROOT_FILES:
        print("Scanning root files...")
        root_modules = scan_root_files()
        print(f"  Found {len(root_modules)} root modules")
        all_modules.update(root_modules)
    
    print(f"Total: {len(all_modules)} modules")
    
    # Generate output
    output = generate_js_output(all_modules)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # Write output file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(output)
    
    print(f"Generated {OUTPUT_FILE} ({len(output)} bytes)")
    
    # Print module list
    print("\nRegistered modules:")
    for name in sorted(all_modules.keys()):
        print(f"  - {name}")


if __name__ == "__main__":
    main()
