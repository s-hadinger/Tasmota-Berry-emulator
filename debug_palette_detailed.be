#!/usr/bin/env berry

# Debug script to see exactly what comments are collected

import animation_dsl

# Test DSL with palette comments
var dsl_source = "palette test_colors = [\n" +
  "  (0, red),      # Start color\n" +
  "  (128, green),  # Middle color\n" +
  "  (255, blue)    # End color\n" +
  "]"

print("=== DSL Source ===")
print(dsl_source)

print("\n=== Compiled Berry Code ===")
var berry_code = animation_dsl.compile(dsl_source)
if berry_code != nil
  print(berry_code)
else
  print("Compilation failed!")
end

# Let's also test with alternative syntax
var dsl_source2 = "palette alt_colors = [\n" +
  "  red,      # First color\n" +
  "  green,    # Second color\n" +
  "  blue      # Third color\n" +
  "]"

print("\n=== Alternative Syntax DSL ===")
print(dsl_source2)

print("\n=== Alternative Syntax Compiled ===")
var berry_code2 = animation_dsl.compile(dsl_source2)
if berry_code2 != nil
  print(berry_code2)
else
  print("Compilation failed!")
end