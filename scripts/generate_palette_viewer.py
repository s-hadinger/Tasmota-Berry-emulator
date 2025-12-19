#!/usr/bin/env python3
"""
Generate HTML viewer for WLED palettes

Reads the Berry palette file and generates a standalone HTML page
that displays all palettes as CSS gradients or pixel views.
"""

import re
from pathlib import Path


def parse_berry_palette(berry_file):
    """Parse palette data from Berry file."""
    with open(berry_file, 'r') as f:
        content = f.read()
    
    palettes = {}
    
    # Find all palette definitions
    # Pattern: var PALETTE_NAME_ = bytes(\n  "VVRRGGBB"  # comment\n  ...)
    # Need to match until the closing parenthesis
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
        # Pattern: "Display Name": PALETTE_VAR_NAME,
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
        # Parse VRGB: VVRRGGBB
        v = int(hex_val[0:2], 16)  # Position (0-255)
        r = int(hex_val[2:4], 16)  # Red
        g = int(hex_val[4:6], 16)  # Green
        b = int(hex_val[6:8], 16)  # Blue
        
        # Convert position to percentage
        percent = (v / 255.0) * 100.0
        
        stops.append(f"#{r:02X}{g:02X}{b:02X} {percent:.1f}%")
    
    return f"linear-gradient(to right, {', '.join(stops)})"


def generate_html(palettes, display_names):
    """Generate complete HTML file."""
    
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset='utf-8'>
    <meta name="viewport" content="width=device-width,initial-scale=1"/>
    <title>WLED Palettes Viewer</title>
    <style>
        :root {
            --c_bg: #252525;
            --c_frm: #4f4f4f;
            --c_ttl: #eaeaea;
            --c_txt: #eaeaea;
            --c_btn: #1fa3ec;
            --c_btnhvr: #0e70a4;
            --c_in: #dddddd;
            --c_intxt: #000000;
        }
        
        body {
            text-align: center;
            font-family: verdana, sans-serif;
            background: var(--c_bg);
            color: var(--c_txt);
            margin: 0;
            padding: 10px;
        }
        
        .container {
            background: var(--c_bg);
            text-align: left;
            display: inline-block;
            color: var(--c_txt);
            min-width: 340px;
            max-width: 800px;
            width: 100%;
            position: relative;
        }
        
        h2, h3 {
            color: var(--c_ttl);
            text-align: center;
            margin: 10px 0;
        }
        
        hr {
            border: 0;
            border-top: 1px solid #666;
        }
        
        fieldset {
            background: var(--c_frm);
            border: 1px solid #666;
            border-radius: 0.3rem;
            padding: 10px;
            margin: 10px 0;
        }
        
        legend {
            color: var(--c_ttl);
            padding: 0 10px;
        }
        
        .palette-item {
            margin: 15px 0;
            padding: 10px;
            background: var(--c_frm);
            border-radius: 0.3rem;
        }
        
        .palette-name {
            font-weight: bold;
            margin-bottom: 8px;
            color: var(--c_ttl);
            font-size: 14px;
        }
        
        .palette-bar {
            width: 100%;
            height: 40px;
            border-radius: 0.3rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .palette-pixels {
            display: flex;
            width: 100%;
            height: 40px;
            border-radius: 0.3rem;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .pixel {
            flex: 1;
            min-width: 1px;
        }
        
        .mode-selector {
            display: flex;
            gap: 10px;
            margin: 15px 0;
            justify-content: center;
        }
        
        .mode-btn {
            border: 0;
            border-radius: 0.3rem;
            background: var(--c_btn);
            color: #faffff;
            padding: 10px 20px;
            font-size: 14px;
            cursor: pointer;
            transition: background 0.4s;
        }
        
        .mode-btn:hover {
            background: var(--c_btnhvr);
        }
        
        .mode-btn.active {
            background: #47c266;
        }
        
        .info {
            text-align: center;
            font-size: 12px;
            color: #999;
            margin: 10px 0;
        }
        
        .pixel-count {
            text-align: center;
            margin: 10px 0;
        }
        
        .pixel-count label {
            color: var(--c_txt);
            margin-right: 5px;
        }
        
        .pixel-count input {
            width: 80px;
            padding: 5px;
            background: var(--c_in);
            color: var(--c_intxt);
            border: 1px solid #666;
            border-radius: 0.3rem;
            text-align: center;
        }
        
        .footer {
            text-align: center;
            font-size: 11px;
            color: #aaa;
            margin-top: 20px;
            padding-top: 10px;
            border-top: 1px solid #666;
        }
        
        .footer a {
            color: #aaa;
            text-decoration: none;
        }
        
        .footer a:hover {
            color: var(--c_btn);
        }
    </style>
</head>
<body>
    <div class="container">
        <div style='text-align:center;color:var(--c_ttl);'>
            <h2>WLED Palettes</h2>
            <h3><hr>59 Gradient Palettes<hr></h3>
        </div>
        
        <div class="mode-selector">
            <button class="mode-btn active" onclick="setMode('gradient')">Smooth Gradient</button>
            <button class="mode-btn" onclick="setMode('pixels')">Pixel View</button>
        </div>
        
        <div id="pixelControl" style="display:none;" class="pixel-count">
            <label>Pixels: </label>
            <input type="number" id="pixelCount" value="40" min="10" max="100" onchange="updatePixelCount()">
        </div>
        
        <div class="info" id="modeInfo">
            Displaying palettes as smooth gradients
        </div>
        
        <fieldset>
            <legend><b>&nbsp;Palettes&nbsp;</b></legend>
            <div id="palettes"></div>
        </fieldset>
        
        <div class="footer">
            <a href='https://github.com/Aircoookie/WLED' target='_blank'>
                WLED Palettes converted for Tasmota Berry Animation Framework
            </a>
        </div>
    </div>
    
    <script>
        // WLED Palette data (VRGB format: Position, R, G, B)
        const paletteData = {
'''
    
    # Add palette data as JavaScript object
    for var_name in sorted(palettes.keys()):
        display_name = display_names.get(var_name, var_name)
        hex_values = palettes[var_name]
        gradient = vrgb_to_css_gradient(hex_values)
        
        html += f'            "{display_name}": {{\n'
        html += f'                gradient: "{gradient}",\n'
        html += f'                data: {hex_values}\n'
        html += f'            }},\n'
    
    html += '''        };
        
        let currentMode = 'gradient';
        let pixelCount = 40;
        
        // Initialize palettes
        function initPalettes() {
            const container = document.getElementById('palettes');
            container.innerHTML = '';
            
            for (const [name, palette] of Object.entries(paletteData)) {
                const item = document.createElement('div');
                item.className = 'palette-item';
                
                const nameDiv = document.createElement('div');
                nameDiv.className = 'palette-name';
                nameDiv.textContent = name;
                item.appendChild(nameDiv);
                
                const barDiv = document.createElement('div');
                barDiv.className = currentMode === 'gradient' ? 'palette-bar' : 'palette-pixels';
                barDiv.dataset.name = name;
                
                if (currentMode === 'gradient') {
                    barDiv.style.background = palette.gradient;
                } else {
                    renderPixels(barDiv, palette.data);
                }
                
                item.appendChild(barDiv);
                container.appendChild(item);
            }
        }
        
        // Render palette as discrete pixels
        function renderPixels(container, vrgbData) {
            container.innerHTML = '';
            
            // Parse VRGB data to get color stops
            const stops = vrgbData.map(hex => {
                const v = parseInt(hex.substr(0, 2), 16);
                const r = parseInt(hex.substr(2, 2), 16);
                const g = parseInt(hex.substr(4, 2), 16);
                const b = parseInt(hex.substr(6, 2), 16);
                return { pos: v / 255, color: `rgb(${r},${g},${b})` };
            });
            
            // Generate pixels by interpolating between stops
            for (let i = 0; i < pixelCount; i++) {
                const pos = i / (pixelCount - 1);
                const color = interpolateColor(stops, pos);
                
                const pixel = document.createElement('div');
                pixel.className = 'pixel';
                pixel.style.backgroundColor = color;
                container.appendChild(pixel);
            }
        }
        
        // Interpolate color at position between stops
        function interpolateColor(stops, pos) {
            // Find surrounding stops
            let before = stops[0];
            let after = stops[stops.length - 1];
            
            for (let i = 0; i < stops.length - 1; i++) {
                if (pos >= stops[i].pos && pos <= stops[i + 1].pos) {
                    before = stops[i];
                    after = stops[i + 1];
                    break;
                }
            }
            
            // If exact match, return that color
            if (before.pos === pos) return before.color;
            if (after.pos === pos) return after.color;
            
            // Interpolate
            const range = after.pos - before.pos;
            const t = range === 0 ? 0 : (pos - before.pos) / range;
            
            const beforeRgb = before.color.match(/\\d+/g).map(Number);
            const afterRgb = after.color.match(/\\d+/g).map(Number);
            
            const r = Math.round(beforeRgb[0] + (afterRgb[0] - beforeRgb[0]) * t);
            const g = Math.round(beforeRgb[1] + (afterRgb[1] - beforeRgb[1]) * t);
            const b = Math.round(beforeRgb[2] + (afterRgb[2] - beforeRgb[2]) * t);
            
            return `rgb(${r},${g},${b})`;
        }
        
        // Set display mode
        function setMode(mode) {
            currentMode = mode;
            
            // Update button states
            document.querySelectorAll('.mode-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Show/hide pixel count control
            document.getElementById('pixelControl').style.display = 
                mode === 'pixels' ? 'block' : 'none';
            
            // Update info text
            document.getElementById('modeInfo').textContent = 
                mode === 'gradient' 
                    ? 'Displaying palettes as smooth gradients'
                    : `Displaying palettes as ${pixelCount} discrete pixels`;
            
            // Re-render palettes
            initPalettes();
        }
        
        // Update pixel count
        function updatePixelCount() {
            pixelCount = parseInt(document.getElementById('pixelCount').value);
            if (pixelCount < 10) pixelCount = 10;
            if (pixelCount > 100) pixelCount = 100;
            document.getElementById('pixelCount').value = pixelCount;
            
            document.getElementById('modeInfo').textContent = 
                `Displaying palettes as ${pixelCount} discrete pixels`;
            
            if (currentMode === 'pixels') {
                initPalettes();
            }
        }
        
        // Initialize on load
        window.addEventListener('load', initPalettes);
    </script>
</body>
</html>
'''
    
    return html


def main():
    berry_file = Path('lib/libesp32/berry_animation/src/dsl/all_wled_palettes.be')
    
    if not berry_file.exists():
        print(f"Error: {berry_file} not found")
        return
    
    print("Parsing Berry palette file...")
    palettes, display_names = parse_berry_palette(berry_file)
    
    print(f"Found {len(palettes)} palettes")
    
    print("Generating HTML...")
    html = generate_html(palettes, display_names)
    
    output_file = Path('wled_palettes_viewer.html')
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"Generated {output_file}")
    print(f"Open {output_file} in a web browser to view the palettes")


if __name__ == '__main__':
    main()
