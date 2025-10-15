#!/usr/bin/env berry
# Example usage of animation_dsl.compile_file() method
# This demonstrates how to compile .anim files to .be files with proper exception handling

import animation
import animation_dsl

# Example 1: Compile a single .anim file
print("Compiling simple_palette.anim...")
try
  animation_dsl.compile_file("lib/libesp32/berry_animation/anim_examples/simple_palette.anim")
  print("✓ Compilation successful!")
except .. as e, msg
  print(f"✗ Compilation failed: {e} - {msg}")
end

# Example 2: Batch compile multiple files with error handling
var anim_files = [
  "lib/libesp32/berry_animation/anim_examples/simple_palette.anim",
  "lib/libesp32/berry_animation/anim_examples/test_template_simple.anim"
]

print("\nBatch compiling multiple files...")
for file : anim_files
  print(f"Compiling {file}...")
  try
    animation_dsl.compile_file(file)
    print("  ✓ Success")
  except .. as e, msg
    print(f"  ✗ Failed: {e} - {msg}")
  end
end

# Example 3: Demonstrate error handling
print("\nTesting error handling...")

# Test invalid extension
try
  animation_dsl.compile_file("test.txt")
  print("Should not reach here")
except "invalid_filename" as e, msg
  print(f"✓ Caught expected error: {msg}")
end

# Test non-existent file
try
  animation_dsl.compile_file("nonexistent.anim")
  print("Should not reach here")
except "io_error" as e, msg
  print(f"✓ Caught expected error: {msg}")
end

print("\nDone!")