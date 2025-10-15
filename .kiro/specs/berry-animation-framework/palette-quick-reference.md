# Palette DSL Quick Reference

## Basic Syntax

```dsl
palette palette_name = [
  (position, color),    # Position 0-255, any color format
  (position, color),    # Add as many entries as needed
  (position, color)     # Comments are preserved
]
```

## Color Formats Supported

```dsl
palette example = [
  (0, #FF0000),      # Hex RGB
  (64, #80FF0000),   # Hex ARGB (with alpha)
  (128, red),        # Named color
  (192, custom_color), # Custom color reference
  (255, #00F)        # Short hex RGB
]
```

## Usage in Animations

```dsl
# Define palette
palette fire = [
  (0, #000000),    # Black
  (128, #FF0000),  # Red
  (255, #FFFF00)   # Yellow
]

# Use in animation
animation fire_effect = filled(
  rich_palette(fire, 5s, smooth, 255),
  loop
)
```

## Complete Example

```dsl
strip length 30

# Define custom palette
palette sunset = [
  (0, #191970),    # Midnight blue
  (64, purple),    # Purple
  (128, #FF69B4),  # Hot pink
  (192, orange),   # Orange
  (255, yellow)    # Yellow
]

# Create animation
animation sunset_glow = filled(
  rich_palette(sunset, 8s, smooth, 200),
  loop
)

# Run animation
sequence demo {
  play sunset_glow for 20s
}

run demo
```

## Tips

1. **Position Values**: Use 0-255 range, don't need to be evenly spaced
2. **Color Mixing**: Mix hex colors and named colors freely
3. **Comments**: Add comments to document your color choices
4. **Smooth Transitions**: The framework automatically interpolates between palette entries
5. **Performance**: Palettes compile to efficient Berry bytes objects

## Common Palettes

### Fire Effect
```dsl
palette fire = [
  (0, #000000),    # Black
  (64, #800000),   # Dark red
  (128, #FF0000),  # Red
  (192, #FF8000),  # Orange
  (255, #FFFF00)   # Yellow
]
```

### Ocean Waves
```dsl
palette ocean = [
  (0, navy),       # Deep ocean
  (64, blue),      # Ocean blue
  (128, cyan),     # Shallow water
  (192, #87CEEB),  # Sky blue
  (255, white)     # Foam
]
```

### Rainbow
```dsl
palette rainbow = [
  (0, red),
  (42, orange),
  (84, yellow),
  (126, green),
  (168, blue),
  (210, indigo),
  (255, violet)
]
```

### Aurora Borealis
```dsl
palette aurora = [
  (0, #000022),    # Dark night sky
  (64, #004400),   # Dark green
  (128, #00AA44),  # Aurora green
  (192, #44AA88),  # Light green
  (255, #88FFAA)   # Bright aurora
]
```