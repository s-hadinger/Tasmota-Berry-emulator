#!/usr/bin/env python3
"""
WLED Palette to Berry/DSL Converter
====================================

This script converts WLED gradient palette definitions from C arrays to both:
1. Berry code with VRGB format (Value, R, G, B as hex bytes)
2. DSL palette format for the Berry Animation Framework

PURPOSE:
--------
WLED (https://github.com/Aircoookie/WLED) contains 59 beautiful gradient palettes
that are used for LED strip animations. This script extracts those palettes and
converts them to formats usable in the Berry Animation Framework for Tasmota.

SOURCE FILE:
-----------
Input: from_wled/src/wled_palettes.h
- Contains palette definitions as C arrays (const uint8_t or const byte)
- Palettes are listed in the gGradientPalettes[] array (line ~710)
- Each palette has a C variable name (e.g., ib_jul01_gp) and a display name in comments (e.g., "Jul")

NAMING CONVENTION:
-----------------
CRITICAL: Palette names come from the gGradientPalettes array comments, NOT the C variable names!

Example from the array:
    ib_jul01_gp,                  //31-18 Jul
    lava_gp,                      //35-22 Fire
    fierce_ice_gp,                //36-23 Icefire

This means:
- C variable: ib_jul01_gp  → Display name: "Jul"  → Berry: PALETTE_JUL_
- C variable: lava_gp      → Display name: "Fire" → Berry: PALETTE_FIRE_
- C variable: fierce_ice_gp → Display name: "Icefire" → Berry: PALETTE_ICEFIRE_

The display names are what users see in WLED's UI, so we use those for consistency.

INPUT FORMAT (C Array):
----------------------
Palettes are defined as arrays of uint8_t or byte values in groups of 4:
[position, red, green, blue, position, red, green, blue, ...]

Example:
    const uint8_t ib_jul01_gp[] PROGMEM = {
        0, 226,   6,  12,      // Position 0: RGB(226,6,12)
       94,  26,  96,  78,      // Position 94: RGB(26,96,78)
      132, 130, 189,  94,      // Position 132: RGB(130,189,94)
      255, 177,   3,   9};     // Position 255: RGB(177,3,9)

Notes:
- Position ranges from 0-255 (0% to 100% of the gradient)
- RGB values are 0-255
- Some palettes have inline comments (e.g., "//gc" for gamma correction notes)
- Comments may contain commas, so they must be stripped before parsing

OUTPUT FORMAT 1 - Berry (VRGB):
-------------------------------
Each palette becomes a Berry bytes() object with VRGB encoding:
- V = Value/Position (0-255)
- R = Red (0-255)
- G = Green (0-255)
- B = Blue (0-255)

Each entry is 8 hex characters (4 bytes): "VVRRGGBB"

Example:
    var PALETTE_JUL_ = bytes(
      "00E2060C"  # pos=0 rgb(226,6,12)
      "5E1A604E"  # pos=94 rgb(26,96,78)
      "8482BD5E"  # pos=132 rgb(130,189,94)
      "FFB10309"  # pos=255 rgb(177,3,9)
    )

The Berry file also includes:
- A WLED_Palettes class with a static map for name-based access
- Module return statement: return {"wled_palettes": WLED_Palettes}

OUTPUT FORMAT 2 - DSL:
---------------------
DSL format uses position-color tuples for the Animation DSL transpiler:

Example:
    palette PALETTE_JUL = [
      (0, 0xE2060C)    # 0.0% rgb(226,6,12) (start)
      (94, 0x1A604E)    # 36.9% rgb(26,96,78)
      (132, 0x82BD5E)    # 51.8% rgb(130,189,94)
      (255, 0xB10309)    # 100.0% rgb(177,3,9) (end)
    ]

OUTPUT FILES:
------------
1. lib/libesp32/berry_animation/src/dsl/all_wled_palettes.be
   - Berry code with 59 palette definitions
   - WLED_Palettes class with map
   - Ready to import in Berry scripts

2. lib/libesp32/berry_animation/src/dsl/all_wled_palettes.anim
   - DSL format with 59 palette definitions
   - Can be compiled by the DSL transpiler
   - Used for animation definitions

PARSING CHALLENGES:
------------------
1. Two declaration types: "const uint8_t" and "const byte"
2. Inline comments with commas (e.g., "//gc from 47, 61,126")
3. Numbers may be comma-separated or whitespace-separated
4. Last entry in gGradientPalettes array has no trailing comma
5. Some palette names have special characters (e.g., "Red & Blue", "C9 2")

USAGE:
------
Run: python3 wled_palette_to_dsl.py

The script will:
1. Parse from_wled/src/wled_palettes.h
2. Extract the gGradientPalettes array to get display names
3. Find all palette definitions in the file
4. Match them with their display names
5. Generate both .be and .dsl files

MAINTENANCE:
-----------
If WLED adds new palettes:
1. Update from_wled/src/wled_palettes.h with the new version
2. Run this script
3. The output files will be regenerated with all palettes

If the gGradientPalettes array format changes:
- Update parse_gradient_palettes_array() function
- The regex pattern may need adjustment

If new C declaration types are added:
- Update parse_palette_name() to recognize them
- Update the regex in parse_wled_palettes()

DEPENDENCIES:
------------
- Python 3.6+
- Standard library only (re, sys, pathlib)
- No external packages required

AUTHOR NOTES FOR AI AGENTS:
--------------------------
When modifying this script:
1. Always preserve the naming convention (display names from array, not C variable names)
2. Test with all 59 palettes to ensure none are missed
3. Verify VRGB byte order is correct (Position, R, G, B)
4. Ensure both output files are generated in the same directory
5. Keep comments in output files for debugging
6. The map in the Berry file must use display names as keys
7. DSL palette names should match Berry variable names (without trailing underscore)
"""

import re
import sys
from pathlib import Path


def parse_palette_name(line):
    """
    Extract palette name from C array declaration.
    
    Handles both declaration types:
    - const uint8_t palette_name_gp[] PROGMEM = {...}
    - const byte palette_name_gp[] PROGMEM = {...}
    
    Args:
        line: A line from the header file
        
    Returns:
        Palette name without _gp suffix, or None if not a palette declaration
        
    Example:
        Input:  "const uint8_t ib_jul01_gp[] PROGMEM = {"
        Output: "ib_jul01"
    """
    # Match both 'const uint8_t' and 'const byte'
    match = re.search(r'const\s+(?:uint8_t|byte)\s+(\w+)\[\]', line)
    if match:
        name = match.group(1)
        # Remove _gp suffix if present (all WLED palettes have this suffix)
        if name.endswith('_gp'):
            name = name[:-3]
        return name
    return None


def parse_palette_data(lines):
    """
    Parse palette data from C array initialization.
    
    Extracts position and RGB values from array data, handling:
    - Inline comments (including those with commas)
    - Various formatting styles (comma-separated or whitespace-separated)
    - Braces and semicolons
    
    Args:
        lines: List of lines containing the array data
        
    Returns:
        List of tuples: [(position, r, g, b), ...]
        
    Example:
        Input lines:
            "    0, 226,   6,  12,  //comment"
            "   94,  26,  96,  78,"
            "  255, 177,   3,   9};"
        Output:
            [(0, 226, 6, 12), (94, 26, 96, 78), (255, 177, 3, 9)]
    
    Note: Comments are removed BEFORE parsing to avoid issues with commas
    in comments like "//gc from 47, 61,126"
    """
    # Process each line separately to handle comments properly
    all_numbers = []
    for line in lines:
        # Remove C++ style comments first (CRITICAL: do this before parsing numbers)
        line = re.sub(r'//.*$', '', line)
        # Remove braces and semicolon
        line = re.sub(r'[{};]', '', line)
        # Extract all numbers from this line using regex
        # This handles both comma-separated and whitespace-separated values
        for match in re.finditer(r'\d+', line):
            all_numbers.append(int(match.group()))
    
    # Group into (position, r, g, b) tuples
    # Each palette entry is 4 values: position (0-255), red, green, blue
    entries = []
    for i in range(0, len(all_numbers), 4):
        if i + 3 < len(all_numbers):
            pos, r, g, b = all_numbers[i:i+4]
            entries.append((pos, r, g, b))
    
    return entries


def format_palette_name(name):
    """Convert palette name to Berry variable format (uppercase with underscores)."""
    # Convert to uppercase
    name = name.upper()
    # Replace any remaining special characters with underscores
    name = re.sub(r'[^A-Z0-9_]', '_', name)
    return name


def format_berry_variable_name(display_name):
    """
    Convert display name to Berry variable format (uppercase with underscores).
    
    Args:
        display_name: Human-readable name from gGradientPalettes array
        
    Returns:
        Berry variable name with PALETTE_ prefix and _ suffix
        
    Examples:
        "Jul" → "PALETTE_JUL_"
        "Fire" → "PALETTE_FIRE_"
        "Red & Blue" → "PALETTE_RED_BLUE_"
        "C9 2" → "PALETTE_C9_2_"
        "Traffic Light" → "PALETTE_TRAFFIC_LIGHT_"
    
    Note: The trailing underscore is Berry convention to avoid conflicts
    with reserved keywords.
    """
    # Convert to uppercase and replace spaces/special chars with underscores
    name = display_name.upper()
    name = re.sub(r'[^A-Z0-9]+', '_', name)
    # Remove leading/trailing underscores
    name = name.strip('_')
    return f"PALETTE_{name}_"


def format_dsl_palette(display_name, entries, comment=None):
    """Format palette entries as DSL code."""
    dsl_name = format_berry_variable_name(display_name)[:-1]  # Remove trailing underscore
    
    lines = []
    if comment:
        lines.append(f"# {comment}")
    lines.append(f"palette {dsl_name} = [")
    
    for i, (pos, r, g, b) in enumerate(entries):
        # Calculate percentage
        percent = (pos / 255.0) * 100.0
        
        # Format hex color
        hex_color = f"0x{r:02X}{g:02X}{b:02X}"
        
        # Add position marker
        if i == 0:
            marker = " (start)"
        elif i == len(entries) - 1:
            marker = " (end)"
        else:
            marker = ""
        
        # Format entry
        lines.append(f"  ({pos}, {hex_color})    # {percent:.1f}% rgb({r},{g},{b}){marker}")
    
    lines.append("]")
    return '\n'.join(lines)


def format_berry_palette(display_name, entries, comment=None):
    """Format palette entries as Berry code with VRGB format."""
    berry_name = format_berry_variable_name(display_name)
    
    lines = []
    if comment:
        lines.append(f"# {comment}")
    lines.append(f"var {berry_name} = bytes(")
    
    for i, (pos, r, g, b) in enumerate(entries):
        # Format as VRGB (Value, R, G, B) hex bytes
        vrgb_hex = f"{pos:02X}{r:02X}{g:02X}{b:02X}"
        
        # Format comment
        lines.append(f'  "{vrgb_hex}"  # pos={pos} rgb({r},{g},{b})')
    
    lines.append(")")
    return '\n'.join(lines), berry_name, display_name


def parse_wled_palettes(header_file):
    """Parse all palettes from WLED header file."""
    with open(header_file, 'r') as f:
        content = f.read()
    
    palettes = []
    lines = content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Look for palette definition (both uint8_t and byte)
        if ('const uint8_t' in line or 'const byte' in line) and '[]' in line and 'PROGMEM' in line:
            # Extract palette name
            name = parse_palette_name(line)
            if not name:
                i += 1
                continue
            
            # Look for comment above (if any)
            comment = None
            if i > 0 and lines[i-1].strip().startswith('//'):
                comment = lines[i-1].strip()[2:].strip()
                # Check for multi-line comment
                j = i - 2
                while j >= 0 and lines[j].strip().startswith('//'):
                    comment = lines[j].strip()[2:].strip() + ' ' + comment
                    j -= 1
            
            # Collect data lines until we find the closing brace
            data_lines = []
            i += 1
            while i < len(lines):
                data_lines.append(lines[i])
                if '};' in lines[i]:
                    break
                i += 1
            
            # Parse the data
            entries = parse_palette_data(data_lines)
            
            if entries:
                palettes.append({
                    'name': name,
                    'entries': entries,
                    'comment': comment
                })
        
        i += 1
    
    return palettes


def parse_gradient_palettes_array(content):
    """
    Parse the gGradientPalettes array to get palette names and their display names.
    
    This is CRITICAL for correct naming! The display names in the array comments
    are what users see in WLED's UI, so we use those instead of C variable names.
    
    Array format (around line 710 in wled_palettes.h):
        const uint8_t* const gGradientPalettes[] PROGMEM = {
          Sunset_Real_gp,               //13-00 Sunset
          ib_jul01_gp,                  //31-18 Jul
          lava_gp,                      //35-22 Fire
          trafficlight_gp               //71-58 Traffic Light  (note: no comma on last entry)
        };
    
    Args:
        content: Full content of wled_palettes.h file
        
    Returns:
        Dictionary mapping C variable names (without _gp) to display names
        Example: {"ib_jul01": "Jul", "lava": "Fire", "Sunset_Real": "Sunset"}
        
    Note: The regex makes the comma optional (,?) to handle the last entry
    which doesn't have a trailing comma.
    """
    # Find the gGradientPalettes array
    array_match = re.search(
        r'const uint8_t\*\s+const\s+gGradientPalettes\[\]\s+PROGMEM\s*=\s*\{([^}]+)\}',
        content,
        re.DOTALL
    )
    if not array_match:
        return {}
    
    array_content = array_match.group(1)
    palette_map = {}
    
    # Parse each line: palette_name_gp,  //index Display Name (or without comma for last entry)
    for line in array_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('//'):
            continue
        
        # Match pattern: palette_name_gp[,] //index Display Name
        # Example: "  ib_jul01_gp,                  //31-18 Jul"
        match = re.match(r'(\w+),?\s*//\d+-\d+\s+(.+)', line)
        if match:
            var_name = match.group(1)
            display_name = match.group(2).strip()
            
            # Remove _gp suffix from variable name to match palette definitions
            if var_name.endswith('_gp'):
                var_name = var_name[:-3]
            
            palette_map[var_name] = display_name
    
    return palette_map


def main():
    """
    Main conversion function.
    
    Process:
    1. Read from_wled/src/wled_palettes.h
    2. Parse gGradientPalettes array to get display names (CRITICAL STEP)
    3. Parse all palette definitions from the file
    4. Match palette definitions with their display names
    5. Generate DSL file (for Animation DSL transpiler)
    6. Generate Berry file (for direct Berry import)
    
    Output files (both in same directory):
    - lib/libesp32/berry_animation/src/dsl/all_wled_palettes.anim
    - lib/libesp32/berry_animation/src/dsl/all_wled_palettes.be
    
    Expected result: 59 palettes in both files
    """
    # Read the WLED header file
    header_file = Path('from_wled/src/wled_palettes.h')
    
    if not header_file.exists():
        print(f"Error: {header_file} not found", file=sys.stderr)
        sys.exit(1)
    
    # Read the entire file
    with open(header_file, 'r') as f:
        full_content = f.read()
    
    # Parse the gGradientPalettes array to get display names
    gradient_palette_names = parse_gradient_palettes_array(full_content)
    
    # Parse all palette definitions
    all_palettes = parse_wled_palettes(header_file)
    
    # Filter and match palettes with their display names
    palettes = []
    for palette in all_palettes:
        if palette['name'] in gradient_palette_names:
            palette['display_name'] = gradient_palette_names[palette['name']]
            palettes.append(palette)
    
    print(f"# Found {len(palettes)} palettes in gGradientPalettes array")
    print()
    
    # Store palette variable names and display names for the map
    palette_map = []
    
    # Generate DSL output
    dsl_output_file = Path('lib/libesp32/berry_animation/src/dsl/all_wled_palettes.anim')
    dsl_output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(dsl_output_file, 'w') as f:
        f.write("# WLED Palettes converted to DSL format\n")
        f.write("# Auto-generated from from_wled/src/wled_palettes.h\n")
        f.write(f"# Total palettes: {len(palettes)}\n")
        f.write("\n")
        
        for i, palette in enumerate(palettes):
            if i > 0:
                f.write("\n")
            
            dsl_code = format_dsl_palette(
                palette['display_name'],
                palette['entries'],
                palette['comment']
            )
            f.write(dsl_code)
            f.write("\n")
    
    print(f"Generated {dsl_output_file} with {len(palettes)} palettes")
    
    # Generate Berry output
    berry_output_file = Path('lib/libesp32/berry_animation/src/dsl/all_wled_palettes.be')
    berry_output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(berry_output_file, 'w') as f:
        f.write("# WLED Palettes converted to Berry format\n")
        f.write("# Auto-generated from from_wled/src/wled_palettes.h\n")
        f.write(f"# Total palettes: {len(palettes)}\n")
        f.write("#\n")
        f.write("# Format: VRGB (Value/Position, Red, Green, Blue) as hex bytes\n")
        f.write("\n")
        
        for i, palette in enumerate(palettes):
            if i > 0:
                f.write("\n")
            
            berry_code, berry_name, display_name = format_berry_palette(
                palette['display_name'],
                palette['entries'],
                palette['comment']
            )
            f.write(berry_code)
            f.write("\n")
            
            # Store for map
            palette_map.append((display_name, berry_name))
        
        # Generate the WLED_Palettes class with map
        f.write("\n")
        f.write("# Palette map for easy access by name\n")
        f.write("class WLED_Palettes\n")
        f.write("  static map = {\n")
        
        for i, (display_name, berry_name) in enumerate(palette_map):
            comma = "," if i < len(palette_map) - 1 else ""
            f.write(f'    "{display_name}": {berry_name}{comma}\n')
        
        f.write("  }\n")
        f.write("end\n")
        f.write("\n")
        f.write('return {"wled_palettes": WLED_Palettes}\n')
    
    print(f"Generated {berry_output_file} with {len(palettes)} palettes")
    
    # Print first few palettes as preview
    print("\nPreview of first 3 palettes:")
    print("=" * 80)
    for palette in palettes[:3]:
        berry_code, berry_name, display_name = format_berry_palette(
            palette['display_name'], 
            palette['entries'], 
            palette['comment']
        )
        print(f"Display name: {display_name}")
        print(f"Variable: {berry_name}")
        print(berry_code)
        print()


if __name__ == '__main__':
    main()
