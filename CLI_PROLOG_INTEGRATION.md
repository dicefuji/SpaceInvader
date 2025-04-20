# CLI-Based Prolog Integration Guide

## Overview

This document explains how to integrate the CLI-based Prolog bridge into the Space Invaders game. This alternative approach avoids compatibility issues between PySwip and newer versions of SWI-Prolog, particularly on macOS with Apple Silicon.

## Why Use the CLI-Based Approach

We found that the PySwip library, which provides Python bindings for SWI-Prolog, has compatibility issues with:

1. SWI-Prolog version 9.x (you're using 9.2.9)
2. macOS on Apple Silicon (arm64-darwin)

The error encountered (`atom_chars/2: Arguments are not sufficiently instantiated`) is a known issue in this combination of software and hardware. The CLI-based approach provides a robust alternative that:

1. Works on all platforms where SWI-Prolog is installed
2. Avoids Python-to-Prolog marshaling issues
3. Has the same interface as the original PrologBridge

## Integration Steps

### 1. Switch to the CLI-Based Prolog Bridge

In any file where you currently use `PrologBridge`, replace the import statement:

```python
# Replace this:
from ai.prolog_bridge import PrologBridge

# With this:
from ai.cli_prolog_bridge import CLIPrologBridge as PrologBridge
```

This allows you to use the CLI-based bridge as a drop-in replacement with the same interface.

### 2. Update the Main Game File

Edit `space_invaders_prolog.py` to use the CLI-based bridge:

1. Change the import statement as shown above
2. Remove any code that checks `prolog_bridge.initialized` since the CLI bridge will throw an exception if there's an issue

### 3. Update the Test Files

Apply the same changes to the test files:
- `test_prolog_integration.py`
- `test_row_strategies.py`

### 4. Simplified Prolog File (Optional)

The `ai/invader_ai_simple.pl` file is a simplified version of the original Prolog knowledge base without any complex features that might cause compatibility issues. You can use either file with the CLI-based bridge.

Choose based on your preference:
- Original file: `ai/invader_ai.pl` (full features)
- Simplified file: `ai/invader_ai_simple.pl` (more compatible)

## Performance Considerations

The CLI-based approach has some performance differences compared to the PySwip integration:

### Advantages
- More reliable on all platforms
- No crashes or instability due to PySwip/SWI-Prolog mismatch
- Isolates Prolog from Python, preventing memory leaks

### Drawbacks
- Slightly slower due to process startup overhead
- Files are created for each query
- Separate process for each Prolog query

## How it Works

The CLI-based bridge uses the following approach:

1. Creates a temporary directory for Prolog files
2. Writes game state to a state file
3. Creates a query file for each query
4. Runs SWI-Prolog as a subprocess to execute the query
5. Reads the result from an output file

This process avoids direct embedding of SWI-Prolog, which is the source of the compatibility issues.

## Testing the Integration

You can test the CLI-based Prolog bridge with the included test script:

```bash
python test_cli_prolog.py
```

This will verify that:
1. SWI-Prolog is properly installed and accessible
2. The bridge can successfully communicate with Prolog
3. Basic queries work as expected

## Troubleshooting

If you encounter issues with the CLI-based bridge:

1. **SWI-Prolog Not Found**: Make sure `swipl` is in your PATH
   - For macOS: `brew install swi-prolog`
   - For Linux: `apt-get install swi-prolog` or similar for your distro
   - For Windows: Add SWI-Prolog's `bin` directory to your PATH

2. **Permission Issues**: Ensure the Python process has write permissions to create temporary files

3. **Slow Performance**: The CLI-based bridge has some overhead. If performance is critical, consider implementing a more efficient integration like a socket-based approach. 