#!/usr/bin/env berry

# Debug script to understand comment collection

import animation_dsl

# Test DSL with palette comments
var dsl_source = "palette test_colors = [\n" +
  "  (0, red),      # Start color\n" +
  "  (128, green),  # Middle color\n" +
  "  (255, blue)    # End color\n" +
  "]"

print("=== DSL Source ===")
print(dsl_source)

print("\n=== Tokenizing ===")
var lexer = animation_dsl.create_lexer(dsl_source)
var tokens = lexer.tokenize()

for i : 0..size(tokens)-1
  var token = tokens[i]
  print(f"Token {i}: {token.type} = '{token.value}'")
end