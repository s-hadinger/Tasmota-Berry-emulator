#!/usr/bin/env python3
"""
WLED Palette Extractor - Extract palettes from WLED header file and convert to DSL

This script extracts palette definitions from the WLED wled_palettes.h file
and converts them to DSL format.
"""

import re
from typing import List, Tuple, Optional

def extract_wled_palettes(header_file_path: str) -> List[Tuple[str, str]]:
    """
    Extract palette definitions from WLED header file.
    
    Returns list of tuples: (palette_name, palette_data)
    """
    palettes = []
    
    try:
        with open(header_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match palette definitions
        pattern = r'const uint8_t (\w+)_gp\[\] PROGMEM = \{([^}]+)\};'
        matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
        
        for palette_name, palette_data in matches:
            palettes.append((palette_name, palette_data))
        
        return palettes
        
    except Exception as e:
        print(f"Error reading {header_file_path}: {e}")
        return []

def convert_wled_palette_data(palette_data: str) -> List[Tuple[int, int, int, int]]:
    """
    Convert WLED palette data to list of (position, r, g, b) tuples.
    """
    # Extract all numbers from the palette data
    numbers = []
    for num_str in re.findall(r'\d+', palette_data):
        numbers.append(int(num_str))
    
    if len(numbers) % 4 != 0:
        raise ValueError(f"Invalid palette data length: {len(numbers)} (expected multiple of 4)")
    
    # Group into position, R, G, B tuples
    colors = []
    for i in range(0, len(numbers), 4):
        position = numbers[i]
        r = numbers[i + 1]
        g = numbers[i + 2]
        b = numbers[i + 3]
        colors.append((position, r, g, b))
    
    return colors

def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB values to hex string"""
    return f"0x{r:02X}{g:02X}{b:02X}"

def palette_name_to_dsl(name: str) -> str:
    """Convert WLED palette name to DSL format"""
    # Remove _gp suffix if present
    if name.endswith('_gp'):
        name = name[:-3]
    
    # Convert to lowercase and replace special chars
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name.lower())
    
    # Ensure it starts with a letter or underscore
    if name and name[0].isdigit():
        name = '_' + name
    
    return name

def convert_wled_palette_to_dsl(palette_name: str, palette_data: str) -> str:
    """
    Convert a single WLED palette to DSL format.
    """
    try:
        colors = convert_wled_palette_data(palette_data)
        dsl_name = palette_name_to_dsl(palette_name)
        
        dsl_lines = [f"palette {dsl_name} = ["]
        
        for position, r, g, b in colors:
            hex_color = rgb_to_hex(r, g, b)
            dsl_lines.append(f"  ({position}, {hex_color})")
        
        dsl_lines.append("]")
        
        return '\n'.join(dsl_lines)
        
    except Exception as e:
        return f"# Error converting {palette_name}: {e}"

def main():
    """Main function to extract and convert WLED palettes"""
    header_file = "from_wled/src/wled_palettes.h"
    output_file = "wled_palettes_converted.dsl"
    
    print(f"Extracting palettes from {header_file}...")
    
    palettes = extract_wled_palettes(header_file)
    
    if not palettes:
        print("No palettes found in header file")
        return
    
    print(f"Found {len(palettes)} WLED palettes")
    
    # Convert all palettes
    converted_palettes = []
    successful_conversions = 0
    
    for palette_name, palette_data in palettes:
        print(f"Converting {palette_name}_gp...")
        
        dsl_palette = convert_wled_palette_to_dsl(palette_name, palette_data)
        if not dsl_palette.startswith("# Error"):
            converted_palettes.append(dsl_palette)
            successful_conversions += 1
        else:
            print(f"  {dsl_palette}")
    
    # Write output file
    if converted_palettes:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# WLED Palettes converted to Berry Animation Framework DSL\n")
            f.write("# Extracted from wled_palettes.h\n")
            f.write(f"# Successfully converted {successful_conversions} palettes\n\n")
            
            for palette in converted_palettes:
                f.write(palette + "\n\n")
        
        print(f"\n✓ Successfully converted {successful_conversions} WLED palettes")
        print(f"✓ Output written to {output_file}")
    else:
        print("No palettes were successfully converted")

if __name__ == "__main__":
    main()