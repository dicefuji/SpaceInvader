# CLI-Based Prolog Bridge Implementation

## Overview

This project implements a CLI-based Prolog bridge for the Space Invaders game to resolve compatibility issues between PySwip and newer versions of SWI-Prolog, particularly on macOS with Apple Silicon. The implementation follows a drop-in replacement strategy to minimize code changes while maintaining functionality.

## Speed Improvements

The game has been optimized for faster gameplay with the following changes:

1. **Increased Frame Rate**: FPS increased from 60 to 75 for smoother gameplay
2. **Faster Movement**:
   - Alien horizontal speed doubled (1 → 2)
   - Player speed increased (5 → 7)
3. **Faster Projectiles**:
   - Alien bullet speed increased (5 → 7)
   - Player bullet speed increased (10 → 12)
4. **More Dynamic Gameplay**:
   - Reduced alien firing cooldown (30 → 20 frames)
   - Increased alien speed progression factor (0.2 → 0.3)

These changes create a more engaging and challenging experience while maintaining balanced gameplay.

## Implementation Details

### Files Created/Modified

1. **No changes to original files**:
   - `ai/cli_prolog_bridge.py` (already implemented)
   - `ai/invader_ai_simple.pl` (already implemented)

2. **Modified import statements in**:
   - `space_invaders_prolog.py`
   - `test_prolog_integration.py`
   - `test_row_strategies.py`
   - `test_required_prolog.py`

3. **New test file**:
   - `test_cli_integration.py` - Verifies the CLI-based Prolog bridge functionality

### How It Works

The CLI-based Prolog bridge (`CLIPrologBridge`) implements the same interface as the original `PrologBridge` but uses subprocess calls to SWI-Prolog rather than direct Python bindings. This approach:

1. Creates a temporary directory for Prolog files
2. Writes game state to a state file
3. Creates a query file for each query
4. Runs SWI-Prolog as a subprocess to execute the query
5. Reads the result from an output file

### Testing

The implementation has been thoroughly tested:

1. **Basic functionality**: `test_cli_integration.py` verifies the core functionality of the bridge.
2. **Integration tests**: All existing tests (`test_required_prolog.py`, etc.) were updated and run successfully.
3. **Main game**: `space_invaders_prolog.py` was tested and confirmed to work with the new bridge.

## Requirements

- SWI-Prolog must be installed and accessible in the PATH.
- Python 3.6+ with Pygame.

## Performance Considerations

The CLI-based bridge has some performance implications:

- **Advantages**:
  - Works reliably on all platforms including macOS with Apple Silicon
  - No crashes due to PySwip/SWI-Prolog compatibility issues
  - Prevents memory leaks by isolating processes

- **Limitations**:
  - Slightly slower due to process startup overhead
  - Creates temporary files for communication

## Troubleshooting

If you encounter issues:

1. **SWI-Prolog Not Found**:
   - Ensure `swipl` is in your PATH
   - For macOS: `brew install swi-prolog`

2. **Permission Issues**:
   - Make sure Python has permission to create and write to temporary files

3. **Slow Performance**:
   - If performance is critical, the code includes optimizations to minimize subprocess calls
   - For extremely performance-sensitive applications, consider a socket-based approach

## Future Improvements

Potential future enhancements:

1. Socket-based communication for better performance
2. Persistent Prolog process to reduce startup overhead
3. Caching of common queries to improve efficiency 