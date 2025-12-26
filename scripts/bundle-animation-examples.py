#!/usr/bin/env python3
"""
Bundle Animation Examples for Browser UI

This script scans the anim_tutorials directory for .anim files and generates
a JavaScript file that provides example animations to the browser UI.

Each .anim file should have a description comment on the first line:
    # @desc Short description of what this animation does

The generated file (dist/animation-examples.js) provides:
- List of example animations with name, description, and code
- Organized by category (extracted from filename prefix)
- Easy loading into the code editor

Usage:
    python scripts/bundle-animation-examples.py

Output:
    dist/animation-examples.js - JavaScript module with animation examples
"""

import os
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configuration
TUTORIALS_DIR = "lib/libesp32/berry_animation/anim_tutorials"
OUTPUT_FILE = "dist/animation-examples.js"

# Category mapping based on filename prefixes
# Matches chapter names from ANIMATION_TUTORIAL.md
CATEGORY_MAP = {
    "chap_1": "1. Getting Started",
    "chap_2": "2. Color Cycling",
    "chap_3": "3. Smooth Transitions",
    "chap_4": "4. Spatial Patterns",
    "chap_5": "5. Beacons & Moving",
    "chap_6": "6. Shutters & Sequences",
    "chap_7": "7. Crenel Patterns",
    "chap_8": "8. Templates",
}


def extract_description(content: str) -> str:
    """
    Extract the description from the first comment line.
    
    Looks for patterns like:
        # @desc This is the description
        # Description text
    
    Returns the description or a default message.
    """
    lines = content.strip().split('\n')
    
    for line in lines[:5]:  # Check first 5 lines
        line = line.strip()
        if line.startswith('#'):
            # Remove the # and any leading whitespace
            comment = line[1:].strip()
            
            # Check for @desc tag
            if comment.lower().startswith('@desc'):
                return comment[5:].strip()
            
            # Use first non-empty comment as description
            if comment and not comment.startswith('#'):
                return comment
    
    return "Animation example"


def extract_category(filename: str) -> str:
    """
    Extract category from filename prefix.
    
    Examples:
        chap_1_00_plain.anim -> "Basics"
        chap_5_10_template.anim -> "Templates"
    """
    for prefix, category in CATEGORY_MAP.items():
        if filename.startswith(prefix):
            return category
    return "Other"


def extract_order(filename: str) -> Tuple[int, int]:
    """
    Extract sort order from filename.
    
    Examples:
        chap_1_00_plain.anim -> (1, 0)
        chap_5_10_template.anim -> (5, 10)
    """
    match = re.match(r'chap_(\d+)_(\d+)', filename)
    if match:
        return (int(match.group(1)), int(match.group(2)))
    return (99, 99)


def extract_number(filename: str) -> str:
    """
    Extract display number from filename.
    
    Examples:
        chap_1_00_plain.anim -> "1.00"
        chap_5_10_template.anim -> "5.10"
    """
    match = re.match(r'chap_(\d+)_(\d+)', filename)
    if match:
        return f"{match.group(1)}.{match.group(2)}"
    return ""


def format_name(filename: str) -> str:
    """
    Format filename into a human-readable name.
    
    Examples:
        chap_1_00_plain.anim -> "Plain"
        chap_5_10_template_cylon_simple.anim -> "Template Cylon Simple"
    """
    # Remove extension
    name = filename.replace('.anim', '')
    
    # Remove chapter prefix (chap_X_XX_)
    name = re.sub(r'^chap_\d+_\d+_', '', name)
    
    # Replace underscores with spaces and title case
    name = name.replace('_', ' ').title()
    
    return name


def scan_tutorials() -> List[Dict]:
    """
    Scan the tutorials directory for .anim files.
    
    Returns a list of dictionaries with:
        - id: unique identifier (filename without extension)
        - name: human-readable name
        - description: extracted description
        - category: category name
        - code: full animation code
        - order: sort order tuple
    """
    examples = []
    
    tutorials_path = Path(TUTORIALS_DIR)
    if not tutorials_path.exists():
        print(f"Warning: {TUTORIALS_DIR} directory not found", file=sys.stderr)
        return examples
    
    for filepath in sorted(tutorials_path.glob("*.anim")):
        filename = filepath.name
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
            continue
        
        example = {
            "id": filename.replace('.anim', ''),
            "number": extract_number(filename),
            "name": format_name(filename),
            "description": extract_description(content),
            "category": extract_category(filename),
            "code": content,
            "order": extract_order(filename),
        }
        
        examples.append(example)
    
    # Sort by order
    examples.sort(key=lambda x: x["order"])
    
    # Remove order from final output (it was just for sorting)
    for example in examples:
        del example["order"]
    
    return examples


def generate_js_output(examples: List[Dict]) -> str:
    """Generate the JavaScript output file content."""
    lines = []
    
    # Header
    lines.append("/**")
    lines.append(" * Animation Examples for Browser UI")
    lines.append(" * ")
    lines.append(f" * Total examples: {len(examples)}")
    lines.append(" * ")
    lines.append(" * This file provides example animations for the Berry Animation Simulator.")
    lines.append(" * Each example includes a name, description, category, and DSL code.")
    lines.append(" * ")
    lines.append(" * Generated by: scripts/bundle-animation-examples.py")
    lines.append(" */")
    lines.append("")
    lines.append("(function(window) {")
    lines.append("    'use strict';")
    lines.append("")
    
    # Examples array
    lines.append("    const examples = [")
    
    for i, example in enumerate(examples):
        comma = "," if i < len(examples) - 1 else ""
        lines.append("        {")
        lines.append(f"            id: {json.dumps(example['id'])},")
        lines.append(f"            number: {json.dumps(example['number'])},")
        lines.append(f"            name: {json.dumps(example['name'])},")
        lines.append(f"            description: {json.dumps(example['description'])},")
        lines.append(f"            category: {json.dumps(example['category'])},")
        lines.append(f"            code: {json.dumps(example['code'])}")
        lines.append(f"        }}{comma}")
    
    lines.append("    ];")
    lines.append("")
    
    # Categories
    categories = sorted(set(ex["category"] for ex in examples))
    lines.append("    const categories = " + json.dumps(categories) + ";")
    lines.append("")
    
    # AnimationExamples class
    lines.append("    /**")
    lines.append("     * AnimationExamples - Provides access to example animations")
    lines.append("     */")
    lines.append("    class AnimationExamples {")
    lines.append("        /**")
    lines.append("         * Get all examples")
    lines.append("         * @returns {Array} Array of example objects")
    lines.append("         */")
    lines.append("        getAll() {")
    lines.append("            return examples;")
    lines.append("        }")
    lines.append("")
    lines.append("        /**")
    lines.append("         * Get all categories")
    lines.append("         * @returns {Array} Array of category names")
    lines.append("         */")
    lines.append("        getCategories() {")
    lines.append("            return categories;")
    lines.append("        }")
    lines.append("")
    lines.append("        /**")
    lines.append("         * Get examples by category")
    lines.append("         * @param {string} category - Category name")
    lines.append("         * @returns {Array} Array of examples in that category")
    lines.append("         */")
    lines.append("        getByCategory(category) {")
    lines.append("            return examples.filter(ex => ex.category === category);")
    lines.append("        }")
    lines.append("")
    lines.append("        /**")
    lines.append("         * Get example by ID")
    lines.append("         * @param {string} id - Example ID")
    lines.append("         * @returns {Object|null} Example object or null if not found")
    lines.append("         */")
    lines.append("        getById(id) {")
    lines.append("            return examples.find(ex => ex.id === id) || null;")
    lines.append("        }")
    lines.append("")
    lines.append("        /**")
    lines.append("         * Search examples by name or description")
    lines.append("         * @param {string} query - Search query")
    lines.append("         * @returns {Array} Matching examples")
    lines.append("         */")
    lines.append("        search(query) {")
    lines.append("            const q = query.toLowerCase();")
    lines.append("            return examples.filter(ex => ")
    lines.append("                ex.name.toLowerCase().includes(q) || ")
    lines.append("                ex.description.toLowerCase().includes(q)")
    lines.append("            );")
    lines.append("        }")
    lines.append("")
    lines.append("        /**")
    lines.append("         * Get example count")
    lines.append("         * @returns {number} Total number of examples")
    lines.append("         */")
    lines.append("        count() {")
    lines.append("            return examples.length;")
    lines.append("        }")
    lines.append("    }")
    lines.append("")
    
    # Export
    lines.append("    // Create global instance")
    lines.append("    window.animationExamples = new AnimationExamples();")
    lines.append("")
    lines.append("    // Also export the class for potential extension")
    lines.append("    window.AnimationExamples = AnimationExamples;")
    lines.append("")
    lines.append("    console.log(`[AnimationExamples] Loaded ${examples.length} examples in ${categories.length} categories`);")
    lines.append("")
    lines.append("})(window);")
    lines.append("")
    
    return "\n".join(lines)


def main():
    """Main entry point."""
    print("Bundling animation examples for browser UI...")
    
    # Scan tutorials
    print(f"Scanning {TUTORIALS_DIR}...")
    examples = scan_tutorials()
    print(f"  Found {len(examples)} examples")
    
    if not examples:
        print("Warning: No examples found!", file=sys.stderr)
        return 1
    
    # Print summary by category
    categories = {}
    for ex in examples:
        cat = ex["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(ex)
    
    print("\nExamples by category:")
    for cat in sorted(categories.keys()):
        print(f"  {cat}: {len(categories[cat])} examples")
        for ex in categories[cat]:
            print(f"    - {ex['name']}: {ex['description'][:50]}...")
    
    # Generate output
    output = generate_js_output(examples)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # Write output file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(output)
    
    print(f"\nGenerated {OUTPUT_FILE} ({len(output)} bytes)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
