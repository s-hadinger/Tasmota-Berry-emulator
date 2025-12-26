# WLED Palette Conversion Project

This project successfully extracted and converted WLED color palettes to the Berry Animation Framework DSL format.

## What Was Accomplished

### 1. Downloaded Original Palette Files
- Extracted 47 URLs from `from_wled/src/wled_palettes.h`
- Downloaded all `.c3g` files from http://seaviewsensing.com/pub/cpt-city/
- Files saved to `from_wled/downloaded/`

### 2. Created Python Conversion Tools
- **`palette_converter.py`** - Converts `.c3g` files (CSS gradient format) to DSL
- **`wled_palette_extractor.py`** - Extracts palettes from WLED header file
- **`complete_palette_converter.py`** - Combined tool for both formats

### 3. Converted Palette Formats

#### From CSS Gradient Format (.c3g files):
```css
linear-gradient(
  0deg,
  rgb( 51,  0,255)   0.000%,
  rgb(102,  0,255)  25.000%,
  rgb(153,  0,255)  50.000%,
  rgb(204,  0,128)  75.000%,
  rgb(255,  0,  0) 100.000%
);
```

#### To DSL Format:
```berry
palette analogous_1 = [
  (0, 0x3300FF)    # 0.0% rgb(51,0,255) (start)
  (64, 0x6600FF)   # 25.0% rgb(102,0,255)
  (128, 0x9900FF)  # 50.0% rgb(153,0,255)
  (191, 0xCC0080)  # 75.0% rgb(204,0,128)
  (255, 0xFF0000)  # 100.0% rgb(255,0,0) (end)
]
```

#### From WLED Header Format:
```c
const uint8_t ib_jul01_gp[] PROGMEM = {
    0, 226,   6,  12,
   94,  26,  96,  78,
  132, 130, 189,  94,
  255, 177,   3,   9};
```

#### To DSL Format:
```berry
palette ib_jul01 = [
  (0, 0xE2060C)    # pos=0 rgb(226,6,12)
  (94, 0x1A604E)   # pos=94 rgb(26,96,78)
  (132, 0x82BD5E)  # pos=132 rgb(130,189,94)
  (255, 0xB10309)  # pos=255 rgb(177,3,9)
]
```

## Final Output

### `all_wled_palettes.dsl`
- **94 total palettes** converted successfully
- **47 from .c3g files** (with percentage comments)
- **47 from WLED header** (direct conversion)
- Ready to use in Berry Animation Framework

## Key Features of the Conversion

1. **Automatic Name Conversion**: Converts filenames to valid DSL identifiers
2. **Position Mapping**: Converts percentages (0-100%) to positions (0-255)
3. **Color Format**: Converts RGB values to hex format (0xRRGGBB)
4. **Original Values Preserved**: Comments include original RGB values and positions/percentages
5. **Source Tracking**: Each palette includes its original source file
6. **Error Handling**: Graceful handling of malformed files
7. **Duplicate Detection**: Both formats converted for comparison

## Usage in Berry Animation Framework

You can now use any of these palettes in your DSL code:

```berry
# Use a converted palette
animation rainbow_effect = rich_palette(
  colors=analogous_1
  period=3s
)

# Or use in color cycling
color dynamic_color = color_cycle(
  colors=lava
  period=5s
)
```

## Files Created

- `all_wled_palettes.dsl` - Complete palette collection (94 palettes)
- `complete_palette_converter.py` - Main conversion tool
- `palette_converter.py` - .c3g file converter
- `wled_palette_extractor.py` - WLED header extractor
- `from_wled/downloaded/` - Directory with 47 original .c3g files

## Conversion Statistics

- ✅ **47/47** .c3g files converted successfully
- ✅ **47/47** WLED header palettes converted successfully  
- ✅ **94 total palettes** ready for use
- ✅ **100% success rate** for both formats

The conversion project is complete and all WLED palettes are now available in Berry Animation Framework DSL format!