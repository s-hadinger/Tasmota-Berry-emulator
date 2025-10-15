#!/usr/bin/env python3
"""
Palette Converter - Convert WLED palette files to Berry Animation DSL format

This script converts downloaded .c3g palette files from the cpt-city format
to the DSL palette format used by the Berry Animation Framework.

Usage:
    python palette_converter.py
"""

import os
import re
import glob
from typing import List, Tuple, Optional

def parse_css_gradient(content: str) -> List[Tuple[float, int, int, int]]:
    """
    Parse CSS3 linear-gradient format and extract color stops.
    
    Returns list of tuples: (percentage, red, green, blue)
    """
    colors = []
    
    # Find all rgb color definitions with percentages
    pattern = r'rgb\(\s*(\d+),\s*(\d+),\s*(\d+)\)\s+([\d.]+)%'
    matches = re.findall(pattern, content)
    
    for match in matches:
        r, g, b, percent = match
        colors.append((float(percent), int(r), int(g), int(b)))
    
    # Sort by percentage
    colors.sort(key=lambda x: x[0])
    return colors

def percentage_to_position(percentage: float) -> int:
    """Convert percentage (0-100) to position value (0-255)"""
    return int(round(percentage * 255 / 100))

def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB values to hex string"""
    return f"0x{r:02X}{g:02X}{b:02X}"

def filename_to_palette_name(filename: str) -> str:
    """Convert filename to valid DSL palette name"""
    # Remove .c3g extension
    name = filename.replace('.c3g', '')
    
    # Replace special characters with underscores
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    
    # Ensure it starts with a letter or underscore
    if name and name[0].isdigit():
        name = '_' + name
    
    # Convert to lowercase for consistency
    name = name.lower()
    
    return name

def convert_palette_file(filepath: str) -> Optional[str]:
    """
    Convert a single .c3g file to DSL palette format.
    
    Returns the DSL palette definition string or None if conversion fails.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the CSS gradient
        colors = parse_css_gradient(content)
        
        if not colors:
            print(f"Warning: No colors found in {filepath}")
            return None
        
        # Get palette name from filename
        filename = os.path.basename(filepath)
        palette_name = filename_to_palette_name(filename)
        
        # Build DSL palette definition
        dsl_lines = [f"palette {palette_name} = ["]
        
        for i, (percentage, r, g, b) in enumerate(colors):
            position = percentage_to_position(percentage)
            hex_color = rgb_to_hex(r, g, b)
            
            # Add comment with original percentage
            comment = f"  # {percentage:.1f}%"
            if i == 0:
                comment += " (start)"
            elif i == len(colors) - 1:
                comment += " (end)"
            
            dsl_lines.append(f"  ({position}, {hex_color}){comment}")
        
        dsl_lines.append("]")
        
        return '\n'.join(dsl_lines)
        
    except Exception as e:
        print(f"Error converting {filepath}: {e}")
        return None

def convert_wled_palette_to_dsl(wled_palette_data: str, palette_name: str) -> str:
    """
    Convert WLED palette data (from wled_palettes.h) to DSL format.
    
    Example input:
    const uint8_t ib_jul01_gp[] PROGMEM = {
        0, 226,   6,  12,
       94,  26,  96,  78,
      132, 130, 189,  94,
      255, 177,   3,   9};
    """
    # Extract the array data
    array_match = re.search(r'\{([^}]+)\}', wled_palette_data)
    if not array_match:
        return f"# Error: Could not parse palette data for {palette_name}"
    
    array_data = array_match.group(1)
    
    # Split into numbers and clean up
    numbers = []
    for num_str in re.findall(r'\d+', array_data):
        numbers.append(int(num_str))
    
    if len(numbers) % 4 != 0:
        return f"# Error: Invalid palette data length for {palette_name} (expected multiple of 4)"
    
    # Group into position, R, G, B tuples
    dsl_lines = [f"palette {palette_name} = ["]
    
    for i in range(0, len(numbers), 4):
        position = numbers[i]
        r = numbers[i + 1]
        g = numbers[i + 2]
        b = numbers[i + 3]
        
        hex_color = rgb_to_hex(r, g, b)
        dsl_lines.append(f"  ({position}, {hex_color})")
    
    dsl_lines.append("]")
    
    return '\n'.join(dsl_lines)

def main():
    """Main conversion function"""
    input_dir = "from_wled/downloaded"
    output_file = "converted_palettes.dsl"
    
    if not os.path.exists(input_dir):
        print(f"Error: Input directory {input_dir} not found")
        return
    
    # Find all .c3g files
    c3g_files = glob.glob(os.path.join(input_dir, "*.c3g"))
    
    if not c3g_files:
        print(f"No .c3g files found in {input_dir}")
        return
    
    print(f"Found {len(c3g_files)} palette files to convert")
    
    # Convert all files
    converted_palettes = []
    successful_conversions = 0
    
    for filepath in sorted(c3g_files):
        print(f"Converting {os.path.basename(filepath)}...")
        
        dsl_palette = convert_palette_file(filepath)
        if dsl_palette:
            converted_palettes.append(dsl_palette)
            successful_conversions += 1
        else:
            print(f"  Failed to convert {filepath}")
    
    # Write output file
    if converted_palettes:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Converted WLED Palettes for Berry Animation Framework\n")
            f.write("# Generated from cpt-city palette files\n")
            f.write(f"# Successfully converted {successful_conversions} palettes\n\n")
            
            for palette in converted_palettes:
                f.write(palette + "\n\n")
        
        print(f"\n✓ Successfully converted {successful_conversions} palettes")
        print(f"✓ Output written to {output_file}")
    else:
        print("No palettes were successfully converted")

def demo_wled_conversion():
    """Demonstrate conversion of WLED palette format"""
    print("\n" + "="*60)
    print("DEMO: Converting WLED palette format")
    print("="*60)
    
    # Example WLED palette data
    wled_example = '''const uint8_t ib_jul01_gp[] PROGMEM = {
    0, 226,   6,  12,
   94,  26,  96,  78,
  132, 130, 189,  94,
  255, 177,   3,   9};'''
    
    print("Input WLED format:")
    print(wled_example)
    print("\nConverted to DSL format:")
    
    dsl_result = convert_wled_palette_to_dsl(wled_example, "ib_jul01")
    print(dsl_result)

if __name__ == "__main__":
    main()
    demo_wled_conversion()