#!/usr/bin/env python3
"""
Generate MkDocs-compatible markdown for WLED palettes

Creates a markdown file with embedded HTML/CSS for palette visualization
that works with MkDocs material theme.
"""

import re
from pathlib import Path


def parse_berry_palette(berry_file):
    """Parse palette data from Berry file."""
    with open(berry_file, 'r') as f:
        content = f.read()
    
    palettes = {}
    
    # Find all palette definitions
    pattern = r'var (PALETTE_\w+) = bytes\(([\s\S]*?)\n\)'
    
    for match in re.finditer(pattern, content):
        var_name = match.group(1)
        data_block = match.group(2)
        
        # Extract hex strings (8 hex digits)
        hex_pattern = r'"([0-9A-F]{8})"'
        hex_values = re.findall(hex_pattern, data_block)
        
        if hex_values:
            palettes[var_name] = hex_values
    
    # Parse the map to get display names
    map_pattern = r'static map = \{(.*?)\}'
    map_match = re.search(map_pattern, content, re.DOTALL)
    
    display_names = {}
    if map_match:
        map_content = map_match.group(1)
        name_pattern = r'"([^"]+)":\s*(PALETTE_\w+)'
        for match in re.finditer(name_pattern, map_content):
            display_name = match.group(1)
            var_name = match.group(2)
            display_names[var_name] = display_name
    
    return palettes, display_names


def vrgb_to_css_gradient(hex_values):
    """Convert VRGB hex values to CSS linear gradient."""
    stops = []
    
    for hex_val in hex_values:
        v = int(hex_val[0:2], 16)
        r = int(hex_val[2:4], 16)
        g = int(hex_val[4:6], 16)
        b = int(hex_val[6:8], 16)
        
        percent = (v / 255.0) * 100.0
        stops.append(f"#{r:02X}{g:02X}{b:02X} {percent:.1f}%")
    
    return f"linear-gradient(to right, {', '.join(stops)})"


def generate_markdown(palettes, display_names):
    """Generate MkDocs-compatible markdown with table format."""
    
    md = '''## WLED Palettes Reference

This page displays all 59 WLED gradient palettes available in the Berry Animation Framework.

<style>
h3#palette-gallery + * td:nth-child(2) {
    background-color: rgb(30, 33, 41);
    padding: 8px;
}
</style>

### Palette Gallery

Palette | Gradient
:--- | :---
'''
    
    # Add each palette as a table row
    for var_name in sorted(palettes.keys()):
        display_name = display_names.get(var_name, var_name)
        hex_values = palettes[var_name]
        gradient = vrgb_to_css_gradient(hex_values)
        
        # Create the gradient div
        gradient_div = f"<div style='width:400px;height:30px;background:{gradient};border-color:#888;border-width:1px;border-style:solid;'></div>"
        
        # Left column: Display name (map key) and color stops
        left_col = f"`{display_name}`<br><small>{len(hex_values)} color stops</small>"
        
        # Add table row
        md += f"{left_col} | {gradient_div}\n"
    
    md += '''
### Credits

- **WLED Palettes**: From [WLED Project](https://github.com/Aircoookie/WLED) by Aircoookie
- **Conversion**: For Tasmota Berry Animation Framework
- **Total Palettes**: 59 gradient palettes
'''
    
    return md


def main():
    berry_file = Path('lib/libesp32/berry_animation/src/dsl/all_wled_palettes.be')
    
    if not berry_file.exists():
        print(f"Error: {berry_file} not found")
        return
    
    print("Parsing Berry palette file...")
    palettes, display_names = parse_berry_palette(berry_file)
    
    print(f"Found {len(palettes)} palettes")
    
    print("Generating MkDocs markdown...")
    markdown = generate_markdown(palettes, display_names)
    
    output_file = Path('wled_palettes.md')
    with open(output_file, 'w') as f:
        f.write(markdown)
    
    print(f"Generated {output_file}")
    print(f"Add this file to your MkDocs docs/ directory")


if __name__ == '__main__':
    main()
